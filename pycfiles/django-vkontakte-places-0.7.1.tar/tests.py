# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-places/vkontakte_places/tests.py
# Compiled at: 2015-02-19 12:23:17
from django.test import TestCase
from models import City, Country, Region
from factories import CityFactory, CountryFactory
import simplejson as json

class VkontaktePlacesTest(TestCase):

    def test_parse_city(self):
        response = '\n            {"response":[\n                {"cid":1,"title":"Москва","region":"Regione Abruzzo область"},\n                {"cid":1074996,"title":"Москва","area":"Порховский район","region":"Псковская область"},\n                {"cid":1102561,"title":"Москва","area":"Пеновский район","region":"Тверская область"},\n                {"cid":1130701,"title":"Москва","area":"Верхошижемский район","region":"Кировская область"}\n            ]}\n            '
        country = CountryFactory.create(remote_id=1)
        instance = City(country=country)
        instance.parse(json.loads(response)['response'][0])
        instance.save()
        self.assertEqual(instance.remote_id, 1)
        self.assertEqual(instance.name, 'Москва')
        instance = City(country=country)
        instance.parse(json.loads(response)['response'][1])
        instance.save()
        self.assertEqual(instance.remote_id, 1074996)
        self.assertEqual(instance.name, 'Москва')
        self.assertEqual(instance.area, 'Порховский район')
        self.assertEqual(instance.region, 'Псковская область')

    def test_fetch_cities(self):
        self.assertEqual(City.objects.count(), 0)
        country = CountryFactory.create(remote_id=1)
        City.remote.fetch(country=country.remote_id)
        self.assertEqual(City.objects.count(), 18)
        self.assertEqual(City.objects.all()[0].country, country)
        City.remote.fetch(country=country)
        self.assertEqual(City.objects.count(), 18)
        City.objects.all().delete()
        City.remote.fetch(country=country, q='Москва')
        self.assertTrue(City.objects.count() > 1)

    def test_fetch_cities_by_id(self):
        self.assertEqual(City.objects.count(), 0)
        City.remote.fetch(ids=[1, 2])
        self.assertEqual(City.objects.count(), 2)