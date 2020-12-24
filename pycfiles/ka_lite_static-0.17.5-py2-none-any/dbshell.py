# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/dbshell.py
# Compiled at: 2018-07-11 18:15:30
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import connections, DEFAULT_DB_ALIAS

class Command(BaseCommand):
    help = 'Runs the command-line client for specified database, or the default database if none is provided.'
    option_list = BaseCommand.option_list + (
     make_option('--database', action='store', dest='database', default=DEFAULT_DB_ALIAS, help='Nominates a database onto which to open a shell.  Defaults to the "default" database.'),)
    requires_model_validation = False

    def handle(self, **options):
        connection = connections[options.get('database')]
        try:
            connection.client.runshell()
        except OSError:
            raise CommandError('You appear not to have the %r program installed or on your path.' % connection.client.executable_name)