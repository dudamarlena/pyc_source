# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-vkontakte-groups-statistic/vkontakte_groups_statistic/factories.py
# Compiled at: 2014-11-11 07:26:45
from models import GroupStat
from vkontakte_groups.factories import GroupFactory
import factory, random

class GroupStatFactory(factory.DjangoModelFactory):
    FACTORY_FOR = GroupStat
    group = factory.SubFactory(GroupFactory)
    members = factory.LazyAttribute(lambda o: random.randrange(0, 1000))
    visitors = factory.LazyAttribute(lambda o: random.randrange(0, 1000))