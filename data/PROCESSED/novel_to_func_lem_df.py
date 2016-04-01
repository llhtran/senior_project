# Learning author writing style using 
# function words

# takes a novel
# divides into 10-sentence chunks
# creates tags for each chunks
# add as a row into dataframe

# returns dataframe

from spacy.en import English
import pandas as pd 

def novel_to_func_df(filename): 
	# get list of function words
	func_file = open("function+words.txt", 'r')
	fws = openfile.read().lower().split()
	fws = [word for word in fws if '\'' not in word]