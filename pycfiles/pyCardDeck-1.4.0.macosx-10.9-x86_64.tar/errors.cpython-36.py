# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/david.jetelina/.local/share/virtualenvs/pyCardDeck/lib/python3.6/site-packages/pyCardDeck/errors.py
# Compiled at: 2018-10-23 07:21:47
# Size of source mod 2**32: 857 bytes


class DeckException(Exception):
    __doc__ = '\n    Base exception class for pyCardDeck\n    '


class NoCards(DeckException):
    __doc__ = "\n    Exception that's thrown when there are no cards to be manipulated.\n    "


class OutOfCards(DeckException):
    __doc__ = "\n    Exception that's thrown when the deck runs out of cards.\n    Unlike NoCardsException, this will happen naturally when reshuffling is disabled\n    "


class NotACard(DeckException):
    __doc__ = "\n    Exception that's thrown when the manipulated object is False/None\n    "


class CardNotFound(DeckException):
    __doc__ = "\n    Exception that's thrown when a card is not found\n    "


class UnknownFormat(Exception):
    __doc__ = '\n    Exception thrown when trying to export to a unknown format.\n    Supported formats: YaML, JSON\n    '