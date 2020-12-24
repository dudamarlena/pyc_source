# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-polls/vkontakte_polls/factories.py
# Compiled at: 2016-03-11 12:36:12
from vkontakte_users.factories import UserFactory
from models import Poll, Answer
from datetime import datetime
import factory

class PollFactory(factory.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    remote_id = factory.Sequence(lambda n: n)
    created = datetime.now()
    votes_count = 0
    answer_id = 0

    class Meta:
        model = Poll


class AnswerFactory(factory.DjangoModelFactory):
    poll = factory.SubFactory(PollFactory)
    votes_count = 0
    rate = 0

    class Meta:
        model = Answer