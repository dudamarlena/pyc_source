# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bas/dev/django-dmarc/dmarc/urls.py
# Compiled at: 2018-06-18 16:39:43
# Size of source mod 2**32: 576 bytes
"""
DMARC urls
http://dmarc.org/resources/specification/
"""
from django.conf.urls import url
from dmarc import views
app_name = 'dmarc'
urlpatterns = [
 url('^report/$', (views.dmarc_report), name='dmarc_report'),
 url('^report/csv/$', (views.dmarc_csv), name='dmarc_csv'),
 url('^report/json/$', (views.dmarc_json), name='dmarc_json')]