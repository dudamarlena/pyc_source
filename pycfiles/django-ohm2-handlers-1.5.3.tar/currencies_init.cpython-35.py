# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/currencies/management/commands/currencies_init.py
# Compiled at: 2016-12-06 14:30:47
# Size of source mod 2**32: 872 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers import utils as h_utils
from ohm2_handlers.currencies import utils
import pycountry

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        currencies = [
         {'code': 'CLP', 
          'name': pycountry.currencies.get(alpha_3='CLP').name, 
          'symbol': '$', 
          'decimals': 0},
         {'code': 'USD', 
          'name': pycountry.currencies.get(alpha_3='USD').name, 
          'symbol': '$', 
          'decimals': 2},
         {'code': 'EUR', 
          'name': pycountry.currencies.get(alpha_3='EUR').name, 
          'symbol': '€', 
          'decimals': 2}]
        for kwargs in currencies:
            utils.create_currency(**kwargs)

        self.stdout.write('Finish OK')