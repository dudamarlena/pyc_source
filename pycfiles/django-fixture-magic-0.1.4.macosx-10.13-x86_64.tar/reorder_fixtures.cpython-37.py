# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/fixture_magic/management/commands/reorder_fixtures.py
# Compiled at: 2018-10-19 13:50:29
# Size of source mod 2**32: 651 bytes
from __future__ import print_function
try:
    import json
except ImportError:
    import django.utils as json

from django.core.management.base import BaseCommand
from fixture_magic.utils import reorder_json

class Command(BaseCommand):
    help = 'Reorder fixtures so some objects come before others.'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='models', nargs='+', help='One or more models.')

    def handle(self, fixture, *models, **options):
        output = reorder_json(json.loads(open(fixture).read()), models)
        print(json.dumps(output, indent=4))