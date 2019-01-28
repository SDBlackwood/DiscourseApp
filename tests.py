
import unittest
from parser import Parser
from logger import TestLogger as p
from reddit import Reddit
from pymongo import MongoClient
from db import Mongo
from config import Config

class BaseCase(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class TestTensor(BaseCase):

    def testTensor(self):
        
        pass


class TestParser(BaseCase):

    def testToString(self):
        string_to_convert = "This is a test String"
        p.p("string", string_to_convert)
        word_array = Parser.run(string_to_convert)
        p.p("word", word_array)
        converted_string = Parser.toString(word_array)
        p.p("done", converted_string)
        assert(string_to_convert == converted_string)

    def testStripHTTPS(self):
        word_array_to_strip = ['https://t.co/6iY8tDmpkd|SOHU', 'IS', 'ICO', 'SOLUTION', 'AGENCY.\n💝💝💝#Airdrop', 'Now!!\nUse', 'my', 'referral', 'link:https://t.co/WEtRtbCSKc…', 'https://t.co/XZDiAyaDqM']
        p.p("Inital Word area: ", word_array_to_strip)
        stripped = Parser.strip_https(word_array_to_strip)
        p.p("Stripped Array: ", stripped)
        for word in stripped:
            assert(word.startswith('https') == False)

    def testA(self):
        import re
        pattern = re.compile(r'https')
        string_array = ['https://t.co/6iY8tDmpkd|SOHU', 'Random']
        stripped = [x for x in string_array if pattern.search(x) == None]
        print (stripped)
    
    def testConvertReturns(self):
        word_array_to_strip = ['AGENCY.\n💝💝💝#Airdrop', 'Now!!\nUse', 'my', 'referral', 'link:https://t.co/WEtRtbCSKc…', 'https://t.co/XZDiAyaDqM']
        p.p("Inital Word array: ", word_array_to_strip)
        stripped = Parser.convert_returns(word_array_to_strip)
        p.p("Stripped Array: ", stripped)

    def test_lower(self):
        test = "RT @kubernan: Healthcare Industry &amp; #Blockchain | CloudExpo #FinTech #Ethrereum #Bitcoin https://t.co/vLM2tdaMm2 #Cloud"
        tweet_str = Parser.tokenize(test)
        print(tweet_str)
        tweet_str = Parser.strip_https(tweet_str)
        print(tweet_str)
        tweet_str = Parser.strip_mentions(tweet_str)
        print(tweet_str)
        tweet_str = Parser.strip_tags(tweet_str)
        print(tweet_str)
        tweet_str = Parser.strip_re(tweet_str)
        tweet_str = Parser.strip_dead(tweet_str)
        tweet_str = Parser.strip_amp(tweet_str)
        tweet_str = Parser.lower(tweet_str)
        
        #tweet_str = Parser.convert_returns(tweet_str)
        print(tweet_str)

    def test_strip_tags(self):
        test = "RT @kubernan: Healthcare Industry &amp; #Blockchain | CloudExpo #FinTech #Ethrereum #Bitcoin https://t.co/vLM2tdaMm2 #Cloud"
        tweet_str = Parser.tokenize(test)
        #tweet_str = Parser.strip_https(tweet_str)
        #tweet_str = Parser.strip_mentions(tweet_str)
        print(tweet_str)
        tweet_str = Parser.strip_tags(tweet_str)
        #tweet_str = Parser.strip_re(tweet_str)
        #tweet_str = Parser.strip_dead(tweet_str)
        #tweet_str = Parser.lower(tweet_str)
        #tweet_str = Parser.strip_amp(tweet_str)
        #tweet_str = Parser.convert_returns(tweet_str)
        print(tweet_str)

    def test_concat_array(self):
        test_string_1 = ['This', 'is','the','first', 'string']
        test_string_2 = ['This', 'could','be','first', 'thing']
        string_array = []
        string_array.append(test_string_1)
        string_array.append(test_string_2)
        print (string_array)
        new_array = Parser.concatArray(string_array)
        print (new_array)
        assert(new_array == ['This', 'is','the','first', 'string','This', 'could','be','first', 'thing'])


class TestReddit(BaseCase):
   

    def test_reddit(self):
        #instantiate a reddit instance
        reddit = Reddit()
    
    def test_set_sub(self):
        reddit = Reddit()
        reddit.set_sub("worldnews")
        assert(reddit.sub=="worldnews")
    
    def get_top_ids(self):
        reddit = Reddit()
        result = reddit.get_top_ids()
        assert(type(result)==list)
        print (result)
    
class TestMongo(BaseCase):
    def test_connect(self):
        # call with none
        mongo = Mongo()
        assert(mongo.db.name == Config().config['DB']['prod'] )

        ## call with test
        mongo = Mongo(env="Test")
        assert(mongo.db.name == Config().config['DB']['test'] )

    def test_put_ids(self): 
        # set up the scenaior
        Mongo().put_ids(ids)

    def test_put_ids_same(self):
        mongo = Mongo(env="Test")
        mongo.db.ids.insert_one({"reddit_id":"aisb0hc"})
        ids = ["aisb0hc"]
        mongo.put_ids(ids)
        assert(mongo.get_ids()==ids)
        ids = ["aisb0hc","jshshfdif"]
        mongo.put_ids(ids)
        result = mongo.get_ids()
        assert(result==ids)
        mongo.db.ids.delete_one({"reddit_id":"aisb0hc"})
        mongo.db.ids.delete_one({"reddit_id":"jshshfdif"})
        assert(mongo.get_ids()==[])

    def test_get_ids(self):
        for a in Mongo().get_ids():
            print (a)
    



if __name__ == '__main__':
    unittest.main()

