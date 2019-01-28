
from my_constants import Auth
import praw

class Reddit():

    def __init__(self):
        client_id, client_secret, user_agent, password, username = Auth.reddit()
        self.reddit = praw.Reddit(
                        client_id=client_id, 
                        client_secret=client_secret, 
                        user_agent=user_agent,
                        password=password,
                        username=username
                        )
        self.sub = "worldnews"

    def run(self):
        ids = self.reddit.get_top_ids("worldnews")

    def set_sub(self, sub):
        """
        sets a str as what sub we are looking for
        """
        self.sub = sub

    def get_top_ids(self, num=25):
        """
        return [str] ids
        """
        top = self.reddit.subreddit(self.sub).hot(limit=num)
        ids = []
        for submission in top:
            ids.append(submission.id)
        return ids


    def func(self):
        submission = reddit.submission(url='https://www.reddit.com/r/Bitcoin/comments/86sdic/how_bitcoin_became_popular_in_my_company_because/')
        for top_level_comment in submission.comments:
            print(top_level_comment.body)


    