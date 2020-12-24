# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/views/survey_detail.py
# Compiled at: 2020-02-25 03:28:52
# Size of source mod 2**32: 4437 bytes
import logging
from datetime import date
from django.conf import settings
from django.shortcuts import Http404, get_object_or_404, redirect, render, reverse
from django.views.generic import View
from survey.forms import ResponseForm
from survey.models import Category, Survey
LOGGER = logging.getLogger(__name__)

class SurveyDetail(View):

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404((Survey.objects.prefetch_related('questions', 'questions__category')),
          is_published=True, id=(kwargs['id']))
        if not survey.is_published:
            raise Http404
        if survey.expire_date < date.today():
            raise Http404
        if survey.publish_date > date.today():
            raise Http404
        step = kwargs.get('step', 0)
        if survey.template is not None and len(survey.template) > 4:
            template_name = survey.template
        else:
            if survey.display_by_question:
                template_name = 'survey/survey.html'
            else:
                template_name = 'survey/one_page_survey.html'
        if survey.need_logged_user:
            if not request.user.is_authenticated:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        categories = Category.objects.filter(survey=survey).order_by('order')
        form = ResponseForm(survey=survey, user=(request.user), step=step)
        context = {'response_form':form,  'survey':survey,  'categories':categories,  'step':step}
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, is_published=True, id=(kwargs['id']))
        if survey.need_logged_user:
            if not request.user.is_authenticated:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        categories = Category.objects.filter(survey=survey).order_by('order')
        form = ResponseForm((request.POST), survey=survey, user=(request.user), step=(kwargs.get('step', 0)))
        if not survey.editable_answers:
            if form.response is not None:
                LOGGER.info('Redirects to survey list after trying to edit non editable answer.')
                return redirect(reverse('survey-list'))
        context = {'response_form':form, 
         'survey':survey,  'categories':categories}
        if form.is_valid():
            return self.treat_valid_form(form, kwargs, request, survey)
        return self.handle_invalid_form(context, form, request, survey)

    @staticmethod
    def handle_invalid_form(context, form, request, survey):
        LOGGER.info('Non valid form: <%s>', form)
        if survey.template is not None and len(survey.template) > 4:
            template_name = survey.template
        else:
            if survey.display_by_question:
                template_name = 'survey/survey.html'
            else:
                template_name = 'survey/one_page_survey.html'
        return render(request, template_name, context)

    def treat_valid_form(self, form, kwargs, request, survey):
        session_key = 'survey_%s' % (kwargs['id'],)
        if session_key not in request.session:
            request.session[session_key] = {}
        else:
            for key, value in list(form.cleaned_data.items()):
                request.session[session_key][key] = value
                request.session.modified = True

            next_url = form.next_step_url()
            response = None
            if survey.display_by_question:
                if not form.has_next_step():
                    save_form = ResponseForm((request.session[session_key]), survey=survey, user=(request.user))
                    if save_form.is_valid():
                        response = save_form.save()
                    else:
                        LOGGER.warning('A step of the multipage form failed but should have been discovered before.')
            else:
                response = form.save()
        if next_url is not None:
            return redirect(next_url)
        del request.session[session_key]
        if response is None:
            return redirect(reverse('survey-list'))
        next_ = request.session.get('next', None)
        if next_ is not None:
            if 'next' in request.session:
                del request.session['next']
            return redirect(next_)
        return redirect('survey-confirmation', uuid=(response.interview_uuid))