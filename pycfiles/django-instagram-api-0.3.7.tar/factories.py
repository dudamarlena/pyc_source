# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/factories.py
# Compiled at: 2016-02-24 16:14:01
import random, string, factory
from django.utils import timezone
from . import models

class UserFactory(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: n + 1)
    username = factory.Sequence(lambda n: ('').join([ random.choice(string.letters) for _ in xrange(30) ]))
    followers_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))

    class Meta:
        model = models.User


class MediaFactory(factory.DjangoModelFactory):
    remote_id = factory.Sequence(lambda n: ('').join([ random.choice(string.letters) for _ in xrange(30) ]))
    user = factory.SubFactory(UserFactory)
    comments_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    likes_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    created_time = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Media


class CommentFactory(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: n + 1)
    owner = factory.SubFactory(UserFactory)
    user = factory.SubFactory(UserFactory)
    media = factory.SubFactory(MediaFactory)
    created_time = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Comment


class TagFactory(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: ('').join([ random.choice(string.letters) for _ in xrange(50) ]))
    media_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))

    @factory.post_generation
    def media_feed(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for media in extracted:
                self.media_feed.add(media)

    class Meta:
        model = models.Tag


class LocationFactory(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: ('').join([ random.choice(string.letters) for _ in xrange(50) ]))
    media_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))

    @factory.post_generation
    def media_feed(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for media in extracted:
                self.media_feed.add(media)

    class Meta:
        model = models.Location