
import unittest
from parser import Parser
from logger import TestLogger as p

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


if __name__ == '__main__':
    unittest.main()

