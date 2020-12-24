# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/youngrok/workspace/djangox/djangox/apps/tools/management/commands/setupdeploy.py
# Compiled at: 2015-10-21 03:17:36
# Size of source mod 2**32: 254 bytes
from django.core.management.base import BaseCommand
from djangox.apps import import_app

class Command(BaseCommand):
    help = 'setup deploy environment'

    def handle(self, *args, **options):
        import_app('djangox.deploy', edit_settings=False)