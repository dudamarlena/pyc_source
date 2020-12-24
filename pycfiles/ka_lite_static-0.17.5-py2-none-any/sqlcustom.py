# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/sqlcustom.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
from optparse import make_option
from django.core.management.base import AppCommand
from django.core.management.sql import sql_custom
from django.db import connections, DEFAULT_DB_ALIAS

class Command(AppCommand):
    help = b'Prints the custom table modifying SQL statements for the given app name(s).'
    option_list = AppCommand.option_list + (
     make_option(b'--database', action=b'store', dest=b'database', default=DEFAULT_DB_ALIAS, help=b'Nominates a database to print the SQL for.  Defaults to the "default" database.'),)
    output_transaction = True

    def handle_app(self, app, **options):
        return (b'\n').join(sql_custom(app, self.style, connections[options.get(b'database')]))