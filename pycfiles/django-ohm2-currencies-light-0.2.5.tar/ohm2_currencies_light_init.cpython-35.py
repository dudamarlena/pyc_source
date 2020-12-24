# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_currencies_light/management/commands/ohm2_currencies_light_init.py
# Compiled at: 2017-12-06 21:10:29
# Size of source mod 2**32: 1106 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers_light import utils as h_utils
from ohm2_currencies_light import utils as ohm2_currencies_light_utils
import os, pycountry

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        CLP = pycountry.currencies.get(alpha_3='CLP')
        USD = pycountry.currencies.get(alpha_3='USD')
        EUR = pycountry.currencies.get(alpha_3='EUR')
        entries = [
         {'alpha_3': CLP.alpha_3, 
          'name': CLP.name, 
          'symbol': '$', 
          'decimals': 0, 
          'available': True},
         {'alpha_3': USD.alpha_3, 
          'name': USD.name, 
          'symbol': '$', 
          'decimals': 2, 
          'available': True},
         {'alpha_3': EUR.alpha_3, 
          'name': EUR.name, 
          'symbol': '€', 
          'decimals': 2, 
          'available': True}]
        for e in entries:
            c = ohm2_currencies_light_utils.get_or_none_currency(alpha_3=e['alpha_3'])
            if c:
                pass
            else:
                c = ohm2_currencies_light_utils.create_currency(**e)
                print(c)