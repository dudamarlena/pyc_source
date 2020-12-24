# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/management/commands/create_us_state_bounds.py
# Compiled at: 2018-03-10 01:49:57
# Size of source mod 2**32: 2344 bytes
from django.core.management.base import BaseCommand
from django_geo_db.models import Location, State, GeoCoordinate, LocationBounds, Country
from django_geo_db.services import get_us_states_boundaries
from django.db import IntegrityError, transaction

@transaction.atomic
class Command(BaseCommand):
    help = 'Creates boundaries for the US States'

    def _get_bounds(self, points):
        data = {'max_lat': 0.0, 
         'min_lat': 0.0, 
         'max_lon': 0.0, 
         'min_lon': 0.0}
        max_lat = None
        min_lat = None
        max_lon = None
        min_lon = None
        for p in points:
            lat = float(p['-lat'])
            lon = float(p['-lng'])
            if max_lat is None or lat > max_lat:
                max_lat = lat
                data['max_lat'] = lat
            if min_lat is None or lat < min_lat:
                min_lat = lat
                data['min_lat'] = lat
            if max_lon is None or lon > max_lon:
                max_lon = lon
                data['max_lon'] = lon
            if min_lon is None or lon < min_lon:
                min_lon = lon
                data['min_lon'] = lon

        return data

    def handle(self, *args, **options):
        boundaries = get_us_states_boundaries()['states']['state']
        united_states = Country.objects.get(name='United States of America')
        for state_dict in boundaries:
            name = state_dict['-name']
            state = State.objects.get(country=united_states, name=name)
            location = Location.objects.get(state=state, city=None, county=None)
            bounds_obj = LocationBounds.objects.filter(location=location).first()
            if not bounds_obj:
                points = state_dict['point']
                bounds_dict = self._get_bounds(points)
                bounds_obj = LocationBounds()
                bounds_obj.location = location
                bounds_obj.max_lat = bounds_dict['max_lat']
                bounds_obj.min_lat = bounds_dict['min_lat']
                bounds_obj.max_lon = bounds_dict['max_lon']
                bounds_obj.min_lon = bounds_dict['min_lon']
                bounds_obj.save()
                print('Created {0}'.format(str(bounds_obj)))
            else:
                print('Found {0}: Skipping'.format(str(bounds_obj)))