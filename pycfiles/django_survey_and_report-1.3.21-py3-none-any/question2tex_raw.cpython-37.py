# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/exporter/tex/question2tex_raw.py
# Compiled at: 2020-01-26 10:04:56
# Size of source mod 2**32: 681 bytes
import django.utils.translation as _
from survey.exporter.tex.question2tex import Question2Tex

class Question2TexRaw(Question2Tex):
    __doc__ = '\n        This class permit to generate latex code directly from the Question\n        object.\n    '
    TEX_SKELETON = '\n\\begin{quote}\n%s\n\\end{quote} \\hfill (%s n\\textsuperscript{o}%s)\n'

    def tex(self):
        """ Return all the answer as quote in latex. """
        raw_answers = ''
        for i, answer in enumerate(self.cardinality):
            if answer:
                raw_answers += Question2TexRaw.TEX_SKELETON % (answer, _('Participant'), i)

        return raw_answers