# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/gszathmari/munchkin/munchkin/core/strategies/top_to_down.py
# Compiled at: 2016-05-02 03:44:35


def top_to_down(card):
    """ If the password from the card is read from top to down """
    data = card.m.getT().getA1().flatten()
    results = data.tolist()
    return results