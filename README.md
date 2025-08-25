# Reddit-Stock-Analyzer  
A Python tool that tracks the relationship between company market capitalizations and subreddit community growth. The script collects daily data, calculates short-term and weekly changes, and flags significant movements in stock market cap or subreddit popularity. Executes everyday at 9 am.

## About  
I wanted to analyze whether there’s any correlation between the financial performance of companies and the growth of their online communities. This project automatically gathers market cap data and subreddit subscriber counts for tracked companies and stores the results in JSON files for further analysis.  

The project runs **daily at 9 AM** on a server and builds a history of changes over time.  

You can see the results of the daily runs on results.json. My script automatically pushes the updates to github everyday at 9 am.


**Default Analysis Intervals**  

- Daily change (1-day difference).  
- Weekly change (7-day difference).  

---

## Author & Date  
- Author: [@hadisrour6](https://github.com/hadisrour6)  
- Version: 1.0.0  
- Date: August 2025  

---

## Technical Documentation  

**To run locally:**  

1. Install Python 3.7 or above. Download Python [here](https://www.python.org/).  

2. Edit `subreddits.json` to include the companies you want to track in the format:  

   ```json
   {
     "subreddit_name_here": "ticker_symbol_here"
   }

3. Run: python app.py
   
(Optional) Use a scheduler (like cron on Linux) to automate app.py calls.
