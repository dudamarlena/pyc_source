# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/directories/management/commands/directory_export_process.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 1957 bytes
import time
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    __doc__ = '\n    Directory export process.\n\n    Usage:\n        python manage.py directory_export_process\n\n        example:\n        python manage.py directory_export_process --export_fields=main_fields\n                                                  --export_status_detail=active\n                                                  --identifier=1359048111\n                                                  --user=1\n    '

    def add_arguments(self, parser):
        parser.add_argument('--export_status_detail',
          action='store',
          dest='export_status_detail',
          default='',
          help='Export directories with the status detail specified')
        parser.add_argument('--export_fields',
          action='store',
          dest='export_fields',
          default='main_fields',
          help='Either main_fields or all_fields to export')
        parser.add_argument('--identifier',
          action='store',
          dest='identifier',
          default='',
          help='Export file identifier')
        parser.add_argument('--user',
          action='store',
          dest='user',
          default='1',
          help='Request user')

    def handle(self, *args, **options):
        from tendenci.apps.directories.utils import process_export
        export_fields = options['export_fields']
        export_status_detail = options['export_status_detail']
        user_id = options['user']
        identifier = options['identifier']
        if not identifier:
            identifier = int(time.time())
        process_export(export_fields=export_fields,
          export_status_detail=export_status_detail,
          identifier=identifier,
          user_id=user_id)
        print('Directory export done %s.' % identifier)