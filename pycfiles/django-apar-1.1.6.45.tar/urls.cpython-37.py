# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/urls/urls.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 405 bytes
from django.conf.urls import url, include
from aparnik.views import install, share
app_name = 'aparnik'
urlpatterns = [
 url('^install$', install, name='install'),
 url('^share/', share, name='share'),
 url('^shops/', include('aparnik.packages.shops.urls.urls', namespace='shops')),
 url('^bank-gateways/', include('aparnik.packages.bankgateways.urls.urls', namespace='bank_gateways'))]