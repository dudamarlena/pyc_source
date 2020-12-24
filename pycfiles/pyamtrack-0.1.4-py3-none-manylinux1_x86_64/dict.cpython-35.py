# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/dict.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1572 bytes
__doc__ = "PyAMS_utils.dict module\n\nThis helper module only contains a single function which can be used to update an input\ndictionary; if given value argument is a boolean 'true' value, given dictionary's key is created\nor updated, otherwise dictionary is left unchanged.\n"
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