# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-groups/odnoklassniki_groups/factories.py
# Compiled at: 2015-03-06 07:16:49
from models import Group
import factory, random

class GroupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Group
    id = factory.Sequence(lambda n: n)
    members_count = random.randrange(0, 10000)