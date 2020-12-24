# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-places/vkontakte_places/factories.py
# Compiled at: 2016-02-23 12:35:05
from models import City, Country
import factory

class CityFactory(factory.DjangoModelFactory):
    remote_id = factory.Sequence(lambda n: n)

    class Meta:
        model = City


class CountryFactory(factory.DjangoModelFactory):
    remote_id = factory.Sequence(lambda n: n)

    class Meta:
        model = Country