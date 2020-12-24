# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sillymap/burrows_wheeler.py
# Compiled at: 2017-03-28 10:33:21


def burrows_wheeler(text):
    """Calculates the burrows wheeler transform of <text>.

    returns the burrows wheeler string and the suffix array indices
    The text is assumed to not contain the character $"""
    text += '$'
    all_permutations = []
    for i in range(len(text)):
        all_permutations.append((text[i:] + text[:i], i))

    all_permutations.sort()
    bw_l = []
    sa_i = []
    for w, j in all_permutations:
        bw_l.append(w[(-1)])
        sa_i.append(j)

    return (('').join(bw_l), sa_i)