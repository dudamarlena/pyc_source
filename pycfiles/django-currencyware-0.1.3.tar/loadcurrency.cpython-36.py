# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.venv/trade/lib/python3.6/site-packages/currencyware/management/commands/loadcurrency.py
# Compiled at: 2018-08-19 20:05:49
# Size of source mod 2**32: 3269 bytes
import os, sys, codecs, logging, json
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils.translation import activate
from ...models import Currency, Rate
from ...currency import get_display
from ... import defaults as defs
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Load currency data'
    path = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../', 'currency.json'))

    def add_arguments(self, parser):
        parser.add_argument('-p',
          '--path', dest='path',
          default=(self.path),
          help='path to a directory for currencies file.')
        parser.add_argument('-f',
          '--flush', dest='flush',
          default=False,
          action='store_true',
          help='delete all existing currencies in db')
        parser.add_argument('-o',
          '--overwrite', dest='overwrite',
          action='store_true',
          default=False,
          help='overwrite currencies if already found in db')

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        path = options['path'] or self.path
        overwrite = options['overwrite']
        flush = options['flush']
        if not os.path.isfile(path):
            self.stdout.write('No currency file found at path')
            self.stdout.write(path)
            self.print_help('', subcommand='loadcurrency')
            return
        if flush:
            self.stdout.write('You are about to delete all currencies from db')
            confirm = input('Are you sure? [yes/no]: ')
            if confirm == 'yes':
                Currency.objects.all().delete()
                self.stdout.write('Currencies deleted from db.')
        if verbosity > 2:
            self.stdout.write('Preparing currency file ...')
        fp = codecs.open(path, encoding='utf-8')
        self.data = json.load(fp)
        activate(defs.DEFAULT_CURRENY_LANGUAGE_CODE)
        new_count, update_count = (0, 0)
        for curr in self.data:
            created = False
            defaults = {'code':curr.get('code'), 
             'name':get_display(curr.get('code')), 
             'number':curr.get('number', 0), 
             'symbol':curr.get('symbol', ''), 
             'unit':curr.get('unit', 2), 
             'country':' '.join(curr.get('country', []))}
            if overwrite:
                instance, created = Currency.objects.get_or_create_unique(defaults, ['code'])
            else:
                instance = Currency.objects.get_unique_or_none(code=(defaults['code']))
            if not instance:
                instance, created = Currency.objects.get_or_create_unique(defaults, ['code'])
            if created:
                new_count += 1
            else:
                if overwrite:
                    update_count += 1

        self.stdout.write('Created {count} currenies'.format(count=new_count))
        self.stdout.write('Updated {count} currenies'.format(count=update_count))