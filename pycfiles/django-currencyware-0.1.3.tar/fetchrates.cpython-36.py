# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.venv/trade/lib/python3.6/site-packages/currencyware/management/commands/fetchrates.py
# Compiled at: 2018-08-17 17:28:34
# Size of source mod 2**32: 3713 bytes
import sys, json, codecs, logging, requests
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.utils import translation
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from toolware.utils.generic import get_days_ago
from ...currency import get_display
from ...models import Rate, Currency
from ... import defaults as defs
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetches live rates from open exchange rates api'
    OXR_URL = defs.OPEN_EXCHANGE_RATES_URL
    OXR_KEY = defs.OPEN_EXCHANGE_RATES_API_KEY
    LANGUAGE_CODE = getattr(settings, 'LANGUAGE_CODE', 'en')

    def add_arguments(self, parser):
        parser.add_argument('-f',
          '--flush',
          action='store_true',
          dest='flush',
          default=False,
          help='Remove all rates from db')
        parser.add_argument('-p',
          '--purge',
          action='store',
          dest='days',
          type=int,
          help='Remove rates older than x days')
        parser.add_argument('-l',
          '--load',
          action='store_true',
          dest='load',
          default=False,
          help='Fetch and load all rates to db')

    def handle(self, *args, **options):
        translation.activate(self.LANGUAGE_CODE)
        self.verbosity = options['verbosity']
        self.days = options['days']
        self.flush = options['flush']
        self.load = options['load']
        if not (self.flush or self.days or self.load):
            self.print_help('', subcommand='loadcurrency')
            return
        if self.flush:
            self.stdout.write('You are about to delete all rates from db')
            confirm = input('Are you sure? [yes/no]: ')
            if confirm == 'yes':
                Rate.objects.all().delete()
                self.stdout.write('Flushed rates from db.')
        if self.days:
            if self.days > 0:
                days_ago = get_days_ago(self.days)
                Rate.objects.filter(date__lte=days_ago).delete()
                self.stdout.write('Purged rates older than ({}) ago from db.'.format(self.days))
        if not self.load:
            return
        if self.verbosity > 2:
            self.stdout.write('Preparing to fetch rates ...')
        resp = requests.get((self.OXR_URL), params={'app_id':self.OXR_KEY,  'base':defs.BASE_CURRENY_CODE})
        if resp.status_code != requests.codes.ok:
            self.stdout.write('Failed to fetch rates ...')
            self.stdout.write(resp.text)
            return
        self.data = resp.json()
        new_count, update_count = (0, 0)
        updated = datetime.fromtimestamp((self.data['timestamp']), tz=(timezone.utc))
        for code, rate in self.data['rates'].items():
            created = False
            defaults = {'code':code, 
             'date':updated, 
             'rate':rate, 
             'name':get_display(code)}
            instance, created = Rate.objects.get_or_create_unique(defaults, ['code', 'date'])
            if created:
                new_count += 1
            else:
                update_count += 1
            if not instance and self.verbosity >= 3:
                sys.stdout.write('Failed to create rate for ({code})\n'.format(code=code))

        self.stdout.write('Created {count} currenies'.format(count=new_count))
        self.stdout.write('Updated {count} currenies'.format(count=update_count))