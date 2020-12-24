# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/exporter/tex/custom_question2tex_child.py
# Compiled at: 2019-03-02 04:44:34
# Size of source mod 2**32: 359 bytes
from survey.exporter.tex.question2tex_chart import Question2TexChart

class CustomQuestion2TexChild(Question2TexChart):

    def get_results(self):
        self.type = 'polar'
        return '        2/There were no answer at all,\n        3/But we have a custom treatment to show some,\n        2/You can make minor changes too !'