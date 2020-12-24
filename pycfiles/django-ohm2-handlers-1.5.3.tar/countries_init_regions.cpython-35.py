# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/countries/management/commands/countries_init_regions.py
# Compiled at: 2016-10-08 12:34:31
# Size of source mod 2**32: 682 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers import utils as h_utils
from ohm2_handlers.countries import utils
import simplejson as json, os

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BD/JSON/BDCUT_CL_Regiones.json')
        with open(path) as (f):
            data = json.load(f)
        CL = utils.get_country(code='CL')
        for c in data:
            region = utils.create_region(CL, c['region_id'], c['name'])

        self.stdout.write('Finish OK')