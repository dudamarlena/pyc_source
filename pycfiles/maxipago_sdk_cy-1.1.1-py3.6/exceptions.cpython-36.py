# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/maxipago/exceptions.py
# Compiled at: 2018-07-08 23:37:16
# Size of source mod 2**32: 582 bytes


class MaxipagoException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ValidationError(MaxipagoException):

    def __repr__(self):
        return 'ValidationError(%s)' % self.message


class CustomerException(MaxipagoException):
    pass


class CustomerAlreadyExists(CustomerException):
    pass


class CardException(MaxipagoException):
    pass


class PaymentException(MaxipagoException):
    pass


class HttpErrorException(MaxipagoException):
    pass