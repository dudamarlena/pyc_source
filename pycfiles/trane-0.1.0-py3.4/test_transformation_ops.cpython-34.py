# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tests/ops/test_transformation_ops.py
# Compiled at: 2018-04-05 20:01:41
# Size of source mod 2**32: 1420 bytes
from trane.ops.transformation_ops import *
from pandas import DataFrame
from trane.utils.table_meta import TableMeta as TM
import numpy as np
df = DataFrame({'col': [1, 2, 3, 4, 5]})
meta = TM({'tables': [
            {'fields': [
                        {'name': 'col',  'type': TM.SUPERTYPE[TM.TYPE_FLOAT], 
                         'subtype': TM.TYPE_FLOAT}]}]})

def test_identity_transformation_op_input_value():
    op = IdentityTransformationOp('col')
    op.op_type_check(meta)
    output = op(df.copy())
    assert np.all(output.values == np.asarray([[1, 2, 3, 4, 5]]).T)


def test_diff_transformation_op_input_value():
    op = DiffTransformationOp('col')
    op.op_type_check(meta)
    output = op(df.copy())
    assert np.all(output.values == np.asarray([[0, 1, 1, 1, 1]]).T)


def test_ObjectFrequencyTransformationOp():
    df = DataFrame([(1.0, 100), (2.0, 70), (3.0, 100),
     (4.0, 70), (5.0, 70)], columns=['id', 'height'])
    op = ObjectFrequencyTransformationOp('height')
    op2 = ObjectFrequencyTransformationOp('id')
    output = op(df.copy())
    output2 = op2(df.copy())
    expected = DataFrame([(1.0, 2), (2.0, 3)], columns=[
     'id', 'height'])
    expected2 = DataFrame([(1, 100), (1, 70), (1, 100),
     (1, 70), (1, 70)], columns=['id', 'height'])
    assert output.equals(expected)
    assert output2.equals(expected2)