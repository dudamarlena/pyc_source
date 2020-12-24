# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-ads/vkontakte_ads/signals.py
# Compiled at: 2015-01-25 02:59:17
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from models import Targeting, Ad
if 'vkontakte_places' in settings.INSTALLED_APPS:
    from vkontakte_places.models import City

    @receiver(post_save, sender=Targeting)
    def fetch_cities_for_targeting(sender, instance, created, **kwargs):
        if instance.cities:
            City.remote.fetch(ids=instance.cities.split(','))
        if instance.cities_not:
            City.remote.fetch(ids=instance.cities_not.split(','))


if 'vkontakte_groups' in settings.INSTALLED_APPS:
    from vkontakte_groups.models import Group

    @receiver(post_save, sender=Targeting)
    def fetch_cities_for_targeting(sender, instance, created, **kwargs):
        if instance.groups:
            Group.remote.fetch(ids=instance.groups.split(','))