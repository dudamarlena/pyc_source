# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/gszathmari/munchkin/munchkin/core/strategies/zig_zag.py
# Compiled at: 2016-05-02 03:44:35
import itertools

def zig_zag(card):
    """ If the password from the card is read in zig-zag directions """
    rows = card.m.getA().tolist()
    for i in range(len(rows)):
        if i % 2 != 0:
            rows[i].reverse()

    results = list(itertools.chain.from_iterable(rows))
    return results