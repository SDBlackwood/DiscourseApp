#!/usr/bin/python3.5.2

import tweepy
from tweepy.auth import OAuthHandler
from my_constants import Auth
import json

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
            '''
            Hash returns a list of Status objects (containing json) - according to a tag
            '''
            for tweet in tweepy.Cursor(api.search, q=tag, count=count, lang="en", since=since).items(count):
                self.tweets.append(tweet)
            
            
        if(type=="user"):
            '''
            User returns a list of Status objects (containing json) - for a user
            '''
            self.tweets = tweepy.Cursor(api.user_timeline, screen_name=SNone).items(count)

    def get(self):
        return self.tweets


    def getText(self):
        """
        Removes the 'text' element of the json list and returns a list of text strings
        """
        items = list()
        for text in self.tweets:
            items.append(text.text)
        return items





