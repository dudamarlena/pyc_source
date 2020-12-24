# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/atulvarma/Documents/18f/django-uswds-forms/example/example/urls.py
# Compiled at: 2017-05-12 10:02:32
# Size of source mod 2**32: 187 bytes
from django.conf.urls import url
from app import views
urlpatterns = [
 url('^$', (views.home), name='home'),
 url('^example/([0-9A-Za-z\\-]+)', (views.example), name='example')]