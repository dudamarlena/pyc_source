# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/key/urls.py
# Compiled at: 2011-08-30 12:21:09
from django.conf.urls.defaults import *
from key.views import *
urlpatterns = patterns('key.views', url('^create_key/$', KeyCreateView.as_view(), name='key.create'), url('^keys/$', KeyListView.as_view(), name='key.list'), url('^delete_key/(?P<key_code>.*)/$', KeyDeleteView.as_view(), name='key.delete'))
import sys
if 'test' in sys.argv:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('', url('^admin/', include(admin.site.urls)))