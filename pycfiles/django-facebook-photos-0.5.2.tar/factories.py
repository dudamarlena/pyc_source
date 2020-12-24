# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-facebook-photos/facebook_photos/factories.py
# Compiled at: 2015-01-25 03:13:36
from django.utils import timezone
import factory, models

class AlbumFactory(factory.DjangoModelFactory):
    graph_id = factory.Sequence(lambda n: n)
    created_time = factory.LazyAttribute(lambda o: timezone.now())
    updated_time = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Album


class PhotoFactory(factory.DjangoModelFactory):
    graph_id = factory.Sequence(lambda n: n)
    album = factory.SubFactory(AlbumFactory)
    created_time = factory.LazyAttribute(lambda o: timezone.now())
    updated_time = factory.LazyAttribute(lambda o: timezone.now())
    width = 10
    height = 10

    class Meta:
        model = models.Photo