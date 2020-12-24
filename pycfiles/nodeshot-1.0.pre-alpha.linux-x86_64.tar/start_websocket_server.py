# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/websockets/management/commands/start_websocket_server.py
# Compiled at: 2014-05-08 06:07:40
from django.core.management.base import BaseCommand
from nodeshot.core.websockets.server import start as start_server

class Command(BaseCommand):
    help = 'Start Tornado WebSocket Server'

    def handle(self, *args, **options):
        """ Go baby go! """
        start_server()