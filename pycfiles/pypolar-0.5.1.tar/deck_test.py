# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/pypokerengine/engine/deck_test.py
# Compiled at: 2016-11-22 02:08:34
from tests.base_unittest import BaseUnitTest
from pypokerengine.engine.card import Card
from pypokerengine.engine.deck import Deck

class DeckTest(BaseUnitTest):

    def setUp(self):
        self.deck = Deck()

    def test_draw_card(self):
        card = self.deck.draw_card()
        self.eq('SK', str(card))
        self.eq(51, self.deck.size())

    def test_draw_cards(self):
        cards = self.deck.draw_cards(3)
        self.eq('SJ', str(cards[2]))
        self.eq(49, self.deck.size())

    def test_restore(self):
        self.deck.draw_cards(5)
        self.deck.restore()
        self.eq(52, self.deck.size())

    def test_serialization(self):
        self.deck.draw_cards(5)
        self.deck.shuffle()
        serial = self.deck.serialize()
        restored = Deck.deserialize(serial)
        self.eq(self.deck.cheat, restored.cheat)
        self.eq(self.deck.deck, restored.deck)

    def test_cheat_draw(self):
        cards = [ Card.from_id(cid) for cid in [12, 15, 17] ]
        cheat = Deck(cheat=True, cheat_card_ids=[12, 15, 17])
        self.eq(cheat.draw_cards(3), cards)

    def test_cheat_restore(self):
        cards = [ Card.from_id(cid) for cid in [12, 15, 17] ]
        cheat = Deck(cheat=True, cheat_card_ids=[12, 15, 17])
        cheat.draw_cards(2)
        cheat.restore()
        self.eq(cheat.draw_cards(3), cards)

    def test_cheat_serialization(self):
        cards = [ Card.from_id(cid) for cid in [12, 15, 17] ]
        cheat = Deck(cheat=True, cheat_card_ids=[12, 15, 17])
        serial = cheat.serialize()
        restored = Deck.deserialize(serial)
        self.eq(cheat.deck, restored.deck)
        self.eq(cheat.cheat, restored.cheat)
        self.eq(cheat.cheat_card_ids, restored.cheat_card_ids)