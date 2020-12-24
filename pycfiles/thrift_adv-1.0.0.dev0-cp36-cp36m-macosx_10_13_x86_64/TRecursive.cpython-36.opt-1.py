# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/TRecursive.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 3333 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from thrift.Thrift import TType
TYPE_IDX = 1
SPEC_ARGS_IDX = 3
SPEC_ARGS_CLASS_REF_IDX = 0
SPEC_ARGS_THRIFT_SPEC_IDX = 1

def fix_spec(all_structs):
    """Wire up recursive references for all TStruct definitions inside of each thrift_spec."""
    for struc in all_structs:
        spec = struc.thrift_spec
        for thrift_spec in spec:
            if thrift_spec is None:
                continue
            else:
                if thrift_spec[TYPE_IDX] == TType.STRUCT:
                    other = thrift_spec[SPEC_ARGS_IDX][SPEC_ARGS_CLASS_REF_IDX].thrift_spec
                    thrift_spec[SPEC_ARGS_IDX][SPEC_ARGS_THRIFT_SPEC_IDX] = other
                else:
                    if thrift_spec[TYPE_IDX] in (TType.LIST, TType.SET):
                        _fix_list_or_set(thrift_spec[SPEC_ARGS_IDX])
                    else:
                        if thrift_spec[TYPE_IDX] == TType.MAP:
                            _fix_map(thrift_spec[SPEC_ARGS_IDX])


def _fix_list_or_set(element_type):
    if element_type[0] == TType.STRUCT:
        element_type[1][1] = element_type[1][0].thrift_spec
    else:
        if element_type[0] in (TType.LIST, TType.SET):
            _fix_list_or_set(element_type[1])
        elif element_type[0] == TType.MAP:
            _fix_map(element_type[1])


def _fix_map(element_type):
    if element_type[0] == TType.STRUCT:
        element_type[1][1] = element_type[1][0].thrift_spec
    else:
        if element_type[0] in (TType.LIST, TType.SET):
            _fix_list_or_set(element_type[1])
        else:
            if element_type[0] == TType.MAP:
                _fix_map(element_type[1])
            if element_type[2] == TType.STRUCT:
                element_type[3][1] = element_type[3][0].thrift_spec
            else:
                if element_type[2] in (TType.LIST, TType.SET):
                    _fix_list_or_set(element_type[3])
                elif element_type[2] == TType.MAP:
                    _fix_map(element_type[3])