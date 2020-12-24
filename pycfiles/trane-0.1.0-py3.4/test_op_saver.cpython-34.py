# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tests/ops/test_op_saver.py
# Compiled at: 2018-04-05 12:35:08
# Size of source mod 2**32: 1636 bytes
from trane.ops import *
from trane.utils.table_meta import TableMeta as TM
import pytest, numpy as np
ALL_OPS = AGGREGATION_OPS + FILTER_OPS + ROW_OPS + TRANSFORMATION_OPS

def test_save_load_before_op_type_check():
    """
    Randomly select 10 operations, check op_to_json and op_from_json work properly before op_type_check
    """
    for i in range(10):
        op_type = np.random.choice(ALL_OPS)
        op = globals()[op_type]('col')
        op_json = op_to_json(op)
        assert type(op_json) == str
        op2 = op_from_json(op_json)
        assert type(op2) == globals()[op_type]
        assert op2.column_name == 'col'
        assert op2.input_type is None and op2.output_type is None
        if not (type(op2.hyper_parameter_settings) == dict and len(op2.hyper_parameter_settings) == 0):
            raise AssertionError


def test_save_load_after_op_type_check():
    """
    Randomly select 10 operations, check op_to_json and op_from_json work properly after op_type_check
    """
    for i in range(10):
        meta = TM({'tables': [
                    {'fields': [
                                {'name': 'col',  'type': TM.SUPERTYPE[TM.TYPE_FLOAT], 
                                 'subtype': TM.TYPE_FLOAT}]}]})
        op_type = np.random.choice(ALL_OPS)
        op = globals()[op_type]('col')
        op.op_type_check(meta)
        op_json = op_to_json(op)
        assert type(op_json) == str
        op2 = op_from_json(op_json)
        assert type(op2) == globals()[op_type]
        assert op2.column_name == 'col'
        assert op2.input_type == TM.TYPE_FLOAT and op2.output_type == op.output_type
        if not type(op2.hyper_parameter_settings) == dict:
            raise AssertionError