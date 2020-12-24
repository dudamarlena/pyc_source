# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/show/urls.py
# Compiled at: 2010-08-24 03:41:55
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('show.views', url('^radioshow/entrylist/$', 'radioshow_entryitem_list', name='radioshow_entryitem_list'), url('^showcontributor/list/(?P<slug>[\\w-]+)/$', 'showcontributor_content_list', name='showcontributor_content_list'), url('^showcontributor/appearance/(?P<slug>[\\w-]+)/$', 'showcontributor_appearance_list', name='showcontributor_appearance_list'), url('^showcontributor/(?P<slug>[\\w-]+)/$', 'showcontributor_detail', name='showcontributor_detail'), url('^showcontributor/content/(?P<slug>[\\w-]+)/$', 'showcontributor_content_detail', name='showcontributor_content_detail'), url('^showcontributor/contact/(?P<slug>[\\w-]+)/$', 'showcontributor_contact', name='showcontributor_contact'))