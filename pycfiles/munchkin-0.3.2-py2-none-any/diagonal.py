# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/gszathmari/munchkin/munchkin/core/strategies/diagonal.py
# Compiled at: 2016-05-02 03:44:35
import itertools

def diagonal(card):
    """ If the password from the card is read diagonally """
    diagonals = []
    for i in range(card.rows * -1, card.columns):
        diagonals.append(card.m.diagonal(offset=i).tolist()[0])

    results = list(itertools.chain.from_iterable(diagonals))
    return results