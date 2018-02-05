from tweets import Tweets

bitcoin = Tweets(type="hash", tag='#Bitcoin', count=100, since="2018-01-01")
tweets = bitcoin.get()

for t in tweets:
    print (t.text)