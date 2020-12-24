# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-pages-statistic/facebook_pages_statistic/signals.py
# Compiled at: 2015-10-06 13:48:35
"""
Copyright 2011-2015 ramusus
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from django.dispatch import receiver
from facebook_api.signals import facebook_api_post_fetch
from facebook_pages.models import Page
from .models import PageStatistic

@receiver(facebook_api_post_fetch, sender=Page)
def page_statistic_create(sender, instance, **kwargs):
    if instance.likes_count is None and instance.talking_about_count is None:
        return
    else:
        PageStatistic.objects.create(page=instance, likes_count=instance.likes_count, talking_about_count=instance.talking_about_count)
        return