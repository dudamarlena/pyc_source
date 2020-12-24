# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/youngrok/workspace/djangox/djangox/apps/djangoxtools/management/commands/importapp.py
# Compiled at: 2015-10-08 13:17:18
# Size of source mod 2**32: 276 bytes
from django.core.management.base import BaseCommand
from djangox.apps import import_app

class Command(BaseCommand):
    args = 'package name of app'
    help = 'copy specified app files into this project.'

    def handle(self, *args, **options):
        import_app(args[0])