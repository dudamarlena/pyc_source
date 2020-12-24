# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-video/vkontakte_video/factories.py
# Compiled at: 2015-03-06 07:14:43
import random
from django.utils import timezone
import factory
from .models import Album, Video

class AlbumFactory(factory.DjangoModelFactory):
    remote_id = factory.LazyAttributeSequence(lambda o, n: n)
    videos_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))

    class Meta:
        model = Album


class VideoFactory(factory.DjangoModelFactory):
    remote_id = factory.LazyAttributeSequence(lambda o, n: n)
    album = factory.SubFactory(AlbumFactory)
    duration = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    likes_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    comments_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    date = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = Video