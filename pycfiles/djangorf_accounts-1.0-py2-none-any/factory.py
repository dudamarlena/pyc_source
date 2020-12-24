# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mass/PythonProjects/oideas/oideas_backend/accounts/tests/factory.py
# Compiled at: 2015-08-17 02:31:54
import factory, random, string
from django.contrib.auth import get_user_model
User = get_user_model()

def get_random_string(length=10):
    return ('u').join(random.choice(string.ascii_letters) for part_of_string in range(length))


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.LazyAttribute(lambda model: get_random_string())
    email = factory.LazyAttribute(lambda model: get_random_string() + '@' + get_random_string())