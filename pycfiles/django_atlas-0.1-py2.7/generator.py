# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atlas/generator.py
# Compiled at: 2015-04-21 15:30:03
import random, math
from atlas.models import Country, Region, City, Location

def generate():
    try:
        country_id = Country.objects.get(country_code='ZA').id
    except Country.DoesNotExist:
        return []

    cities = City.objects.filter(country=country_id, name__in=('Cape Town', 'Stellenbosch',
                                                               'Worcester', 'Johannesburg')).exclude(region__name='Limpopo').values_list('id', 'name', 'coordinates')
    lon = (18.39111328125, 18.689117431640625)
    x_max = (lon[1] - lon[0]) / 2
    lat = (-34.031038397347814, -33.82023008524739)
    y_max = (lat[1] - lat[0]) / 2
    x = lambda t, a: a * math.cos(t)
    y = lambda t, b: b * math.sin(t)
    objects = []
    for city in cities:
        center_x = city[2].x
        center_y = city[2].y
        for i in range(1, 1001):
            t = random.random() * math.pi * 2
            fraction = math.fabs(random.normalvariate(0, 0.5))
            x_new = center_x + x(t, fraction * x_max)
            y_new = center_y + y(t, fraction * y_max)
            objects.append({'model': 'atlas.Location', 
               'fields': {'name': ('%s_%d' % (city[1], i)).encode('ascii'), 
                          'country': {'model': 'atlas.Country', 'fields': {'id': int(country_id)}}, 'city': {'model': 'atlas.City', 'fields': {'id': int(city[0])}}, 'coordinates': 'POINT(%f %f)' % (x_new, y_new)}})

    return objects