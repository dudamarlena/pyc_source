# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/views/index_view.py
# Compiled at: 2020-02-25 03:28:52
# Size of source mod 2**32: 630 bytes
from datetime import date
from django.views.generic import TemplateView
from survey.models import Survey

class IndexView(TemplateView):
    template_name = 'survey/list.html'

    def get_context_data(self, **kwargs):
        context = (super(IndexView, self).get_context_data)(**kwargs)
        surveys = Survey.objects.filter(is_published=True,
          expire_date__gte=(date.today()),
          publish_date__lte=(date.today()))
        if not self.request.user.is_authenticated:
            surveys = surveys.filter(need_logged_user=False)
        context['surveys'] = surveys
        return context