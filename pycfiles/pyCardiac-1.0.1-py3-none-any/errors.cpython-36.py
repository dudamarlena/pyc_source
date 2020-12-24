# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/david.jetelina/.local/share/virtualenvs/pyCardDeck/lib/python3.6/site-packages/pyCardDeck/errors.py
# Compiled at: 2018-10-23 07:21:47
# Size of source mod 2**32: 857 bytes


class DeckException(Exception):
    """DeckException"""
    pass


class NoCards(DeckException):
    """NoCards"""
    pass


class OutOfCards(DeckException):
    """OutOfCards"""
    pass


class NotACard(DeckException):
    """NotACard"""
    pass


class CardNotFound(DeckException):
    """CardNotFound"""
    pass


class UnknownFormat(Exception):
    """UnknownFormat"""
    pass