# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/baselines_conf.py
# Compiled at: 2018-01-15 04:49:20
"""
This module gives an example of how to configure baseline estimates
computation.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import BaselineOnly
from surprise import KNNBasic
from surprise import Dataset
from surprise.model_selection import cross_validate
data = Dataset.load_builtin(b'ml-100k')
print(b'Using ALS')
bsl_options = {b'method': b'als', b'n_epochs': 5, 
   b'reg_u': 12, 
   b'reg_i': 5}
algo = BaselineOnly(bsl_options=bsl_options)
cross_validate(algo, data, verbose=True)
print(b'Using SGD')
bsl_options = {b'method': b'sgd', b'learning_rate': 5e-05}
algo = BaselineOnly(bsl_options=bsl_options)
cross_validate(algo, data, verbose=True)
print(b'Using ALS with pearson_baseline similarity')
bsl_options = {b'method': b'als', b'n_epochs': 20}
sim_options = {b'name': b'pearson_baseline'}
algo = KNNBasic(bsl_options=bsl_options, sim_options=sim_options)
cross_validate(algo, data, verbose=True)