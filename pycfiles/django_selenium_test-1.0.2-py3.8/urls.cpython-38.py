# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/urls.py
# Compiled at: 2020-04-15 06:20:40
# Size of source mod 2**32: 970 bytes
from __future__ import annotations
from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from .views import DownloadView, SampleFormView
urlpatterns = [
 path('core/', TemplateView.as_view(template_name='core.html'), name='core'),
 path('integration/', (SampleFormView.as_view()), name='integration'),
 path('integration/submit/',
   TemplateView.as_view(template_name='integration.html'),
   name='integrationsubmit'),
 path('integration/parameter/<int:parameter>/',
   TemplateView.as_view(template_name='integration.html'),
   name='integrationparams'),
 path('integration/redirect/',
   RedirectView.as_view(pattern_name='integration'),
   name='integrationredirect'),
 path('integration/file/', (DownloadView.as_view()), name='integrationdownload')]