# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/myfact/fact.py
# Compiled at: 2017-07-08 02:28:19
# Size of source mod 2**32: 109 bytes


def factorial(num):
    if num >= 0:
        if num == 0:
            return 1
        return num * factorial(num - 1)
    return -1