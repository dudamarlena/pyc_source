# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/lead/tx.py
# Compiled at: 2008-04-27 07:30:45
import transaction, threading
from zope.interface import implements
from zope.component import adapts
from transaction.interfaces import IDataManager
from collective.lead.interfaces import ITransactionAware
from collective.lead.database import Database

class ThreadlocalDatabaseTransactions(object):
    """Implementation-specific adapter for transaction awareness
    """
    __module__ = __name__
    implements(ITransactionAware)
    adapts(Database)

    def __init__(self, context):
        self.context = context

    def begin(self):
        assert not self.active, 'Transaction already in progress'
        transaction.get().join(ThreadlocalDatabaseDataManager(self))
        self.context._threadlocal.active = True
        self.context.engine.begin()

    @property
    def active(self):
        return getattr(self.context._threadlocal, 'active', False)

    def rollback(self):
        self.context.engine.rollback()
        self.context._threadlocal.active = False
        self.context._threadlocal.session = None
        return

    def commit(self):
        self.context.engine.commit()
        self.context._threadlocal.active = False
        self.context._threadlocal.session = None
        return


class ThreadlocalDatabaseDataManager(object):
    """Use join the transactions of a threadlocal engine to Zope
    transactions
    """
    __module__ = __name__
    implements(IDataManager)

    def __init__(self, tx):
        self.tx = tx

    def abort(self, trans):
        if self.tx is not None:
            self.tx.rollback()
            self.tx = None
        return

    def commit(self, trans):
        pass

    def tpc_begin(self, trans):
        pass

    def tpc_vote(self, trans):
        self.tx.commit()
        self.tx = None
        return

    def tpc_finish(self, trans):
        pass

    def tpc_abort(self, trans):
        self.abort(trans)

    def sortKey(self):
        return '~lead:%d' % id(self.tx)