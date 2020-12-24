# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/core/order_repository.py
# Compiled at: 2019-05-25 07:28:23
from __future__ import absolute_import
import logging
from abc import ABCMeta, abstractmethod
from anydex.core.message import TraderId
from anydex.core.order import OrderId, OrderNumber

class OrderRepository(object):
    """A repository interface for orders in the order manager"""
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Do not use this class directly

        Make a subclass of this class with a specific implementation for a storage backend
        """
        super(OrderRepository, self).__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, order_id):
        pass

    @abstractmethod
    def add(self, order):
        pass

    @abstractmethod
    def update(self, order):
        pass

    @abstractmethod
    def delete_by_id(self, order_id):
        pass

    @abstractmethod
    def next_identity(self):
        pass


class MemoryOrderRepository(OrderRepository):
    """A repository for orders in the order manager stored in memory"""

    def __init__(self, mid):
        """
        :param mid: Hex encoded version of the member id of this node
        :type mid: str
        """
        super(MemoryOrderRepository, self).__init__()
        self._logger.info('Memory order repository used')
        self._mid = mid
        self._next_id = 0
        self._orders = {}

    def find_all(self):
        """
        :rtype: [Order]
        """
        return self._orders.values()

    def find_by_id(self, order_id):
        """
        :param order_id: The order id to look for
        :type order_id: OrderId
        :return: The order or null if it cannot be found
        :rtype: Order
        """
        return self._orders.get(order_id)

    def add(self, order):
        """
        :type order: Order
        """
        self._logger.debug('Order with the id: ' + str(order.order_id) + ' was added to the order repository')
        self._orders[order.order_id] = order

    def update(self, order):
        """
        :type order: Order
        """
        self._logger.debug('Order with the id: ' + str(order.order_id) + ' was updated to the order repository')
        self._orders[order.order_id] = order

    def delete_by_id(self, order_id):
        """
        :type order_id: OrderId
        """
        self._logger.debug('Order with the id: ' + str(order_id) + ' was deleted from the order repository')
        del self._orders[order_id]

    def next_identity(self):
        """
        :rtype: OrderId
        """
        self._next_id += 1
        return OrderId(TraderId(self._mid), OrderNumber(self._next_id))


class DatabaseOrderRepository(OrderRepository):
    """A repository that stores orders in the database"""

    def __init__(self, mid, persistence):
        """
        :param mid: Hex encoded version of the member id of this node
        :type mid: str
        """
        super(DatabaseOrderRepository, self).__init__()
        self._logger.info('Memory order repository used')
        self._mid = mid
        self.persistence = persistence

    def find_all(self):
        """
        :rtype: [Order]
        """
        return self.persistence.get_all_orders()

    def find_by_id(self, order_id):
        """
        :param order_id: The order id to look for
        :type order_id: OrderId
        :return: The order or null if it cannot be found
        :rtype: Order
        """
        return self.persistence.get_order(order_id)

    def add(self, order):
        """
        :param order: The order to add to the database
        :type order: Order
        """
        self.persistence.add_order(order)

    def update(self, order):
        """
        :param order: The order to update
        :type order: Order
        """
        self.delete_by_id(order.order_id)
        self.add(order)

    def delete_by_id(self, order_id):
        """
        :param order_id: The id of the order to remove
        """
        self.persistence.delete_order(order_id)

    def next_identity(self):
        """
        :rtype OrderId
        """
        return OrderId(TraderId(self._mid), OrderNumber(self.persistence.get_next_order_number()))