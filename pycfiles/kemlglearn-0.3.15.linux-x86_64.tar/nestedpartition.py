# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/kemlglearn/metrics/nestedpartition.py
# Compiled at: 2016-03-30 05:36:29
"""
.. module:: nestedpartition

nestedpartition
*************

:Description: nestedpartition

    

:Authors: bejar
    

:Version: 

:Created on: 09/07/2015 11:18 

"""
__author__ = 'bejar'
import numpy as np, pprint

def nested_item(depth, value):
    if depth <= 1:
        print value
        return [
         value]
    else:
        return [
         nested_item(depth - 1, value)]


def nested_list(n):
    """Generate a nested list where the i'th item is at depth i."""
    lis = []
    for i in range(n):
        if i == 0:
            lis.append(i)
        else:
            lis.append(nested_item(i, i))

    return lis


def flatten(lis):
    """Given a list, possibly nested to any level, return it flattened."""
    new_lis = []
    for item in lis:
        if type(item) == type([]):
            new_lis.extend(flatten(item))
        else:
            new_lis.append(item)

    return new_lis


def nested_partitions_distance(p1, p2):
    """
    Distance among nested partitions represented as nested lists

    :param p1:
    :param p2:
    :return:

    """
    if len(p1) > 1 and len(p2) > 1:
        set1a = set(flatten(p1[0]))
        set1b = set(flatten(p1[1]))
        set2a = set(flatten(p2[0]))
        set2b = set(flatten(p2[1]))
        if len(set1a.intersection(set2a)) > len(set1a.intersection(set2b)):
            return len(set1a.intersection(set2a)) + len(set1b.intersection(set2b)) + nested_partitions_distance(p1[0], p2[0]) + nested_partitions_distance(p1[1], p2[1])
        return len(set1a.intersection(set2b)) + len(set1b.intersection(set2a)) + nested_partitions_distance(p1[0], p2[1]) + nested_partitions_distance(p1[1], p2[0])
    elif len(p1) == 1 and len(p2) > 1:
        if p1[0] in set(flatten(p2[0])) or p1[0] in set(flatten(p2[1])):
            return 1
        else:
            return 0

    elif len(p2) == 1 and len(p1) > 1:
        if p2[0] in set(flatten(p1[0])) or p2[0] in set(flatten(p1[1])):
            return 1
        else:
            return 0

    else:
        if p1[0] == p2[0]:
            return 1
        else:
            return 0


def nested_partitions_distance2(p1, p2):
    """
    Distance among nested partitions represented as nested lists

    :param p1:
    :param p2:
    :return:

    """
    if len(p1) > 1 and len(p2) > 1:
        set1a = set(flatten(p1[0]))
        set1b = set(flatten(p1[1]))
        set2a = set(flatten(p2[0]))
        set2b = set(flatten(p2[1]))
        if len(set1a.intersection(set2a)) > len(set1a.intersection(set2b)):
            return nested_partitions_distance(p1[0], p2[0]) + nested_partitions_distance(p1[1], p2[1])
        return nested_partitions_distance(p1[0], p2[1]) + nested_partitions_distance(p1[1], p2[0])
    elif len(p1) == 1 and len(p2) > 1:
        if p1[0] in set(flatten(p2[0])) or p1[0] in set(flatten(p2[1])):
            return 1
        else:
            return 0

    elif len(p2) == 1 and len(p1) > 1:
        if p2[0] in set(flatten(p1[0])) or p2[0] in set(flatten(p1[1])):
            return 1
        else:
            return 0

    else:
        if p1[0] == p2[0]:
            return 1
        else:
            return 0


def generate_partitions(data):
    """
    Generates a random nested partition for an array of integers

    :param data:
    :return:
    """
    if len(data) == 1:
        return data
    else:
        mask1 = np.random.choice(len(data), np.floor(len(data) / 2), replace=False)
        par1 = [ data[i] for i in range(len(data)) if i in mask1 ]
        par2 = [ data[i] for i in range(len(data)) if i not in mask1 ]
        return [generate_partitions(par1), generate_partitions(par2)]


def print_nested(l, p):
    if len(l) == 1:
        print (
         ' ' * p, l)
    else:
        for v in l:
            print_nested(v, p + 1)


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    a = np.array(range(100))
    b = generate_partitions(a)
    c = generate_partitions(a)
    print nested_partitions_distance2(b, c)