# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/projects/pythonunited/provgroningen/buildout/src/djinn_core/djinn_core/urls.py
# Compiled at: 2014-12-08 04:48:46
from django.conf.urls import patterns, include, url
from views.admin import AdminView
_urlpatterns = patterns('', url('^djinn_admin/?$', AdminView.as_view(), name='djinn_admin'))
urlpatterns = patterns('', (
 '^djinn/', include(_urlpatterns)))