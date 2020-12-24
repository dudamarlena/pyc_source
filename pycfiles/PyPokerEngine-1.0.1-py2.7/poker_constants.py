# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pypokerengine/engine/poker_constants.py
# Compiled at: 2017-02-23 21:05:37


class PokerConstants:

    class Action:
        FOLD = 0
        CALL = 1
        RAISE = 2
        SMALL_BLIND = 3
        BIG_BLIND = 4
        ANTE = 5

    class Street:
        PREFLOP = 0
        FLOP = 1
        TURN = 2
        RIVER = 3
        SHOWDOWN = 4
        FINISHED = 5