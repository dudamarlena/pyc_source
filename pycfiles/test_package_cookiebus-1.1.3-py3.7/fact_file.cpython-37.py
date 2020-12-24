# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/fact/fact_file.py
# Compiled at: 2019-02-19 08:29:43
# Size of source mod 2**32: 72 bytes


def fact(n):
    if n == 1:
        return 1
    return fact(n - 1) * n