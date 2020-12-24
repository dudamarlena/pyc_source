# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djsld/tests/djsld-test/models.py
# Compiled at: 2012-10-05 18:48:33
"""
Test models for django-sld unit tests.

License
=======
Copyright 2011-2012 David Zwarg <U{dzwarg@azavea.com}>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

U{http://www.apache.org/licenses/LICENSE-2.0}

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: David Zwarg
@contact: dzwarg@azavea.com
@copyright: 2011-2012, Azavea
@license: Apache 2.0
@version: 1.0.7
"""
from django.contrib.gis.db import models

class Hydrant(models.Model):
    """
    A sample point-based geographic model.
    """
    number = models.IntegerField()
    location = models.PointField()
    pressure = models.FloatField()
    pipeline = models.ForeignKey('Pipeline')
    objects = models.GeoManager()


class Pipeline(models.Model):
    """
    A sample line-based geographic model.
    """
    material = models.CharField(max_length=25)
    path = models.LineStringField()
    diameter = models.FloatField()
    reservoir = models.ForeignKey('Reservoir')
    objects = models.GeoManager()


class Reservoir(models.Model):
    """
    A sample polygon-based geographic model.
    """
    name = models.CharField(max_length=25)
    volume = models.FloatField()
    coastline = models.PolygonField()
    objects = models.GeoManager()