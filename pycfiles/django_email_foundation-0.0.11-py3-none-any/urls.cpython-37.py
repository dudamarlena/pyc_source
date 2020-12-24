# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/farpi/Workspace/cesc/django-email-foundation/django_email_foundation/urls.py
# Compiled at: 2019-03-15 06:19:17
# Size of source mod 2**32: 317 bytes
from django.urls import path
from django_email_foundation.views import TemplatesPreviewIndex, TemplatePreview
app_name = 'django_email_foundation'
urlpatterns = [
 path('', (TemplatesPreviewIndex.as_view()), name='index'),
 path('preview/<str:folder>/<str:file>/', (TemplatePreview.as_view()), name='preview')]