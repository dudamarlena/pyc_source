# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Mohammed Yusuf Khan\Google Drive\WorkArea\GitHub\toolstack-dev\toolstack\feature\feature_encoding.py
# Compiled at: 2019-06-29 21:39:53
# Size of source mod 2**32: 3541 bytes
import pandas as pd, numpy as np
from .feature_base import Feature

class LabelEncoder(Feature):
    __doc__ = '\n    Label encodes the data passed\n\n    Parameters\n    ----------\n    df : DataFrame\n        The df to perform case operation on.\n    column : string, int\n        The column selected should be present in the Dataframe passed\n\n    Returns\n    -------\n    DataFrame\n    '

    def __init__(self, df, column):
        super(LabelEncoder, self).__init__(df, column)
        self.df = df.copy()
        self._LabelEncoder__mapper = {}

    def stack(self):
        unique_values = self.df[self.column].unique()
        for idx, val in enumerate(unique_values):
            if val not in self._LabelEncoder__mapper.keys():
                self._LabelEncoder__mapper[val] = idx

        self.df[self.column] = self.df[self.column].map(self._LabelEncoder__mapper)
        self.inverse = {y:x for x, y in self._LabelEncoder__mapper.items()}
        return self.df


class CountEncoder(Feature):
    __doc__ = '\n    Count encodes the data passed\n\n    Parameters\n    ----------\n    df : DataFrame\n        The df to perform case operation on.\n    column : string, int\n        The column selected should be present in the Dataframe passed\n\n    Returns\n    -------\n    DataFrame\n    '

    def __init__(self, df, column, transformation=None):
        super(CountEncoder, self).__init__(df, column)
        self.transformation = transformation
        self.df = df.copy()

    def stack(self):
        if self.transformation == 'log':
            self._CountEncoder__mapper = self.df[self.column].value_counts().to_dict()
            self._CountEncoder__mapper = {x:np.log(y) for x, y in self._CountEncoder__mapper.items()}
        else:
            self._CountEncoder__mapper = self.df[self.column].value_counts().to_dict()
        self.df[self.column] = self.df[self.column].map(self._CountEncoder__mapper)
        self.inverse = {y:x for x, y in self._CountEncoder__mapper.items()}
        return self.df


class TargetEncoder(Feature):

    def __init__(self, df, column, target, strategy=None):
        super(TargetEncoder, self).__init__(df, column)
        self.strategy = strategy
        self.target = target
        self.df = df.copy()

    def stack(self):
        if not self.strategy or self.strategy == 'count':
            self._TargetEncoder__mapper = self.df[self.target].value_counts().to_dict()
            self.df[self.column] = self.df[self.target].map(self._TargetEncoder__mapper)
        else:
            if self.strategy == 'conditional':
                unique_values = self.df[self.column].unique().tolist()
                unique_classes = self.df[self.target].unique().tolist()
                for val in unique_values:
                    for c in unique_classes:
                        self.df.loc[((self.df[self.target] == c) & (self.df[self.column] == val), self.column)] = len(self.df[((self.df[self.column] == val) & (self.df[self.target] == c))]) / len(self.df[(self.df[self.column] == val)])

            else:
                if self.strategy == 'percentage':
                    unique_values = self.df[self.column].unique().tolist()
                    unique_classes = self.df[self.target].unique().tolist()
                    for val in unique_values:
                        for c in unique_classes:
                            self.df.loc[((self.df[self.target] == c) & (self.df[self.column] == val), self.column)] = len(self.df[((self.df[self.column] == val) & (self.df[self.target] == c))]) / len(self.df)

                return self.df