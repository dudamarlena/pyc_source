# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/waitressd/management/commands/waitress.py
# Compiled at: 2018-12-06 15:43:57
# Size of source mod 2**32: 464 bytes
import signal
from django.conf import settings
from django.core.management.base import BaseCommand
from waitress import serve

class Command(BaseCommand):
    help = 'Run waitress'

    def handle(self, *args, **options):
        from feedsubs.wsgi import application

        def handle_sigterm(*args):
            raise KeyboardInterrupt()

        signal.signal(signal.SIGTERM, handle_sigterm)
        serve(application, **getattr(settings, 'WAITRESS', {}))