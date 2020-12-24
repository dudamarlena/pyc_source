# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/common/listhelper.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 1847 bytes
"""
    Functions for handling lists.
    
    :copyright: Copyright 2010-2014 by Nicklas Boerjesson
    :license: BSD, see LICENSE for details.
"""

def ci_index(_list, _value):
    """Case-insensitively finds an item in a list"""
    if _value is not None:
        for index in range(len(_list)):
            if _list[index].lower() == _value.lower():
                return index

    return -1


def unenumerate(value, type):
    """Returns the value of a specific type"""
    return value[type]


def find_next_match(_list, _start_idx, _match):
    """Finds next _match from _start_idx"""
    for _curr_idx in range(_start_idx, len(_list)):
        if _list[_curr_idx] == _match:
            return _curr_idx

    return -1


def find_previous_match(_list, _start_idx, _match):
    """Finds previous _match from _start_idx"""
    for _curr_idx in range(_start_idx, 0, -1):
        if _list[_curr_idx] == _match:
            return _curr_idx

    return -1


def pretty_list(_array):
    """Returns proper array data representation syntax, but with each row on a new text row, to make it more readable
     and usable.
     """

    def _handle_types(_data):
        if isinstance(_data, list):
            return str(_data)
        else:
            if isinstance(_data, str):
                return "['" + _data + "']"
            return '[' + str(_data) + ']'

    _result = ''
    if _array is None:
        return False
    else:
        if len(_array) == 1:
            return '[\n' + _handle_types(_array[0]) + '\n]'
        if len(_array) > 0:
            for _row_idx in range(len(_array) - 1):
                _result += _handle_types(_array[_row_idx]) + ',\n'

            _result += _handle_types(_array[(_row_idx + 1)]) + '\n'
            return '[\n' + _result + ']'
        return '[]'