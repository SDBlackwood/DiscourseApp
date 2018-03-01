import textblob
from textblob import TextBlob

class Tokeniser():
    
    @staticmethod
    def tokenise_word_array(word_array):
        '''
        This uses textblob to part of speach tag (POS) the words
        returns: ?
        '''

        word_array = TextBlob(word_array)
        return word_array