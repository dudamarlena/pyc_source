# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/quejebo/zippy/zippy/zippy/utils.py
# Compiled at: 2018-04-11 20:07:59


def sub_check_wilds(wildcard_map, s):
    """
    Given a dictionary of substitutions to make, and a string <s> to find such substitutions, return
    the substituted string.
    """
    for wildcard in wildcard_map.keys():
        s = s.replace('{' + wildcard + '}', wildcard_map[wildcard])

    return s