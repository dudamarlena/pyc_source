# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sorno/stringutil.py
# Compiled at: 2019-08-09 12:21:44
# Size of source mod 2**32: 1435 bytes
"""
Utility functions for dealing with strings
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re

def oneline(s):
    """
    Compact all space characters to a single space. Leading and trailing
    spaces are stripped.
    """
    return re.sub('\\s+', ' ', s).strip()


def u(s):
    """
    Converts s to unicode with utf-8 encoding if it is not already a unicode.
    Leave it as is otherwise.
    """
    if type(s) == unicode:
        return s
    else:
        return s.decode('utf8')


def format_with_default_value(handle_missing_key, s, d):
    """Formats a string with handling of missing keys from the dict.

    Calls s.format(**d) while handling missing keys by calling
    handle_missing_key to get the appropriate values for the missing keys.

    Args:
        handle_issing_key: A function that takes a missing key as the argument
            and returns a value for the value of the missing key.
        s: A format string.
        d: A dict providing values to format s.

    Returns s.format(**d) with missing keys handled by calling
    handle_missing_key to get the values for the missing keys.
    """
    copy = dict(**d)
    while True:
        try:
            return (s.format)(**copy)
        except KeyError as ex:
            key = ex.args[0]
            copy[key] = handle_missing_key(key)