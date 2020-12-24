# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-intel/egg/tumbledore/urls.py
# Compiled at: 2012-08-24 17:56:34
from django.conf.urls.defaults import *
urlpatterns = patterns('tumbledore.views', url('^tumblelog/widget/(?P<widget_id>[\\d]+).js$', 'widget', name='tumble_widget'), url('^(?P<mount_point>[\\d\\w\\/_\\-]*)/post/(?P<slug>[\\w\\d_\\-]+)/$', 'post', name='tumble_post'), url('^(?P<mount_point>[\\d\\w\\/_\\-]*)/$', 'index', name='tumble_index'))