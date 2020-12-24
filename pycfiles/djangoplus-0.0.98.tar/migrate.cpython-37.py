# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/management/commands/migrate.py
# Compiled at: 2019-02-17 16:35:08
# Size of source mod 2**32: 548 bytes
from django.core.management.commands import migrate
from djangoplus.admin.management import sync_permissions

class Command(migrate.Command):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--ignore_sync_permissions', action='store_true', dest='ignore_sync_permissions')

    def handle(self, *args, **options):
        (super(Command, self).handle)(*args, **options)
        if not options.get('ignore_sync_permissions'):
            sync_permissions()