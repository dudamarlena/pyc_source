# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/repos/django-composer/composer/urls.py
# Compiled at: 2015-08-31 13:00:30
# Size of source mod 2**32: 404 bytes
"""
urls.py
"""
from django.conf.urls import patterns, url
from django.conf import settings
from .views import EditComposerElementView, ExampleView
urlpatterns = patterns('', url('edit/(?P<pk>[\\d]+)$', EditComposerElementView.as_view(), name='composer-edit-element'))
if settings.DEBUG:
    urlpatterns += (
     url('example/', ExampleView.as_view(), name='composer-example'),)