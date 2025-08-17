import json
import requests
import datetime


def scrape_subscribers(subreddit_name: str):
    url = f"https://www.reddit.com/r/{subreddit_name}/about.json"
    headers = {
        # Use a descriptive UA; Reddit may throttle/deny generic requests
        "User-Agent": "subreddit-tracker/1.0 (by u/yourusername)"
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()  # raise helpful error if non-200

    payload = resp.json()
    count = payload["data"]["subscribers"]
    name = payload["data"]["display_name"]
    snapshot = {
        "subreddit_Name": name,
        "subreddit_Count": count,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return snapshot





