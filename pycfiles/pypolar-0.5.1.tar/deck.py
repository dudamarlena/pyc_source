# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pypokerengine/engine/deck.py
# Compiled at: 2017-02-24 03:36:19
from functools import reduce
from pypokerengine.engine.card import Card
import random

class Deck:

    def __init__(self, deck_ids=None, cheat=False, cheat_card_ids=[]):
        self.cheat = cheat
        self.cheat_card_ids = cheat_card_ids
        self.deck = [ Card.from_id(cid) for cid in deck_ids ] if deck_ids else self.__setup()

    def draw_card(self):
        return self.deck.pop()

    def draw_cards(self, num):
        return reduce(lambda acc, _: acc + [self.draw_card()], range(num), [])

    def size(self):
        return len(self.deck)

    def restore(self):
        self.deck = self.__setup()

    def shuffle(self):
        if not self.cheat:
            random.shuffle(self.deck)

    def serialize(self):
        return [
         self.cheat, self.cheat_card_ids, [ card.to_id() for card in self.deck ]]

    @classmethod
    def deserialize(self, serial):
        cheat, cheat_card_ids, deck_ids = serial
        return self(deck_ids=deck_ids, cheat=cheat, cheat_card_ids=cheat_card_ids)

    def __setup(self):
        if self.cheat:
            return self.__setup_cheat_deck()
        return self.__setup_52_cards()

    def __setup_52_cards(self):
        return [ Card.from_id(cid) for cid in range(1, 53) ]

    def __setup_cheat_deck(self):
        cards = [ Card.from_id(cid) for cid in self.cheat_card_ids ]
        return cards[::-1]