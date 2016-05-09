# CPSC 490 2015-16
# Senior Project
# Advisor: Professor Dana Angluin
# Author: Lien Tran, Yale College Class of 2016

# Learning author writing style using 
# part-of-speech tagging

# takes a novel
# divides into 10-sentence chunks
# creates tags for each chunks
# add as a row into dataframe

# returns dataframe

from spacy.en import English
import pandas as pd 

def novel_to_pos_df(filename): 
	# because there's no documented way of doing this...
	tags = ['ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'X', 
			'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'EOL', 'SPACE']

	# create list of all possible combinations of consecutive tags
	tag_pairs = []
	for tag1 in tags:
		for tag2 in tags:
			tag_pairs.append(tag1+'-'+tag2)


	nlp = English()
	openfile = open(filename, 'r+')
	s = openfile.read()
	u = unicode(s, "utf-8")

	# processed unicode string
	pu = nlp(u)

	# creating a dictionary for effective counting
	d = {key: [] for key in tag_pairs}

	ten_sents = [] # contains chunks of 10 sentences or less
	chunk = []
	# for every sentence in the text
	for i, sent in enumerate(pu.sents):
		# if it's the 10th, 20th, etc, then start new chunk
		# else just add it to the current chunk
		if i%10 == 0:
			chunk = []
		chunk.append(sent)
		# if it's the last sentence of a chunk, then add chunk to ten_sents
		if i%10 == 9:
			ten_sents.append(chunk)
	# edge case: when sentences run out, add whatever chunk is left
	if chunk:
		ten_sents.append(chunk)

	for chunk in ten_sents:
		# turning each chunk into a pure text chunk again
		text_chunk = [unicode(str(sen), "utf-8") for sen in chunk]
		text_chunk = ''.join(text_chunk)
		# process sentence again
		ps = nlp(text_chunk)
		tags = [str(token.pos_) for token in ps]
		# creating a dictionary for effective counting
		pairs = [tag1+'-'+tag2 for tag1, tag2 in zip(tags[:-1], tags[1:])]
		for key in d:
			d[key].append(0)
		for pair in pairs:
			d[pair][-1] += 1

	df = pd.DataFrame(d)
	return df
	# df.to_csv("persuasion.csv", sep=',')

# novel_to_df("austen/persuasion.txt")