# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/transit/helpers.py
# Compiled at: 2017-12-12 16:52:26
import itertools
from transit.pyversion import imap, izip

def mapcat(f, i):
    return itertools.chain.from_iterable(imap(f, i))


def pairs(i):
    return izip(*([iter(i)] * 2))


cycle = itertools.cycle

def take(n, i):
    return itertools.islice(i, 0, n)