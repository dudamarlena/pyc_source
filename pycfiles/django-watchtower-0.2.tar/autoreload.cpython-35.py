# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo54/mogo/autoreload/management/commands/autoreload.py
# Compiled at: 2017-07-01 14:54:00
# Size of source mod 2**32: 970 bytes
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
import subprocess
from django.conf import settings
from instant.conf import CENTRIFUGO_HOST, CENTRIFUGO_PORT, SECRET_KEY
from autoreload.conf import CHANNEL, WL
addr = CENTRIFUGO_HOST.replace('http://', '') + ':' + str(CENTRIFUGO_PORT)

class Command(BaseCommand):
    help = 'Start autoreload daemon'

    def handle(self, *args, **options):
        print('Watching file changes ...')
        pth = settings.BASE_DIR + '/autoreload/watcher/'
        c = pth + 'watcher'
        cmd = [c, '-path', settings.BASE_DIR, '-w', WL, '-addr', addr, '-key', SECRET_KEY, '-chan', CHANNEL]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in p.stdout:
            print(str(line))

        p.wait()
        print(p.returncode)