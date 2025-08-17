import JSON_scraper
from JSON_scraper import *
from pathlib import Path
from add_to_JSON import *
from market_cap_getter import *

FILENAME = Path("subreddits.json")

def main():
    if FILENAME.exists():
        with FILENAME.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

    for subreddit in data:
        final_snapshot = scrape_subscribers(subreddit)
        final_snapshot['ticker'] = data[subreddit]
        final_snapshot['current_market_cap'] = get_market_cap(final_snapshot['ticker'])

        add_snapshot(final_snapshot)

if __name__ == "__main__":
    main()

