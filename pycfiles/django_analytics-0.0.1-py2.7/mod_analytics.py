# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/analytics/mod_analytics.py
# Compiled at: 2011-05-24 10:07:46
from django.contrib.auth.models import User
from analytics.basemetric import BaseMetric

class Registrations(BaseMetric):
    """
    Monitors the number of new user signups.
    """
    uid = 'registrations'
    title = 'Registrations'

    def calculate(self, start_datetime, end_datetime):
        return User.objects.filter(date_joined__gte=start_datetime, date_joined__lt=end_datetime).count()

    def get_earliest_timestamp(self):
        try:
            return User.objects.order_by('date_joined')[0].date_joined
        except IndexError:
            return

        return