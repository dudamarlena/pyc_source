# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-wall/vkontakte_wall/factories.py
# Compiled at: 2015-03-31 07:41:24
import random
from django.utils import timezone
import factory
from vkontakte_api.factories import DjangoModelNoCommitFactory
from vkontakte_groups.factories import GroupFactory
from vkontakte_users.factories import UserFactory
from .models import Post

class PostFactory(DjangoModelNoCommitFactory):
    date = factory.LazyAttribute(lambda o: timezone.now())
    owner = factory.SubFactory(UserFactory)
    author = factory.SubFactory(UserFactory)
    remote_id = factory.LazyAttributeSequence(lambda o, n: '%s_%s' % (o.owner.remote_id, n))
    likes_count = factory.LazyAttribute(lambda o: random.randrange(100))
    reposts_count = factory.LazyAttribute(lambda o: random.randrange(100))
    comments_count = factory.LazyAttribute(lambda o: random.randrange(100))

    class Meta:
        model = Post


class GroupPostFactory(PostFactory):
    owner = factory.SubFactory(GroupFactory)
    remote_id = factory.LazyAttributeSequence(lambda o, n: '-%s_%s' % (o.owner.remote_id, n))