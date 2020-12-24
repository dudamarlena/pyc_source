# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/transaction.py
# Compiled at: 2019-02-14 00:35:17
from django.db import DEFAULT_DB_ALIAS, DatabaseError, Error, ProgrammingError, connections
from django.utils.decorators import ContextDecorator

class TransactionManagementError(ProgrammingError):
    """
    This exception is thrown when transaction management is used improperly.
    """
    pass


def get_connection(using=None):
    """
    Get a database connection by name, or the default database connection
    if no name is provided. This is a private API.
    """
    if using is None:
        using = DEFAULT_DB_ALIAS
    return connections[using]


def get_autocommit(using=None):
    """
    Get the autocommit status of the connection.
    """
    return get_connection(using).get_autocommit()


def set_autocommit(autocommit, using=None):
    """
    Set the autocommit status of the connection.
    """
    return get_connection(using).set_autocommit(autocommit)


def commit(using=None):
    """
    Commits a transaction.
    """
    get_connection(using).commit()


def rollback(using=None):
    """
    Rolls back a transaction.
    """
    get_connection(using).rollback()


def savepoint(using=None):
    """
    Creates a savepoint (if supported and required by the backend) inside the
    current transaction. Returns an identifier for the savepoint that will be
    used for the subsequent rollback or commit.
    """
    return get_connection(using).savepoint()


def savepoint_rollback(sid, using=None):
    """
    Rolls back the most recent savepoint (if one exists). Does nothing if
    savepoints are not supported.
    """
    get_connection(using).savepoint_rollback(sid)


def savepoint_commit(sid, using=None):
    """
    Commits the most recent savepoint (if one exists). Does nothing if
    savepoints are not supported.
    """
    get_connection(using).savepoint_commit(sid)


def clean_savepoints(using=None):
    """
    Resets the counter used to generate unique savepoint ids in this thread.
    """
    get_connection(using).clean_savepoints()


def get_rollback(using=None):
    """
    Gets the "needs rollback" flag -- for *advanced use* only.
    """
    return get_connection(using).get_rollback()


def set_rollback(rollback, using=None):
    """
    Sets or unsets the "needs rollback" flag -- for *advanced use* only.

    When `rollback` is `True`, it triggers a rollback when exiting the
    innermost enclosing atomic block that has `savepoint=True` (that's the
    default). Use this to force a rollback without raising an exception.

    When `rollback` is `False`, it prevents such a rollback. Use this only
    after rolling back to a known-good state! Otherwise, you break the atomic
    block and data corruption may occur.
    """
    return get_connection(using).set_rollback(rollback)


def on_commit(func, using=None):
    """
    Register `func` to be called when the current transaction is committed.
    If the current transaction is rolled back, `func` will not be called.
    """
    get_connection(using).on_commit(func)


class Atomic(ContextDecorator):
    """
    This class guarantees the atomic execution of a given block.

    An instance can be used either as a decorator or as a context manager.

    When it's used as a decorator, __call__ wraps the execution of the
    decorated function in the instance itself, used as a context manager.

    When it's used as a context manager, __enter__ creates a transaction or a
    savepoint, depending on whether a transaction is already in progress, and
    __exit__ commits the transaction or releases the savepoint on normal exit,
    and rolls back the transaction or to the savepoint on exceptions.

    It's possible to disable the creation of savepoints if the goal is to
    ensure that some code runs within a transaction without creating overhead.

    A stack of savepoints identifiers is maintained as an attribute of the
    connection. None denotes the absence of a savepoint.

    This allows reentrancy even if the same AtomicWrapper is reused. For
    example, it's possible to define `oa = atomic('other')` and use `@oa` or
    `with oa:` multiple times.

    Since database connections are thread-local, this is thread-safe.

    This is a private API.
    """

    def __init__(self, using, savepoint):
        self.using = using
        self.savepoint = savepoint

    def __enter__(self):
        connection = get_connection(self.using)
        if not connection.in_atomic_block:
            connection.commit_on_exit = True
            connection.needs_rollback = False
            if not connection.get_autocommit():
                if connection.features.autocommits_when_autocommit_is_off:
                    raise TransactionManagementError("Your database backend doesn't behave properly when autocommit is off. Turn it on before using 'atomic'.")
                connection.in_atomic_block = True
                connection.commit_on_exit = False
        if connection.in_atomic_block:
            if self.savepoint and not connection.needs_rollback:
                sid = connection.savepoint()
                connection.savepoint_ids.append(sid)
            else:
                connection.savepoint_ids.append(None)
        else:
            connection.set_autocommit(False, force_begin_transaction_with_broken_autocommit=True)
            connection.in_atomic_block = True
        return

    def __exit__(self, exc_type, exc_value, traceback):
        connection = get_connection(self.using)
        if connection.savepoint_ids:
            sid = connection.savepoint_ids.pop()
        else:
            connection.in_atomic_block = False
        try:
            if connection.closed_in_transaction:
                pass
            elif exc_type is None and not connection.needs_rollback:
                if connection.in_atomic_block:
                    if sid is not None:
                        try:
                            connection.savepoint_commit(sid)
                        except DatabaseError:
                            try:
                                connection.savepoint_rollback(sid)
                                connection.savepoint_commit(sid)
                            except Error:
                                connection.needs_rollback = True

                            raise

                else:
                    try:
                        connection.commit()
                    except DatabaseError:
                        try:
                            connection.rollback()
                        except Error:
                            connection.close()

                        raise

            else:
                connection.needs_rollback = False
                if connection.in_atomic_block:
                    if sid is None:
                        connection.needs_rollback = True
                    else:
                        try:
                            connection.savepoint_rollback(sid)
                            connection.savepoint_commit(sid)
                        except Error:
                            connection.needs_rollback = True

                else:
                    try:
                        connection.rollback()
                    except Error:
                        connection.close()

        finally:
            if not connection.in_atomic_block:
                if connection.closed_in_transaction:
                    connection.connection = None
                else:
                    connection.set_autocommit(True)
            elif not connection.savepoint_ids and not connection.commit_on_exit:
                if connection.closed_in_transaction:
                    connection.connection = None
                else:
                    connection.in_atomic_block = False

        return


def atomic(using=None, savepoint=True):
    if callable(using):
        return Atomic(DEFAULT_DB_ALIAS, savepoint)(using)
    else:
        return Atomic(using, savepoint)


def _non_atomic_requests(view, using):
    try:
        view._non_atomic_requests.add(using)
    except AttributeError:
        view._non_atomic_requests = {
         using}

    return view


def non_atomic_requests(using=None):
    if callable(using):
        return _non_atomic_requests(using, DEFAULT_DB_ALIAS)
    else:
        if using is None:
            using = DEFAULT_DB_ALIAS
        return lambda view: _non_atomic_requests(view, using)
        return