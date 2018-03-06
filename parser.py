#!/usr/bin/python3.5.2
#import pandas as pd
import re
import numpy

#~ Technical parsing outwith semantic analysis

class Parser():

    @staticmethod
    def strip_https(word_array):
        stripped_array = [x for x in word_array if x.startswith('https') == False]
        pattern = re.compile(r'https://')
        stripped_array = [x for x in word_array if pattern.search(x) == None]
        return stripped_array

    @staticmethod
    def strip_tags(word_array):
        search = r'#'
        return Parser.replace(word_array, search, '')
    
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
    def replace(word_array, pattern, replace):
        p = re.compile(pattern)
        stripped_array = []
        for word in word_array:
            if(p.search(word)):
                word = word.replace(pattern, replace)
            stripped_array.append(word)
        return stripped_array

    @staticmethod
    def convert_returns(word_array):
        search = r'\n'
        return Parser.replace(word_array, search, '')

    @staticmethod
    def toString(word_array):
        string = str()
        for x in word_array:
            string += x +" "
        string = string[:-1]
        return string

    @staticmethod
    def concatArray(word_array_array):
        # [['Another'],['Words']]
        '''Pass a array '''
        concat_array = []
        for array in word_array_array:
            concat_array.extend(array)
        return concat_array

        

    @staticmethod
    def lower(word_array):
        lowered_array = [ x.lower() for x in word_array]
        return lowered_array


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
        tweet_str = Parser.lower(tweet_str)
        tweet_str = Parser.strip_amp(tweet_str)
        tweet_str = Parser.convert_returns(tweet_str)
        return tweet_str

