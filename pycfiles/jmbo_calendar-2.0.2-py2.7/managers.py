# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_calendar/managers.py
# Compiled at: 2016-03-08 06:26:36
from datetime import datetime, timedelta
from django.db.models.query import Q
from django.utils import timezone
from jmbo import managers

class CoordinatorManager(managers.PermittedManager):

    def upcoming(self):
        qs = super(CoordinatorManager, self).get_query_set()
        now = timezone.now()
        return qs.exclude(Q(end__lte=now) & (Q(repeat='does_not_repeat') | ~Q(repeat_until=None) & Q(repeat_until__lt=now.date())))