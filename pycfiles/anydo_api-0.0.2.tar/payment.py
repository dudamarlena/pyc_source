# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/payment.py
# Compiled at: 2019-06-08 04:52:20
from __future__ import absolute_import
from binascii import unhexlify
from ipv8.database import database_blob
from six import text_type
from anydex.core.assetamount import AssetAmount
from anydex.core.message import Message, TraderId
from anydex.core.payment_id import PaymentId
from anydex.core.timestamp import Timestamp
from anydex.core.transaction import TransactionId
from anydex.core.wallet_address import WalletAddress

class Payment(Message):
    """Class representing a payment."""

    def __init__(self, trader_id, transaction_id, transferred_assets, address_from, address_to, payment_id, timestamp):
        super(Payment, self).__init__(trader_id, timestamp)
        self._transaction_id = transaction_id
        self._transferred_assets = transferred_assets
        self._address_from = address_from
        self._address_to = address_to
        self._payment_id = payment_id

    @classmethod
    def from_database(cls, data):
        """
        Create a Payment object based on information in the database.
        """
        trader_id, transaction_id, payment_id, transferred_amount, transferred_id, address_from, address_to, timestamp = data
        transaction_id = TransactionId(bytes(transaction_id))
        return cls(TraderId(bytes(trader_id)), transaction_id, AssetAmount(transferred_amount, str(transferred_id)), WalletAddress(str(address_from)), WalletAddress(str(address_to)), PaymentId(str(payment_id)), Timestamp(timestamp))

    def to_database(self):
        """
        Returns a database representation of a Payment object.
        :rtype: tuple
        """
        return (
         database_blob(bytes(self.trader_id)), database_blob(bytes(self.transaction_id)),
         text_type(self.payment_id), self.transferred_assets.amount,
         text_type(self.transferred_assets.asset_id), text_type(self.address_from),
         text_type(self.address_to), int(self.timestamp))

    @classmethod
    def from_block(cls, block):
        """
        Restore a payment from a TrustChain block

        :param block: TrustChainBlock
        :return: Restored payment
        :rtype: Payment
        """
        tx_dict = block.transaction['payment']
        return cls(TraderId(unhexlify(tx_dict['trader_id'])), TransactionId(unhexlify(tx_dict['transaction_id'])), AssetAmount(tx_dict['transferred']['amount'], tx_dict['transferred']['type']), WalletAddress(tx_dict['address_from']), WalletAddress(tx_dict['address_to']), PaymentId(tx_dict['payment_id']), Timestamp(tx_dict['timestamp']))

    @property
    def transaction_id(self):
        return self._transaction_id

    @property
    def transferred_assets(self):
        return self._transferred_assets

    @property
    def address_from(self):
        return self._address_from

    @property
    def address_to(self):
        return self._address_to

    @property
    def payment_id(self):
        return self._payment_id

    def to_dictionary(self):
        return {'trader_id': self.trader_id.as_hex(), 
           'transaction_id': self.transaction_id.as_hex(), 
           'transferred': self.transferred_assets.to_dictionary(), 
           'payment_id': str(self.payment_id), 
           'address_from': str(self.address_from), 
           'address_to': str(self.address_to), 
           'timestamp': int(self.timestamp)}