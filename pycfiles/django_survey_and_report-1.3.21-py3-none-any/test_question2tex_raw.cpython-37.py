# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/exporter/tex/test_question2tex_raw.py
# Compiled at: 2019-03-02 04:44:34
# Size of source mod 2**32: 509 bytes
from survey.exporter.tex.question2tex_raw import Question2TexRaw
from survey.tests.management.test_management import TestManagement

class TestQuestion2TexRaw(TestManagement):

    def test_raw_tex(self):
        """ We can create a raw chart. """
        question = self.survey.questions.get(text='Aèbc?')
        expected = ['1é', '1', '1a', '1b', '1e', '1ë']
        container = Question2TexRaw(question).tex()
        for i in expected:
            self.assertIn(i, container)