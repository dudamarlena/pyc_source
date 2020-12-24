# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/minimum/findmin.py
# Compiled at: 2019-03-14 17:53:52
"""This script find the minimum value from the vector/list given by user"""
from __future__ import print_function

def find_minimum(input_list):
    """This function first validate the vector/list and then
    find minimum from it"""
    mini = None
    desc_part = []
    asc_part = []
    check = True
    str_list = [ x for x in input_list if isinstance(x, str) ]
    if str_list:
        check = False
    if len(input_list) in (0, 1, 2):
        check = False
    if check:
        for i in range(len(input_list) - 1):
            if input_list[i] - input_list[(i + 1)] < 0:
                break
            elif input_list[i] - input_list[(i + 1)] == 0:
                check = False
            mini = input_list[(i + 1)]
            desc_part = input_list[:i + 1]
            asc_part = input_list[i + 1:]

        if len(desc_part) == 0:
            check = False
        if len(asc_part) > 1:
            for i in range(len(asc_part) - 1):
                if asc_part[i] - asc_part[(i + 1)] > 0:
                    check = False
                elif asc_part[i] - asc_part[(i + 1)] == 0:
                    check = False

        else:
            check = False
    if check:
        print(' INPUT: ', input_list)
        print(' OUTPUT: ', mini)
    else:
        print(' OUTPUT: INVALID INPUT')
    return