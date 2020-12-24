# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maintenance_in_progress/tests/urls.py
# Compiled at: 2014-11-11 03:11:26
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
urlpatterns = patterns('', url('^mip-error/$', TemplateView.as_view(template_name='error.html'), name='mip-error'))
handler500 = 'maintenance_in_progress.views.server_error'