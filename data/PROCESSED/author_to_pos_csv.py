# CPSC 490 2015-16
# Senior Project
# Advisor: Professor Dana Angluin
# Author: Lien Tran, Yale College Class of 2016

import os
import sys
import pandas as pd
import novel_to_pos_df

# pass in a folder of novels of a particular author
# this file will turn each novel into a dataframe
# and compile all novels into one dataframe
# and outputs that as a csv file with the author's name as title

frames = []
rootdir = sys.argv[1]
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file[0] != '.':
			filename = os.path.join(subdir, file)
			frames.append(novel_to_pos_df.novel_to_pos_df(filename))
author = pd.concat(frames)
name = rootdir + "_pos" + ".csv"
author.to_csv(name, sep=',')
