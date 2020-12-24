# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/david.jetelina/.local/share/virtualenvs/pyCardDeck/lib/python3.6/site-packages/pyCardDeck/cards.py
# Compiled at: 2018-10-23 07:25:13
# Size of source mod 2**32: 1080 bytes
from typing import Union

class BaseCard:
    __doc__ = '\n    This is an example Card, showing that each Card should have a name.\n\n    This is good, because when we can show player their cards just by converting\n    them to strings.\n    '

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{0}({1.__dict__})'.format(type(self).__name__, self)


class PokerCard(BaseCard):
    __doc__ = '\n    Example Poker Card, since Poker is a a deck of Unique cards,\n    we can say that if their name equals, they equal too.\n    '

    def __init__(self, suit, rank, name):
        super().__init__('{} of {}'.format(name, suit))
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        return self.name == other


CardType = Union[(BaseCard, PokerCard, object, str, int)]