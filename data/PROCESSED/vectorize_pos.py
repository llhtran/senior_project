# CPSC 490 2015-16
# Senior Project
# Advisor: Professor Dana Angluin
# Author: Lien Tran, Yale College Class of 2016

# practice code for counting all tag pairs in a novel

from spacy.en import English
import sys

# because there's no documented way of doing this...
tags = ['ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'X', 
		'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'EOL', 'SPACE']

# create list of all possible combinations of consecutive tags
tag_pairs = []
for tag1 in tags:
	for tag2 in tags:
		tag_pairs.append(tag1+'-'+tag2)


nlp = English()
openfile = open("austen/emma.txt", 'r+')
s = openfile.read()
u = unicode(s, "utf-8")

# processed unicode string
pu = nlp(u)

# turn string into array of tags
pos_tags = [str(token.pos_) for token in pu]

# creating a dictionary for effective counting
d = dict.fromkeys(tag_pairs, 0)

# count consecutive pairs of tags for each category
pairs = [tag1+'-'+tag2 for tag1, tag2 in zip(pos_tags[:-1], pos_tags[1:])]

for pair in pairs:
	d[pair] += 1

# make dictionary into a numpy array / pandas dataframe
