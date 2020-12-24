# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/fixture_magic/management/commands/merge_fixtures.py
# Compiled at: 2018-10-19 13:50:29
# Size of source mod 2**32: 1213 bytes
from __future__ import print_function
try:
    import json
except ImportError:
    import django.utils as json

from django.core.management.base import BaseCommand

def write_json(output):
    try:
        json.dumps([1], sort_keys=True)
    except TypeError:
        print(json.dumps(output, indent=4))
    else:
        print(json.dumps(output, sort_keys=True, indent=4))


class Command(BaseCommand):
    help = 'Merge a series of fixtures and remove duplicates.'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='files', nargs='+', help='One or more fixture.')

    def handle(self, *files, **options):
        """
        Load a bunch of json files.  Store the pk/model in a seen dictionary.
        Add all the unseen objects into output.
        """
        output = []
        seen = {}
        for f in files:
            f = open(f)
            data = json.loads(f.read())
            for obj in data:
                key = '%s|%s' % (obj['model'], obj['pk'])
                if key not in seen:
                    seen[key] = 1
                    output.append(obj)

        write_json(output)