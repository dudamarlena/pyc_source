# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/views/test_survey_result.py
# Compiled at: 2019-09-21 05:02:58
# Size of source mod 2**32: 1165 bytes
from django.urls.base import reverse
from survey.tests.management.test_management import TestManagement

class TestSurveyResult(TestManagement):

    def test_survey_result(self):
        """ We need logging for survey result if the survey need login. """
        url = reverse('survey-result', args=(2, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('survey-result', args=(1, )))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('survey-result', args=(4, )), follow=True)
        try:
            _, status_code = response.redirect_chain[(-1)]
        except IndexError:
            status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertContains(response, 'This survey has not been published')
        self.login()
        response = self.client.get(reverse('survey-result', args=(2, )))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('survey-result', args=(1, )))
        self.assertEqual(response.status_code, 200)