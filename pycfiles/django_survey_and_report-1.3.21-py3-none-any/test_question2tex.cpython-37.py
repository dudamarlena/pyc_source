# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/exporter/tex/test_question2tex.py
# Compiled at: 2019-03-02 04:44:34
# Size of source mod 2**32: 910 bytes
from survey.exporter.tex.question2tex import Question2Tex
from survey.tests.management.test_management import TestManagement

class TestQuestion2Tex(TestManagement):

    def test_html2latex(self):
        """ We correctly translate a question to the latex equivalent. """
        translation = Question2Tex.html2latex('&lt;filetype&gt; ?')
        self.assertEqual('<filetype> ?', translation)
        translation = Question2Tex.html2latex('Is <strong>42</strong> true ?')
        self.assertEqual('Is \\textbf{42} true ?', translation)
        translation = Question2Tex.html2latex('<code>is(this).sparta</code>?')
        self.assertEqual('$is(this).sparta$?', translation)

    def test_tex(self):
        """ Question2Tex.tex() is abstract. """
        question = self.survey.questions.get(text='Aèbc?')
        self.assertRaises(NotImplementedError, Question2Tex(question).tex)