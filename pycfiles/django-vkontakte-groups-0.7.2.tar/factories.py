# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-groups/vkontakte_groups/factories.py
# Compiled at: 2015-01-25 08:07:39
import factory
from .models import Group

class GroupFactory(factory.DjangoModelFactory):
    remote_id = factory.Sequence(lambda n: n)

    class Meta:
        model = Group