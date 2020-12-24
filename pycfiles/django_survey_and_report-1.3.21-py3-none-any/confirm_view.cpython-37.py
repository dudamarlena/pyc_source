# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/views/confirm_view.py
# Compiled at: 2020-01-26 11:18:54
# Size of source mod 2**32: 444 bytes
from django.views.generic import TemplateView
from survey.models import Response

class ConfirmView(TemplateView):
    template_name = 'survey/confirm.html'

    def get_context_data(self, **kwargs):
        context = (super(ConfirmView, self).get_context_data)(**kwargs)
        context['uuid'] = kwargs['uuid']
        context['response'] = Response.objects.get(interview_uuid=(kwargs['uuid']))
        return context