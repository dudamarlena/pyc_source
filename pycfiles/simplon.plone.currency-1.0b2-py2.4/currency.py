# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/simplon/plone/currency/currency.py
# Compiled at: 2007-09-08 18:44:19
from zope.component import getUtility
from zope.component import queryMultiAdapter
from BTrees.OOBTree import OOBTree
from OFS.SimpleItem import SimpleItem
from zope.interface import implements
from zope.app.container.ordered import OrderedContainer
from zope.app.container.contained import Contained
from simplon.plone.currency.interfaces import ICurrency
from simplon.plone.currency.interfaces import ICurrencyStorage
from simplon.plone.currency.currencies import currencies

class Currency(SimpleItem, Contained):
    __module__ = __name__
    implements(ICurrency)

    def __init__(self, code='', rate=1.0):
        self.code = code
        self.rate = rate

    @property
    def symbol(self):
        return currencies[self.code][1]

    @property
    def description(self):
        return currencies[self.code][0]


class CurrencyStorage(OrderedContainer):
    __module__ = __name__
    implements(ICurrencyStorage)

    def __init__(self):
        OrderedContainer.__init__(self)
        self._data = OOBTree()

    def addItem(self, item):
        self[item.code] = item