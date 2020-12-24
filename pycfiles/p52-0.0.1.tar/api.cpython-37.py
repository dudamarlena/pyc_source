# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/p52/p52/api.py
# Compiled at: 2019-12-03 19:58:26
# Size of source mod 2**32: 522 bytes
from p52.base import Rank, Suit, Card
from p52.static import *
Spades, Hearts, Clubs, Diamonds = [Suit(**data) for data in SUITS_DATA]
suits = (Spades, Hearts, Clubs, Diamonds)
Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Jack, Queen, King, Ace = [Rank(**data) for data in RANKS_DATA]
ranks = (Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Jack, Queen, King, Ace)

def gen_new_deck():
    cards = list()
    for r in ranks:
        for s in suits:
            cards.append(Card(r, s))

    return cards