# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/ui/components/select/urls.py
# Compiled at: 2019-03-07 14:51:35
# Size of source mod 2**32: 382 bytes
from django.conf.urls import url
from djangoplus.ui.components.select import views
urlpatterns = [
 url('^autocomplete/(?P<app_name>\\w+)/(?P<class_name>\\w+)/$', views.autocomplete),
 url('^reload_options/(?P<app_name>\\w+)/(?P<class_name>\\w+)/(?P<current_value>\\w+)/(?P<lookup>\\w+)/(?P<selected_value>\\w+)/(?P<lazy>\\w+)/$', views.reload_options)]