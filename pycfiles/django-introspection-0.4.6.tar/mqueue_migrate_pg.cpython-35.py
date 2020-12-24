# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo52/mogo/mqueue/management/commands/mqueue_migrate_pg.py
# Compiled at: 2017-06-20 06:13:31
# Size of source mod 2**32: 860 bytes
from __future__ import print_function
import os
from django.core.management.base import BaseCommand, CommandError
from mqueue.hooks import postgresql
from mqueue.conf import HOOKS

class Command(BaseCommand):
    help = 'Migrates a postgresql database for mqueue hook'

    def handle(self, *args, **options):
        if 'postgresql' not in HOOKS:
            print('No postgresql database configured: please check HOOKS in settings')
        conf = HOOKS['postgresql']
        params = [
         '-a=' + conf['addr']]
        params.append('-du="' + conf['user'] + '"')
        params.append('-p="' + conf['password'] + '"')
        params.append('-d="' + conf['database'] + '"')
        params.append('-m')
        pth = os.path.dirname(postgresql.__file__)
        cmd = pth + '/run ' + str.join(' ', params)
        os.system(cmd)