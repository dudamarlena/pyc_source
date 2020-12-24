# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/djweed/urls.py
# Compiled at: 2018-03-12 01:56:47
# Size of source mod 2**32: 222 bytes
from django.conf.urls import url
from .views import get_file
urlpatterns = [
 url('^(?P<content_type_id>\\d+)/(?P<object_id>\\d+)/(?P<field_name>[\\w\\_]+)/(?P<file_name>[\\w\\.\\_\\-]*)$', get_file, name='weedfs_get_file')]