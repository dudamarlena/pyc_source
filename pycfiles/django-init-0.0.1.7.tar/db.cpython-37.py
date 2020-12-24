# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/projects/django-init/django_init/management/commands/db.py
# Compiled at: 2020-01-15 01:28:34
# Size of source mod 2**32: 1486 bytes
from django.core.management.base import BaseCommand
from django_init.db.mysql import DatabaseMySQL
from django_init.db.postgresql import DatabasePostgreSQL

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('command_name', help='Name of command')
        parser.add_argument('database_name', help='Name of database')
        parser.add_argument('-e', '--engine', choices=['mysql', 'postgres'], required=True,
          help='Databases: mysql, postgres')

    def handle(self, *args, **options):
        database_name = options.get('database_name')
        engine = options.get('engine')
        if database_name:
            if engine == 'mysql':
                config = {'host':'localhost',  'user':'root', 
                 'passwd':'root'}
                bd = DatabaseMySQL(config)
                bd.create_db(database_name)
                bd.show_dbs()
                bd.drop_db(database_name)
            if engine == 'postgres':
                config = {'dbname':'postgres',  'user':'root', 
                 'password':'root', 
                 'host':'localhost'}
                bd = DatabasePostgreSQL(config)
                bd.create_db(database_name)
                bd.show_dbs()
                bd.drop_db(database_name)