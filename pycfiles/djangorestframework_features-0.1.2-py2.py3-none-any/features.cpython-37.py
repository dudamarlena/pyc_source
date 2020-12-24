# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dev/dev/django-rest-framework-features/rest_framework_features/management/commands/features.py
# Compiled at: 2019-10-07 03:33:53
# Size of source mod 2**32: 1317 bytes
import re
from django.core.management.base import BaseCommand, CommandError
from rest_framework_features import schema

class Command(BaseCommand):
    help = 'CLI utility for django-rest-framework-features'

    def add_arguments(self, parser):
        self.parser = parser
        parser.add_argument('--json',
          action='store_true',
          default=False,
          help='Use this flag to print the json schema to stdout')
        parser.add_argument('--locale-js',
          action='store_true',
          default=False,
          help='Use this flag to print the js api locale to stdout')
        parser.add_argument('--locale-py',
          action='store_true',
          default=False,
          help='Use this flag to print the python api locale to stdout')

    def handle(self, *args, **options):
        if options['json']:
            self.stdout.write(re.sub('\\s+', '', schema.render_json_schema()))
        else:
            if options['locale_js']:
                self.stdout.write(schema.render_locale_js_schema())
            else:
                if options['locale_py']:
                    self.stdout.write(schema.render_locale_py_schema())
                else:
                    self.parser.print_help()
                    raise CommandError('no options provided')