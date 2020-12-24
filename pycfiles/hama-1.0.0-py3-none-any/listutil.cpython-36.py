# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/listutil.py
# Compiled at: 2020-03-20 01:04:27
# Size of source mod 2**32: 663 bytes
from itertools import product

def insert(l, i, e):
    """Inserts element e into list l at index i.

    Args:
        l (list): List to insert into.
        i (int): Index to insert at.
        e (obj): Object to insert.

    Returns:
        list: Returns a new list containing the inserted element.
    """
    temp = l[:]
    temp[i:i] = [e]
    return temp


def cartesian_product(*lists):
    """Produces every possible pair of elements from input lists.

    Args:
        lists (list): Lists of variable length.

    Returns:
        list: List containing tuples of all possible combinations. 
    """
    pairs = list(product(*lists))
    return pairs