# generate 2000 characters
# get 10 sentences
# spellcorrect
# turn into pos / func words column
# save to file
# import and predict

from spacy.en import English
import pandas as pd 
from enchant.checker import SpellChecker
import sys
import os

# given some number of characters
# extracts at most 10 sentence from the text
def ten_trim_chunk(text, nlp):
	for i, letter in enumerate(text):
		if letter == '.' and i < len(text)-2:
			first = i+2
			break
	text = text[first:] # starts from the next sentence.
	pt = nlp(unicode(text, "utf-8"))
	ten = []
	count = 0
	for sent in pt.sents:
		ten.append(sent)
		count += 1
		if count == 10:
			break
	par = [str(sen) for sen in ten]
	par = ' '.join(par)
	return par

def correct(text):
	chkr = SpellChecker("en_US")
	chkr.set_text(text)
	for err in chkr:
		sug = err.suggest()
		if sug:
			err.replace(sug[0])
	return chkr.get_text()

# turns a chunk of text into a data row of pos tags
def text_to_pos_df(text, nlp):
	pt = unicode(text, "utf-8")
	ps = nlp(pt)
	tags = [str(token.pos_) for token in ps]
	pairs = [tag1+'-'+tag2 for tag1, tag2 in zip(tags[:-1], tags[1:])]
	
	pos_tags = ['ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'X', 
			'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'EOL', 'SPACE']

	# create list of all possible combinations of consecutive tags
	tag_pairs = []
	for tag1 in pos_tags:
		for tag2 in pos_tags:
			tag_pairs.append(tag1+'-'+tag2)
	d = {key: [] for key in tag_pairs}
	for key in d:
		d[key].append(0)
	for pair in pairs:
		d[pair][-1] += 1
	df = pd.DataFrame(d)
	return df

# turns a chunk of text into a data row of func words
def text_to_func_df(text, nlp):
	func_file = open("../function+words.txt", 'r')
	fws = func_file.read().lower().split()
	fws = [word for word in fws if '\'' not in word]

	pt = unicode(text, "utf-8")
	ps = nlp(pt)

	d = {key: [] for key in fws}
	for key in d:
		d[key].append(0)
	for token in ps:
		if token.lemma_ in fws:
			d[token.lemma_][-1] += 1

	df = pd.DataFrame(d)
	return df

def sample_to_df(filename, nlp, typ):
	sample = open(filename, 'r+')
	s = sample.read()
	s = correct(s)
	block = ten_trim_chunk(s, nlp)
	if typ == "pos":
		df = text_to_pos_df(block, nlp) 
	else:
		df = text_to_func_df(block, nlp)
	return df

nlp = English()
print("Done loading English language")
frames = []
rootdir = sys.argv[1]
typ = sys.argv[2]
if typ == "pos": 
	print("Turning text into part-of-speech dataframes")
else:
	print("Turning text into function word dataframes")

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file[0] != '.':
			filename = os.path.join(subdir, file)
			frames.append(sample_to_df(filename, nlp, typ))
			print("Done %s" % filename)
author = pd.concat(frames)

if typ == "pos": 
	name = rootdir + "_sample_pos" + ".csv"
else:
	name = rootdir + "_sample_func" + ".csv"
author.to_csv(name, sep=',')