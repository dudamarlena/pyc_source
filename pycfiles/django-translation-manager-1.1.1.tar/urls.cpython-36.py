# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/urls.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 568 bytes
from .settings import get_settings
from django.conf.urls import url, include
from .views import SyncView
urlpatterns = [
 url('^sync/$', (SyncView.as_view()), name='sync')]
if get_settings('TRANSLATIONS_PROCESSING_METHOD') == 'async_django_rq':
    urlpatterns.append(url('^django-rq/', include('django_rq.urls')))
if get_settings('TRANSLATIONS_ENABLE_API_COMMUNICATION'):
    from translation_manager import views
    urlpatterns.append(url('^(?P<language>[\\w-]+)/$', (views.TranslationListView.as_view()), name='translations'))