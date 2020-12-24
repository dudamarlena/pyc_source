# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/metaimage/urls.py
# Compiled at: 2011-02-23 23:41:04
from django.conf.urls.defaults import patterns, url, handler404, handler500
urlpatterns = patterns('', url('^$', 'metaimage.views.show_metaimages', name='show_metaimages'), url('^details/(?P<id>\\d+)/$', 'metaimage.views.metaimage_details', name='metaimage_details'), url('^edit/(?P<id>\\d+)/$', 'metaimage.views.edit_metaimage', name='edit_metaimage'), url('^upload/$', 'metaimage.views.upload_metaimage', name='upload_metaimage'), url('^yours/$', 'metaimage.views.your_metaimages', name='your_metaimages'), url('^user/(?P<username>[\\w]+)/$', 'metaimage.views.show_user_metaimages', name='show_user_metaimages'), url('^destroy/(?P<id>\\d+)/$', 'metaimage.views.destroy_metaimage', name='destroy_metaimage'))