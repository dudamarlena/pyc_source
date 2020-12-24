# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/daarmaan/daarmaan/server/urls.py
# Compiled at: 2012-10-16 13:11:42
from django.conf.urls import patterns, include, url
from daarmaan.server.views.sso import daarmaan_service
from daarmaan.server.views.index import index_page
from daarmaan.server.views.profile import profile
urlpatterns = patterns('', url('^gstatics/$', 'daarmaan.server.views.statics.serv_statics', name='statics-serv'), url('^jsonp/validate/$', 'daarmaan.server.views.statics.ajax_widget_jsonp', name='ajax-widget-jsonp'), url('^me/', include(profile.urls)), url('^\\~([A-Za-z][^/]+)/$', profile.view_profile, name='view_user_profile'), url('^', include(index_page.urls)), url('^', include(daarmaan_service.urls)))