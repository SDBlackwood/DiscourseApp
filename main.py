from tweets import Tweets
from parser import Parser
from sentiment import Tokeniser
from logger import ApplicationLogger as p
import collections
from tensor import Tensor

bitcoin = Tweets(type="hash", tag='#Bitcoin', 
                    count=20, since="2018-01-01")

tweets = bitcoin.getText()

bag = []

## Pass in each tweet string to the parser and print

for t in tweets:
    # Print raw tweet
    ##p.p("Raw Tweet", t)
    # Gets a cleaned word array for this tweet
    tweet_str = Parser.run(t)
    ##p.p("Word Array: ", tweet_str)
    # Converts back to a string
    #tweet_str = Parser.toString(tweet_str)
    #print(tweet_str)

    # POS Tags the string tweet
    ##print ("POS Tagges Array:")
    #tweet_str = Tokeniser.tokenise_word_array(tweet_str)
    # Here we will print out the list of cleaned tweets
    # We need to feed this into the nlp tokeniser
    #print (tweet_str.tags)
    #p.p("Sentiment: ", tweet_str.sentiment.polarity)
    #p.p("Entities: ",tweet_str.noun_phrases)
    #print("")
    bag.extend(tweet_str)

# concat_array = Parser.concatArray(tweets)
# print (concat_array)
# start = [['UNK', -1]]
# n_words = len(bag)
# start.extend(collections.Counter(bag).most_common(n_words - 1))
# print (start)

tensor = Tensor()
tensor.run(bag)


    

        

    
     