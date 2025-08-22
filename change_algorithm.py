import json
from pathlib import Path

def compute_pct_change(new_val, old_val):
    if old_val == 0 or old_val is None:
        return None
    return round(((new_val - old_val) / old_val) * 100, 2)

def process_history(history):
    """
    Given a list of history entries, compute 1-day and 7-day % changes.
    Updates each entry in place.
    """
    for i in range(len(history)):
        today = history[i]

        # 1-day % change
        if i > 0:
            yesterday = history[i - 1]
            today["subreddit_change_1d_pct"] = compute_pct_change(
                today["subreddit_Count"], yesterday["subreddit_Count"]
            )
            today["marketcap_change_1d_pct"] = compute_pct_change(
                today["current_market_cap"], yesterday["current_market_cap"]
            )
        else:
            today["subreddit_change_1d_pct"] = None
            today["marketcap_change_1d_pct"] = None

        # 7-day % change
        if i >= 7:
            week_ago = history[i - 7]
            today["subreddit_change_7d_pct"] = compute_pct_change(
                today["subreddit_Count"], week_ago["subreddit_Count"]
            )
            today["marketcap_change_7d_pct"] = compute_pct_change(
                today["current_market_cap"], week_ago["current_market_cap"]
            )
        else:
            today["subreddit_change_7d_pct"] = None
            today["marketcap_change_7d_pct"] = None

    return history


def main():
    tracker_path = Path("tracker.json")
    results_path = Path("results.json")

    with tracker_path.open("r", encoding="utf-8") as f:
        tracker_data = json.load(f)

    results = {}

    # Process each company
    for company, data in tracker_data.items():
        history = data.get("history", [])
        processed_history = process_history(history)
        results[company] = {"history": processed_history}

    # Save results.json
    with results_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"Processed data written to {results_path}")


if __name__ == "__main__":
    main()
