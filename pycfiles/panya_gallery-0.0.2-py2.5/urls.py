# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gallery/urls.py
# Compiled at: 2010-07-19 06:54:12
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('gallery.views', url('^list/$', 'object_list', name='gallery_object_list'), url('^(?P<slug>[\\w-]+)/$', 'object_detail', name='gallery_object_detail'), url('^item/ajax/galleriffic/(?P<slug>[\\w-]+)/$', 'gallery_item_ajax_galleriffic', name='gallery_item_ajax_galleriffic'))