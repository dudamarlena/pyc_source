# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/managers.py
# Compiled at: 2017-10-20 11:35:08
from django.db import models
from django.contrib.sites.shortcuts import get_current_site
from crum import get_current_request

class PermittedManager(models.Manager):
    """This maneger filters by site."""

    def get_queryset(self):
        queryset = super(PermittedManager, self).get_queryset()
        site = get_current_site(get_current_request())
        queryset = queryset.filter(sites__id__exact=site.id)
        return queryset