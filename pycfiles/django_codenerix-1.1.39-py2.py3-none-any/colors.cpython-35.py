# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/searchwally/codenerix/management/commands/colors.py
# Compiled at: 2017-11-28 06:03:36
# Size of source mod 2**32: 2163 bytes
import os
try:
    from subprocess import getstatusoutput
    pythoncmd = 'python3'
except:
    from commands import getstatusoutput
    pythoncmd = 'python2'

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from codenerix.lib.debugger import Debugger
from codenerix.lib.colors import colors

class Command(BaseCommand, Debugger):
    help = 'Show colors for Debugger'

    def handle(self, *args, **options):
        self.set_name('CODENERIX')
        self.set_debug()
        keys = []
        for key in colors.keys():
            keys.append((colors[key][0], colors[key][1], key))

        keys.sort()
        for color in keys:
            simplebit, subcolor = colors[color[2]]
            print('{0:1d}:{1:02d} - \x1b[{2:1d};{3:02d}m{4:<14s}\x1b[1;00m{5:<s}'.format(simplebit, subcolor, simplebit, subcolor, color[2], color[2]))
            appname = settings.ROOT_URLCONF.split('.')[0]
            basedir = settings.BASE_DIR
            appdir = os.path.abspath('{}/{}'.format(basedir, appname))
            status, output = getstatusoutput("find {}/ -type f -name '*.pyc' -delete".format(appdir))
            if status:
                raise CommandError(output)