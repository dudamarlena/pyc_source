# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/urls.py
# Compiled at: 2018-02-10 07:51:58
# Size of source mod 2**32: 403 bytes
from django.conf.urls import url
from django_files_library import views
urlpatterns = [
 url('^file/downaload-file/(\\d+)/(.+)', (views.download_file), name='django_files_library_download_file'),
 url('^file/add/(?P<library_id>\\d+)/', (views.add_file), name='django_files_library_add_file'),
 url('^file/delete/(?P<file_id>\\d+)/', (views.delete_file), name='django_files_library_delete_file')]