# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/test_survey_auth_required.py
# Compiled at: 2020-01-26 12:52:24
# Size of source mod 2**32: 2110 bytes
from django.conf import settings
from django.urls.base import reverse
from survey.models import Response, Survey
from survey.tests import BaseTest

class TestSurveyAuthRequired(BaseTest):
    __doc__ = ' Permit to check if need_logged_user is working as intended. '

    def assert_accessible(self, url):
        """ Assert that everything is accessible. """
        try:
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.login()
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.logout()
        except Exception as exc:
            try:
                exc.args += (url,)
                raise
            finally:
                exc = None
                del exc

    def test_need_login(self):
        """ If a survey has need_logged_user=True user need to authenticate."""
        urls = [
         reverse('survey-detail', kwargs={'id': 1}),
         reverse('survey-completed', kwargs={'id': 1}),
         reverse('survey-detail-step', kwargs={'id':1,  'step':1})]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(settings.LOGIN_URL in response['location'])
            self.login()
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.logout()

    def test_accessible(self):
        """ If need_logged_user=False user do not need to authenticate. """
        survey = Survey.objects.get(id=2)
        responses = Response.objects.filter(survey=survey)
        response = responses.all()[0]
        urls = [
         reverse('survey-list'),
         reverse('survey-detail', kwargs={'id': 2}),
         reverse('survey-completed', kwargs={'id': 2}),
         reverse('survey-detail-step', kwargs={'id':2,  'step':1}),
         reverse('survey-confirmation', kwargs={'uuid': response.interview_uuid})]
        for url in urls:
            self.assert_accessible(url)