# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Projects/personal/test_mock_server/rest_mock_server/management/commands/startmockserver.py
# Compiled at: 2018-02-25 21:29:16
# Size of source mod 2**32: 648 bytes
from django.core.management.base import BaseCommand
from rest_mock_server.builder import build

class Command(BaseCommand):
    help = 'Starts mock server (generates file if necessary)'

    def add_arguments(self, parser):
        parser.add_argument('--file',
          dest='server_file',
          help='Express server file path')

    def handle(self, *args, **options):
        server_file = options.get('server_file')
        express = build()
        if server_file is None:
            server_file = 'index.js'
        express.generate(file_path=server_file)
        express.start_server(file_path=server_file)