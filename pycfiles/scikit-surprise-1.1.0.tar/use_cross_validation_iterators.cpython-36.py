# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/use_cross_validation_iterators.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 684 bytes
"""
This module descibes how to use cross-validation iterators.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import KFold
data = Dataset.load_builtin('ml-100k')
kf = KFold(n_splits=3)
algo = SVD()
for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset)
    accuracy.rmse(predictions, verbose=True)