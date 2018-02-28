from tweets import Tweets

bitcoin = Tweets(type="hash", tag='#Bitcoin', count=5, since="2018-01-01")
#tweets = bitcoin.get()
tweets = bitcoin.getText()

# print (type(bitcoin))
# print (type(tweets))
# print (tweets[0])

for t in tweets:
    #print (dir(t))
    print (t)
    
    