# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/Dropbox/c0d3z/python/libs/bottle-rest/docs/__init__.py
# Compiled at: 2015-04-25 06:11:50
# Size of source mod 2**32: 525 bytes


def allSame(s):
    return not any(filter(lambda x: x != s[0], s))


def hasDigit(s):
    return any(char.isdigit() for char in s)


def getVersion(data):
    """
    Parse version from changelog written in RST format.
    """
    data = data.splitlines()
    return next(v for v, u in zip(data, data[1:]) if len(v) == len(u) and allSame(u) and hasDigit(v) and '.' in v)