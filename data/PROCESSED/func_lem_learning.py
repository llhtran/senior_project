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

austen = pd.read_csv("austen_func_lem.csv")
twain = pd.read_csv("twain_func_lem.csv")
dickens = pd.read_csv("dickens_func_lem.csv")

austen_pred = 0
twain_pred = 0
dickens_pred = 1

austen_drop = austen.drop(['Unnamed: 0'], 1)
twain_drop = twain.drop(['Unnamed: 0'], 1)
dickens_drop = dickens.drop(['Unnamed: 0'], 1)

print("Distinguish AUSTEN %d; TWAIN %d; DICKENS %d; - FUNC" % 
		(austen_pred, twain_pred, dickens_pred))
austen_drop['type']= austen_pred
twain_drop['type']= twain_pred
dickens_drop['type']= dickens_pred

frames = [austen_drop, twain_drop, dickens_drop]
all_authors = pd.concat(frames)

X = all_authors.drop(['type'], 1)
Y = all_authors['type']

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y,
									test_size=0.25, random_state=0)

rf = ensemble.RandomForestClassifier(n_estimators=175, max_features=15, n_jobs=-1)
rf.fit(X_train, Y_train)
pred = rf.predict(X_test)
score = metrics.accuracy_score(Y_test, pred)
print "Random Forest ", score

a = zip(rf.feature_importances_, X_train.dtypes.index)
s = sorted(a, key=lambda x: x[0])
for pair in s:
	print(pair)

svm = svm.SVC()
svm.fit(X_train, Y_train)
predsvm = svm.predict(X_test)
score = metrics.accuracy_score(Y_test, predsvm)
print "SVM ", score

print("Predicting generated data")
austen_gen = pd.read_csv("gen_samples/austen_sample_func.csv")
twain_gen = pd.read_csv("gen_samples/twain_sample_func.csv")
dickens_gen = pd.read_csv("gen_samples/dickens_sample_func.csv")
austen_gen_drop = austen_gen.drop(['Unnamed: 0'], 1)
twain_gen_drop = twain_gen.drop(['Unnamed: 0'], 1)
dickens_gen_drop = dickens_gen.drop(['Unnamed: 0'], 1)

austen_gen_drop['type']= austen_pred
twain_gen_drop['type']= twain_pred
dickens_gen_drop['type']= dickens_pred

frames = [austen_gen_drop, twain_gen_drop, dickens_gen_drop]
all_gen = pd.concat(frames)

X_gen_test = all_gen.drop(['type'], 1)
Y_gen_test = all_gen['type']

gen_score = metrics.accuracy_score(Y_gen_test, rf.predict(X_gen_test))
print "Random Forest predict generated data: ", gen_score
gen_score = metrics.accuracy_score(Y_gen_test, svm.predict(X_gen_test))
print "SVM predict generated data: ", gen_score

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
