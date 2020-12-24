# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/urls.py
# Compiled at: 2016-07-04 06:45:25
# Size of source mod 2**32: 651 bytes
from django.conf.urls import url
from .views import IndexView
from .views import AboutView
from .views.admin import select2_contenttypes_view
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'
urlpatterns = [
 url('^$', name='index', view=IndexView.as_view()),
 url('^about/', name='about', view=AboutView.as_view()),
 url('^select2\\-(?P<content_type>[a-z]+)\\-list/$', name='select2_contenttypes_list', view=select2_contenttypes_view)]
handler403 = 'hacs.views.errors.permission_denied'
handler404 = 'hacs.views.errors.page_not_found'