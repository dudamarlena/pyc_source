# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\appli\Documents\GitHub\alphaVantageAPI Project\alphaVantageAPI\_base_pandas_object.py
# Compiled at: 2020-04-19 14:39:13
# Size of source mod 2**32: 462 bytes
import pandas as pd
from pandas.core.base import PandasObject

class BasePandasObject(PandasObject):
    """BasePandasObject"""

    def __init__(self, df, **kwargs):
        if df.empty:
            return
        self._df = df

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()