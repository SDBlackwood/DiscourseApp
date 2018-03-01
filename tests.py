
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


class TestParserToString(BaseCase):

    string_to_convert = "This is a test String"
    p.p("string", string_to_convert)
    word_array = Parser.run(string_to_convert)
    p.p("word", word_array)
    converted_string = Parser.toString(word_array)
    p.p("done", converted_string)
    assert(string_to_convert == converted_string)


if __name__ == '__main__':
    unittest.main()

