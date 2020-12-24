# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/management/commands/geo.py
# Compiled at: 2017-01-27 09:53:00
# Size of source mod 2**32: 1654 bytes
import logging
from django.core.management.base import BaseCommand
from django.core.management import call_command
from ... import defaults as defs
logger = logging.getLogger('geoware.cmd.geo')

class Command(BaseCommand):
    help = 'Description: Downloads and/or loads geoname data'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--download', action='store_true', default=False, help='Download the related files if newer files are available.')
        parser.add_argument('-l', '--load', action='store_true', default=False, help='Load the info from the downloaded files into the DB')
        parser.add_argument('-f', '--force', action='store_true', default=False, help='Force an action.')
        parser.add_argument('-s', '--speed', action='store_true', default=False, help='Optimize for systems with no memory constrains.')
        (
         parser.add_argument('-o', '--overwrite', action='store_true', default=False, help='Overwrite any locally modified data with the newly downloaded data.'),)

    def handle(self, *args, **options):
        if options['download'] or options['load']:
            for cmd in defs.GEOWARE_LOADING_ORDER + ['Hierarchy']:
                call_command(cmd.lower(), **options)

        else:
            self.print_help('', subcommand='geo')