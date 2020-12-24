# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/sqlsequencereset.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.core.management.base import AppCommand
from django.db import DEFAULT_DB_ALIAS, connections

class Command(AppCommand):
    help = b'Prints the SQL statements for resetting sequences for the given app name(s).'
    output_transaction = True

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(b'--database', default=DEFAULT_DB_ALIAS, help=b'Nominates a database to print the SQL for. Defaults to the "default" database.')

    def handle_app_config(self, app_config, **options):
        if app_config.models_module is None:
            return
        else:
            connection = connections[options[b'database']]
            models = app_config.get_models(include_auto_created=True)
            statements = connection.ops.sequence_reset_sql(self.style, models)
            return (b'\n').join(statements)