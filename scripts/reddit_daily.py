import sys
import pandas as pd
import os
import praw
from datetime import date
from datetime import timedelta 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from config.config import RedditConfig

def connect_reddit() : 
    if(os.getenv("GITHUB_ACTIONS") != False) :
        reddit_config = RedditConfig()
        reddit = praw.Reddit(
            client_id = reddit_config.CLIENT_ID,
            client_secret = reddit_config.CLIENT_SECRET,
            password = reddit_config.PASSWORD,
            username = reddit_config.USERNAME,
            user_agent = reddit_config.USER_AGENT
        )
    else :
        reddit = praw.Reddit(
        client_id = os.environ['CLIENT_ID'],
        client_secret = os.environ['CLIENT_SECRET'],
        password = os.environ['PASSWORD'],
        username = os.environ['USERNAME'],
        user_agent = os.environ['USER_AGENT']
        )
    return reddit    

def get_new_submission(subreddits, reddit):
    all_submission = []
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).new():
            all_submission.append(submission)
    return all_submission

def main():
    reddit = connect_reddit()
    week = date.today() - timedelta(date.today().weekday()) + timedelta(6)
    file_name = sys.path[0]+ "/../data/collected_data/" + week.strftime('%Y_%m_%d') + ".xlsx"
    subreddits = ['Nails', 'RedditLaqueristas', 'NailArt']

    # Get pre-existing posts if file for this week exists
    try:
        all_posts_df = pd.read_excel(file_name, sheet_name ="new")
        if(len(all_posts_df)==0):
            all_posts_df = pd.DataFrame(columns=['id','title','image_url'])
    except :
        all_posts_df = pd.DataFrame(columns=['id','title','image_url'])

    # Get today's new posts
    new_posts_df = pd.DataFrame(pd.Series(get_new_submission(subreddits, reddit)).unique(),columns=['id'])
    new_posts_df['title'] = new_posts_df['id'].apply(lambda x : x.title if str(x) not in set(all_posts_df['id']) else '0')
    new_posts_df = new_posts_df[new_posts_df['title']!='0']
    new_posts_df['image_url'] = new_posts_df['id'].apply(lambda x : x.url)

    #Concat all and save 
    all_posts_df = pd.concat([all_posts_df,new_posts_df],ignore_index=True)
    all_posts_df['id'] = all_posts_df['id'].astype(str)

    if os.path.isfile(file_name) :
        with pd.ExcelWriter(file_name, mode="a", if_sheet_exists="overlay") as writer:
            all_posts_df.to_excel(writer, sheet_name = "new", index=False)
    else :
        all_posts_df.to_excel(file_name, sheet_name = "new", index=False)

main()
