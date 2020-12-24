# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/common/strings.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 3636 bytes
"""
    Contains miscellaneous string functions.
    
    :copyright: Copyright 2010-2014 by Nicklas Boerjesson
    :license: BSD, see LICENSE for details. 
"""
import os

def parse_balanced_delimiters(_input, _d_left, _d_right, _text_qualifier):
    """Removes all balanced delimiters. Handles multiple levels and ignores those contained within text delimiters."""
    _depth = 0
    _balanced = []
    _cleared = ''
    _text_mode = False
    _start_pos = None
    _clear_start_pos = 0
    for _curr_idx in range(len(_input)):
        _curr_char = _input[_curr_idx]
        if _curr_char == _text_qualifier:
            _text_mode = not _text_mode
        elif not _text_mode:
            if _curr_char == _d_left:
                if _depth == 0:
                    _start_pos = _curr_idx
                    _cleared += _input[_clear_start_pos:_curr_idx]
                    _clear_start_pos = None
                _depth += 1
            else:
                if _curr_char == _d_right:
                    _depth -= 1
                if _start_pos and _depth == 0 and _start_pos < _curr_idx:
                    _balanced.append(_input[_start_pos + 1:_curr_idx])
                    _start_pos = None
                    _clear_start_pos = _curr_idx + 1

    if _cleared == '':
        return (_balanced, _input)
    else:
        return (
         _balanced, _cleared)


def empty_if_none(_string, _source=None):
    """If _source if None, return an empty string, otherwise return string. 
    This is useful when you build strings and want it to be empty if you don't have any data.
    For example when building a comma-separated string with a dynamic number of parameters: 
    .. code-block:: python
    
    command = (_id +";" +  +  empty_if_none(";"+str(_comment), _comment))
    """
    if _source is None:
        return ''
    else:
        return str(_string)


def empty_when_none(_string=None):
    """If _string if None, return an empty string, otherwise return string.
    """
    if _string is None:
        return ''
    else:
        return str(_string)


def make_path_absolute(_path, _base_path):
    """Makes a path defined as relative in the resource definition absolute using _base_path."""
    _path = os.path.normpath(_path)
    if _base_path is not None and _base_path != '':
        _base_path = os.path.normpath(_base_path)
    if os.path.isabs(_path):
        return _path
    if _base_path:
        return os.path.join(_base_path, _path)
    raise Exception('Resource.make_path_absolute: make_path_absolute cannot resolve and make ' + _path + ' absolute without a _base_path.')


def bool_to_binary_int(_value):
    """Converts True to 1 and False and None to 0."""
    if _value is None or _value is False:
        return 0
    if _value is True:
        return 1


def binary_int_to_bool(_value):
    """Converts 1 to True and 1 and None to False."""
    if _value is None or _value == 0:
        return False
    if _value == 1:
        return True


def string_to_bool(_value):
    """Converts "True" to True None to False. Case-insensitive."""
    if _value is not None and _value.lower() == 'true':
        return True
    else:
        return False