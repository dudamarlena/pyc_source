# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\appli\Documents\GitHub\AlphaVantageAPI\alphaVantageAPI\_base_pandas_object.py
# Compiled at: 2019-09-29 14:24:31
# Size of source mod 2**32: 746 bytes
import pandas as pd
from pandas.core.base import PandasObject

class BasePandasObject(PandasObject):
    __doc__ = 'Simple PandasObject Extension\n\n    Ensures the DataFrame is not empty and has columns.\n\n    Args:\n        df (pd.DataFrame): Extends Pandas DataFrame\n    '

    def __init__(self, df, **kwargs):
        if df.empty:
            return
        self._df = df

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()