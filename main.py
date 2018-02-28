from tweets import Tweets
from parser import Parser

bitcoin = Tweets(type="hash", tag='#Bitcoin', 
                    count=5, since="2018-01-01")
#tweets = bitcoin.get()
tweets = bitcoin.getText()

# print (type(bitcoin))
# print (type(tweets))
# print (tweets[0])


## Pass in each tweet string to the parser and print
for t in tweets:
    tweet_str = Parser.run(t)

    # Here we will print out the list of cleaned tweets
    # We need to feed this into the 

    print (tweet_str)

        

    
    