# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bf3stats\utils.py
# Compiled at: 2012-02-28 11:58:10


def _to_str(name):
    """Add _ if given string is a digit."""
    if name.isdigit():
        name = '_%s' % name
    return name