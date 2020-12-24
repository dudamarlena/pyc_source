# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-wall-statistic/vkontakte_wall_statistic/factories.py
# Compiled at: 2015-03-06 07:14:17
from models import PostStatistic
from vkontakte_wall.factories import PostFactory
import factory

class PostStatisticFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PostStatistic
    post = factory.SubFactory(PostFactory)