# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/sqlmigrate.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import AmbiguityError

class Command(BaseCommand):
    help = b'Prints the SQL statements for the named migration.'
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument(b'app_label', help=b'App label of the application containing the migration.')
        parser.add_argument(b'migration_name', help=b'Migration name to print the SQL for.')
        parser.add_argument(b'--database', default=DEFAULT_DB_ALIAS, help=b'Nominates a database to create SQL for. Defaults to the "default" database.')
        parser.add_argument(b'--backwards', action=b'store_true', dest=b'backwards', default=False, help=b'Creates SQL to unapply the migration, rather than to apply it')

    def execute(self, *args, **options):
        options[b'no_color'] = True
        return super(Command, self).execute(*args, **options)

    def handle(self, *args, **options):
        connection = connections[options[b'database']]
        executor = MigrationExecutor(connection)
        app_label, migration_name = options[b'app_label'], options[b'migration_name']
        if app_label not in executor.loader.migrated_apps:
            raise CommandError(b"App '%s' does not have migrations" % app_label)
        try:
            migration = executor.loader.get_migration_by_prefix(app_label, migration_name)
        except AmbiguityError:
            raise CommandError(b"More than one migration matches '%s' in app '%s'. Please be more specific." % (
             migration_name, app_label))
        except KeyError:
            raise CommandError(b"Cannot find a migration matching '%s' from app '%s'. Is it in INSTALLED_APPS?" % (
             migration_name, app_label))

        targets = [
         (
          app_label, migration.name)]
        self.output_transaction = migration.atomic
        plan = [
         (
          executor.loader.graph.nodes[targets[0]], options[b'backwards'])]
        sql_statements = executor.collect_sql(plan)
        return (b'\n').join(sql_statements)