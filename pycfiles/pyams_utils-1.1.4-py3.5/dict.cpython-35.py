# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/dict.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1572 bytes
"""PyAMS_utils.dict module

This helper module only contains a single function which can be used to update an input
dictionary; if given value argument is a boolean 'true' value, given dictionary's key is created
or updated, otherwise dictionary is left unchanged.
"""
__docformat__ = 'restructuredtext'

def update_dict(input_dict, key, value):
    """Update given mapping if input value is a boolean 'True' value

    :param dict input_dict: input dictionary
    :param key: mapping key
    :param value: new value

    'False' values leave mapping unchanged::

    >>> from pyams_utils.dict import update_dict
    >>> mydict = {}
    >>> update_dict(mydict, 'key1', None)
    >>> mydict
    {}
    >>> update_dict(mydict, 'key1', '')
    >>> mydict
    {}
    >>> update_dict(mydict, 'key1', 0)
    >>> mydict
    {}

    'True' values modify the mapping::

    >>> update_dict(mydict, 'key1', 'value')
    >>> mydict
    {'key1': 'value'}
    >>> update_dict(mydict, 'key1', 'value2')
    >>> mydict
    {'key1': 'value2'}
    """
    if value:
        input_dict[key] = value