# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/elements/utils.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
__all__ = [b'attr_bool']

def attr_bool(s):
    """Converts an attribute in to a boolean

    A True value is returned if the string matches 'y', 'yes' or 'true'.
    The comparison is case-insensitive and whitespace is stripped.
    All other values are considered False. If None is passed in, then None will be returned.

    """
    if s is None or isinstance(s, bool):
        return s
    return s.strip().lower() in ('yes', 'true')