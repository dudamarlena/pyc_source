# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/admin/management/commands/migrate.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 289 bytes
from django.core.management.commands import migrate
from djangoplus.admin.management import sync_permissions

class Command(migrate.Command):

    def handle(self, *args, **options):
        (super(Command, self).handle)(*args, **options)
        sync_permissions()