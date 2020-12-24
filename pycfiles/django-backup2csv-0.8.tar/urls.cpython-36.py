# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mmandrille/Secundario/Dropbox/GitLab/escrutinio/escrutinio/backups/urls.py
# Compiled at: 2019-06-02 17:36:27
# Size of source mod 2**32: 400 bytes
from django.conf.urls import url
from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
 path('', (views.select_app), name='select_app'),
 path('select_models/<str:app_name>', (views.select_models), name='select_models'),
 path('dw/<str:app_name>', (views.download), name='download'),
 path('up/<str:app_name>', (views.restore), name='restore')]