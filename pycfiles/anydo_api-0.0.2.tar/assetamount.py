# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/assetamount.py
# Compiled at: 2019-05-25 07:28:23
from __future__ import absolute_import
from six import string_types
try:
    long
except NameError:
    long = int

class AssetAmount(object):
    """
    This class represents a specific number of assets. It contains various utility methods to add/substract asset
    amounts.
    """

    def __init__(self, amount, asset_id):
        """
        :param amount: Integer representation of the asset amount
        :param asset_id: Identifier of the asset type of this amount
        :type amount: int
        :type asset_id: str
        """
        super(AssetAmount, self).__init__()
        if isinstance(amount, int):
            amount = long(amount)
        if not isinstance(amount, long):
            raise ValueError('Price must be a long')
        if not isinstance(asset_id, string_types):
            raise ValueError('Asset id must be a string')
        self._amount = amount
        self._asset_id = asset_id

    @property
    def asset_id(self):
        """
        :rtype: str
        """
        return self._asset_id

    @property
    def amount(self):
        """
        :rtype long
        """
        return self._amount

    def __str__(self):
        return '%d %s' % (self.amount, self.asset_id)

    def __add__(self, other):
        if isinstance(other, AssetAmount) and self.asset_id == other.asset_id:
            return self.__class__(self.amount + other.amount, self.asset_id)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, AssetAmount) and self.asset_id == other.asset_id:
            return self.__class__(self.amount - other.amount, self.asset_id)
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, AssetAmount) and self.asset_id == other.asset_id:
            return self.amount < other.amount
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, AssetAmount) and self.asset_id == other.asset_id:
            return self.amount <= other.amount
        else:
            return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, AssetAmount) or self.asset_id != other.asset_id:
            return NotImplemented
        return self.amount == other.amount

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, AssetAmount) and self.asset_id == other.asset_id:
            return self.amount > other.amount
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, AssetAmount) and self.asset_id == other.asset_id:
            return self.amount >= other.amount
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.amount, self.asset_id))

    def to_dictionary(self):
        return {'amount': self.amount, 
           'type': self.asset_id}