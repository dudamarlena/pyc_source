# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/generate_grid_search_cv_results_example.py
# Compiled at: 2018-01-15 04:49:20
"""
This module is used for generating the doc tables about the
GridSearchCV.cv_results attribute.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from tabulate import tabulate
from six import iteritems
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import GridSearchCV
data = Dataset.load_builtin(b'ml-100k')
param_grid = {b'n_epochs': [5, 10], b'lr_all': [0.002, 0.005], b'reg_all': [
              0.4, 0.6]}
gs = GridSearchCV(SVD, param_grid, measures=[b'rmse', b'mae'], cv=3)
gs.fit(data)
table = [ [] for _ in range(len(gs.cv_results[b'params'])) ]
for i in range(len(gs.cv_results[b'params'])):
    for key in gs.cv_results.keys():
        table[i].append(gs.cv_results[key][i])

header = gs.cv_results.keys()
print(tabulate(table, header, tablefmt=b'rst'))
print()
for key, val in iteritems(gs.cv_results):
    print((b'{:<20}').format(b"'" + key + b"':"), end=b'')
    if isinstance(val[0], float):
        print([ float((b'{:.2f}').format(f)) for f in val ])
    else:
        print(val)