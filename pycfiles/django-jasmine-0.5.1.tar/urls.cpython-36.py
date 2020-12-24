# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jake/Github/django-jasmine/django_jasmine/urls.py
# Compiled at: 2017-05-08 17:55:27
# Size of source mod 2**32: 671 bytes
import os
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from .views import DjangoJasmineView
dj_jas_view = DjangoJasmineView.as_view()
urlpatterns = [
 url('^tests/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.JASMINE_TEST_DIRECTORY, 'spec')},
   name='jasmine_test'),
 url('^fixtures/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.JASMINE_TEST_DIRECTORY, 'fixtures')},
   name='jasmine_fixtures'),
 url('^$', dj_jas_view, name='jasmine_default'),
 url('^(?P<version>.*)/$', dj_jas_view, name='jasmine_version')]