# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/countries/management/commands/countries_init.py
# Compiled at: 2016-12-06 14:15:12
# Size of source mod 2**32: 491 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers import utils as h_utils
from ohm2_handlers.countries import utils
import simplejson as json, pycountry

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for c in pycountry.countries:
            utils.create_country(code=c.alpha_2, name=c.name)

        self.stdout.write('Finish OK')