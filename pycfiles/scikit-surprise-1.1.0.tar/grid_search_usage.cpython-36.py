# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/grid_search_usage.py
# Compiled at: 2019-01-04 08:05:49
# Size of source mod 2**32: 933 bytes
"""
This module describes how to use the GridSearchCV() class for finding the best
parameter combination of a given algorithm.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import GridSearchCV
data = Dataset.load_builtin('ml-100k')
param_grid = {'n_epochs':[
  5, 10], 
 'lr_all':[0.002, 0.005],  'reg_all':[
  0.4, 0.6]}
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
gs.fit(data)
print(gs.best_score['rmse'])
print(gs.best_params['rmse'])
algo = gs.best_estimator['rmse']
algo.fit(data.build_full_trainset())
import pandas as pd
results_df = pd.DataFrame.from_dict(gs.cv_results)