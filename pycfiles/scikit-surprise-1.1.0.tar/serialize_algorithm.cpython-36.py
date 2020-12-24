# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/serialize_algorithm.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 1019 bytes
"""
This module illustrates the use of the dump and load methods for serializing an
algorithm. The SVD algorithm is trained on a dataset and then serialized. It is
then reloaded and can be used again for making predictions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os
from surprise import SVD
from surprise import Dataset
from surprise import dump
data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)
predictions = algo.test(trainset.build_testset())
file_name = os.path.expanduser('~/dump_file')
dump.dump(file_name, algo=algo)
_, loaded_algo = dump.load(file_name)
predictions_loaded_algo = loaded_algo.test(trainset.build_testset())
assert predictions == predictions_loaded_algo
print('Predictions are the same')