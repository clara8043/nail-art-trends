
# Nail Art Design Trends
- Collect data from nail art related subreddits and etsy
- analyze how many posts each store has and what type of keywords they use (which stores show up in front 5 pages)

## Reddit data collection
- "New" and "Top" posts saved every week using github actions workflow
- /src/reddit_daily.py
    - Save "New" posts every day at 11:59 pm UTC
    - Accumulated weekly data is saved to 1 file (/data/{year}_{month}_{last day of week-Sunday}.xlsx, sheet name = "new")
- /src/reddit_weekly.py
    - Save weekly "Top" posts on Sunday of every week at 11:59 pm UTC
    - Data is saved into file (/data/{year}_{month}_{last day of week-Sunday}.xlsx, sheet name = "top")
