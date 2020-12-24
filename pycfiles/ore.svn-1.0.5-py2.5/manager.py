# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/manager.py
# Compiled at: 2008-05-07 15:44:29
"""
Subversion Data Manager to integrate with zope transactions.

dev notes.

 - we don't, really need to lock all nodes for pessimistic behavior, just the lcd
   parent nodes for the txn node set.

$Id: manager.py 2205 2008-05-07 19:44:27Z hazmat $
"""
import weakref, transaction
from zope.interface import implements
from transaction.interfaces import IDataManager
from interfaces import ISubversionDirectory, NoTransaction
from svn import core, fs as svn_fs
from property import txn_property
import tree

class SubversionTransaction(object):
    """
    a user consumable facade to the data manager, we bind to the
    resource context, to allow for easy usage across transactions
    boundaries.
    """
    __slots__ = ('_ctx', )

    def __init__(self, resource_ctx):
        self._ctx = weakref.ref(resource_ctx)

    def _get_dm(self):
        dm = self._ctx().getDataManager()
        if not dm or not dm.svnfs_txn:
            raise NoTransaction('no active transaction')
        return dm

    dm = property(_get_dm)

    def commit(self):
        self.dm.svnfs_txn
        transaction.commit()

    def abort(self):
        self.dm.svnfs_txn
        transaction.abort()

    author = txn_property(core.SVN_PROP_REVISION_AUTHOR)
    message = txn_property(core.SVN_PROP_REVISION_LOG)


class SubversionDataManager(object):
    implements(IDataManager)

    def __init__(self, resource_ctx):
        self.resource_ctx = resource_ctx
        self.svnfs_txn = None
        self.nodes = set()
        self.lock_token = None
        return

    def do_nothing(self, *args):
        pass

    tpc_begin = tpc_vote = do_nothing

    def commit(self, transaction):
        if not self.svnfs_txn:
            return
        self._acquireLocks()

    def tpc_finish(self, transaction):
        if self.svnfs_txn:
            results = svn_fs.commit_txn(self.svnfs_txn, self.resource_ctx.pool)
            self._releaseLocks()
        self._clear()

    def tpc_abort(self, transaction):
        if self.svnfs_txn:
            svn_fs.abort_txn(self.svnfs_txn, self.resource_ctx.pool)
            self._releaseLocks()
        self._clear()

    def abort(self, transaction):
        if self.svnfs_txn:
            svn_fs.abort_txn(self.svnfs_txn, self.resource_ctx.pool)
        self._clear()

    def sortKey(self):
        return 'ore.svn-1'

    def register(self, node):
        self.nodes.add(node)
        if not self.svnfs_txn:
            self._begin()

    def registerForTxn(self):
        transaction.get().join(self)

    def getProperties(self):
        if not self.svnfs_txn:
            raise RuntimeError('no transaction in progress')
        return svn_fs.txn_proplist(self.svnfs_txn)

    def setProperty(self, property_name, property_value):
        if not self.svnfs_txn:
            raise RuntimeError('no transaction in progress')
        svn_fs.change_txn_prop(self.svnfs_txn, property_name, property_value, self.resource_ctx.pool)

    def getProperty(self, property_name):
        if not self.svnfs_txn:
            raise RuntimeError('no transaction in progress')
        return svn_fs.txn_prop(self.svnfs_txn, property_name, self.resource_ctx.pool)

    def delProperty(self, property_name):
        if not self.svnfs_txn:
            raise RuntimeError('no transaction in progress')
        self.setProperty(property_name, None)
        return

    def _clear(self):
        self.svnfs_txn = None
        self.resource_ctx.locked = False
        self.resource_ctx.clearDetails()
        self.resource_ctx.setRevision()
        self.resource_ctx = None
        self.nodes = set()
        self.lock_token = None
        return

    def _begin(self):
        self.resource_ctx.locked = True
        self.svnfs_txn = svn_fs.begin_txn2(self.resource_ctx.fsptr, self.resource_ctx.revision, svn_fs.SVN_FS_TXN_CHECK_LOCKS, self.resource_ctx.pool)
        self.resource_ctx.txnroot = svn_fs.txn_root(self.svnfs_txn, self.resource_ctx.pool)
        if self.resource_ctx.access is not None:
            self.setProperty(core.SVN_PROP_REVISION_AUTHOR, self.resource_ctx.access_name)
        return

    def _releaseLocks(self):
        if self.lock_token is None:
            return
        for n in self.locks:
            svn_fs.unlock(n, self.lock_token)

        self.lock_token = None
        self.locks = set()
        return

    def _acquireLocks(self):
        return
        self.lock_token = svn_fs.generate_lock_token(self.resource_ctx.fsroot, self.resource_ctx.pool)
        svn_fs.add_lock_token(self.resource_context.access, self.lock_token)
        for n in self.nodes:
            if n is None:
                continue
            n_lock = svn_fs.lock(self.resource_ctx.fsroot, n.svn_path, self.lock_token, 'ztxn', 0, 0, self.resource_ctx.revision, 0, self.resource_ctx.pool)
            self.locks.add(n.svn_path)
            if ISubversionDirectory.providedBy(n):
                tree.lockTree(n, self.lock_token)

        return