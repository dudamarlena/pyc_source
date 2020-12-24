# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/split_data_for_unbiased_estimation.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 1567 bytes
"""
This module descibes how to split a dataset into two parts A and B: A is for
tuning the algorithm parameters, and B is for having an unbiased estimation of
its performances. The tuning is done by Grid Search.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import random
from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import GridSearchCV
data = Dataset.load_builtin('ml-100k')
raw_ratings = data.raw_ratings
random.shuffle(raw_ratings)
threshold = int(0.9 * len(raw_ratings))
A_raw_ratings = raw_ratings[:threshold]
B_raw_ratings = raw_ratings[threshold:]
data.raw_ratings = A_raw_ratings
print('Grid Search...')
param_grid = {'n_epochs':[5, 10],  'lr_all':[0.002, 0.005]}
grid_search = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=3)
grid_search.fit(data)
algo = grid_search.best_estimator['rmse']
trainset = data.build_full_trainset()
algo.fit(trainset)
predictions = algo.test(trainset.build_testset())
print('Biased accuracy on A,', end='   ')
accuracy.rmse(predictions)
testset = data.construct_testset(B_raw_ratings)
predictions = algo.test(testset)
print('Unbiased accuracy on B,', end=' ')
accuracy.rmse(predictions)