# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anderson/src/django-searchable-select/searchableselect/urls.py
# Compiled at: 2016-11-01 07:35:17
from django.conf.urls import url
try:
    from django.conf.urls import patterns
except ImportError:
    patterns = None

from . import views
urls = [
 url('^filter$', views.filter_models, name='searchable-select-filter')]
if patterns:
    urlpatterns = patterns('', *urls)
else:
    urlpatterns = urls