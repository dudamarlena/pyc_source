# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gthomas/dev/management-server/managementserver/django_sql_dashboards/context_processors.py
# Compiled at: 2014-02-16 11:51:21
from django.conf import settings

def prefix(request):
    return {'SQL_DASHBOARDS_PREFIX': settings.SQL_DASHBOARDS_PREFIX}