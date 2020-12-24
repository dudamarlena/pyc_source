# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-ads/vkontakte_ads/factories.py
# Compiled at: 2015-02-03 11:31:19
import random, factory
from django.utils import timezone
from vkontakte_api.factories import DjangoModelNoCommitFactory
from . import models

class AccountFactory(factory.DjangoModelFactory):
    remote_id = factory.Sequence(lambda n: n)
    fetched = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Account


class ClientFactory(DjangoModelNoCommitFactory):
    remote_id = factory.Sequence(lambda n: n)
    fetched = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Client


class CampaignFactory(DjangoModelNoCommitFactory):
    remote_id = factory.Sequence(lambda n: n)
    fetched = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.Campaign


class AdFactory(DjangoModelNoCommitFactory):
    remote_id = factory.Sequence(lambda n: n)
    fetched = factory.LazyAttribute(lambda o: timezone.now())
    cpc = bool(random.randint(0, 1))
    cpm = not bool(cpc)

    class Meta:
        model = models.Ad