# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/estimate_columns_utils.py
# Compiled at: 2015-02-12 15:25:14
import re, utils, numpy, os, pylab, matplotlib.cm, inspect, operator, ast, utils, functions, data_utils as du

def filter_column_indices(column_indices, where_conditions, M_c, T, X_L_list, X_D_list, engine, numsamples):
    column_indices_and_data = []
    for c_idx in column_indices:
        data = []
        for (func, f_args), op, val in where_conditions:
            if f_args is not None:
                f_args = (
                 f_args, c_idx)
            else:
                f_args = c_idx
            where_value = func(f_args, None, None, M_c, X_L_list, X_D_list, T, engine, numsamples)
            data.append(where_value)
            if not op(where_value, val):
                break

        column_indices_and_data.append((data, c_idx))

    return column_indices_and_data
    return [ c_idx for c_idx in column_indices if _is_column_valid(c_idx, where_conditions, M_c, X_L_list, X_D_list, T, engine, numsamples) ]


def _is_column_valid(c_idx, where_conditions, M_c, X_L_list, X_D_list, T, engine, numsamples):
    for (func, f_args), op, val in where_conditions:
        if f_args is not None:
            f_args = (
             f_args, c_idx)
        else:
            f_args = c_idx
        where_value = func(f_args, None, None, M_c, X_L_list, X_D_list, T, engine, numsamples)
        return op(where_value, val)

    return True


def order_columns(column_indices, order_by, M_c, X_L_list, X_D_list, T, engine, numsamples):
    if not order_by:
        return column_indices
    return _column_order_by(column_indices, order_by, M_c, X_L_list, X_D_list, T, engine, numsamples)


def _column_order_by(column_indices_and_data, function_list, M_c, X_L_list, X_D_list, T, engine, numsamples):
    """
  Return the original column indices, but sorted by the individual functions.
  """
    if len(column_indices_and_data) == 0 or not function_list:
        return column_indices_and_data
    scored_column_indices = list()
    for data, c_idx in column_indices_and_data:
        scores = []
        values = []
        for f, f_args, desc in function_list:
            if f_args:
                f_args = (
                 f_args, c_idx)
            else:
                f_args = c_idx
            score = f(f_args, None, None, M_c, X_L_list, X_D_list, T, engine, numsamples)
            data.append(score)
            if numpy.isnan(score):
                score = float('inf')
            elif desc:
                score *= -1
            scores.append(score)

        scored_column_indices.append((tuple(scores), c_idx, tuple(data)))

    scored_column_indices.sort(key=lambda tup: tup[0], reverse=False)
    return [ (data, c_idx) for scores, c_idx, data in scored_column_indices ]


def function_description(func, f_args, M_c):
    function_names = {'_col_typicality': 'typicality', '_dependence_probability': 'dependence probability', 
       '_correlation': 'correlation', 
       '_mutual_information': 'mutual information'}
    function_name = function_names[func.__name__]
    if function_name == 'typicality':
        description = 'typicality'
    elif f_args is not None:
        function_arg = M_c['idx_to_name'][str(f_args)]
        description = '%s with %s' % (function_name, function_arg)
    else:
        raise utils.BayesDBError()
    return description