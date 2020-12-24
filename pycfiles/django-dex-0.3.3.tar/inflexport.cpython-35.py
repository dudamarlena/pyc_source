# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/econso11/econso/inflex/management/commands/inflexport.py
# Compiled at: 2017-07-11 13:16:24
# Size of source mod 2**32: 4854 bytes
from __future__ import print_function
import time
from influxdb import InfluxDBClient
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from inflex.serializers import serialize, format_data
from inflex.producers import write
EXCLUDE = getattr(settings, 'INFLEX_EXCLUDE', ['filebrowser', 'admin'])
MEASUREMENT = getattr(settings, 'INFLEX_MEASUREMENT', 'django_model')
TIME_FIELD = getattr(settings, 'INFLEX_DEFAULT_TIME_FIELD', 'date')
TIME_FIELDS = getattr(settings, 'INFLEX_TIME_FIELDS', {'User': 'date_joined'})
DB = getattr(settings, 'INFLEX_DB', 'django_models')
HOST = getattr(settings, 'INFLEX_HOST', 'localhost')
PORT = getattr(settings, 'INFLEX_PORT', 8086)
USER = getattr(settings, 'INFLEX_USER', 'admin')
PWD = getattr(settings, 'INFLEX_PASSWORD', 'admin')
SERIALIZERS = getattr(settings, 'INFLEX_SERIALIZERS', {})
INFLUX = {'host': HOST, 
 'port': PORT, 
 'user': USER, 
 'password': PWD, 
 'database': DB}
cli = InfluxDBClient(INFLUX['host'], INFLUX['port'], INFLUX['user'], INFLUX['password'], INFLUX['database'], timeout=5, ssl=False)
POINTS = []

class Command(BaseCommand):
    help = 'Export data'

    def add_arguments(self, parser):
        parser.add_argument('-a', default=None, dest='appname', help='Name of the app to export')
        parser.add_argument('-m', default=None, dest='measurement', help='Name of the measurement')
        parser.add_argument('-f', default=None, dest='time_field', help='Name of the default time field')

    def handle(self, *args, **options):
        global MEASUREMENT
        global POINTS
        global TIME_FIELD
        t = time.time()
        if options['measurement'] is not None:
            MEASUREMENT = options['measurement']
        if options['time_field'] is not 'date':
            TIME_FIELD = options['time_field']
        print('Start exporting data to measurement', MEASUREMENT)
        stats = {}
        i = 0
        num_apps = 0
        appname = options['appname']
        models_list = settings.INSTALLED_APPS
        if appname is not None:
            models_list = [
             appname]
        for appstr in models_list:
            last_app = False
            if len(models_list) == num_apps + 1:
                last_app = True
            if not appstr in EXCLUDE:
                if appstr.startswith('django.'):
                    pass
                else:
                    print('# Processing', appstr)
                    at = time.time()
                    appstr = appstr.split('.')[(-1)]
                    app_models = apps.get_app_config(appstr).get_models()
                    num_models = 0
                    last_model = False
                    appmods = []
                    for model in app_models:
                        appmods.append(model)

                    total_models = len(appmods)
                    for model in appmods:
                        if total_models == num_models + 1:
                            last_model = True
                        modelname = model.__name__
                        if modelname in SERIALIZERS:
                            qs = model.objects.all().prefetch_related(SERIALIZERS[modelname][1])
                        qs = model.objects.all()
                        print(appstr, ':', modelname, len(qs))
                        last_instance = False
                        num_instances = 0
                        for instance in qs:
                            if len(qs) == num_instances + 1:
                                last_instance = True
                            data = serialize(instance, modelname, SERIALIZERS)
                            idata = format_data(model, instance, data, MEASUREMENT, TIME_FIELD, TIME_FIELDS)
                            save = False
                            if last_app is True and last_model is True and last_instance is True:
                                save = True
                            POINTS.append(idata)
                            POINTS = write(cli, POINTS, save)
                            print(i, appstr, model.__name__, ':', instance, instance.pk)
                            num_instances += 1
                            i += 1

                        num_models += 1

                    aet = time.time() - at
                    stats[appstr] = {'process_time': aet, 
                     'num_models': num_models}
                    num_apps += 1

        elapsed_time = time.time() - t
        print('Exported', i, 'objects from', num_apps, 'apps in', elapsed_time, 's')
        for stat in stats:
            if stats[stat]['num_models'] > 0:
                print('# App', stat, ': exported', stats[stat]['num_models'], 'model instances in', stats[stat]['process_time'], 's')