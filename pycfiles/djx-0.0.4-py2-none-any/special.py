# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/migrations/operations/special.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.db import router
from django.utils import six
from .base import Operation

class SeparateDatabaseAndState(Operation):
    """
    Takes two lists of operations - ones that will be used for the database,
    and ones that will be used for the state change. This allows operations
    that don't support state change to have it applied, or have operations
    that affect the state or not the database, or so on.
    """
    serialization_expand_args = [
     b'database_operations', b'state_operations']

    def __init__(self, database_operations=None, state_operations=None):
        self.database_operations = database_operations or []
        self.state_operations = state_operations or []

    def deconstruct(self):
        kwargs = {}
        if self.database_operations:
            kwargs[b'database_operations'] = self.database_operations
        if self.state_operations:
            kwargs[b'state_operations'] = self.state_operations
        return (self.__class__.__name__, [],
         kwargs)

    def state_forwards(self, app_label, state):
        for state_operation in self.state_operations:
            state_operation.state_forwards(app_label, state)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        for database_operation in self.database_operations:
            to_state = from_state.clone()
            database_operation.state_forwards(app_label, to_state)
            database_operation.database_forwards(app_label, schema_editor, from_state, to_state)
            from_state = to_state

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        to_states = {}
        for dbop in self.database_operations:
            to_states[dbop] = to_state
            to_state = to_state.clone()
            dbop.state_forwards(app_label, to_state)

        for database_operation in reversed(self.database_operations):
            from_state = to_state
            to_state = to_states[database_operation]
            database_operation.database_backwards(app_label, schema_editor, from_state, to_state)

    def describe(self):
        return b'Custom state/database change combination'


class RunSQL(Operation):
    """
    Runs some raw SQL. A reverse SQL statement may be provided.

    Also accepts a list of operations that represent the state change effected
    by this SQL change, in case it's custom column/table creation/deletion.
    """
    noop = b''

    def __init__(self, sql, reverse_sql=None, state_operations=None, hints=None, elidable=False):
        self.sql = sql
        self.reverse_sql = reverse_sql
        self.state_operations = state_operations or []
        self.hints = hints or {}
        self.elidable = elidable

    def deconstruct(self):
        kwargs = {b'sql': self.sql}
        if self.reverse_sql is not None:
            kwargs[b'reverse_sql'] = self.reverse_sql
        if self.state_operations:
            kwargs[b'state_operations'] = self.state_operations
        if self.hints:
            kwargs[b'hints'] = self.hints
        return (self.__class__.__name__, [],
         kwargs)

    @property
    def reversible(self):
        return self.reverse_sql is not None

    def state_forwards(self, app_label, state):
        for state_operation in self.state_operations:
            state_operation.state_forwards(app_label, state)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if router.allow_migrate(schema_editor.connection.alias, app_label, **self.hints):
            self._run_sql(schema_editor, self.sql)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        if self.reverse_sql is None:
            raise NotImplementedError(b'You cannot reverse this operation')
        if router.allow_migrate(schema_editor.connection.alias, app_label, **self.hints):
            self._run_sql(schema_editor, self.reverse_sql)
        return

    def describe(self):
        return b'Raw SQL operation'

    def _run_sql(self, schema_editor, sqls):
        if isinstance(sqls, (list, tuple)):
            for sql in sqls:
                params = None
                if isinstance(sql, (list, tuple)):
                    elements = len(sql)
                    if elements == 2:
                        sql, params = sql
                    else:
                        raise ValueError(b'Expected a 2-tuple but got %d' % elements)
                schema_editor.execute(sql, params=params)

        elif sqls != RunSQL.noop:
            statements = schema_editor.connection.ops.prepare_sql_script(sqls)
            for statement in statements:
                schema_editor.execute(statement, params=None)

        return


class RunPython(Operation):
    """
    Runs Python code in a context suitable for doing versioned ORM operations.
    """
    reduces_to_sql = False

    def __init__(self, code, reverse_code=None, atomic=None, hints=None, elidable=False):
        self.atomic = atomic
        if not callable(code):
            raise ValueError(b'RunPython must be supplied with a callable')
        self.code = code
        if reverse_code is None:
            self.reverse_code = None
        else:
            if not callable(reverse_code):
                raise ValueError(b'RunPython must be supplied with callable arguments')
            self.reverse_code = reverse_code
        self.hints = hints or {}
        self.elidable = elidable
        return

    def deconstruct(self):
        kwargs = {b'code': self.code}
        if self.reverse_code is not None:
            kwargs[b'reverse_code'] = self.reverse_code
        if self.atomic is not None:
            kwargs[b'atomic'] = self.atomic
        if self.hints:
            kwargs[b'hints'] = self.hints
        return (self.__class__.__name__, [],
         kwargs)

    @property
    def reversible(self):
        return self.reverse_code is not None

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        from_state.clear_delayed_apps_cache()
        if router.allow_migrate(schema_editor.connection.alias, app_label, **self.hints):
            self.code(from_state.apps, schema_editor)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        if self.reverse_code is None:
            raise NotImplementedError(b'You cannot reverse this operation')
        if router.allow_migrate(schema_editor.connection.alias, app_label, **self.hints):
            self.reverse_code(from_state.apps, schema_editor)
        return

    def describe(self):
        return b'Raw Python operation'

    @staticmethod
    def noop(apps, schema_editor):
        return


if six.PY2:

    def noop(apps, schema_editor):
        return


    RunPython.noop = staticmethod(noop)