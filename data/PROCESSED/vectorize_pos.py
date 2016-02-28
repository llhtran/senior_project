from spacy.en import English
import sys

nlp = English()
s = open(sys.argv[1], 'r+')
u = unicode(s, "utf-8")