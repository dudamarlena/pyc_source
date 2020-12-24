# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/common/listhelper.py
# Compiled at: 2011-10-03 18:07:54
"""
Created on Oct 10, 2010

@author: Nicklas Boerjesson
@note: Helper functions for list types
"""

def CI_index(_List, _value):
    for index in range(len(_List)):
        if _List[index].lower() == _value.lower():
            return index

    return -1


def unenumerate(value, _Type):
    return value[_Type]