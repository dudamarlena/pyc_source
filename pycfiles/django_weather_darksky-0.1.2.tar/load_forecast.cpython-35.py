# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/slava/myprojects/django_weather_darksky/django_weather_darksky/management/commands/load_forecast.py
# Compiled at: 2017-03-21 22:30:54
# Size of source mod 2**32: 1308 bytes
import time
from django.core.management.base import BaseCommand
from django.db import transaction
from django_weather_darksky.settings import api_key, lang
from django_weather_darksky.api import DarkSkyAPI
from django_weather_darksky.models import WeatherLocation, WeatherForecast

class Command(BaseCommand):
    __doc__ = '\n    Usage:\n    python manage.py load_forecast --type currently\n    python manage.py load_forecast --type daily --clear CLEAR\n    '

    @transaction.atomic
    def load_forecast(self, clear, tp):
        if clear:
            WeatherForecast.objects.filter(forecast_type=tp).delete()
        api = DarkSkyAPI(api_key, lang)
        for loc in WeatherLocation.objects.all():
            api.set_location(loc.latitude, loc.longitude)
            data = api.get_forecast(tp)
            WeatherForecast(location=loc, forecast_type=tp, json_data=data).save(force_insert=True)
            time.sleep(2)

    def add_arguments(self, parser):
        parser.add_argument('--clear', default=False, help='Delete old data')
        parser.add_argument('--type', default='currently', help='Limit of records for load')

    def handle(self, *args, **options):
        self.load_forecast(options['clear'], options['type'])