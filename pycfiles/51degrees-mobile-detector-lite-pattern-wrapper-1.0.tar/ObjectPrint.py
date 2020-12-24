# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\ObjectPrint.py
# Compiled at: 2003-01-18 13:03:42
__doc__ = '\nPretty-printing of objects\n\nCopyright 2003 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
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