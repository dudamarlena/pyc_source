# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-twitter-api/twitter_api/factories.py
# Compiled at: 2015-11-01 17:29:06
import random
from django.utils import timezone
import factory, models

class UserFactory(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    screen_name = factory.Sequence(lambda n: n)
    created_at = factory.LazyAttribute(lambda o: timezone.now())
    entities = {}
    favorites_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    followers_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    friends_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    listed_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    statuses_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    utc_offset = factory.LazyAttribute(lambda o: random.randint(0, 1000))

    class Meta:
        model = models.User


class StatusFactory(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    created_at = factory.LazyAttribute(lambda o: timezone.now())
    entities = {}
    author = factory.SubFactory(UserFactory)
    favorites_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    retweets_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))
    replies_count = factory.LazyAttribute(lambda o: random.randint(0, 1000))

    class Meta:
        model = models.Status