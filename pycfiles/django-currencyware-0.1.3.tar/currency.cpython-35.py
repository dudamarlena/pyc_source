# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/backend-repo/apps/currency/management/commands/currency.py
# Compiled at: 2017-09-06 15:37:16
# Size of source mod 2**32: 3269 bytes
import sys, json, codecs
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils.translation import ugettext as _
from django.utils import translation
from django.conf import settings
from utilware.query import get_or_create_object
from ...models import *

class Command(BaseCommand):
    help = _('COMMAND.CURRENCY.LOAD_ISO')

    def add_arguments(self, parser):
        parser.add_argument('file')
        parser.add_argument('--flush', dest='flush', default=False, action='store_true', help=_('COMMAND.FLUSH_DB'))
        parser.add_argument('-n', '--verify', action='store_true', dest='verify_only', default=False, help='Verify the file but do not replace existing data')

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']
        translation.activate(getattr(settings, 'LANGUAGE_CODE', 'en'))
        if 'file' not in options:
            raise CommandError(_('ERROR.PARAM_MISSING_FMT').format(param='file'))
        try:
            ifp = codecs.open(options['file'], encoding='utf-8')
        except:
            raise CommandError(_('ERROR.FILE.OPEN_FMT').format(file=options['file'], error=sys.exc_info()[1]))

        try:
            self.data = json.load(ifp)
        except:
            raise CommandError(_('ERROR.FILE.PARSE_FMT').format(file=options['file'], error=sys.exc_info()[1]))

        if not ('currency' in self.data and 'usage' in self.data):
            raise CommandError(_('ERROR.CURRENCY.FILE_INVALID_FMT').format(keys=', '.join(sorted(self.data.keys()))))
        if options['verify_only']:
            return
        if options['flush']:
            confirm = input(_('CURRENCY.DELETE_CONFIRM_FMT').format(file=options['file']))
            if confirm != 'yes':
                self.stdout.write(self.style.WARNING(_('COMMAND.ABORT_LOAD')))
                return
            self.flush()
        self.create_currencies()
        self.create_usage()

    def flush(self):
        Currency.objects.all().delete()
        Usage.objects.all().delete()

    def create_currencies(self):
        for row in self.data.get('currency'):
            instance, created = get_or_create_object(Currency, ['code'], row)
            if not instance and self.verbosity >= 3:
                sys.stdout.write('Failed to add/update Currency ({code})\n'.format(code=row.get('code')))

    def create_usage(self):
        for row in self.data.get('usage'):
            instance, created = get_or_create_object(Usage, ['country', 'currency'], row)
            if not instance and self.verbosity >= 3:
                sys.stdout.write('Failed to add/update Usage ({code})\n'.format(code=row.get('currency')))