import sys
import pandas as pd
import os
import praw
from datetime import date
from datetime import timedelta 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from config.config import reddit

is_github_actions = os.environ.get("GITHUB_ACTIONS") == "true"

try:
    from config.config import RedditConfig
except ImportError:
    pass

def connect_reddit() : 
    if(is_github_actions) :
        reddit = praw.Reddit(
        client_id = os.environ['CLIENT_ID'],
        client_secret = os.environ['CLIENT_SECRET'],
        password = os.environ['PASSWORD'],
        username = os.environ['USERNAME'],
        user_agent = os.environ['USER_AGENT']
        )
    else :
        reddit_config = RedditConfig()
        reddit = praw.Reddit(
            client_id = reddit_config.CLIENT_ID,
            client_secret = reddit_config.CLIENT_SECRET,
            password = reddit_config.PASSWORD,
            username = reddit_config.USERNAME,
            user_agent = reddit_config.USER_AGENT
        )
        
    return reddit    

def get_top_submission(subreddits, reddit):
    all_submission = []
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).top(time_filter="week"):
            all_submission.append(submission)
    return all_submission

def main():
    reddit = connect_reddit()
    week = date.today() - timedelta(date.today().weekday()) + timedelta(6)
    file_name = sys.path[0]+ "/../data/collected_data/" + week.strftime('%Y_%m_%d') + ".xlsx"
    subreddits = ['Nails', 'RedditLaqueristas', 'NailArt']

    # Get this week's top posts
    top_posts_df = pd.DataFrame(pd.Series(get_top_submission(subreddits, reddit)).unique(),columns=['id'])
    top_posts_df['title'] = top_posts_df['id'].apply(lambda x : x.title if str(x) not in set(top_posts_df['id']) else '0')
    top_posts_df = top_posts_df[top_posts_df['title']!='0']
    top_posts_df['image_url'] = top_posts_df['id'].apply(lambda x : x.url)
    top_posts_df['id'] = top_posts_df['id'].astype(str)

    # Save
    if os.path.isfile(file_name) :
        with pd.ExcelWriter(file_name, mode="a", if_sheet_exists="overlay", engine='openpyxl') as writer:
            top_posts_df.to_excel(writer, sheet_name = "top", index=False)
    else :
        top_posts_df.to_excel(file_name, sheet_name = "top", index=False)

main()