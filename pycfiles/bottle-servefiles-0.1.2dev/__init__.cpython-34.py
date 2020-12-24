# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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