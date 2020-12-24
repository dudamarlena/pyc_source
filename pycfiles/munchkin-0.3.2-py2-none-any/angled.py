# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/gszathmari/munchkin/munchkin/core/strategies/angled.py
# Compiled at: 2016-05-02 03:44:35


def angled(card):
    """ If the password from the card is read in a rotated 'L' shape """
    results = []
    for i in range(0, card.rows - 1):
        stream = card.m[i].tolist()[0]
        for j in range(i + 1, card.rows):
            stream.append(card.m[j].tolist()[0][(-1)])

        results.append(stream)

    return results