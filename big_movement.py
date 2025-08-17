import json
from pathlib import Path
from datetime import datetime, UTC

def find_big_movements(results_file="results.json",
                       output_file="big_movement.json",
                       threshold_1d=5.0,
                       threshold_7d=20.0):
    """
    Only checks the latest entry in results.json for each company.
    If thresholds are crossed, adds that entry to big_movement.json grouped by date.
    """

    results_path = Path(results_file)
    output_path = Path(output_file)

    # Load results.json
    with results_path.open("r", encoding="utf-8") as f:
        results = json.load(f)

    # Load or init big_movement.json safely
    big_moves = {}
    if output_path.exists() and output_path.stat().st_size > 0:
        try:
            with output_path.open("r", encoding="utf-8") as f:
                big_moves = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ big_movement.json was invalid, starting fresh")
            big_moves = {}

    today = datetime.now(UTC).strftime("%Y-%m-%d")
    if today not in big_moves:
        big_moves[today] = {}

    for company, data in results.items():
        history = data.get("history", [])
        if not history:
            continue

        # ✅ only take the latest snapshot
        latest = history[-1]

        crossed = False

        # check 1-day %
        for k in ["subreddit_change_1d_pct", "marketcap_change_1d_pct"]:
            val = latest.get(k)
            if val is not None and abs(val) >= threshold_1d:
                crossed = True

        # check 7-day %
        for k in ["subreddit_change_7d_pct", "marketcap_change_7d_pct"]:
            val = latest.get(k)
            if val is not None and abs(val) >= threshold_7d:
                crossed = True

        if crossed:
            # only insert the latest snapshot
            big_moves[today][company] = latest

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(big_moves, f, indent=4)

    print(f"Inserted {len(big_moves[today])} movers for {today} into {output_path}")

    if len(big_moves[today]) > 0:
        return 1

    else:
        return 0


# Example usage
if __name__ == "__main__":
    find_big_movements(threshold_1d=5.0, threshold_7d=5.0)
