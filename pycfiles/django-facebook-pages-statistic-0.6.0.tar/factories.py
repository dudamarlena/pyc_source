# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-pages-statistic/facebook_pages_statistic/factories.py
# Compiled at: 2015-03-06 07:16:08
from django.utils import timezone
from facebook_pages.factories import PageFactory
from models import PageStatistic
import factory, random

class PageStatisticFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PageStatistic
    page = factory.SubFactory(PageFactory)
    likes_count = factory.LazyAttribute(lambda o: random.randint(0, 10000))
    talking_about_count = factory.LazyAttribute(lambda o: random.randint(0, 10000))
    updated_at = factory.LazyAttribute(lambda o: timezone.now())