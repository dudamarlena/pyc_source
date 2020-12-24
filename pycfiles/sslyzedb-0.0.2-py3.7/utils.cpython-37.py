# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sslyzedb\utils.py
# Compiled at: 2019-02-25 13:40:54
# Size of source mod 2**32: 155 bytes


def a(x):
    if x is None:
        return 'N/A'
    return x


def b(x, sep=','):
    if x is None:
        return 'N/A'
    return sep.join(x)