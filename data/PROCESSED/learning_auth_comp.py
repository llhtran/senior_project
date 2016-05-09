# CPSC 490 2015-16
# Senior Project
# Advisor: Professor Dana Angluin
# Author: Lien Tran, Yale College Class of 2016

import sys
import argparse
import numpy as np
from sklearn import neighbors as nb
from sklearn import ensemble 
from sklearn import metrics
from sklearn import svm
from sklearn import linear_model as lm
from sklearn import decomposition as deco
from sklearn import cross_validation
import pandas as pd
import matplotlib.pyplot as plt

austen_pred = 0
twain_pred = 0
dickens_pred = 1

see_rd_features = True

austen_pos = pd.read_csv("austen.csv")
comp_pos= pd.read_csv("gen_samples/austen_sample_pos.csv")

austen_pos = austen_pos.drop(['Unnamed: 0'], 1)
comp_pos = comp_pos.drop(['Unnamed: 0'], 1)

austen_func = pd.read_csv("austen_func_lem.csv")
comp_func = pd.read_csv("gen_samples/austen_sample_func.csv")

austen_func = austen_func.drop(['Unnamed: 0'], 1)
comp_func = comp_func.drop(['Unnamed: 0'], 1)

austen = pd.concat([austen_pos, austen_func], axis=1, join_axes=[austen_pos.index])
comp = pd.concat([comp_pos, comp_func], axis=1, join_axes=[comp_pos.index])

austen['type'] = 1
comp['type'] = 0

frames = [austen, comp]
ALL = pd.concat(frames)

X = ALL.drop(['type'], 1)
Y = ALL['type']

# print("Distinguish AUSTEN %d; TWAIN %d; DICKENS %d; - PART OF SPEECH" % 
		# (austen_pred, twain_pred, dickens_pred))
# austen['type']= austen_pred
# twain['type']= twain_pred
# dickens['type']= dickens_pred

# frames = [austen, twain, dickens]
# all_authors = pd.concat(frames)

# X = all_authors.drop(['type'], 1)
# Y = all_authors['type']

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y,
									test_size=0.5, random_state=0)

rf = ensemble.RandomForestClassifier(n_estimators=175, max_features=15, n_jobs=-1)
rf.fit(X_train, Y_train)
pred = rf.predict(X_test)
score = metrics.accuracy_score(Y_test, pred)
print "Random Forest ", score

if see_rd_features: 
	a = zip(rf.feature_importances_, X_train.dtypes.index)
	s = sorted(a, key=lambda x: x[0], reverse=True)
	for pair in s:
		print pair[1], pair[0]

svm = svm.SVC()
svm.fit(X_train, Y_train)
predsvm = svm.predict(X_test)
score = metrics.accuracy_score(Y_test, predsvm)
print "SVM ", score

# print("Predicting generated data")
# austen_gen_pos = pd.read_csv("gen_samples/austen_sample_pos.csv")
# twain_gen_pos = pd.read_csv("gen_samples/twain_sample_pos.csv")
# dickens_gen_pos = pd.read_csv("gen_samples/dickens_sample_pos.csv")
# austen_gen_pos = austen_gen_pos.drop(['Unnamed: 0'], 1)
# twain_gen_pos = twain_gen_pos.drop(['Unnamed: 0'], 1)
# dickens_gen_pos = dickens_gen_pos.drop(['Unnamed: 0'], 1)

# austen_gen_func = pd.read_csv("gen_samples/austen_sample_func.csv")
# twain_gen_func = pd.read_csv("gen_samples/twain_sample_func.csv")
# dickens_gen_func = pd.read_csv("gen_samples/dickens_sample_func.csv")
# austen_gen_func = austen_gen_func.drop(['Unnamed: 0'], 1)
# twain_gen_func = twain_gen_func.drop(['Unnamed: 0'], 1)
# dickens_gen_func = dickens_gen_func.drop(['Unnamed: 0'], 1)

# austen_gen = pd.concat([austen_gen_pos, austen_gen_func], axis=1, join_axes=[austen_gen_pos.index])
# twain_gen = pd.concat([twain_gen_pos, twain_gen_func], axis=1, join_axes=[twain_gen_pos.index])
# dickens_gen = pd.concat([dickens_gen_pos, dickens_gen_func], axis=1, join_axes=[dickens_gen_pos.index])

# austen_gen['type']= austen_pred
# twain_gen['type']= twain_pred
# dickens_gen['type']= dickens_pred

# frames = [austen_gen, twain_gen, dickens_gen]
# all_gen = pd.concat(frames)

# X_gen_test = all_gen.drop(['type'], 1)
# Y_gen_test = all_gen['type']

# gen_score = metrics.accuracy_score(Y_gen_test, rf.predict(X_gen_test))
# print "Random Forest predict generated data: ", gen_score
# gen_score = metrics.accuracy_score(Y_gen_test, svm.predict(X_gen_test))
# print "SVM predict generated data: ", gen_score

# principal component analysis
# x = (X - np.mean(X, 0)) / np.std(X, 0)
# n_components = 15
# pca = deco.PCA(n_components)
# x_r = pca.fit(x).transform(x)
# print ('explained variance (first %d components): %.2f'%(n_components, sum(pca.explained_variance_ratio_)))

# http://mlpy.sourceforge.net/docs/3.2/tutorial.html
# How to figure out which components were most important?
# Why do we need to normalize for PCA?
# How do we see what distinguishes Twain from others? 
