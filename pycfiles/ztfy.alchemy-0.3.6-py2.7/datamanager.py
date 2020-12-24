# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/alchemy/datamanager.py
# Compiled at: 2013-07-11 04:31:08
import transaction as zope_transaction
from transaction.interfaces import ISavepointDataManager, IDataManagerSavepoint
from transaction._transaction import Status as ZopeStatus
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import ConcurrentModificationError
from sqlalchemy.orm.session import SessionExtension
from sqlalchemy.engine.base import Engine
from zope.interface import implements
_retryable_errors = []
try:
    import psycopg2.extensions
except ImportError:
    pass
else:
    _retryable_errors.append((psycopg2.extensions.TransactionRollbackError, None))

try:
    import cx_Oracle
except ImportError:
    pass
else:
    _retryable_errors.append((cx_Oracle.DatabaseError, lambda e: e.args[0].code == 8177))

STATUS_ACTIVE = 'active'
STATUS_CHANGED = 'changed'
STATUS_READONLY = 'readonly'
STATUS_INVALIDATED = STATUS_CHANGED
NO_SAVEPOINT_SUPPORT = set(['sqlite'])
_SESSION_STATE = {}

class SessionDataManager(object):
    """Integrate a top level sqlalchemy session transaction into a zope transaction
    
    One phase variant.
    """
    implements(ISavepointDataManager)

    def __init__(self, session, status, transaction_manager):
        self.transaction_manager = transaction_manager
        self.tx = session.transaction._iterate_parents()[(-1)]
        self.session = session
        _SESSION_STATE[id(session)] = status
        self.state = 'init'

    def _finish(self, final_state):
        assert self.tx is not None
        session = self.session
        del _SESSION_STATE[id(self.session)]
        self.tx = self.session = None
        self.state = final_state
        session.close()
        return

    def abort(self, trans):
        if self.tx is not None:
            self._finish('aborted')
        return

    def tpc_begin(self, trans):
        self.session.flush()

    def commit(self, trans):
        status = _SESSION_STATE[id(self.session)]
        if status is not STATUS_INVALIDATED:
            self._finish('no work')

    def tpc_vote(self, trans):
        if self.tx is not None:
            self.tx.commit()
            self._finish('committed')
        return

    def tpc_finish(self, trans):
        pass

    def tpc_abort(self, trans):
        assert self.state is not 'committed'

    def sortKey(self):
        return '~sqlalchemy:%d' % id(self.tx)

    @property
    def savepoint(self):
        """Savepoints are only supported when all connections support subtransactions
        """
        if set(engine.url.drivername for engine in self.session.transaction._connections.keys() if isinstance(engine, Engine)).intersection(NO_SAVEPOINT_SUPPORT):
            raise AttributeError('savepoint')
        return self._savepoint

    def _savepoint(self):
        return SessionSavepoint(self.session)

    def should_retry(self, error):
        if isinstance(error, ConcurrentModificationError):
            return True
        else:
            if isinstance(error, DBAPIError):
                orig = error.orig
                for error_type, test in _retryable_errors:
                    if isinstance(orig, error_type):
                        if test is None:
                            return True
                        if test(orig):
                            return True

            return


class TwoPhaseSessionDataManager(SessionDataManager):
    """Two phase variant.
    """

    def tpc_vote(self, trans):
        if self.tx is not None:
            self.tx.prepare()
            self.state = 'voted'
        return

    def tpc_finish(self, trans):
        if self.tx is not None:
            self.tx.commit()
            self._finish('committed')
        return

    def tpc_abort(self, trans):
        if self.tx is not None:
            self.tx.rollback()
            self._finish('aborted commit')
        return

    def sortKey(self):
        return 'sqlalchemy.twophase:%d' % id(self.tx)


class SessionSavepoint:
    implements(IDataManagerSavepoint)

    def __init__(self, session):
        self.session = session
        self.transaction = session.begin_nested()

    def rollback(self):
        self.transaction.rollback()


def join_transaction(session, initial_state=STATUS_ACTIVE, transaction_manager=zope_transaction.manager):
    """Join a session to a transaction using the appropriate datamanager.
       
    It is safe to call this multiple times, if the session is already joined
    then it just returns.
       
    `initial_state` is either STATUS_ACTIVE, STATUS_INVALIDATED or STATUS_READONLY
    
    If using the default initial status of STATUS_ACTIVE, you must ensure that
    mark_changed(session) is called when data is written to the database.
    
    The ZopeTransactionExtension SessionExtension can be used to ensure that this is
    called automatically after session write operations.
    """
    if _SESSION_STATE.get(id(session), None) is None:
        if session.twophase:
            DataManager = TwoPhaseSessionDataManager
        else:
            DataManager = SessionDataManager
        transaction_manager.get().join(DataManager(session, initial_state, transaction_manager))
    return


def mark_changed(session, transaction_manager=zope_transaction.manager):
    """Mark a session as needing to be committed
    """
    session_id = id(session)
    assert _SESSION_STATE.get(session_id, None) is not STATUS_READONLY, 'Session already registered as read only'
    join_transaction(session, STATUS_CHANGED, transaction_manager)
    _SESSION_STATE[session_id] = STATUS_CHANGED
    return


class ZopeTransactionExtension(SessionExtension):
    """Record that a flush has occurred on a session's connection. This allows
    the DataManager to rollback rather than commit on read only transactions.
    """

    def __init__(self, initial_state=STATUS_ACTIVE, transaction_manager=zope_transaction.manager):
        if initial_state == 'invalidated':
            initial_state = STATUS_CHANGED
        SessionExtension.__init__(self)
        self.initial_state = initial_state
        self.transaction_manager = transaction_manager

    def after_begin(self, session, transaction, connection):
        join_transaction(session, self.initial_state, self.transaction_manager)

    def after_attach(self, session, instance):
        join_transaction(session, self.initial_state, self.transaction_manager)

    def after_flush(self, session, flush_context):
        mark_changed(session, self.transaction_manager)

    def after_bulk_update(self, session, query, query_context, result):
        mark_changed(session, self.transaction_manager)

    def after_bulk_delete(self, session, query, query_context, result):
        mark_changed(session, self.transaction_manager)

    def before_commit(self, session):
        assert self.transaction_manager.get().status == ZopeStatus.COMMITTING, 'Transaction must be committed using the transaction manager'