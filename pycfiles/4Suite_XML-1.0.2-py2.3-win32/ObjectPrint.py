# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\ObjectPrint.py
# Compiled at: 2003-01-18 13:03:42
"""
Pretty-printing of objects

Copyright 2003 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import pprint as _pprint, types as _types

def _inst_to_dict(inst):
    dict = vars(inst).copy()
    for (key, value) in dict.items():
        if type(value) is _types.InstanceType:
            dict[key] = _inst_to_dict(value)

    return dict


def pprint(object):
    if type(object) is _types.InstanceType:
        object = _inst_to_dict(object)
    _pprint.pprint(object)