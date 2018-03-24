#!/usr/bin/python3.5.2
#import pandas as pd
import re
import numpy
import nltk

import pprint as p

#~ Technical parsing outwith semantic analysis

class Parser():

    @staticmethod
    def strip_https(word_array):
        stripped_array = [x for x in word_array if x.startswith('https') == False]
        pattern = re.compile(r'https://')
        stripped_array = [x for x in word_array if pattern.search(x) == None]
        return stripped_array

    @staticmethod
    def remove_stop_words(corpus_raw):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        raw_sentences = tokenizer.tokenize(corpus_raw)
        #sentence where each word is tokenized
        sentences = []

        def sentence_to_wordlist(raw):
            clean = re.sub("[^a-zA-Z]"," ", raw)
            words = clean.split()
            return words

        for raw_sentence in raw_sentences:
            if len(raw_sentence) > 0:
                sentences.append(sentence_to_wordlist(raw_sentence))

        p.pprint(raw_sentences)
        p.pprint(sentence_to_wordlist(raw_sentences))       
    
    @staticmethod
    def strip_tags(word_array):
        search = r'#'
        return Parser.replace(word_array, search, '')
    
    @staticmethod
    def utf(word_array):
        return [u"{}".format(a) for a in word_array]
    
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
    def strip_stop_words(word_array):
        # Give me an array of words
        # Set up the stop words
        stop_words = set('for a as at you you I go this get of is the and | to in it . .. ... - / '.split())
        text = [x for x in word_array if x not in stop_words]
        return text


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
        tweet_str = Parser.strip_stop_words(tweet_str)
        tweet_str = Parser.utf(tweet_str)
        return tweet_str
    