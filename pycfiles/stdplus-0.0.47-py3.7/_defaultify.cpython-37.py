# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/stdplus/_defaultify.py
# Compiled at: 2018-12-11 10:37:42
# Size of source mod 2**32: 472 bytes


def defaultify(value, default):
    """Return `default` if `value` is `None`. Otherwise, return `value`"""
    if None == value:
        return default
    return value


def defaultifyDict(dictionary, key, default):
    """Return `default` if either `key` is not in `dictionary`, or `dictionary[key]` is `None`. Otherwise, return `dictionary[key]`"""
    if key in dictionary:
        return defaultify(dictionary[key], default)
    return default