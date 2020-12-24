# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: autoant/utils.py
# Compiled at: 2014-09-18 18:51:52


def sub_list(x, y):
    return [ item for item in x if item not in y ]


def boolstr(str):
    return str == 'True'