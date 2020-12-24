# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/migrations/migration.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.db.transaction import atomic
from django.utils.encoding import python_2_unicode_compatible
from .exceptions import IrreversibleError

@python_2_unicode_compatible
class Migration(object):
    """
    The base class for all migrations.

    Migration files will import this from django.db.migrations.Migration
    and subclass it as a class called Migration. It will have one or more
    of the following attributes:

     - operations: A list of Operation instances, probably from django.db.migrations.operations
     - dependencies: A list of tuples of (app_path, migration_name)
     - run_before: A list of tuples of (app_path, migration_name)
     - replaces: A list of migration_names

    Note that all migrations come out of migrations and into the Loader or
    Graph as instances, having been initialized with their app label and name.
    """
    operations = []
    dependencies = []
    run_before = []
    replaces = []
    initial = None
    atomic = True

    def __init__(self, name, app_label):
        self.name = name
        self.app_label = app_label
        self.operations = list(self.__class__.operations)
        self.dependencies = list(self.__class__.dependencies)
        self.run_before = list(self.__class__.run_before)
        self.replaces = list(self.__class__.replaces)

    def __eq__(self, other):
        if not isinstance(other, Migration):
            return False
        return self.name == other.name and self.app_label == other.app_label

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return b'<Migration %s.%s>' % (self.app_label, self.name)

    def __str__(self):
        return b'%s.%s' % (self.app_label, self.name)

    def __hash__(self):
        return hash(b'%s.%s' % (self.app_label, self.name))

    def mutate_state(self, project_state, preserve=True):
        """
        Takes a ProjectState and returns a new one with the migration's
        operations applied to it. Preserves the original object state by
        default and will return a mutated state from a copy.
        """
        new_state = project_state
        if preserve:
            new_state = project_state.clone()
        for operation in self.operations:
            operation.state_forwards(self.app_label, new_state)

        return new_state

    def apply(self, project_state, schema_editor, collect_sql=False):
        """
        Takes a project_state representing all migrations prior to this one
        and a schema_editor for a live database and applies the migration
        in a forwards order.

        Returns the resulting project state for efficient re-use by following
        Migrations.
        """
        for operation in self.operations:
            if collect_sql:
                schema_editor.collected_sql.append(b'--')
                if not operation.reduces_to_sql:
                    schema_editor.collected_sql.append(b'-- MIGRATION NOW PERFORMS OPERATION THAT CANNOT BE WRITTEN AS SQL:')
                schema_editor.collected_sql.append(b'-- %s' % operation.describe())
                schema_editor.collected_sql.append(b'--')
                if not operation.reduces_to_sql:
                    continue
            old_state = project_state.clone()
            operation.state_forwards(self.app_label, project_state)
            atomic_operation = operation.atomic or self.atomic and operation.atomic is not False
            if not schema_editor.atomic_migration and atomic_operation:
                with atomic(schema_editor.connection.alias):
                    operation.database_forwards(self.app_label, schema_editor, old_state, project_state)
            else:
                operation.database_forwards(self.app_label, schema_editor, old_state, project_state)

        return project_state

    def unapply(self, project_state, schema_editor, collect_sql=False):
        """
        Takes a project_state representing all migrations prior to this one
        and a schema_editor for a live database and applies the migration
        in a reverse order.

        The backwards migration process consists of two phases:

        1. The intermediate states from right before the first until right
           after the last operation inside this migration are preserved.
        2. The operations are applied in reverse order using the states
           recorded in step 1.
        """
        to_run = []
        new_state = project_state
        for operation in self.operations:
            if not operation.reversible:
                raise IrreversibleError(b'Operation %s in %s is not reversible' % (operation, self))
            new_state = new_state.clone()
            old_state = new_state.clone()
            operation.state_forwards(self.app_label, new_state)
            to_run.insert(0, (operation, old_state, new_state))

        for operation, to_state, from_state in to_run:
            if collect_sql:
                schema_editor.collected_sql.append(b'--')
                if not operation.reduces_to_sql:
                    schema_editor.collected_sql.append(b'-- MIGRATION NOW PERFORMS OPERATION THAT CANNOT BE WRITTEN AS SQL:')
                schema_editor.collected_sql.append(b'-- %s' % operation.describe())
                schema_editor.collected_sql.append(b'--')
                if not operation.reduces_to_sql:
                    continue
            if not schema_editor.connection.features.can_rollback_ddl and operation.atomic:
                with atomic(schema_editor.connection.alias):
                    operation.database_backwards(self.app_label, schema_editor, from_state, to_state)
            else:
                operation.database_backwards(self.app_label, schema_editor, from_state, to_state)

        return project_state


class SwappableTuple(tuple):
    """
    Subclass of tuple so Django can tell this was originally a swappable
    dependency when it reads the migration file.
    """

    def __new__(cls, value, setting):
        self = tuple.__new__(cls, value)
        self.setting = setting
        return self


def swappable_dependency(value):
    """
    Turns a setting value into a dependency.
    """
    return SwappableTuple((value.split(b'.', 1)[0], b'__first__'), value)