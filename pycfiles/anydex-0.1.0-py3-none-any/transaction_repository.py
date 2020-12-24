# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/transaction_repository.py
# Compiled at: 2019-06-08 04:52:20
import logging
from abc import ABCMeta, abstractmethod
from anydex.core.message import TraderId
from anydex.core.transaction import TransactionId

class TransactionRepository(object):
    """A repository interface for transactions in the transaction manager"""
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Do not use this class directly

        Make a subclass of this class with a specific implementation for a storage backend
        """
        super(TransactionRepository, self).__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, transaction_id):
        pass

    @abstractmethod
    def add(self, transaction):
        pass

    @abstractmethod
    def update(self, transaction):
        pass

    @abstractmethod
    def delete_by_id(self, transaction_id):
        pass


class MemoryTransactionRepository(TransactionRepository):
    """A repository for transactions in the transaction manager stored in memory"""

    def __init__(self, mid):
        """
        :param mid: Hex encoded version of the member id of this node
        :type mid: str
        """
        super(MemoryTransactionRepository, self).__init__()
        self._logger.info('Memory transaction repository used')
        self._mid = mid
        self._next_id = 0
        self._transactions = {}

    def find_all(self):
        """
        :rtype: [Transaction]
        """
        return self._transactions.values()

    def find_by_id(self, transaction_id):
        """
        :param transaction_id: The transaction id to look for
        :type transaction_id: TransactionId
        :return: The transaction or null if it cannot be found
        :rtype: Transaction
        """
        return self._transactions.get(transaction_id)

    def add(self, transaction):
        """
        :type transaction: Transaction
        """
        self._logger.debug('Transaction with the id: %s was added to the transaction repository', transaction.transaction_id.as_hex())
        self._transactions[transaction.transaction_id] = transaction

    def update(self, transaction):
        """
        :type transaction: Transaction
        """
        self._logger.debug('Transaction with the id: %s was updated in the transaction repository', transaction.transaction_id.as_hex())
        self._transactions[transaction.transaction_id] = transaction

    def delete_by_id(self, transaction_id):
        """
        :type transaction_id: TransactionId
        """
        self._logger.debug('Transaction with the id: %s was deleted from the transaction repository', transaction_id.as_hex())
        del self._transactions[transaction_id]


class DatabaseTransactionRepository(TransactionRepository):
    """A repository for transactions in the transaction manager stored in a database"""

    def __init__(self, mid, persistence):
        """
        :param mid: Hex encoded version of the member id of this node
        :type mid: str
        """
        super(DatabaseTransactionRepository, self).__init__()
        self._logger.info('Database transaction repository used')
        self._mid = mid
        self.persistence = persistence

    def find_all(self):
        """
        :rtype: [Transaction]
        """
        return self.persistence.get_all_transactions()

    def find_by_id(self, transaction_id):
        """
        :param transaction_id: The transaction id to look for
        :type transaction_id: TransactionId
        :return: The transaction or null if it cannot be found
        :rtype: Transaction
        """
        return self.persistence.get_transaction(transaction_id)

    def add(self, transaction):
        """
        :param transaction: The transaction to add to the database
        :type transaction: Transaction
        """
        self.persistence.add_transaction(transaction)

    def update(self, transaction):
        """
        :param transaction: The transaction to update
        :type transaction: Transaction
        """
        self.delete_by_id(transaction.transaction_id)
        self.add(transaction)

    def delete_by_id(self, transaction_id):
        """
        :param transaction_id: The id of the transaction to remove
        """
        self.persistence.delete_transaction(transaction_id)