# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/dev/Surprise/examples/load_from_dataframe.py
# Compiled at: 2018-05-27 10:18:34
"""
This module descibes how to load a dataset from a pandas dataframe.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import pandas as pd
from surprise import NormalPredictor
from surprise import Dataset
from surprise.model_selection import cross_validate
ratings_dict = {b'itemID': [1, 1, 1, 2, 2], b'userID': [
             9, 32, 2, 45, b'user_foo'], 
   b'rating': [
             3, 2, 4, 3, 1]}
df = pd.DataFrame(ratings_dict)
data = Dataset.load_from_df(df[[b'userID', b'itemID', b'rating']], rating_scale=(1,
                                                                                 5))
cross_validate(NormalPredictor(), data, cv=2)