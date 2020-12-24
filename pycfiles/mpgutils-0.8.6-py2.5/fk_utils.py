# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mpgutils/fk_utils.py
# Compiled at: 2008-12-04 16:36:20
import commands, sys, re, math, decimal, os

def wc(fname):
    if os.path.exists(fname) == False:
        return 0
    f = open(fname)
    counter = 0
    for z in f:
        counter = counter + 1

    f.close()
    return counter


def extract_na(fname):
    na_get = re.compile('NA\\d+', re.IGNORECASE)
    na_match = na_get.search(fname)
    if na_match:
        return na_match.group().upper()
    else:
        return 0


def mean(x):
    return sum(x) / float(len(x))


def variance(x):
    m_x = mean(x)
    length = len(x)
    if length == 1:
        return decimal.Decimal('NaN')
    sum = 0.0
    for k in range(length):
        sum += (x[k] - m_x) ** 2

    return sum / float(length - 1)


def stdev(x):
    return math.sqrt(variance(x))


def intersect(seq1, seq2):
    res = []
    for x in seq1:
        if x in seq2:
            res.append(x)

    return res


def unique(x):
    y = []
    for e in x:
        if e not in y:
            y.append(e)

    return y


def indices(x, e):
    y = []
    for k in range(len(x)):
        if x[k] == e:
            y.append(k)

    return y


def arbslice(x, indices):
    y = []
    for e in indices:
        y.append(x[e])

    return y


def arbNegSlice(x, indices):
    y = []
    remaining = set(range(0, len(x)))
    remaining = remaining.difference(indices)
    lstRemaining = [ z for z in remaining ]
    lstRemaining.sort()
    for e in lstRemaining:
        y.append(x[e])

    return y


def sorted_copy(alist):
    indices = map(_generate_index, alist)
    decorated = zip(indices, alist)
    decorated.sort()
    return [ item for (index, item) in decorated ]


def _generate_index(str):
    """
    Splits a string into alpha and numeric elements, which
    is used as an index for sorting
    """
    index = []

    def _append(fragment, alist=index):
        if fragment.isdigit():
            fragment = int(fragment)
        alist.append(fragment)

    prev_isdigit = str[0].isdigit()
    current_fragment = ''
    for char in str:
        curr_isdigit = char.isdigit()
        if curr_isdigit == prev_isdigit:
            current_fragment += char
        else:
            _append(current_fragment)
            current_fragment = char
            prev_isdigit = curr_isdigit

    _append(current_fragment)
    return tuple(index)