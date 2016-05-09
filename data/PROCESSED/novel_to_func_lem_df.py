# CPSC 490 2015-16
# Senior Project
# Advisor: Professor Dana Angluin
# Author: Lien Tran, Yale College Class of 2016

# Learning author writing style using 
# function words

# takes a novel
# divides into 10-sentence chunks
# creates tags for each chunks
# add as a row into dataframe

# returns dataframe

from spacy.en import English
import pandas as pd 

def novel_to_func_lem_df(filename): 
	# get list of function words
	func_file = open("function+words.txt", 'r')
	fws = func_file.read().lower().split()
	fws = [word for word in fws if '\'' not in word]

	nlp = English()
	openfile = open(filename, 'r+')
	s = openfile.read()
	u = unicode(s, "utf-8")

	# processed unicode string
	pu = nlp(u)

	# creating a dictionary for effective counting
	d = {key: [] for key in fws}

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
		for key in d:
			d[key].append(0)
		for token in ps:
			if token.lemma_ in fws:
				d[token.lemma_][-1] += 1

	df = pd.DataFrame(d)
	return df


