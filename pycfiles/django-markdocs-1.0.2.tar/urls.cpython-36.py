# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amarkey/projects/markdoc_project/markdocs/urls.py
# Compiled at: 2018-03-15 15:04:15
# Size of source mod 2**32: 292 bytes
from django.urls import path
from . import views
app_name = 'markdocs'
urlpatterns = [
 path('', (views.MarkdocsView.as_view()), name='index'),
 path('<document>', (views.MarkdocsView.as_view()), name='document'),
 path('<document>/', (views.MarkdocsView.as_view()), name='document')]