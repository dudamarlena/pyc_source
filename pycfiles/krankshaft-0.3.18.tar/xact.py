# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/daniel_lamotte/sandbox/krankshaft/krankshaft/compat/xact.py
# Compiled at: 2013-11-12 15:39:53
""" This code provides a decorator / context manager for transaction management in
    Django on PostgreSQL.  It is intended as a replacement for the existing Django
    commit_on_success() function, and provides some nice features:
    
    * Nested transactions: The top-level transaction will be a BEGIN/COMMIT/ROLLBACK
      block; inner "transactions" are implemented as savepoints.
    * Commits even if is_dirty is False, eliminating the mistake of forgetting to set
      the dirty flag when doing database-modifying raw SQL.
    * Better interaction with pgPool II, if you're using it.
    * A workaround for a subtle but nasty bug in Django's transaction management.
    
    For full details, check the README.md file.
"""
from functools import wraps
import psycopg2.extensions
from django.db import transaction, DEFAULT_DB_ALIAS, connections

class Rollback(Exception):
    """ This class provides a standard exception that can be thrown to handle a
        rollback condition.  If Xact receives an exception of this class (or
        a subclass), it swallows it and continues exception, rather than
        re-raising the exception.
    """
    pass


class _Transaction(object):
    """ This class manages a particular transaction or savepoint block, using context
        manager-style __enter__ and __exit__ statements.  We don't use it directly
        (for reasons noted below), but as a delegate for the _TransactionWrapper
        class.
    """

    def __init__(self, using):
        self.using = using
        self.sid = None
        return

    def __enter__(self):
        if transaction.is_managed(self.using):
            self.sid = transaction.savepoint(self.using)
        else:
            transaction.enter_transaction_management(using=self.using)
            transaction.managed(True, using=self.using)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            if self.sid is None:
                try:
                    try:
                        transaction.commit(self.using)
                    except:
                        transaction.rollback(self.using)
                        raise

                finally:
                    self._leave_transaction_management()

            else:
                try:
                    transaction.savepoint_commit(self.sid, self.using)
                except:
                    transaction.savepoint_rollback(self.sid, self.using)
                    raise

        elif self.sid is None:
            transaction.rollback(self.using)
            self._leave_transaction_management()
        else:
            transaction.savepoint_rollback(self.sid, self.using)
        if exc_type is None:
            return False
        else:
            return issubclass(exc_type, Rollback)
            return

    def _leave_transaction_management(self):
        transaction.leave_transaction_management(using=self.using)
        if not connections[self.using].is_managed() and connections[self.using].features.uses_autocommit:
            connections[self.using]._set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)


class _TransactionWrapper:
    """ This class wraps the above _Transaction class.  We do this to allow reentrancy
        and thread-safety.  When being used as a decorator, only one _TransactionWrapper
        object is created per function being wrapped, and thus we can't store the state
        of the tranasction here (because multiple concurrent calls in the same address
        space to the same function would cause the state to be crunched), so delegate
        that to a _Transaction object that is created at the appropriate time.
        
        The "appropriate time" is two places: If the _TransactionWrapper is being used
        as a context manager, it's when the __enter__ function is called; if it is being
        used as a decorator, it's when the decorated function is about to be called
        (see the `inner` function below in __call__).
        
        The __enter__ and __exit__ functions on _TransactionWrapper are only called
        if we're using xact() as a context manager; if we're using it as a decorator,
        they're skipped and self.transaction is always None. Similarly, __call__ is
        not used if this is a context manager usage. This is not super-elegant, but
        it's the only way I've found to allow xact() to be used as both a context
        manager and a decorator using the same syntax.
    """

    def __init__(self, using):
        self.using = using
        self.transaction = None
        return

    def __enter__(self):
        if self.transaction is None:
            self.transaction = _Transaction(self.using)
        return self.transaction.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.transaction.__exit__(exc_type, exc_value, traceback)

    def __call__(self, func):

        @wraps(func)
        def inner(*args, **kwargs):
            with _Transaction(self.using):
                return func(*args, **kwargs)

        return inner


def xact(using=None):
    if using is None:
        using = DEFAULT_DB_ALIAS
    if callable(using):
        return _TransactionWrapper(DEFAULT_DB_ALIAS)(using)
    else:
        return _TransactionWrapper(using)
        return