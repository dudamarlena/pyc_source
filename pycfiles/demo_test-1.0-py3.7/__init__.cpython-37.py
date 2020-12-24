# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mL\__init__.py
# Compiled at: 2018-12-19 04:10:38
# Size of source mod 2**32: 3391 bytes
"""
Created on Tue Dec 11 14:40:40 2018

@author: Zhong-Ying Wang
"""
import numpy as np, math
from sklearn import svm
import csv
from sklearn.model_selection import train_test_split
import re
from sklearn.preprocessing import StandardScaler
import copy

def turn_to_train(x):
    train = []
    target = []
    length = len(x)
    length2 = len(x[0])
    test_len = int(length * 8 / 10)
    for i in range(0, test_len):
        train.append(x[i][0:length2 - 1])
        target.append(x[i][(length2 - 1)])

    return (train, target)


def turn_to_test(x):
    test = []
    target = []
    length = len(x)
    length2 = len(x[0])
    test_len = int(length * 8 / 10)
    for i in range(test_len, length):
        test.append(x[i][0:length2 - 1])
        target.append(x[i][(length2 - 1)])

    return (test, target)


def del_array(x):
    length = len(x)
    length2 = len(x[0])
    for i in range(0, length):
        del x[i][length2 - 1]

    return x


array = []
array_temp = []
array_temp2 = []
array_temp3 = []
with open('資料集處理過.txt', 'r') as (f):
    a = f.readlines()
    for line in a:
        temp = line.split()
        temp = list(map(int, temp))
        array_temp.append(temp)

train, train_target = turn_to_train(array_temp)
test, test_target = turn_to_test(array_temp)
clf = svm.SVC()
clf.fit(train, train_target)
result = clf.predict(test)
print(result)
print(len(result))
print(clf.score(test, test_target))
array_temp2 = copy.deepcopy(array_temp)
array_temp2 = del_array(array_temp2)
from sklearn.decomposition import PCA
pca = PCA(n_components=8)
array = pca.fit_transform(array_temp2)
print(len(array))
train2, train_target2 = turn_to_train(array)
test2, test_target2 = turn_to_test(array)
clf = svm.SVC()
clf.fit(train2, train_target)
result2 = clf.predict(test2)
print(result2)
print(len(train2), '  ', len(train_target2), '  ', len(test2), '  ', len(test_target2))
print(len(result2))
print(clf.score(test2, test_target))
array_temp3 = copy.deepcopy(array_temp)
for i in range(0, len(array_temp)):
    del array_temp3[i][23]
    del array_temp3[i][21]
    del array_temp3[i][10]
    del array_temp3[i][9]
    del array_temp3[i][3]
    del array_temp3[i][1]

train, train_target = turn_to_train(array_temp3)
test, test_target = turn_to_test(array_temp3)
clf = svm.SVC()
clf.fit(train, train_target)
result = clf.predict(test)
print(result)
print(len(result))
print(clf.score(test, test_target))