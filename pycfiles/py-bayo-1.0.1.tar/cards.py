# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.5/site-packages/bankpassweb/cards.py
# Compiled at: 2007-12-03 09:04:00
from datatypes import Parsable

class Card(Parsable):
    """
        Base class for credit cards.
        """

    def __init__(self):
        self.name = self.__class__.__name__


class Visa(Card):
    code = '01'


class Mastercard(Card):
    code = '02'


class Amex(Card):
    code = '03'


class Diners(Card):
    code = '06'


class JCB(Card):
    code = '08'


class PagoBancomat(Card):
    code = '09'


class CartaAura(Card):
    code = '10'


class UnknownCard(Card):

    def __init__(self, code):
        self.code = code
        self.name = 'Unknown card %s' % code