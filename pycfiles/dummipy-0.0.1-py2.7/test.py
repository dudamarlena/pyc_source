# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dummipy/test.py
# Compiled at: 2015-05-18 12:51:33
import pandas as pd, numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV
from dummipy import CategoricalDataFrame
regular_df = pd.DataFrame({'a': np.random.choice(['a', 'b', 'c'], 100), 
   'x': np.arange(100) + np.random.normal(0, 1, 100), 
   'y': np.arange(100)})
cat_df = CategoricalDataFrame({'a': np.random.choice(['a', 'b', 'c'], 100), 
   'x': np.arange(100) + np.random.normal(0, 1, 100), 
   'y': np.arange(100)})
r = LinearRegression()
r = RidgeCV()
print type(cat_df)
d = cat_df[['a', 'x']].tail()
y = cat_df.y
print type(d)
data = d
print y
print r.fit(data, y.head())
print r.fit(cat_df[['a']], y)
print r.fit(cat_df[['a', 'x']], y)