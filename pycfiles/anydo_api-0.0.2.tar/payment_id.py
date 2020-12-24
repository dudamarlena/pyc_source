# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/payment_id.py
# Compiled at: 2019-05-25 07:28:23
from __future__ import absolute_import
from six import string_types

class PaymentId(object):
    """Used for having a validated instance of a payment id that we can monitor."""

    def __init__(self, payment_id):
        """
        :param payment_id: String representation of the id of the payment
        :type payment_id: str
        :raises ValueError: Thrown when one of the arguments are invalid
        """
        super(PaymentId, self).__init__()
        if not isinstance(payment_id, string_types):
            raise ValueError('Payment id must be a string')
        self._payment_id = payment_id

    @property
    def payment_id(self):
        """
        Return the payment id.
        """
        return self._payment_id

    def __str__(self):
        return '%s' % self._payment_id

    def __eq__(self, other):
        if not isinstance(other, PaymentId):
            return NotImplemented
        else:
            return self._payment_id == other.payment_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._payment_id)