import json
from pathlib import Path
from datetime import datetime, UTC

def find_big_movements(results_file="results.json",
                       output_file="big_movement.json",
                       threshold_1d=5.0,
                       threshold_7d=20.0):
    """
    Insert only the latest history entry into big_movement.json when thresholds are crossed.
    Keys = date of movement, values = companies with their latest snapshot.
    """

    results_path = Path(results_file)
    output_path = Path(output_file)

    with results_path.open("r", encoding="utf-8") as f:
        results = json.load(f)

    # Load existing big_movement.json (or start fresh)
    if output_path.exists() and output_path.stat().st_size > 0:
        with output_path.open("r", encoding="utf-8") as f:
            big_moves = json.load(f)
    else:
        big_moves = {}

    today = datetime.now(UTC).strftime("%Y-%m-%d")

    if today not in big_moves:
        big_moves[today] = {}

    for company, data in results.items():
        history = data.get("history", [])
        if not history:
            continue

        latest = history[-1]  # only take the most recent snapshot

        crossed = False

        # 1-day checks
        for k in ["subreddit_change_1d_pct", "marketcap_change_1d_pct"]:
            val = latest.get(k)
            if val is not None and abs(val) >= threshold_1d:
                crossed = True

        # 7-day checks
        for k in ["subreddit_change_7d_pct", "marketcap_change_7d_pct"]:
            val = latest.get(k)
            if val is not None and abs(val) >= threshold_7d:
                crossed = True

        if crossed:
            # insert only the latest snapshot
            big_moves[today][company] = latest

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(big_moves, f, indent=4)

    print(f"Inserted {len(big_moves[today])} movers for {today} into {output_path}")

    if len(big_moves[today]) > 1:
        return 1

    else:
        return 0


# Example usage
if __name__ == "__main__":
    find_big_movements(threshold_1d=5.0, threshold_7d=5.0)
