#!/usr/bin/python3.5.2
import pandas as pd
import re

#~ Technical parsing outwith semantic analysis

class Parser():

    @staticmethod
    def strip_https(word_array):
        stripped_array = [x for x in word_array if x.startswith('https') == False]
        return stripped_array

    @staticmethod
    def strip_tags(word_array):
        stripped_array = [x.replace('#', '') for x in word_array if x.startswith('#') == False]
        return stripped_array
    
    @staticmethod
    def strip_mentions(word_array):
        stripped_array = [x.replace('@', '') for x in word_array if x.startswith('@') == False]
        return stripped_array

    @staticmethod
    def strip_re(word_array):
        stripped_array = [x for x in word_array if x.startswith('RT') == False]
        return stripped_array
    
    @staticmethod
    def strip_dead(word_array):
        stripped_array = [x for x in word_array if x != ('')]
        return stripped_array

    @staticmethod
    def strip_amp(word_array):
        stripped_array = [x for x in word_array if x.startswith('&amp') == False]
        return stripped_array

    @staticmethod
    def convert_returns(word_array):
        pattern = re.compile(r'\n')
        stripped_array = [x.replace('\n', '') for x in word_array if pattern.findall(x)]
        return stripped_array


    @staticmethod
    def tokenize(tweet_str):
        return [x.strip() for x in tweet_str.split(' ')]

    @staticmethod
    def run(tweet_str):
        tweet_str = Parser.tokenize(tweet_str)
        tweet_str = Parser.strip_https(tweet_str)
        tweet_str = Parser.strip_mentions(tweet_str)
        tweet_str = Parser.strip_tags(tweet_str)
        tweet_str = Parser.strip_re(tweet_str)
        tweet_str = Parser.strip_dead(tweet_str)
        tweet_str = Parser.strip_amp(tweet_str)
        #tweet_str = Parser.convert_returns(tweet_str)
        return tweet_str

