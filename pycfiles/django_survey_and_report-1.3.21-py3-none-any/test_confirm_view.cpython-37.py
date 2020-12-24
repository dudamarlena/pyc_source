# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/views/test_confirm_view.py
# Compiled at: 2020-01-26 12:42:16
# Size of source mod 2**32: 935 bytes
from django.urls.base import reverse
from survey.models import Response, Survey
from survey.tests.base_test import BaseTest

class TestConfirmView(BaseTest):

    def get_first_response(self, survey_name):
        survey = Survey.objects.get(name=survey_name)
        responses = Response.objects.filter(survey=survey)
        response = responses.all()[0]
        url = reverse('survey-confirmation', args=(response.interview_uuid,))
        return self.client.get(url)

    def test_editable_survey(self):
        response = self.get_first_response('Unicode问卷')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'come back and change them')

    def test_uneditable_survey(self):
        response = self.get_first_response('Test survëy')
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, 'come back and change them')