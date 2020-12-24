# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/basic_usage.py
# Compiled at: 2018-01-15 04:49:20
"""
This module describes the most basic usage of Surprise: you define a prediction
algorithm, (down)load a dataset and run a cross-validation procedure.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
data = Dataset.load_builtin(b'ml-100k')
algo = SVD()
cross_validate(algo, data, measures=[b'RMSE', b'MAE'], cv=5, verbose=True)