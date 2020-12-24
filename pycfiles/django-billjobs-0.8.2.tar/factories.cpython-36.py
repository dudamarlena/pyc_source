# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/factories.py
# Compiled at: 2018-06-27 08:22:15
# Size of source mod 2**32: 1509 bytes
import factory, factory.fuzzy, factory.django
from django.contrib.auth.models import User
from django.db.models.signals import post_save

@factory.django.mute_signals(post_save)
class UserProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'billjobs.UserProfile'

    billing_address = factory.Faker('address')
    user = factory.SubFactory('billjobs.tests.factories.UserFactory',
      profile=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username', )

    username = 'steve'
    password = 'gates'
    first_name = 'Steve'
    last_name = 'Gates'
    email = 'steve.gates@billjobs.org'
    userprofile = factory.RelatedFactory(UserProfileFactory, 'user')


class SuperUserFactory(UserFactory):
    username = 'bill'
    password = 'jobs'
    first_name = 'Bill'
    last_name = 'Jobs'
    email = 'bill.jobs@billjobs.org'
    is_staff = True
    is_superuser = True


class ServiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'billjobs.Service'

    reference = factory.Sequence(lambda n: 'SE%03d' % n)
    price = factory.fuzzy.FuzzyInteger(100, 200, 10)


class BillFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'billjobs.Bill'
        django_get_or_create = ('user', )

    user = factory.SubFactory(UserFactory)
    amount = factory.fuzzy.FuzzyInteger(100, 200, 10)