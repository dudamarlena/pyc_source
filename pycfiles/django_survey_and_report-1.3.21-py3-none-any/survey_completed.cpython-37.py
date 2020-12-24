# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/views/survey_completed.py
# Compiled at: 2019-03-02 04:44:34
# Size of source mod 2**32: 437 bytes
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from survey.models import Survey

class SurveyCompleted(TemplateView):
    template_name = 'survey/completed.html'

    def get_context_data(self, **kwargs):
        context = {}
        survey = get_object_or_404(Survey, is_published=True, id=(kwargs['id']))
        context['survey'] = survey
        return context