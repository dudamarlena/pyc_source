# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/urls.py
# Compiled at: 2019-09-02 09:54:35
# Size of source mod 2**32: 448 bytes
from django.urls import path
from common import views
namespace = 'common'
app_name = 'common'
urlpatterns = [
 path('cache/', (views.view_cache), name='cache'),
 path('scripts.js', (views.scripts), name='scripts')]
urls = (
 urlpatterns, namespace, app_name)
try:
    from rest_framework.schemas import get_schema_view
    urlpatterns.append(path('schema/', get_schema_view()))
except (AssertionError, ImportError):
    pass