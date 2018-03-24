
import unittest
import pprint
from tweets import Tweets
from logger import TestLogger as p
from parser import Parser
from model import Model

import collections
import math
import os
import sys
import argparse
import random
from tempfile import gettempdir
import zipfile
import traceback
import sys
import pprint


import numpy as np
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

from tensorflow.contrib.tensorboard.plugins import projector

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

def get(self):
    bitcoin = Tweets(type="hash", tag='#Bitcoin', 
                    count=50, since="2018-01-01")
    tweets = bitcoin.getText()
    bag = []
    for t in tweets:
        tweet_str = Parser.run(t)
        bag.extend(tweet_str)
    return bag

class TestTensor(BaseCase):

    def testTensor(self):
        pass

    def test_reverse(self):
        words = get(self)
        vocabulary_size = 10000
        """Process raw inputs into a dataset."""
        count = [['UNK', -1]] 
        # Basically add all the top used words from the word array 
        count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
        dictionary = dict()
        print (count)
        for word, _ in count:
            # For each str, make an entry into the dictionary and asign it a number
            # e.g ['word'] : 1
            dictionary[word] = len(dictionary)
        data = list()
        unk_count = 0
        for word in words:
            index = dictionary.get(word, 0)
            if index == 0:  # dictionary['UNK']
                unk_count += 1
                print (unk_count)
            data.append(index)
        data_len = len(data)    
        count[0][1] = unk_count
        print (dictionary.values())
        print (dictionary.keys())
        reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        p.pprint(reversed_dictionary)
        p.pprint(reversed_dictionary[1].shape)
        p.pprint(data_len)
        for i in xrange(len(reversed_dictionary)-1):
            p.pprint(reversed_dictionary[i])

class TestModel(BaseCase):

    def test_(self):
        sentances = []
        sentances.append('I am a sentance')
        sentances.append('I am another cool thing')
        print (sentances)
        vec = Model()
        vec.train(sentances)
        vec.plot()

class TestParser(BaseCase):

    def test_strip_stop(self):
        tweets = ['RT @GymRewards: a the to in but of for Join the GYM Rewards Beta @ https://t.co/PmWCZISLYL … … #GYMRewards, #ICO #cryptocurrency #mobile #app #mining #exercising…']
        for t in tweets:
            tweet_str = Parser.run(t)
            tweet_str = Parser.strip_stop_words(tweet_str)
        

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
    
        tweet_str = Parser.run(test)
        #tweet_str = Parser.strip_https(tweet_str)
        #tweet_str = Parser.strip_mentions(tweet_str)
        pprint.pprint(tweet_str)
        #tweet_str = Parser.strip_tags(tweet_str)
        #tweet_str = Parser.strip_re(tweet_str)
        #tweet_str = Parser.strip_dead(tweet_str)
        #tweet_str = Parser.lower(tweet_str)
        #tweet_str = Parser.strip_amp(tweet_str)
        #tweet_str = Parser.convert_returns(tweet_str)
        #print(tweet_str)

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


    def test_all(self):
        test = "RT @kubernan: Healthcare Industry &amp; #Blockchain | CloudExpo #FinTech #Ethrereum #Bitcoin https://t.co/vLM2tdaMm2 #Cloud"
        tweet_str = Parser.run(test)
        #tweet_str = Parser.strip_https(tweet_str)
        #tweet_str = Parser.strip_mentions(tweet_str)
       # print(tweet_str)
        #tweet_str = Parser.strip_tags(tweet_str)
        #tweet_str = Parser.strip_re(tweet_str)
        #tweet_str = Parser.strip_dead(tweet_str)
        #tweet_str = Parser.lower(tweet_str)
        #tweet_str = Parser.strip_amp(tweet_str)
        #tweet_str = Parser.convert_returns(tweet_str)
        print(tweet_str)

if __name__ == '__main__':
    unittest.main()

