# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/models/test_answer.py
# Compiled at: 2020-01-26 10:04:57
# Size of source mod 2**32: 840 bytes
from django.core.exceptions import ValidationError
from survey.models import Answer
from survey.tests.models import BaseModelTest

class TestAnswer(BaseModelTest):

    def test_unicode(self):
        """ Unicode generation. """
        for answer in self.answers:
            self.assertIsNotNone(str(answer))

    def test_init(self):
        """ We raise validation error if the answer is not a possible choice"""
        self.assertRaises(ValidationError, Answer, response=(self.response), question=(self.questions[4]), body='Dd')

    def test_values(self):
        """ We can have multiple nasty values ans it will be detected. """
        self.assertEqual(self.answers[0].values, ['Mytext'])
        self.assertEqual(self.answers[4].values, ['Yes'])
        self.assertEqual(self.answers[6].values, ['2', '4'])