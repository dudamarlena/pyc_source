# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/conf/urls/shortcut.py
# Compiled at: 2018-07-11 18:15:30
from django.conf.urls import patterns
urlpatterns = patterns('django.views', ('^(?P<content_type_id>\\d+)/(?P<object_id>.*)/$',
                                        'defaults.shortcut'))