# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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