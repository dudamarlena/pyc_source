# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/factories.py
# Compiled at: 2016-03-10 19:09:28
# Size of source mod 2**32: 605 bytes
import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
Account = get_user_model()

class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Account

    email = factory.Sequence(lambda n: 'email{0}@email.com'.format(n))
    is_staff = False
    is_active = True
    date_joined = timezone.now()
    passwordless_key = '12345'


class AdminFactory(AccountFactory):
    is_staff = True


class PasswordlessAccountFactory(AccountFactory):
    password = '!abcdefghijklmnopqrstuvwxyzabcdefghiklmn'
    passwordless_key = '12345'