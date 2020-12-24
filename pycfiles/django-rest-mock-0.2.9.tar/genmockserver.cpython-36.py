# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Projects/personal/test_mock_server/rest_mock_server/management/commands/genmockserver.py
# Compiled at: 2018-02-23 03:45:14
# Size of source mod 2**32: 811 bytes
from django.core.management.base import BaseCommand
from rest_mock_server.builder import build

class Command(BaseCommand):
    help = 'Generates an Express server file for mocking endpoint responses'

    def add_arguments(self, parser):
        parser.add_argument('--output',
          dest='output_file',
          help='Custom output file name')
        parser.add_argument('--port',
          dest='port',
          help='Custom port to be exposed')

    def handle(self, *args, **options):
        output = options.get('output_file')
        if output is None:
            output = 'index.js'
        port = options.get('port')
        if port is None:
            port = 8000
        express = build(port)
        express.generate(file_path=output)