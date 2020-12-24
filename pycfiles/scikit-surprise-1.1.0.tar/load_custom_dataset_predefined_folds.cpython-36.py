# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/load_custom_dataset_predefined_folds.py
# Compiled at: 2019-09-12 15:29:52
# Size of source mod 2**32: 1287 bytes
"""
This module descibes how to load a custom dataset when folds (for
cross-validation) are predefined by train and test files.

As a custom dataset we will actually use the movielens-100k dataset, but act as
if it were not built-in.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os
from surprise import SVD
from surprise import Dataset
from surprise import Reader
from surprise import accuracy
from surprise.model_selection import PredefinedKFold
files_dir = os.path.expanduser('~/.surprise_data/ml-100k/ml-100k/')
reader = Reader('ml-100k')
train_file = files_dir + 'u%d.base'
test_file = files_dir + 'u%d.test'
folds_files = [(train_file % i, test_file % i) for i in (1, 2, 3, 4, 5)]
data = Dataset.load_from_folds(folds_files, reader=reader)
pkf = PredefinedKFold()
algo = SVD()
for trainset, testset in pkf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset)
    accuracy.rmse(predictions, verbose=True)