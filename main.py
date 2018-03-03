from tweets import Tweets
from parser import Parser
from sentiment import Tokeniser
from logger import ApplicationLogger

bitcoin = Tweets(type="hash", tag='#Bitcoin', 
                    count=5, since="2018-01-01")

tweets = bitcoin.getText()

## Pass in each tweet string to the parser and print
for t in tweets:
    # Gets a cleaned word array for this tweet
    tweet_str = Parser.run(t)
    # Converts back to a string
    tweet_str = Parser.toString(tweet_str)
    # POS Tags the string tweet
    tweet_str = Tokeniser.tokenise_word_array(tweet_str)
    # Here we will print out the list of cleaned tweets
    # We need to feed this into the nlp tokeniser

    print (tweet_str.tags)
    print (tweet_str.sentiment.polarity)
    ApplicationLogger.debug(tweet_str.noun_phrases)

        

    
    