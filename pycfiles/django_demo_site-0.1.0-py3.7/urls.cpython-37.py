# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\demo_site\urls.py
# Compiled at: 2018-10-03 10:44:20
# Size of source mod 2**32: 186 bytes
from django.urls import path
from demo_site.views import demo_site_index
app_name = 'demo_site'
urlpatterns = [
 path('', demo_site_index, name='index')]