# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/permutation.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1090 bytes
import operator

def advance_permutation(a, increasing=True, forward=True):
    """
    Advance a list of unique, ordered elements in-place, lexicographically
    increasing or backward, by rightmost or leftmost digit.

    Returns False if the permutation wrapped around - i.e. went from
    lexicographically greatest to least, and True in all other cases.

    If the length of the list is N, then this function will repeat values after
    N! steps, and will return False exactly once.

    See also https://stackoverflow.com/a/34325140/43839
    """
    if not forward:
        a.reverse()
    cmp = operator.lt if increasing else operator.gt
    try:
        i = next(i for i in reversed(range(len(a) - 1)) if cmp(a[i], a[(i + 1)]))
        j = next(j for j in reversed(range(i + 1, len(a))) if cmp(a[i], a[j]))
    except StopIteration:
        if forward:
            a.reverse()
        return False
    else:
        a[i], a[j] = a[j], a[i]
        a[i + 1:] = reversed(a[i + 1:])
        if not forward:
            a.reverse()
        return True