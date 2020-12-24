# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/fhlb/utils.py
# Compiled at: 2019-03-11 21:39:48
# Size of source mod 2**32: 236 bytes


def mapt(f, *args):
    return tuple(map(f, *args))


def partition_all(n, data):
    return [data[i:i + n] for i in range(0, len(data), n)]


def partition(n, data):
    return [data[i:i + n] for i in range(0, len(data), n) if len(data[i:i + n]) == n]