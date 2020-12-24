# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-paymecash/paymecash/urls.py
# Compiled at: 2013-09-11 00:20:43
from django.conf.urls import patterns, url
from .views import Confirm
urlpatterns = patterns('', url('^confirm/$', Confirm.as_view(), name='paymentcash_confirm'))