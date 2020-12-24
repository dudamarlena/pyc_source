# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/urls.py
# Compiled at: 2017-11-28 02:57:16
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from formfactory.views import FactoryFormView, FactoryFormNoCSRFView, FactoryWizardView
urlpatterns = [
 url('^wizard/(?P<slug>[\\w-]+)(?:/(?P<step>[\\w-]+))?/$', FactoryWizardView.as_view(url_name='formfactory:wizard-detail'), name='wizard-detail'),
 url('^(?P<slug>[-\\w]+)/$', FactoryFormView.as_view(), name='form-detail'),
 url('^nocsrf/(?P<slug>[-\\w]+)/$', csrf_exempt(FactoryFormNoCSRFView.as_view()), name='form-detail-nocsrf')]