# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/similarity_conf.py
# Compiled at: 2018-01-15 04:49:20
"""
This module gives an example of how to configure similarity measures
computation.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import KNNBasic
from surprise import Dataset
from surprise.model_selection import cross_validate
data = Dataset.load_builtin(b'ml-100k')
sim_options = {b'name': b'cosine', b'user_based': False}
algo = KNNBasic(sim_options=sim_options)
cross_validate(algo, data, verbose=True)
sim_options = {b'name': b'pearson_baseline', b'shrinkage': 0}
algo = KNNBasic(sim_options=sim_options)
cross_validate(algo, data, verbose=True)