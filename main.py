from tweets import Tweets
from parser import Parser
from sentiment import Tokeniser
from logger import ApplicationLogger as p
import collections
from tensor import Tensor
import pprint
from model import Model
from reddit import Reddit
from db import Mongo
import importlib

#bitcoin = Tweets(type="hash", tag='#Bitcoin', 
                    #count=500, since="2018-01-01")
#tweets = bitcoin.getText()

#bag = []

## Pass in each tweet string to the parser and print

#for t in tweets:
 #   tweet_str = Parser.run(t)
  #  bag.extend(tweet_str)
    

#tensor = Tensor(10001)
#tensor.run(bag)

# Word to Vec model
# Get a stripped list of tweets
#for t in tweets:
 #   tweet_str = Parser.run(t)
    #tweet_str = Parser.toString(tweet_str)
    # Append to the bag to get a list of tweet strings
  #  bag.append(tweet_str)

    # Expect to see a list of words in 1 tweet
#print (bag)


#w2v = Model()
#w2v.train(bag)
#w2v.plot()
reddit = Reddit()
db = Mongo()

## set the sub and get the top ids for it
reddit.set_sub("worldnews")
ids = reddit.get_top_ids()

## put ids into the db
db.put_ids(ids)
print([x for x in db.get_ids()])





    

        

    
     