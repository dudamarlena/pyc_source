# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/urls.py
# Compiled at: 2020-01-26 10:04:58
# Size of source mod 2**32: 692 bytes
from django.conf.urls import url
from survey.views import ConfirmView, IndexView, SurveyCompleted, SurveyDetail
from survey.views.survey_result import serve_result_csv
urlpatterns = [
 url('^$', (IndexView.as_view()), name='survey-list'),
 url('^(?P<id>\\d+)/', (SurveyDetail.as_view()), name='survey-detail'),
 url('^csv/(?P<primary_key>\\d+)/', serve_result_csv, name='survey-result'),
 url('^(?P<id>\\d+)/completed/', (SurveyCompleted.as_view()), name='survey-completed'),
 url('^(?P<id>\\d+)-(?P<step>\\d+)/', (SurveyDetail.as_view()), name='survey-detail-step'),
 url('^confirm/(?P<uuid>\\w+)/', (ConfirmView.as_view()), name='survey-confirmation')]