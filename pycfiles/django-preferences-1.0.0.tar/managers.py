# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-preferences/preferences/managers.py
# Compiled at: 2018-12-20 02:32:17
from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site

class SingletonManager(models.Manager):
    """
    Returns only a single preferences object per site.
    """

    def get_queryset(self):
        """
        Return the first preferences object for the current site.
        If preferences do not exist create it.
        """
        queryset = super(SingletonManager, self).get_queryset()
        current_site = None
        if getattr(settings, 'SITE_ID', None) is not None:
            current_site = Site.objects.get_current()
        if current_site is not None:
            queryset = queryset.filter(sites=settings.SITE_ID)
        if not queryset.exists():
            obj = self.model.objects.create()
            if current_site is not None:
                obj.sites.add(current_site)
        return queryset