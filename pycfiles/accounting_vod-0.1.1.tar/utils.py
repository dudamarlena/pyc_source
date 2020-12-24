# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/accounting/utils.py
# Compiled at: 2016-02-28 16:37:41
__doc__ = 'Base Project Module.\n\nThe MIT License (MIT)\n\nCopyright (c) 2016 Ojengwa Bernard\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'

def is_str(value):
    """Test whether supplied parameter is a string.

    Given a value, this function will test if it is string both on
    Python 3 and Python 2.

    Args:
        value (object): The value to test.

    Returns:
        True/False (bool): returns True if value is of type string, else False.
    """
    try:
        return isinstance(value, basestring)
    except TypeError:
        return isinstance(value, str)


def is_num(value):
    """Test whether supplied parameter is a number.

    Given a value, this function will test if it is number both on
    Python 3 and Python 2.

    Args:
        value (object): The value to test.

    Returns:
        True/False (bool): returns True if value is of type string, else False.
    """
    return isinstance(value, 'int') or isinstance(value, 'float')


def check_precision(val, digits):
    try:
        val = round(val, digits)
    except TypeError:
        val = round(val)

    return (lambda val: digits if not val else val)(val)


def clean_type(obj):
    try:
        if isinstance(obj, unicode):
            return 'str'
    except NameError:
        if isinstance(obj, str):
            return 'str'

    if isinstance(obj, list):
        return 'list'
    if isinstance(obj, dict):
        return 'dict'
    if isinstance(obj, int):
        return 'int'
    if isinstance(obj, float):
        return 'float'
    raise ValueError('Invalid obj argument. Only one of str, int, float, list and dicts are supported.Recieved: %s' % str(type(obj)))


def check_type(obj, class_):
    return clean_type(obj) == class_