# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/tools/management/commands/play.py
# Compiled at: 2018-10-11 14:48:56
# Size of source mod 2**32: 831 bytes
import os
from subprocess import Popen, DEVNULL
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('video', default=None)

    def handle(self, *args, **options):
        vlc = None
        if os.path.exists('/Applications/VLC.app/Contents/MacOS/VLC'):
            vlc = '/Applications/VLC.app/Contents/MacOS/VLC'
        else:
            if os.path.exists('/usr/bin/vlc'):
                vlc = '/usr/bin/vlc'
            elif vlc:
                video = options.get('video')
                cmd = '{} --play-and-exit --fullscreen {}'.format(vlc, video)
                Popen((cmd.split()), stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
            else:
                print('VLC is not installed!')