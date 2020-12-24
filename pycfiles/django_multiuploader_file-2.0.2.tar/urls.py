# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matheus/Documents/projects/enki/Admin-Django/msk/multiuploader/urls.py
# Compiled at: 2013-04-04 15:38:21
from django.conf.urls.defaults import *
from django.conf import settings
try:
    delete_url = settings.MULTI_FILE_DELETE_URL
except AttributeError:
    delete_url = 'multi_delete'

try:
    image_url = settings.MULTI_IMAGE_URL
except AttributeError:
    image_url = 'multi_image'

urlpatterns = patterns('', url('^' + delete_url + '/(\\d+)/$', 'multiuploader.views.multiuploader_delete'), url('^multi/$', 'multiuploader.views.multiuploader', name='multi'), url('^' + image_url + '/(\\d+)/$', 'multiuploader.views.multi_show_uploaded'))