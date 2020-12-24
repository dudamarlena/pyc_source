# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/Exceptions.py
# Compiled at: 2015-07-18 19:38:10


class BankingException(Exception):
    """
    an exception within the BastionBanking suite
    """


class InvalidAmount(BankingException):
    """
    an amount is invalid eg zero (say), for the context it's being used
    """


class UnsupportedCurrency(BankingException):
    """
    We don't know about this currency type, you probably need a Tradeable entry
    to translate it into a base currency we can enact upon
    """


class CreditCardInvalid(BankingException):
    """
    Credit card number doesn't pass validation test
    """


class CreditCardExpired(BankingException):
    """
    Credit card has expired 
    """


class ProcessingFailure(BankingException):
    """
    Back office rejected our request
    """
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, error, messages={}):
        """
        messages is a hash of form-fields and their error messages
        """
        self.error = error
        self.messages = messages

    def __str__(self):
        return self.error