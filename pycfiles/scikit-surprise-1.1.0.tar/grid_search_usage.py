# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/grid_search_usage.py
# Compiled at: 2018-01-15 04:49:20
"""
This module describes how to use the GridSearchCV() class for finding the best
parameter combination of a given algorithm.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import GridSearchCV
data = Dataset.load_builtin(b'ml-100k')
param_grid = {b'n_epochs': [5, 10], b'lr_all': [0.002, 0.005], b'reg_all': [
              0.4, 0.6]}
gs = GridSearchCV(SVD, param_grid, measures=[b'rmse', b'mae'], cv=3)
gs.fit(data)
print(gs.best_score[b'rmse'])
print(gs.best_params[b'rmse'])
algo = gs.best_estimator[b'rmse']
algo.fit(data.build_full_trainset())
import pandas as pd
results_df = pd.DataFrame.from_dict(gs.cv_results)