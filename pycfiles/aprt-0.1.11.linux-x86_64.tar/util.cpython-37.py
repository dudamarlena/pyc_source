# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/aprt/util.py
# Compiled at: 2019-08-02 08:01:39
# Size of source mod 2**32: 1740 bytes


def is_one_of(value, test):
    for elem in test:
        if value == elem:
            return True

    return False


def find_if(iterable, condition):
    for index, value in enumerate(iterable):
        if condition(value):
            return index

    return -1