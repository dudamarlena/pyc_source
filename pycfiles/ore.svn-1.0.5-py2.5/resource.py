# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/resource.py
# Compiled at: 2008-05-07 15:44:29
"""
we manage svn resource contexts, in such as way as to allow for retrieval by persistent contexts in a
thread local manner, and to allow for proper cleanup.

$Id: resource.py 2205 2008-05-07 19:44:27Z hazmat $
"""
import atexit, transaction
from thread import get_ident
from svn import fs, repos, core
from manager import SubversionDataManager
from log import log

def initializeAPR():
    log.debug('Initializing APR')
    core.apr_initialize()

    def apr_exit():
        global tls
        for ctx in tls.iterReset():
            ctx.finalize()

        core.apr_terminate()

    atexit.register(apr_exit)


initializeAPR()

class TLSContextManager(object):

    def __init__(self):
        self.data = {}

    def getFor(self, ob):
        ob_data = self.data.get(hash(ob), None)
        if ob_data is None:
            return
        return ob_data.get(get_ident())

    def setFor(self, ob, value):
        self.data.setdefault(hash(ob), {})[get_ident()] = value

    def delFor(self, ob):
        del self.data.setdefault(hash(ob), {})[get_ident()]

    def iterReset(self):
        for ob_data in self.data.values():
            for tls_data in ob_data.values():
                yield tls_data

        self.data = {}

    def pprint(self):
        import pprint
        pprint.pprint(self.data)


tls = TLSContextManager()

class ResourceContext(object):
    """
    All Subversion/APR resources held/used by an svn context are stored in
    a resource context. The encapsulation in a resource context allows for
    tranparent cleanup of variables for finalization methods when the volatile
    variable reference used by the svn context goes out of scope or is garbage
    collected.
    """

    def __init__(self, repository_path, svn_path, revision=None):
        self.repository_path = repository_path
        self.svn_path = repository_path
        self.finalized = False
        self.initialized = False
        self.master_pool = None
        self.pool = None
        self.repository = None
        self.fsptr = None
        self.fsroot = None
        self.revision = revision
        self.txnroot = None
        self.access = None
        self.access_name = None
        self.locked = False
        self.data_manager = None
        self.master_pool = core.svn_pool_create(None)
        self.pool = core.svn_pool_create(self.master_pool)
        self.repository = repos.svn_repos_open(str(self.repository_path), self.master_pool)
        self.fsptr = repos.svn_repos_fs(self.repository)
        self._initialize()
        return

    def _root(self):
        return self.txnroot or self.fsroot
        return self.fsroot

    root = property(_root)

    def register(self):
        if not self.data_manager:
            self.data_manager = SubversionDataManager(self)
            self.data_manager.registerForTxn()

    def setAccess(self, access_name=None):
        if self.access and access_name == self.access_name:
            return
        if not access_name and not self.access:
            access_name = self.access_name
        if not access_name and not self.access_name:
            raise SyntaxError('access name not given')
        self.access_name = access_name
        self.access = fs.create_access(access_name, self.pool)
        fs.set_access(self.fsptr, self.access)

    def setRevision(self, revision=None):
        if self.locked:
            raise RuntimeError('resource context is locked')
        if revision is not None:
            revision = int(revision)
        else:
            revision = fs.youngest_rev(self.fsptr, self.pool)
        if self.revision == revision and self.fsroot is not None:
            return
        if self.fsroot is not None:
            fs.close_root(self.fsroot)
        self.fsroot = fs.revision_root(self.fsptr, revision, self.pool)
        self.revision = revision
        return

    def getDataManager(self):
        return self.data_manager

    def _initialize(self):
        """
        create main pool if nesc, set to youngest revision
        """
        if self.initialized:
            return
        if self.locked:
            raise RuntimeError('resource context is locked')
        if self.revision is not None:
            if not isinstance(self.revision, int):
                try:
                    self.revision = int(self.revision)
                except:
                    raise SyntaxError('Revisions must be specified as integers')

        log.debug('initializing')
        if self.pool is None:
            self.pool = core.svn_pool_create(self.master_pool)
        if self.revision is None:
            self.revision = fs.youngest_rev(self.fsptr, self.pool)
        self.setRevision(self.revision)
        self.initialized = True
        return

    def clearDetails(self):
        if self.locked:
            raise RuntimeError('resource context is locked')
        if self.access is not None:
            fs.set_access(self.fsptr, None)
            self.access = None
        if self.txnroot is not None:
            fs.close_root(self.txnroot)
            self.txnroot = None
        if self.fsroot is not None:
            fs.close_root(self.fsroot)
            self.fsroot = None
        if self.pool is not None:
            core.svn_pool_clear(self.pool)
        self.data_manager = None
        self.locked = False
        return

    def finalize(self):
        if self.finalized or not self.initialized:
            return
        fs.close_root(self.fsroot)
        core.svn_pool_clear(self.pool)
        core.svn_pool_destroy(self.pool)
        core.svn_pool_clear(self.master_pool)
        core.svn_pool_destroy(self.master_pool)
        self.access = None
        self.fsroot = None
        self.fsptr = None
        self.pool = None
        self.finalized = True
        self.locked = False
        return