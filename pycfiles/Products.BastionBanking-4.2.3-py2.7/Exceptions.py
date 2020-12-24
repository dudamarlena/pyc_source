# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/Exceptions.py
# Compiled at: 2015-07-18 19:38:10


class BankingException(Exception):
    """
    an exception within the BastionBanking suite
    """
    pass


class InvalidAmount(BankingException):
    """
    an amount is invalid eg zero (say), for the context it's being used
    """
    pass


class UnsupportedCurrency(BankingException):
    """
    We don't know about this currency type, you probably need a Tradeable entry
    to translate it into a base currency we can enact upon
    """
    pass


class CreditCardInvalid(BankingException):
    """
    Credit card number doesn't pass validation test
    """
    pass


class CreditCardExpired(BankingException):
    """
    Credit card has expired 
    """
    pass


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