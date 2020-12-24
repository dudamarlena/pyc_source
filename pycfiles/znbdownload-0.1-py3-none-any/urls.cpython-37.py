# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/znbdownload/urls.py
# Compiled at: 2019-07-04 12:11:53
# Size of source mod 2**32: 403 bytes
from django.urls import path
from . import views
app_name = 'znbdownload'
urlpatterns = [
 path('<int:id>/', (views.SecretFileView.as_view()), name='secret_file'),
 path('<int:id>/secret', (views.SecretFileLinkView.as_view()), name='secret_file_link')]