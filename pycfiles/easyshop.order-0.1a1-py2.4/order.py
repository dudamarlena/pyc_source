# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/order/events/order.py
# Compiled at: 2008-09-03 11:15:08
from zope.interface import implements
from easyshop.core.interfaces import IOrderClosed
from easyshop.core.interfaces import IOrderPayed
from easyshop.core.interfaces import IOrderSent
from easyshop.core.interfaces import IOrderSubmitted

class OrderClosed(object):
    """
    """
    __module__ = __name__
    implements(IOrderClosed)

    def __init__(self, context):
        self.context = context


class OrderPayed(object):
    """
    """
    __module__ = __name__
    implements(IOrderPayed)

    def __init__(self, context):
        self.context = context


class OrderSent(object):
    """
    """
    __module__ = __name__
    implements(IOrderSent)

    def __init__(self, context):
        self.context = context


class OrderSubmitted(object):
    """
    """
    __module__ = __name__
    implements(IOrderSubmitted)

    def __init__(self, context):
        self.context = context