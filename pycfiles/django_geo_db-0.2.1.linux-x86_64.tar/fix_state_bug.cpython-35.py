# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/management/commands/fix_state_bug.py
# Compiled at: 2018-02-19 10:58:44
# Size of source mod 2**32: 1183 bytes
from django.core.management.base import BaseCommand
from django_geo_db.models import State

class Command(BaseCommand):
    help = 'Fixes a state mixup bug.'

    def handle(self, *args, **options):
        raise Exception('Make sure you know what you"re doing')
        data = [
         [
          'New York', 'Montana', 'Maryland'],
         [
          'Massachusetts', 'North Carolina', 'Nebraska'],
         [
          'Michigan', 'North Dakota', 'Nevada'],
         [
          'Mississippi', 'Oklahoma', 'New Jersey'],
         [
          'New Hampshire', 'Minnesota', 'Ohio'],
         [
          'New Mexico', 'Missouri', 'Oregon']]
        for idx in range(len(data)):
            a, b, c = data[idx]
            a = State.objects.get(name=a)
            b = State.objects.get(name=b)
            c = State.objects.get(name=c)
            data[idx] = [a, b, c]

        for a, b, c in data:
            a_coordinate = a.geocoordinate
            b_coordinate = b.geocoordinate
            c_coordinate = c.geocoordinate
            b.geocoordinate = a_coordinate
            c.geocoordinate = b_coordinate
            a.geocoordinate = c_coordinate
            b.save()
            a.save()
            c.save()