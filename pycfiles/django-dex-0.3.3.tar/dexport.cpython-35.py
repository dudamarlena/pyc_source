# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/econso11/econso/dex/management/commands/dexport.py
# Compiled at: 2017-07-22 07:24:58
# Size of source mod 2**32: 1776 bytes
from __future__ import print_function
from django.core.management.base import BaseCommand
from dex.exporter import Exporter
from dex.conf import MEASUREMENT, TIME_FIELD

class Command(BaseCommand):
    help = 'Export data'

    def add_arguments(self, parser):
        parser.add_argument('db', type=str)
        parser.add_argument('-a', default=None, dest='appname', help='Name of the app to export')
        parser.add_argument('-m', default=None, dest='measurement', help='Name of the measurement')
        parser.add_argument('-t', default=None, dest='time_field', help='Name of the default time field')
        parser.add_argument('-s', default=0, dest='stats', help='Return json stats')
        parser.add_argument('-txt', default=1, dest='text_field', help='Enable text fields to be serialized')

    def handle(self, *args, **options):
        global MEASUREMENT
        global TIME_FIELD
        if options['measurement'] is not None:
            MEASUREMENT = options['measurement']
        if options['time_field'] is not 'date':
            TIME_FIELD = options['time_field']
        stats = options['stats']
        isstats = True
        if stats == 0:
            isstats = False
        istext = True
        if istext == 0:
            istext = False
        db = options['db']
        ex = Exporter(db)
        if ex.err != None:
            print('ERROR', ex.err)
            return
        ex.run(MEASUREMENT, TIME_FIELD, options['appname'], isstats, istext)