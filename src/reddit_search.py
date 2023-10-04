import config.config as reddit
import sys
import pandas as pd
import os
import requests
import time
import praw
import json
from datetime import date
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
class Post:
    def __init__(self, title, comments, content):
        self.title = title
        self.comments = comments
        self.content = content


reddit = praw.Reddit(
    client_id=reddit.client_id,
    client_secret=reddit.client_secret,
    password=reddit.password,
    username=reddit.username,
    user_agent=reddit.user_agent
)

subreddits = ['Nails', 'RedditLaqueristas']


def get_new_submission(subreddits):
    all_submission = []
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).top(time_filter="day", limit=1):
            all_submission.append(submission)

    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).new(limit=1):
            all_submission.append(submission)

    return all_submission


def get_all_comments(post):
    # TODO: Get a list of comments
    return comments


def main():
    all_submission = pd.Series(get_new_submission(subreddits))
    all_submission = all_submission.unique()
    all_posts = []
    for x in all_submission:
        post = Post(x.title, get_all_comments(x), x.selftext)
        all_posts.append(post)

    json_string = json.dumps([post.__dict__ for post in all_posts])
    with open("reddit_"+date.today().strftime('%Y_%m_%d')+".json", "w") as outfile:
        json.dump(json_string, outfile)

main()

# TODO:
# Top -  time_filter  = month
# New - limit 200
# For each post store title/comments/content - what else?
