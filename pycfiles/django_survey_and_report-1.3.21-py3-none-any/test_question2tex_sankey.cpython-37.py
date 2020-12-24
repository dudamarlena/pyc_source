# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/exporter/tex/test_question2tex_sankey.py
# Compiled at: 2020-02-25 02:49:28
# Size of source mod 2**32: 1192 bytes
from survey.exporter.tex.question2tex_sankey import Question2TexSankey
from survey.tests.management.test_management import TestManagement

class TestQuestion2TexSankey(TestManagement):

    def test_other_question_type(self):
        """ We get a type error if we do not give a Question. """
        question = self.survey.questions.get(text='Aèbc?')
        self.assertRaises(TypeError, Question2TexSankey.__init__, question, {'other_question': 'other_question'})
        other_question = self.survey.questions.get(text='Aèbc?')
        q2s = Question2TexSankey(question, other_question=other_question)
        self.assertIsNotNone(q2s.tex())