# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/incoan/codenerix/management/commands/clean.py
# Compiled at: 2018-01-17 09:45:18
# Size of source mod 2**32: 1630 bytes
import os
try:
    from subprocess import getstatusoutput
    pythoncmd = 'python3'
except Exception:
    from commands import getstatusoutput
    pythoncmd = 'python2'

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from codenerix.lib.debugger import Debugger

class Command(BaseCommand, Debugger):
    help = 'Remove *.pyc files'

    def handle(self, *args, **options):
        self.set_name('CODENERIX')
        self.set_debug()
        appname = settings.ROOT_URLCONF.split('.')[0]
        basedir = settings.BASE_DIR
        appdir = os.path.abspath('{}/{}'.format(basedir, appname))
        status, output = getstatusoutput("find {}/ -name '*.py[c|o]' -o -name __pycache__ -exec rm -rf {{}} +".format(appdir))
        if status:
            raise CommandError(output)