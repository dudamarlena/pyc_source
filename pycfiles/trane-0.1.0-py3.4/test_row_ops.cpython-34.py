# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tests/ops/test_row_ops.py
# Compiled at: 2018-04-05 12:35:08
# Size of source mod 2**32: 1805 bytes
from trane.ops.row_ops import *
from pandas import DataFrame
from trane.utils.table_meta import TableMeta as TM
import numpy as np
df = DataFrame({'col': [1, 2, 3, 4, 5]})
meta = TM({'tables': [
            {'fields': [
                        {'name': 'col',  'type': TM.SUPERTYPE[TM.TYPE_FLOAT], 
                         'subtype': TM.TYPE_FLOAT}]}]})

def test_identity_row_op_input_value():
    op = IdentityRowOp('col')
    op.op_type_check(meta)
    output = op(df.copy())
    assert np.all(output.values == np.asarray([[1, 2, 3, 4, 5]]).T)


def test_eq_row_op_input_value():
    op = EqRowOp('col')
    op.op_type_check(meta)
    op.hyper_parameter_settings['threshold'] = 2
    output = op(df.copy())
    assert np.all(output.values == np.asarray([
     [
      False, True, False, False, False]]).T)


def test_neq_row_op_input_value():
    op = NeqRowOp('col')
    op.op_type_check(meta)
    op.hyper_parameter_settings['threshold'] = 2
    output = op(df.copy())
    assert np.all(output.values == np.asarray([
     [
      True, False, True, True, True]]).T)


def test_greater_row_op_input_value():
    op = GreaterRowOp('col')
    op.op_type_check(meta)
    op.hyper_parameter_settings['threshold'] = 2
    output = op(df.copy())
    assert np.all(output.values == np.asarray([
     [
      False, False, True, True, True]]).T)


def test_less_row_op_input_value():
    op = LessRowOp('col')
    op.op_type_check(meta)
    op.hyper_parameter_settings['threshold'] = 2
    output = op(df.copy())
    assert np.all(output.values == np.asarray([
     [
      True, False, False, False, False]]).T)


def test_exp_row_op_input_value():
    op = ExpRowOp('col')
    op.op_type_check(meta)
    op.hyper_parameter_settings['threshold'] = 2
    output = op(df.copy())
    assert np.all(output.values == np.exp(np.asarray([[1, 2, 3, 4, 5]]).T))