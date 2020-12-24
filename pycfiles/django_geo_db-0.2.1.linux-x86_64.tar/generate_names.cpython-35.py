# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/management/commands/generate_names.py
# Compiled at: 2018-02-04 15:10:23
# Size of source mod 2**32: 1198 bytes
from django.core.management.base import BaseCommand
from django_geo_db.models import Location, Zipcode, City, State, GeoCoordinate
from django.db import IntegrityError, transaction

@transaction.atomic
class Command(BaseCommand):
    help = 'Sets up all of the generated names of geo objects'

    def __generate(self, modelType):
        models = modelType.objects.all()
        count = models.count()
        print('Generating {0}: {1}'.format(modelType.__name__, count))
        buffer = []
        for index in range(count):
            l = models[index]
            buffer.append(l)
            if len(buffer) > 1000:
                try:
                    with transaction.atomic():
                        for l in buffer:
                            l.save()

                    print('Saved {0}'.format(index))
                except IntegrityError as e:
                    print('Exception occurred while committing.')
                    raise e

                buffer = []

    def handle(self, *args, **options):
        self._Command__generate(Location)
        self._Command__generate(Zipcode)
        self._Command__generate(City)
        self._Command__generate(State)
        self._Command__generate(GeoCoordinate)