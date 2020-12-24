# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\directional\angular.py
# Compiled at: 2014-09-15 22:54:07
# Size of source mod 2**32: 2245 bytes
import numpy as np, pandas as pd

def col_names_from_sin_cos_matrix(df):
    half_columns = list(df.columns)[:int(len(df.columns) / 2)]
    return [col[:-5] for col in half_columns]


def sin_cos_matrix_to_radian_matrix(sin_cos_matrix):
    radian_matrix = pd.DataFrame(index=sin_cos_matrix.index)
    for col in col_names_from_sin_cos_matrix(sin_cos_matrix):
        radian_matrix[col] = np.arctan2(sin_cos_matrix[(col + '--SIN')].values, sin_cos_matrix[(col + '--COS')].values)

    return radian_matrix


def radian_matrix_to_sin_cos_matrix(radian_matrix):
    sin_matrix = radian_matrix.apply(np.sin)
    sin_matrix.columns = map(lambda x: x + '--SIN', radian_matrix.columns)
    cos_matrix = radian_matrix.apply(np.cos)
    cos_matrix.columns = map(lambda x: x + '--COS', radian_matrix.columns)
    return pd.concat([sin_matrix, cos_matrix], axis=1, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=True)


def sin_cos_matrix_to_degrees_matrix(sin_cos_matrix):
    return sin_cos_matrix_to_radian_matrix(sin_cos_matrix).applymap(np.degrees)


def sin_cos_matrix_mean(sin_cos_matrix):
    return sin_cos_matrix.mean()


def sin_cos_matrix_to_radians_mean(sin_cos_matrix):
    mean = sin_cos_matrix_mean(sin_cos_matrix)
    result = pd.Series(index=col_names_from_sin_cos_matrix(sin_cos_matrix))
    for col in result.index:
        result[col] = np.arctan2(mean[(col + '--SIN')], mean[(col + '--COS')])

    return result


def sin_cos_matrix_to_radian_std(sin_cos_matrix):
    var = sin_cos_matrix_var(sin_cos_matrix)
    result = pd.Series(index=var.index)
    for col in result.index:
        result[col] = np.sqrt(-2 * np.log(1 - var[col]))

    return result


def sin_cos_matrix_var(sin_cos_matrix):
    mean = sin_cos_matrix_mean(sin_cos_matrix)
    result = pd.Series(index=col_names_from_sin_cos_matrix(sin_cos_matrix))
    for col in result.index:
        result[col] = 1 - np.sqrt(np.power(mean[(col + '--SIN')], 2) + np.power(mean[(col + '--COS')], 2))

    return result


def radian_matrix_std(radian_matrix):
    return sin_cos_matrix_to_radian_std(radian_matrix_to_sin_cos_matrix(radian_matrix))