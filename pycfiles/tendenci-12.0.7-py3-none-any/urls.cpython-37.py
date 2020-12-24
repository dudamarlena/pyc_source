# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/tinymce/urls.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 726 bytes
from django.conf.urls import url
from . import views
urlpatterns = [
 url('^js/textareas/(?P<name>.+)/$', (views.textareas_js), name='tinymce-js'),
 url('^js/textareas/(?P<name>.+)/(?P<lang>.*)$', (views.textareas_js), name='tinymce-js-lang'),
 url('^spellchecker/$', (views.spell_check), name='tinymce-spellcheck'),
 url('^flatpages_link_list/$', views.flatpages_link_list),
 url('^compressor/$', (views.compressor), name='tinymce-compressor'),
 url('^filebrowser/$', (views.filebrowser), name='tinymce-filebrowser'),
 url('^preview/(?P<name>.+)/$', (views.preview), name='tinymce-preview')]