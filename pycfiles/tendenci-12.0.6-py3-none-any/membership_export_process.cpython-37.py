# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/memberships/management/commands/membership_export_process.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 2836 bytes
import time
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    __doc__ = '\n    Membership export process.\n\n    Usage:\n        python manage.py membership_export_process\n\n        example:\n        python manage.py membership_export_process --export_type main_fields\n                                                   --export_status_detail active\n                                                   --identifier 1359048111\n                                                   --user 1\n                                                   --cp_id 21\n    '

    def add_arguments(self, parser):
        parser.add_argument('--export_status_detail',
          action='store',
          dest='export_status_detail',
          default='active',
          help='Export memberships with the status detail specified')
        parser.add_argument('--export_fields',
          action='store',
          dest='export_fields',
          default='main_fields',
          help='Either main_fields or all_fields to export')
        parser.add_argument('--export_type',
          action='store',
          dest='export_type',
          default='all',
          help='All or one specific membership type')
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
        parser.add_argument('--cp_id',
          action='store',
          dest='cp_id',
          default=0,
          help='corp_profile id')
        parser.add_argument('--ids',
          action='store',
          dest='ids',
          default='',
          help='Membership IDs')

    def handle(self, *args, **options):
        from tendenci.apps.memberships.utils import process_export
        export_fields = options.get('export_fields', 'main_fields')
        export_type = options.get('export_type', 'all')
        export_status_detail = options.get('export_status_detail', 'active')
        identifier = options.get('identifier', None)
        ids = options.get('ids', '')
        if not identifier:
            identifier = int(time.time())
        cp_id = int(options.get('cp_id', 0)) or 0
        user_id = options.get('user', '1')
        process_export(export_fields=export_fields,
          export_type=export_type,
          export_status_detail=export_status_detail,
          identifier=identifier,
          user_id=user_id,
          cp_id=cp_id,
          ids=ids)
        print('Membership export done %s.' % identifier)