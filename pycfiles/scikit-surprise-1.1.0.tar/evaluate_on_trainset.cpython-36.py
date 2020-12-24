# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/evaluate_on_trainset.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 1102 bytes
"""
This module descibes how to test the performances of an algorithm on the
trainset.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import Dataset
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import KFold
data = Dataset.load_builtin('ml-100k')
algo = SVD()
trainset = data.build_full_trainset()
algo.fit(trainset)
testset = trainset.build_testset()
predictions = algo.test(testset)
accuracy.rmse(predictions, verbose=True)
print('CV procedure:')
kf = KFold(n_splits=3)
for i, (trainset_cv, testset_cv) in enumerate(kf.split(data)):
    print('fold number', i + 1)
    algo.fit(trainset_cv)
    print('On testset,', end='  ')
    predictions = algo.test(testset_cv)
    accuracy.rmse(predictions, verbose=True)
    print('On trainset,', end=' ')
    predictions = algo.test(trainset_cv.build_testset())
    accuracy.rmse(predictions, verbose=True)