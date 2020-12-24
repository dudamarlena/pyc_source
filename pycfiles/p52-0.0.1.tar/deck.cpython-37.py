# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/p52/p52/deck.py
# Compiled at: 2019-12-03 20:59:23
# Size of source mod 2**32: 1262 bytes
import random
from datetime import datetime
from p52.base import Card
from p52.api import ranks, suits, gen_new_deck

class Deck:
    _Deck__cards = list()
    trump = None

    def __init__(self, init_shuffle=True, *args, **kwargs):
        self._Deck__cards = gen_new_deck() if not kwargs.get('cards') else None
        self.shuffle() if init_shuffle else None
        self.time = datetime.now()
        self.__name__ = f"Deck {hex(self.__hash__())}"
        self.__repr__ = f"{self.__name__}\nCreated: {self.time}\nCards: {self.number_of_cards}\n"

    def __iter__(self):
        for card in self._Deck__cards:
            yield card

    def __len__(self):
        return len(self._Deck__cards)

    def __repr__(self):
        return self.__repr__

    def __str__(self):
        return self.__name__

    def __hash__(self):
        return hash(self.time)

    def __getitem__(self, item):
        return self._Deck__cards[item]

    @property
    def number_of_cards(self):
        return self.__len__()

    def get_cards(self):
        return self._Deck__cards

    def shuffle(self):
        random.shuffle(self._Deck__cards)

    def fetch_card(self):
        return self._Deck__cards.pop()