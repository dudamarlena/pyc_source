# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/baselines_conf.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 1251 bytes
"""
This module gives an example of how to configure baseline estimates
computation.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import BaselineOnly
from surprise import KNNBasic
from surprise import Dataset
from surprise.model_selection import cross_validate
data = Dataset.load_builtin('ml-100k')
print('Using ALS')
bsl_options = {'method':'als',  'n_epochs':5, 
 'reg_u':12, 
 'reg_i':5}
algo = BaselineOnly(bsl_options=bsl_options)
cross_validate(algo, data, verbose=True)
print('Using SGD')
bsl_options = {'method':'sgd',  'learning_rate':5e-05}
algo = BaselineOnly(bsl_options=bsl_options)
cross_validate(algo, data, verbose=True)
print('Using ALS with pearson_baseline similarity')
bsl_options = {'method':'als',  'n_epochs':20}
sim_options = {'name': 'pearson_baseline'}
algo = KNNBasic(bsl_options=bsl_options, sim_options=sim_options)
cross_validate(algo, data, verbose=True)