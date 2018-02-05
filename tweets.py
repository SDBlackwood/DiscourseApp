import tweepy
from tweepy.auth import OAuthHandler
from constants import Auth

# Twitter access keys 
consumer_key = Auth.consumer_key()
consumer_secret = Auth.consumer_secret()

access_token = Auth.access_token()
access_token_secret = Auth.access_secret()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print ('Error! Failed to get request token.')

api = tweepy.API(auth)

class Tweets():

    tweets = []

    def __init__(self, type=None, count=100, since=None, tag=None, user=None):
        if(type=="hash"):
            self.tweets = tweepy.Cursor(api.search, q=tag, count=count, lang="en", since=since).items()
            
        if(type=="user"):
            self.tweets = tweepy.Cursor(api.user_timeline, screen_name=SNone).items(count)

    def get(self):
        return self.tweets




