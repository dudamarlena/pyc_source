# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/management/commands/setup_map_types.py
# Compiled at: 2018-03-10 10:16:54
# Size of source mod 2**32: 421 bytes
from django.core.management.base import BaseCommand
from django_geo_db.models import LocationMapType
TYPES = [
 'simple']

class Command(BaseCommand):
    help = 'Adds default map types.'

    def handle(self, *args, **options):
        for t in TYPES:
            map_type, created = LocationMapType.objects.get_or_create(type=t)
            if created:
                print('Created: {0}'.format(str(map_type)))