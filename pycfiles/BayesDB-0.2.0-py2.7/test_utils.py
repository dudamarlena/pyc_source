# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/tests/test_utils.py
# Compiled at: 2015-02-12 15:25:14
import time, inspect, pickle, os, numpy, pytest, random, shutil, pandas, bayesdb.utils as utils
from bayesdb.client import Client
from bayesdb.engine import Engine
import bayesdb.bql_grammar as bql
test_M_c = {'idx_to_name': {'1': 'b', '0': 'a', '3': 'd', '2': 'c'}, 'column_metadata': [
                     {'code_to_value': {'a': 0, '1': 1, '2': 2, '4': 3, '6': 4}, 'value_to_code': {0: 'a', 1: '1', 2: '2', 3: '4', 4: '6'}, 'modeltype': 'symmetric_dirichlet_discrete'},
                     {'code_to_value': {}, 'value_to_code': {}, 'modeltype': 'normal_inverse_gamma'},
                     {'code_to_value': {'we': 0, 'e': 1, 'w': 2, 'sd': 3}, 'value_to_code': {0: 'we', 1: 'e', 2: 'w', 3: 'sd'}, 'modeltype': 'symmetric_dirichlet_discrete'},
                     {'code_to_value': {'3': 1, '2': 2, '5': 0, '4': 3}, 'value_to_code': {0: '5', 1: '3', 2: '2', 3: '4'}, 'modeltype': 'symmetric_dirichlet_discrete'}], 
   'name_to_idx': {'a': 0, 'c': 2, 'b': 1, 'd': 3}}
test_T = [
 [
  1.0, 1.0, 0.0, numpy.nan],
 [
  2.0, 2.0, 0.0, 2.0],
 [
  0.0, 3.0, 0.0, 3.0],
 [
  3.0, 3.0, 2.0, numpy.nan],
 [
  3.0, 4.0, 2.0, 0.0],
 [
  4.0, 5.0, 1.0, numpy.nan],
 [
  numpy.nan, 6.0, 2.0, 1.0],
 [
  numpy.nan, 7.0, 3.0, 1.0],
 [
  numpy.nan, 7.0, 3.0, 1.0]]

def test_row_id_from_col_value():
    assert utils.row_id_from_col_value('1', 'a', test_M_c, test_T) == 0
    assert utils.row_id_from_col_value('7', 'a', test_M_c, test_T) == None
    assert utils.row_id_from_col_value('1', 'b', test_M_c, test_T) == 0
    assert utils.row_id_from_col_value(1, 'b', test_M_c, test_T) == 0
    assert utils.row_id_from_col_value('1', 'b', test_M_c, test_T) == 0
    try:
        utils.row_id_from_col_value('4', 'a', test_M_c, test_T)
        assert False
    except utils.BayesDBUniqueValueError:
        assert True

    return


def test_string_to_column_type():
    assert utils.string_to_column_type('1', 'a', test_M_c) == '1'
    assert utils.string_to_column_type('1', 'b', test_M_c) == 1
    assert utils.string_to_column_type(1, 'a', test_M_c) == 1