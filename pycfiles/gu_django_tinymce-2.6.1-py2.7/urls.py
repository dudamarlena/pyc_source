# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Bucket/projects/tinymce/gu-django-tinymce/tinymce/urls.py
# Compiled at: 2016-04-21 01:35:11
from django.conf.urls import url
from tinymce import views
urlpatterns = [
 url('^spellchecker/$', views.spell_check),
 url('^flatpages_link_list/$', views.flatpages_link_list),
 url('^compressor/$', views.compressor, name='tinymce-compressor'),
 url('^filebrowser/$', views.filebrowser, name='tinymce-filebrowser'),
 url('^filebrowserPath/$', views.filebrowserPath, name='tinymce-filebrowser-path')]