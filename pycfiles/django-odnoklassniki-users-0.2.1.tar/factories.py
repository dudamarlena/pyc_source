# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-users/odnoklassniki_users/factories.py
# Compiled at: 2015-03-06 07:16:55
from models import User
from datetime import datetime
import factory, random

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    id = factory.Sequence(lambda n: n)
    gender = random.choice([1, 2])
    registered_date = datetime.now()