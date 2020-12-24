# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/select_utils.py
# Compiled at: 2015-02-12 15:25:14
import re, utils, numpy, os, pylab, matplotlib.cm, inspect, operator, ast, string, utils, functions, data_utils as du
from pyparsing import *
import bayesdb.bql_grammar as bql_grammar

def evaluate_where_on_row(row_idx, row, where_conditions, M_c, M_c_full, X_L_list, X_D_list, T, T_full, engine, tablename, numsamples, impute_confidence):
    """
  Helper function that applies WHERE conditions to row, returning False if row doesn't satisfy where
  clause, and the list of function results if it does satisfy the where clause.
  """
    function_values = []
    for func, f_args, op, val in where_conditions:
        if func == functions._column and f_args[1] != None and numpy.isnan(T[row_idx][f_args[0]]):
            col_idx = f_args[0]
            confidence = f_args[1]
            Y = [ (row_idx, cidx, row[cidx]) for cidx in M_c['name_to_idx'].values() if not numpy.isnan(T[row_idx][cidx])
                ]
            samples = engine.call_backend('simple_predictive_sample', dict(M_c=M_c, X_L=X_L_list, X_D=X_D_list, Y=Y, Q=[[row_idx, col_idx]], n=numsamples))
            samples_satisfying_where = 0
            for sample in samples:
                value = du.convert_code_to_value(M_c, col_idx, sample[0])
                if op(value, val):
                    samples_satisfying_where += 1

            if float(samples_satisfying_where) / len(samples) >= confidence:
                imputed_code, imputation_confidence = utils.get_imputation_and_confidence_from_samples(M_c, X_L_list[0], col_idx, samples)
                if imputed_code is not None:
                    imputed_value = du.convert_code_to_value(M_c, col_idx, imputed_code)
                else:
                    imputed_value = T[row_idx][col_idx]
                function_values.append(imputed_value)
            else:
                return False
        else:
            if func != functions._column_ignore:
                where_value = func(f_args, row_idx, row, M_c, X_L_list, X_D_list, T, engine, numsamples)
            else:
                where_value = func(f_args, row_idx, row, M_c_full, T_full, engine)
            if func == functions._row_id:
                val = engine.persistence_layer.get_row_list(tablename, val)
                if op(val, where_value):
                    function_values.append(where_value)
                else:
                    return False
            elif op(where_value, val):
                function_values.append(where_value)
            else:
                return False

    return function_values


def convert_row_from_codes_to_values(row, M_c):
    """
  Helper function to convert a row from its 'code' (as it's stored in T) to its 'value'
  (the human-understandable value).
  """
    ret = []
    for cidx, code in enumerate(row):
        if not du.flexible_isnan(code):
            ret.append(du.convert_code_to_value(M_c, cidx, code))
        else:
            ret.append(code)

    return tuple(ret)


def check_if_functions_need_models(queries, tablename, order_by, where_conditions):
    """
  If there are no models, make sure that we aren't using functions that require models.
  TODO: make this less hardcoded
  """
    blacklisted_functions = [
     functions._similarity, functions._row_typicality, functions._col_typicality, functions._probability]
    used_functions = [ q[0] for q in queries ] + [ w[0] for w in where_conditions ] + [ x[0] for x in order_by ]
    for bf in blacklisted_functions:
        if bf in queries:
            raise utils.BayesDBNoModelsError(tablename)


def compute_result_and_limit(rows, limit, queries, M_c, X_L_list, X_D_list, T, engine, numsamples):
    data = []
    row_count = 0
    aggregate_cache = dict()
    for query_idx, (query_function, query_args, aggregate) in enumerate(queries):
        if aggregate:
            aggregate_cache[query_idx] = query_function(query_args, None, None, M_c, X_L_list, X_D_list, T, engine, numsamples)

    assert queries[0][0] == functions._row_id
    if len(aggregate_cache) == len(queries) - 1:
        limit = 1
    for row_id, row_values in rows:
        ret_row = []
        for query_idx, (query_function, query_args, aggregate) in enumerate(queries):
            if aggregate:
                ret_row.append(aggregate_cache[query_idx])
            else:
                ret_row.append(query_function(query_args, row_id, row_values, M_c, X_L_list, X_D_list, T, engine, numsamples))

        data.append(tuple(ret_row))
        row_count += 1
        if row_count >= limit:
            break

    return data