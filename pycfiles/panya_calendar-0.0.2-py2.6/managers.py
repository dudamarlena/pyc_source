# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cal/managers.py
# Compiled at: 2011-03-28 05:04:09
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import Q

class EntryItemQuerySet(models.query.QuerySet):

    def by_model(self, model):
        """
        Should only return entry items for content of the provided model.
        """
        content_type = ContentType.objects.get_for_model(model)
        return self.filter(content__content_type__exact=content_type)

    def now(self):
        """
        Filters for currently active entry items
        """
        now = datetime.now()
        return self.filter(start__lt=now, end__gt=now)

    def by_date(self, date):
        start = datetime(date.year, date.month, date.day)
        end = start + timedelta(days=1)
        return self.by_range(start, end)

    def by_range(self, start, end):
        return self.exclude(start__gte=end).exclude(end__lte=start)

    def next7days(self):
        start = datetime.now()
        end = start + timedelta(days=7)
        return self.by_range(start, end)

    def thisweekend(self):
        now = datetime.now()
        start = now + timedelta(4 - now.weekday())
        end = now + timedelta(6 - now.weekday())
        result = self.by_range(start, end)
        for item in result:
            if item.start < start:
                item.start = start
            if item.end > end:
                item.end = end

        return result

    def thismonth(self):
        start = datetime.now()
        end = datetime(start.year, start.month + 1, 1)
        return self.by_range(start, end)

    def upcoming(self):
        now = datetime.now()
        return self.exclude(end__lte=now)


class PermittedManager(models.Manager):

    def get_query_set(self):
        queryset = EntryItemQuerySet(self.model)
        queryset = queryset.exclude(calendars__state='unpublished')
        queryset = queryset.exclude(content__state='unpublished')
        if not getattr(settings, 'STAGING', False):
            queryset = queryset.exclude(calendars__state='staging')
            queryset = queryset.exclude(content__state='staging')
        queryset = queryset.filter(calendars__sites__id__exact=settings.SITE_ID)
        queryset = queryset.filter(content__sites__id__exact=settings.SITE_ID)
        return queryset

    def by_model(self, model):
        return self.get_query_set().by_model(model)

    def now(self):
        return self.get_query_set().now()

    def by_date(self, date):
        return self.get_query_set().by_date(date)

    def by_range(self, start, end):
        return self.get_query_set().by_range(start, end)

    def next7days(self):
        return self.get_query_set().next7days()

    def thisweekend(self):
        return self.get_query_set().thisweekend()

    def thismonth(self):
        return self.get_query_set().thismonth()

    def upcoming(self):
        return self.get_query_set().upcoming()