# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/flush.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import sys
from importlib import import_module
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.core.management.sql import emit_post_migrate_signal, sql_flush
from django.db import DEFAULT_DB_ALIAS, connections, transaction
from django.utils import six
from django.utils.six.moves import input

class Command(BaseCommand):
    help = b'Removes ALL DATA from the database, including data added during migrations. Does not achieve a "fresh install" state.'

    def add_arguments(self, parser):
        parser.add_argument(b'--noinput', b'--no-input', action=b'store_false', dest=b'interactive', default=True, help=b'Tells Django to NOT prompt the user for input of any kind.')
        parser.add_argument(b'--database', action=b'store', dest=b'database', default=DEFAULT_DB_ALIAS, help=b'Nominates a database to flush. Defaults to the "default" database.')

    def handle(self, **options):
        database = options[b'database']
        connection = connections[database]
        verbosity = options[b'verbosity']
        interactive = options[b'interactive']
        reset_sequences = options.get(b'reset_sequences', True)
        allow_cascade = options.get(b'allow_cascade', False)
        inhibit_post_migrate = options.get(b'inhibit_post_migrate', False)
        self.style = no_style()
        for app_config in apps.get_app_configs():
            try:
                import_module(b'.management', app_config.name)
            except ImportError:
                pass

        sql_list = sql_flush(self.style, connection, only_django=True, reset_sequences=reset_sequences, allow_cascade=allow_cascade)
        if interactive:
            confirm = input(b"You have requested a flush of the database.\nThis will IRREVERSIBLY DESTROY all data currently in the %r database,\nand return each table to an empty state.\nAre you sure you want to do this?\n\n    Type 'yes' to continue, or 'no' to cancel: " % connection.settings_dict[b'NAME'])
        else:
            confirm = b'yes'
        if confirm == b'yes':
            try:
                with transaction.atomic(using=database, savepoint=connection.features.can_rollback_ddl):
                    with connection.cursor() as (cursor):
                        for sql in sql_list:
                            cursor.execute(sql)

            except Exception as e:
                new_msg = b"Database %s couldn't be flushed. Possible reasons:\n  * The database isn't running or isn't configured correctly.\n  * At least one of the expected database tables doesn't exist.\n  * The SQL was invalid.\nHint: Look at the output of 'django-admin sqlflush'. That's the SQL this command wasn't able to run.\nThe full error: %s" % (
                 connection.settings_dict[b'NAME'], e)
                six.reraise(CommandError, CommandError(new_msg), sys.exc_info()[2])

            if sql_list and not inhibit_post_migrate:
                emit_post_migrate_signal(verbosity, interactive, database)
        else:
            self.stdout.write(b'Flush cancelled.\n')