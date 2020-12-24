# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/condition/comparators.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 978 bytes
import operator as py_operator_fun, types
from typing import Any, Callable

class ComparisonOperator(tuple):

    def __new__(cls, name: str, operator_fun: Callable[([Any, Any], int)]):
        return tuple.__new__(cls, (name, operator_fun))

    @property
    def name(self) -> str:
        return self[0]

    @property
    def operator_fun(self) -> types.FunctionType:
        """A function that takes two arguments and returns an integer à la cmp§"""
        return self[1]


NE = ComparisonOperator('!=', py_operator_fun.ne)
LT = ComparisonOperator('<', py_operator_fun.lt)
LTE = ComparisonOperator('<=', py_operator_fun.le)
EQ = ComparisonOperator('==', py_operator_fun.eq)
GTE = ComparisonOperator('>=', py_operator_fun.ge)
GT = ComparisonOperator('>', py_operator_fun.gt)
ALL_OPERATORS = {
 NE,
 LT,
 LTE,
 EQ,
 GTE,
 GT}
NAME_2_OPERATOR = dict([(op.name, op) for op in ALL_OPERATORS])