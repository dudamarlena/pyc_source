# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tailow/operators/inopr.py
# Compiled at: 2018-06-26 09:23:48
# Size of source mod 2**32: 377 bytes
from tailow.operators.base import Operator

class InOperator(Operator):

    def to_query(self, field_name, value):
        """ To query operator """
        return {field_name: {'$in': value}}

    def get_value(self, field, value):
        """ get value for the field """
        return [field.to_son(val) for val in value]