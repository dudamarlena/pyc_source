# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/forman/urls.py
# Compiled at: 2017-05-08 12:16:33
from django.conf.urls import url, include
import views
urlpatterns = [url('^survey/(?P<survey_id>[0-9]+)\\/submit$', views.submit, name='submit'),
 url('^survey/(?P<survey_id>[0-9]+)\\/download?', views.download_csv, name='download'),
 url('^survey/(?P<survey_id>[0-9]+)\\/?', views.preview_survey, name='preview')]