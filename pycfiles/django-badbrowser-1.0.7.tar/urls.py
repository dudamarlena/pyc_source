# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/dev/.virtualenvs/playnicely/src/django-badbrowser/django_badbrowser/urls.py
# Compiled at: 2012-03-16 06:30:06
from django.conf.urls.defaults import *
from django_badbrowser.views import ignore, unsupported
urlpatterns = patterns('', url('^$', unsupported, name='django-badbrowser-unsupported'), url('^ignore/$', ignore, name='django-badbrowser-ignore'))