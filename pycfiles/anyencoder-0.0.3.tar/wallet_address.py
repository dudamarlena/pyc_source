# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/wallet_address.py
# Compiled at: 2019-05-25 07:28:23
from __future__ import absolute_import
from six import string_types

class WalletAddress(object):
    """Used for having a validated instance of a wallet address that we can easily check if it still valid."""

    def __init__(self, wallet_address):
        """
        :param wallet_address: String representation of a wallet address
        :type wallet_address: str or unicode
        :raises ValueError: Thrown when one of the arguments are invalid
        """
        super(WalletAddress, self).__init__()
        if not isinstance(wallet_address, string_types):
            raise ValueError('Wallet address must be a string, found %s instead' % type(wallet_address))
        self._wallet_address = wallet_address

    def __eq__(self, other):
        return str(other) == self._wallet_address

    @property
    def address(self):
        return self._wallet_address

    def __str__(self):
        return '%s' % self._wallet_address