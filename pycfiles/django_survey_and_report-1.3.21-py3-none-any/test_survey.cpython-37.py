# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/models/test_survey.py
# Compiled at: 2020-02-25 03:12:20
# Size of source mod 2**32: 1317 bytes
from datetime import date
from django.utils.timezone import now
from survey.tests.models import BaseModelTest

class TestSurvey(BaseModelTest):

    def test_unicode(self):
        """ Unicode generation. """
        self.assertIsNotNone(str(self.survey))

    def test_questions(self):
        """ Recovering a list of questions from a survey. """
        questions = self.survey.questions.all()
        self.assertEqual(len(questions), len(self.data))

    def test_absolute_url(self):
        """ Absoulte url is not None and do not raise error. """
        self.assertIsNotNone(self.survey.get_absolute_url())

    def test_latest_answer(self):
        """ the lastest answer date is returned. """
        self.assertIsInstance(self.survey.latest_answer_date(), date)

    def test_publish_date(self):
        """ the pblish date must be None or datetime date instance. """
        self.assertIsInstance(self.survey.publish_date, date)

    def test_expiration_date(self):
        """ expirationdate must be datetime date instance or None """
        self.assertIsInstance(self.survey.expire_date, date)

    def test_expiration_date_is_in_future(self):
        """ by default the expiration should be a week in the future """
        self.assertGreater(self.survey.expire_date, now())