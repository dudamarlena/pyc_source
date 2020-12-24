# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Mohammed Yusuf Khan\Google Drive\WorkArea\GitHub\toolstack-dev\toolstack\feature\feature_base.py
# Compiled at: 2019-06-29 20:43:03
# Size of source mod 2**32: 400 bytes
from abc import ABC, abstractmethod
import pandas as pd

class Feature(ABC):

    def __init__(self, df, column):
        assert isinstance(df, pd.DataFrame), 'Pass a DataFrame'
        assert column in df, 'The column is not present in the DataFrame, pass a valid column name'
        self.df = df
        self.column = column

    @abstractmethod
    def stack(self):
        pass