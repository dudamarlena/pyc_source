# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/itercompat.py
# Compiled at: 2019-02-14 00:35:17
"""
Providing iterator functions that are not in all version of Python we support.
Where possible, we try to use the system-native version and only fall back to
these implementations if necessary.
"""

def is_iterable(x):
    """A implementation independent way of checking for iterables"""
    try:
        iter(x)
    except TypeError:
        return False

    return True