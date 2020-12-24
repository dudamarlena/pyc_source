# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/receivers/savedsearch.py
# Compiled at: 2019-08-16 12:27:40
from __future__ import absolute_import, print_function
from django.db.models.signals import post_save
from sentry.models import Project, SavedSearch
from sentry.models.savedsearch import DEFAULT_SAVED_SEARCHES

def create_default_saved_searches(instance, created=True, **kwargs):
    if not created:
        return
    for search_kwargs in DEFAULT_SAVED_SEARCHES:
        SavedSearch.objects.create(project=instance, **search_kwargs)


post_save.connect(create_default_saved_searches, sender=Project, dispatch_uid='create_default_saved_searches', weak=False)