# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/alchemist/manager.py
# Compiled at: 2008-09-11 20:29:53
"""
zope transaction manager integration for sqlalchemy

$Id: manager.py 299 2008-05-23 20:31:48Z kapilt $
"""
from zope import interface
import transaction, transaction.interfaces

class SessionDataManager(object):
    """
    a data manager facade for sqlalchemy sessions participating in
    zope transactions.    
    """
    interface.implements(transaction.interfaces.IDataManager)

    def __init__(self, session):
        self.session = session
        self.joined = False

    def _check(self):
        return bool(self.session.new or self.session.deleted or self.session.dirty)

    def abort(self, transaction):
        self.session.joined = False
        if self.session.transaction:
            self.session.transaction.rollback()
        self.session.clear()

    def commit(self, transaction):
        if not self.session.transaction:
            self.session.begin()
        if self.session.autoflush:
            return
        self.session.flush()

    def tpc_finish(self, transaction):
        self.session.joined = False
        self.session.transaction.commit()
        self.session.clear()

    def tpc_abort(self, transaction):
        self.session.joined = False
        self.session.transaction.rollback()
        self.session.clear()

    def sortKey(self):
        return '100-alchemist'

    def null(self, *args, **kw):
        pass

    tpc_vote = tpc_begin = null

    def register(self):
        txn = transaction.get()
        txn.join(self)