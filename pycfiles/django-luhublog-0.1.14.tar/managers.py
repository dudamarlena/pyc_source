# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johsanca/Projects/luhu-blog-app/luhublog/managers.py
# Compiled at: 2015-10-20 16:35:47
from django.db import models
from django.utils import timezone

def entries_published(queryset):
    """
        Return only the entries published.
        """
    now = timezone.now()
    return queryset.filter(models.Q(start_publication__lte=now) | models.Q(start_publication=None), status='PUBLISHED')


class EntryPublishedManager(models.Manager):
    """
        Manager to retrieve published entries.
        """

    def get_queryset(self):
        """
                Return published entries.
                """
        return entries_published(super(EntryPublishedManager, self).get_queryset())