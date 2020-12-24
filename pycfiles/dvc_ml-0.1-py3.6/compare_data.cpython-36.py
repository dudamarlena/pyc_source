# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dvc_ml/compare_data/compare_data.py
# Compiled at: 2019-08-25 22:15:30
# Size of source mod 2**32: 3205 bytes
import pandas as pd

class CompareData:

    def __init__(self):
        pass

    def _get_same_columns(self, df_one: pd.DataFrame, df_two: pd.DataFrame) -> list:
        same_cols = []
        for col in df_one.columns:
            if (df_one[col] == df_two[col]).all():
                same_cols.append(col)

        return same_cols

    def _get_different_columns(self, df_one: pd.DataFrame, df_two: pd.DataFrame) -> list:
        different_cols = []
        for col in df_one.columns:
            if (df_one[col] != df_two[col]).all():
                different_cols.append(col)

        return different_cols

    def _get_same_column_names(self, first_cols: list, second_cols: list) -> list:
        first_set = set(first_cols)
        second_set = set(second_cols)
        diff_set = first_set - second_set
        return list(first_set - diff_set)

    def _get_different_column_names(self, first_cols: list, second_cols: list) -> list:
        first_set = set(first_cols)
        second_set = set(second_cols)
        diff_set = first_set - second_set
        return list(diff_set)

    def get_same_column_names(self, first_cols: list, second_cols: list) -> list:
        if len(first_cols) > len(second_cols):
            return self._get_same_column_names(first_cols, second_cols)
        else:
            return self._get_same_column_names(second_cols, first_cols)

    def get_different_column_names(self, first_cols: list, second_cols: list) -> list:
        if len(first_cols) > len(second_cols):
            return self._get_different_column_names(first_cols, second_cols)
        else:
            return self._get_different_column_names(second_cols, first_cols)

    def get_same_columns(self, df_one: pd.DataFrame, df_two: pd.DataFrame) -> list:
        first_cols = df_one.columns.tolist()
        second_cols = df_two.columns.tolist()
        same_cols = self.get_same_column_names(first_cols, second_cols)
        df_one = df_one[same_cols]
        df_two = df_two[same_cols]
        return self._get_same_colums(df_one, df_two)

    def get_different_columns(self, df_one: pd.DataFrame, df_two: pd.DataFrame) -> list:
        first_cols = df_one.columns.tolist()
        second_cols = df_two.columns.tolist()
        different_cols = self.get_different_column_names(first_cols, second_cols)
        same_cols = self.get_same_column_names(first_cols, second_cols)
        diff_cols_same_name = self._get_different_columns(df_one, df_two)
        return different_cols + diff_cols_same_name