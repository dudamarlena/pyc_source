# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/comparator/comps/basic.py
# Compiled at: 2018-10-03 12:25:08
__doc__ = '\n    Comparison callables\n'
BASIC_COMP = 'basic'
LEN_COMP = 'len'
FIRST_COMP = 'first'
DEFAULT_COMP = BASIC_COMP

def basic_comp(left, right):
    return left == right


def len_comp(left, right):
    return basic_comp(len(left), len(right))


def first_eq_comp(left, right):
    return basic_comp(left.first(), right.first())


COMPS = {BASIC_COMP: basic_comp, 
   LEN_COMP: len_comp, 
   FIRST_COMP: first_eq_comp}