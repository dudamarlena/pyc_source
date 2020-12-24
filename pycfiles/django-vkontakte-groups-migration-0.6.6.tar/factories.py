# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-vkontakte-groups-migration/vkontakte_groups_migration/factories.py
# Compiled at: 2014-01-27 11:13:34
from vkontakte_groups.factories import GroupFactory
from models import GroupMigration, GroupMembership
from datetime import datetime
import factory

class GroupMigrationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = GroupMigration
    group = factory.SubFactory(GroupFactory)
    time = datetime.now()


class GroupMembershipFactory(factory.DjangoModelFactory):
    FACTORY_FOR = GroupMembership
    group = factory.SubFactory(GroupFactory)
    user_id = factory.Sequence(lambda n: n)
    time_entered = None
    time_left = None