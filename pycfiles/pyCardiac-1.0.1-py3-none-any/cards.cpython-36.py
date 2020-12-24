# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/david.jetelina/.local/share/virtualenvs/pyCardDeck/lib/python3.6/site-packages/pyCardDeck/cards.py
# Compiled at: 2018-10-23 07:25:13
# Size of source mod 2**32: 1080 bytes
from typing import Union

class BaseCard:
    """BaseCard"""

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{0}({1.__dict__})'.format(type(self).__name__, self)


class PokerCard(BaseCard):
    """PokerCard"""

    def __init__(self, suit, rank, name):
        super().__init__('{} of {}'.format(name, suit))
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        return self.name == other


CardType = Union[(BaseCard, PokerCard, object, str, int)]