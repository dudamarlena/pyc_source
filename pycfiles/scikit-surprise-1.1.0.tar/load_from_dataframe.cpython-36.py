# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/load_from_dataframe.py
# Compiled at: 2019-09-12 15:29:52
# Size of source mod 2**32: 968 bytes
"""
This module descibes how to load a dataset from a pandas dataframe.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import pandas as pd
from surprise import NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
ratings_dict = {'itemID':[
  1, 1, 1, 2, 2], 
 'userID':[
  9, 32, 2, 45, 'user_foo'], 
 'rating':[
  3, 2, 4, 3, 1]}
df = pd.DataFrame(ratings_dict)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
cross_validate((NormalPredictor()), data, cv=2)