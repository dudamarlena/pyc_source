# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gallery/admin_urls.py
# Compiled at: 2016-03-08 06:27:04
from django.conf.urls import patterns, url
urlpatterns = patterns('', url('^gallery/gallery/(?P<gallery_id>\\d+)/bulk-image-upload/$', 'gallery.admin_views.bulk_image_upload', {}, name='gallery-bulk-image-upload'))