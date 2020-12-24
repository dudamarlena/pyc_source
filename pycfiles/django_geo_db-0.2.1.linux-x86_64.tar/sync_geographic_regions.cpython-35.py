# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/management/commands/sync_geographic_regions.py
# Compiled at: 2018-02-17 18:58:54
# Size of source mod 2**32: 1399 bytes
from django.core.management.base import BaseCommand
from django_geo_db.models import Location, GeographicRegion, State, Country
SOUTHEAST = [
 'Virginia',
 'North Carolina',
 'South Carolina',
 'Tennessee',
 'Georgia',
 'Alabama',
 'Florida',
 'Louisiana',
 'Texas',
 'Mississippi']

class Command(BaseCommand):
    help = 'Generates the default Geographic Regions.'

    def __get_or_create_region(self, country, name, state_list):
        region = GeographicRegion.objects.filter(name=name)
        if len(region) < 1:
            print('Creating ' + name)
            region = GeographicRegion()
            region.name = name
            region.save()
            states = State.objects.filter(country=country, name__in=state_list)
            if len(states) < 1:
                raise Exception('No states found for {0} list.'.format(name))
            locations = Location.objects.filter(state__in=states, city=None, county=None)
            if len(states) < 1:
                raise Exception('No locations found for {0} list.'.format(name))
            region.locations = locations
            region.save()

    def handle(self, *args, **options):
        us = Country.objects.get(name__iexact='United States of America')
        print('Generating Southeast')
        self._Command__get_or_create_region(us, 'Southeast', SOUTHEAST)