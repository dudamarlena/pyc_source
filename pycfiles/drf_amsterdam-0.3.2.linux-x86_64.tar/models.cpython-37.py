# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3393)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stephan/.virtualenvs/drf_amsterdam/lib/python3.7/site-packages/tests/models.py
"""Test models."""
from django.contrib.gis.db import models

class WeatherStation(models.Model):
    number = models.IntegerField(unique=True)
    centroid = models.PointField(name='centroid', srid=4326)
    centroid_rd = models.PointField(name='centroid_rd', srid=28992)

    def __str__(self):
        return 'DISPLAY FIELD CONTENT'


class TemperatureRecord(models.Model):

    class Meta:
        unique_together = ('station', 'date')

    station = models.ForeignKey(WeatherStation, on_delete=(models.CASCADE))
    date = models.DateField()
    temperature = models.DecimalField(decimal_places=3, max_digits=6)