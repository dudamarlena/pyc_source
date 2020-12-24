# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tooth/lists.py
# Compiled at: 2015-04-29 20:46:50
__author__ = 'Tom James Holub'

def unique(list_with_possible_duplicates):
    return list(set(list_with_possible_duplicates))


def subtract(first, second):
    if type(first) is list and type(second) is list:
        result = []
        for value in first:
            if value not in second:
                result.append(value)

        return result
    raise TypeError('can only subtract list-list')


def add_unique(unique_list, unique):
    if unique not in unique_list:
        unique_list.append(unique)