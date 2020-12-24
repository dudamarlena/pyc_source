# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/DjangoProjects/basitapi/basitapi/tests/factories.py
# Compiled at: 2013-01-17 09:17:31
import factory
from django.contrib.auth.models import User

class UserFactory(factory.Factory):
    FACTORY_FOR = User
    id = factory.Sequence(lambda a: int(a) + 1)
    username = factory.Sequence(lambda a: 'username%d' % (int(a) + 1))
    password = factory.Sequence(lambda a: 'password%d' % (int(a) + 1))

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user