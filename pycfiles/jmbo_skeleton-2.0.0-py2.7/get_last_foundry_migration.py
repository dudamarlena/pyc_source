# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skeleton/management/commands/get_last_foundry_migration.py
# Compiled at: 2013-09-27 03:12:03
from django.core.management.base import BaseCommand, CommandError
from south.migration.base import Migrations

class Command(BaseCommand):

    def handle(self, *args, **options):
        migrations = Migrations('foundry')
        print migrations[(-1)].name()