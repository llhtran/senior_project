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

austen = pd.read_csv("austen.csv")
twain = pd.read_csv("twain.csv")
dickens = pd.read_csv("dickens.csv")

# need to revise this
# currently just dropping all columns that = 0 in twain
drop_columns = twain.ix[:, (twain == 0).all()].columns

austen_drop = austen.drop(drop_columns, 1).drop(['Unnamed: 0'], 1)
twain_drop = twain.drop(drop_columns, 1).drop(['Unnamed: 0'], 1)
dickens_drop = dickens.drop(drop_columns, 1).drop(['Unnamed: 0'], 1)

austen_drop['type']=0
twain_drop['type']=1
dickens_drop['type']=0

frames = [austen_drop, twain_drop, dickens_drop]
all_authors = pd.concat(frames)

X = all_authors.drop(['type'], 1)
Y = all_authors['type']

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y,
									test_size=0.4, random_state=0)

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
svm.fit(X_test, Y_test)
predsvm = svm.predict(X_test)
score = metrics.accuracy_score(Y_test, predsvm)
print "SVM ", score



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
