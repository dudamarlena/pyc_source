# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/urls.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 243 bytes
from django.conf.urls import url, include
from ovp_core import views
urlpatterns = [
 url('^startup/$', views.startup, name='startup'),
 url('^contact/$', views.contact, name='contact'),
 url('^lead/$', views.record_lead, name='lead')]