# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/tests/test_location.py
# Compiled at: 2017-05-03 05:57:29
from django.test import TestCase
from jmbo import USE_GIS
from jmbo.models import ModelBase
if USE_GIS:
    from atlas.models import Location, City, Country
if USE_GIS:

    class LocationAwarenessTestCase(TestCase):

        def setUp(self):
            super(LocationAwarenessTestCase, self).setUp()
            country = Country(name='South Africa', country_code='ZA')
            country.save()
            self.ct = City(name='Cape Town', country=country, coordinates=fromstr('POINT(18.423218 -33.925839)', srid=4326))
            self.ct.save()
            loc1 = Location(city=self.ct, country=country, coordinates=fromstr('POINT(18.41 -33.91)', srid=4326), name='loc1')
            loc1.save()
            self.model = ModelBase(title='title1', location=loc1)
            self.model.save()

        def test_distance_calculation(self):
            qs = ModelBase.objects.distance(self.ct.coordinates)
            for obj in qs:
                if obj.distance is not None:
                    self.assertEqual(obj.location.coordinates.distance(self.ct.coordinates), obj.distance)

            return