# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/management/commands/resave_all_geocoordinates.py
# Compiled at: 2018-02-28 07:20:55
# Size of source mod 2**32: 397 bytes
from django.core.management.base import BaseCommand
from django_geo_db.models import GeoCoordinate
from django.db.transaction import atomic

class Command(BaseCommand):
    help = 'Calls save on every GeoCoordinate, which will regenerated all auto-generated values.'

    @atomic
    def handle(self, *args, **options):
        for coord in GeoCoordinate.objects.all():
            coord.save()