# part-of-speech tagger
# trying to figure out if I need to keep the newlines in the data

from spacy.en import English
from spacy.parts_of_speech import ADV

def is_adverb(token):
    return token.pos == spacy.parts_of_speech.ADV

def is_plural_noun(token):
    return token.tag == NNS or token.tag == NNPS

def print_coarse_pos(token):
    print(token.pos_)

def print_fine_pos(token):
    print(token.tag_)

nlp = English()
doc = nlp(u"Hello, world. Here are two sentences.\n\nWhat's up?")
NNS = nlp.vocab.strings['NNS']
NNPS = nlp.vocab.strings['NNPS']
