# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tmiedema/.pyenv/versions/3.6.0/lib/python3.6/site-packages/holdmybeer/util.py
# Compiled at: 2017-03-28 17:06:13
# Size of source mod 2**32: 970 bytes
"""
How to divide an amount according to ratios, without introducing rounding errors? A clean implementation is the
largest remainder method, see https://en.wikipedia.org/wiki/Largest_remainder_method or
http://stackoverflow.com/questions/13483430/how-to-make-rounded-percentages-add-up-to-100
"""

def divide(amount, ratios):
    total = sum(ratios)
    truediv = [amount * r / float(total) for r in ratios]
    floordiv = [int(div) for div in truediv]
    diff = amount - sum(floordiv)
    order = argsort_by_fraction(truediv)
    for i in range(diff):
        floordiv[order[i]] += 1

    return floordiv


def argsort_by_fraction(array):
    fractions = [1 - num % 1.0 for num in array]
    return sorted((range(len(fractions))), key=(fractions.__getitem__))