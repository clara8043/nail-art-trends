import sys
import pandas as pd
import os
import requests
import time
import praw
from datetime import date
from datetime import timedelta 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import config.config as reddit

#config
reddit = praw.Reddit(
    client_id=reddit.client_id,
    client_secret=reddit.client_secret,
    password=reddit.password,
    username=reddit.username,
    user_agent=reddit.user_agent
)

def get_top_submission(subreddits):
    all_submission = []
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).top(time_filter="week"):
            all_submission.append(submission)
    return all_submission


def main():
    week = date.today() - timedelta(date.today().weekday()) + timedelta(6)
    file_name = week.strftime('%Y_%m_%d') + ".xlsx"
    subreddits = ['Nails', 'RedditLaqueristas', 'NailArt']

    # Get this week's top posts
    top_posts_df = pd.DataFrame(pd.Series(get_new_submission(subreddits)).unique(),columns=['id'])
    top_posts_df['title'] = new_posts_df['id'].apply(lambda x : x.title)
    top_posts_df['image_url'] = new_posts_df['id'].apply(lambda x : x.url)

    # Save in pre-existing sheet
    top_posts_df['id'] = all_posts_df['id'].astype(str)
    top_posts_df.to_excel(file_name, sheet_name = "new",index=False, encoding='utf-8-sig', engine='xlsxwriter')

main()