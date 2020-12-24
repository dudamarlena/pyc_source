# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/panya/managers.py
# Compiled at: 2011-05-26 02:47:52
from django.conf import settings
from django.db import models

class PermittedManager(models.Manager):

    def get_query_set(self):
        queryset = super(PermittedManager, self).get_query_set().exclude(state='unpublished')
        if not getattr(settings, 'STAGING', False):
            queryset = queryset.exclude(state='staging')
        queryset = queryset.filter(sites__id__exact=settings.SITE_ID)
        return queryset