# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo64/mogo/dex/management/commands/testcom.py
# Compiled at: 2017-08-04 14:58:50
# Size of source mod 2**32: 643 bytes
from __future__ import print_function
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from instant.producers import publish

class Command(BaseCommand):
    help = 'Test'

    def handle(self, *args, **options):
        path = settings.BASE_DIR + '/static'
        cmd = ['df', '-h', path]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in p.stdout:
            msg = line.decode('UTF-8')
            publish(message=msg, channel='$mogo_command')
            if settings.DEBUG == True:
                print(line)

        p.wait()
        print(p.returncode)