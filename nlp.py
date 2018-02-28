import nltk
import Constants
nltk.download('words')

from nltk.tag import pos_tag_sents

sentance = "This is a test sentance.  George should like it"

tokens = nltk.word_tokenize(sentance, language='english')

print tokens

tagged = nltk.pos_tag(tokens)

print tagged
entities = nltk.chunk.ne_chunk(tagged)

print entities