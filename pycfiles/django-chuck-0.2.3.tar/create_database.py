# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/commands/create_database.py
# Compiled at: 2012-06-01 04:12:37
from django_chuck.commands.base import BaseCommand
from django_chuck.commands import sync_database, migrate_database

class Command(BaseCommand):
    help = 'Sync and migrate database'

    def __init__(self):
        super(Command, self).__init__()
        self.opts.append(('extra_syncdb_options',
         {'help': 'Options to append at syncdb command', 
            'nargs': '?'}))

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)
        sync_database.Command().handle(args, cfg)
        if 'south' in self.get_install_modules():
            migrate_database.Command().handle(args, cfg)