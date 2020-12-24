# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/dbshell.py
# Compiled at: 2019-02-14 00:35:17
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections

class Command(BaseCommand):
    help = 'Runs the command-line client for specified database, or the default database if none is provided.'
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--database', action='store', dest='database', default=DEFAULT_DB_ALIAS, help='Nominates a database onto which to open a shell. Defaults to the "default" database.')

    def handle(self, **options):
        connection = connections[options['database']]
        try:
            connection.client.runshell()
        except OSError:
            raise CommandError('You appear not to have the %r program installed or on your path.' % connection.client.executable_name)