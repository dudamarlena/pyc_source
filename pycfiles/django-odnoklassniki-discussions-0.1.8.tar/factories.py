# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-discussions/odnoklassniki_discussions/factories.py
# Compiled at: 2015-03-06 07:17:02
from odnoklassniki_users.factories import UserFactory
from odnoklassniki_groups.factories import GroupFactory
from models import Discussion, Comment
from datetime import datetime
from random import randrange
import factory

class DiscussionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Discussion
    id = factory.Sequence(lambda n: n)
    date = datetime.now()
    last_activity_date = datetime.now()
    last_user_access_date = datetime.now()
    owner = factory.SubFactory(GroupFactory)
    author = factory.SubFactory(UserFactory)


class CommentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Comment
    id = factory.Sequence(lambda n: n)
    date = datetime.now()
    discussion = factory.SubFactory(DiscussionFactory)
    author = factory.SubFactory(UserFactory)