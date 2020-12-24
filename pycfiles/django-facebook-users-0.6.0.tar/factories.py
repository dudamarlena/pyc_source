# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-users/facebook_users/factories.py
# Compiled at: 2015-03-06 07:15:54
from models import User
import factory, random

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    graph_id = factory.Sequence(lambda n: n)
    gender = random.choice(['male', 'female'])