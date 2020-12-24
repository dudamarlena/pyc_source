# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/predict_ratings.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 818 bytes
"""
This module descibes how to train on a full dataset (when no testset is
built/specified) and how to use the predict() method.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import KNNBasic
from surprise import Dataset
data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
algo = KNNBasic()
algo.fit(trainset)
uid = str(196)
iid = str(302)
pred = algo.predict(uid, iid, r_ui=4, verbose=True)