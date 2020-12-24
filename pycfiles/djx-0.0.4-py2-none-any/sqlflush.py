# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/sqlflush.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.core.management.sql import sql_flush
from django.db import DEFAULT_DB_ALIAS, connections

class Command(BaseCommand):
    help = b'Returns a list of the SQL statements required to return all tables in the database to the state they were in just after they were installed.'
    output_transaction = True

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(b'--database', default=DEFAULT_DB_ALIAS, help=b'Nominates a database to print the SQL for. Defaults to the "default" database.')

    def handle(self, **options):
        return (b'\n').join(sql_flush(self.style, connections[options[b'database']], only_django=True))