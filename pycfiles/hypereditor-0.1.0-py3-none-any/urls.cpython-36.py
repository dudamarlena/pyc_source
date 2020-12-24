# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shimul/Projects/django-hyper-editor/hypereditor/urls.py
# Compiled at: 2019-04-09 11:30:09
# Size of source mod 2**32: 301 bytes
from django.conf.urls import include, url
from hypereditor.views import *
app_name = 'hypereditor'
urlpatterns = [
 url('editor/$', (EditorView.as_view()), name='editor'),
 url('preview/', (PreviewView.as_view()), name='preview'),
 url('js/blocks', (GenerateBlock.as_view()), name='blocks')]