# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/use_cross_validation_iterators.py
# Compiled at: 2018-01-15 04:49:20
"""
This module descibes how to use cross-validation iterators.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import KFold
data = Dataset.load_builtin(b'ml-100k')
kf = KFold(n_splits=3)
algo = SVD()
for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset)
    accuracy.rmse(predictions, verbose=True)