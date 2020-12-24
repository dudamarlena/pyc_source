# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-country-dialcode/country_dialcode/management/commands/load_country_dialcode.py
# Compiled at: 2014-07-16 07:20:09
from django.core.management.base import BaseCommand
from django.core.management import call_command
import inspect, os

class Command(BaseCommand):
    args = ' '
    help = 'Load Dial Code\n'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        """
        Load country dialcode
        """
        script_directory = os.path.dirname(inspect.getfile(inspect.currentframe()))
        fixture_file = script_directory + '/../../fixtures/country_dialcode.json'
        print 'This fixture is going to be loaded : ' + fixture_file
        call_command('loaddata', fixture_file)