# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pielgrzym/work/imaging/git/example_project/imaging/urls.py
# Compiled at: 2012-06-06 15:56:17
from django.conf.urls.defaults import *
urlpatterns = patterns('imaging.views', url('^iframe_form/$', 'iframe_form', name='imaging_iframe_form'), url('^ajax_delete/$', 'ajax_image_removal', name='imaging_image_removal'))