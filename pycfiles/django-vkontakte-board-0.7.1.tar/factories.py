# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-board/vkontakte_board/factories.py
# Compiled at: 2016-02-23 12:34:17
from vkontakte_groups.factories import GroupFactory
from vkontakte_users.factories import UserFactory
from models import Topic, Comment
from datetime import datetime
import factory, random

class TopicFactory(factory.DjangoModelFactory):
    group = factory.SubFactory(GroupFactory)
    remote_id = factory.LazyAttributeSequence(lambda o, n: '-%s_%s' % (o.group.remote_id, n))
    created = datetime.now()
    comments_count = 1
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)
    is_closed = random.choice((True, False))
    is_fixed = random.choice((True, False))

    class Meta:
        model = Topic


class CommentFactory(factory.DjangoModelFactory):
    remote_id = factory.LazyAttributeSequence(lambda o, n: '%s_%s' % (o.topic.remote_id, n))
    topic = factory.SubFactory(TopicFactory)
    date = datetime.now()
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Comment