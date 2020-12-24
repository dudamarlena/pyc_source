# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/invoices/management/commands/invoice_export_process.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 2445 bytes
import time
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    __doc__ = '\n    Directory export process.\n\n    Usage:\n        python manage.py event_export_process\n\n        example:\n        python manage.py invoice_export_process --start_dt=2010-10-30\n                                                --end_dt=2011-11-30\n                                                --identifier=1359048111\n                                                --user=1\n    '

    def add_arguments(self, parser):
        parser.add_argument('--start_dt',
          action='store',
          dest='start_dt',
          default='',
          help='Export invoices whose update date is greater than or equal to the value specified')
        parser.add_argument('--end_dt',
          action='store',
          dest='end_dt',
          default='',
          help='Export invoices whose update date is less than the value specified')
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
        from tendenci.apps.invoices.utils import process_invoice_export
        start_dt = options['start_dt']
        end_dt = options['end_dt']
        user_id = options['user']
        identifier = options['identifier']
        if not identifier:
            identifier = int(time.time())
        if start_dt:
            try:
                start_dt = datetime.strptime(start_dt, '%Y-%m-%d')
            except:
                raise CommandError('Please use the following date format YYYY-MM-DD.\n')

        if end_dt:
            try:
                end_dt = datetime.strptime(end_dt, '%Y-%m-%d')
                end_dt = end_dt + timedelta(days=1)
            except:
                raise CommandError('Please use the following date format YYYY-MM-DD.\n')

        process_invoice_export(start_dt=start_dt, end_dt=end_dt,
          identifier=identifier,
          user_id=user_id)
        print('Invoice export done %s.' % identifier)