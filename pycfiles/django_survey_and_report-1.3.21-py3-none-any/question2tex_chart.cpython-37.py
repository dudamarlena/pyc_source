# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/exporter/tex/question2tex_chart.py
# Compiled at: 2020-02-22 13:47:33
# Size of source mod 2**32: 4704 bytes
import logging
from django.conf import settings
import django.utils.translation as _
from survey.exporter.tex.question2tex import Question2Tex
LOGGER = logging.getLogger(__name__)

class Question2TexChart(Question2Tex):
    __doc__ = '\n        This class permit to generate latex code directly from the Question\n        object.\n    '
    TEX_SKELETON = '\n\\begin{figure}[h!]\n    \\begin{tikzpicture}\n        \\pie%s{\n%s\n        }\n    \\end{tikzpicture}\n    \\caption{\\label{figure:q%d-%d}%s}\n\\end{figure}\n'

    def __init__(self, question, **options):
        (super(Question2TexChart, self).__init__)(question, **options)
        self.pos = options.get('pos')
        self.rotate = options.get('rotate')
        self.radius = options.get('radius')
        self.color = options.get('color')
        self.explode = options.get('explode')
        self.sum = options.get('sum')
        self.after_number = options.get('after_number')
        self.before_number = options.get('before_number')
        self.scale_font = options.get('scale_font')
        self.text = options.get('text')
        self.style = options.get('style')
        self.type = options.get('type')
        self.latex_label = options.get('latex_label', 1)

    def get_colors(self):
        """ Return a formated string for a tikz pgf-pie chart.

        :param Question question: The question..
        :param Dict colors_dict: Color to use (String answer: String color)
        """
        colors = []
        for answer in self.cardinality:
            answer = Question2Tex.get_clean_answer(answer)
            try:
                colors.append(self.color[answer])
            except (KeyError, ValueError):
                msg = "Color for '%s' not provided. You could " % answer
                msg += 'add \'%s: "red!50"\', in your color config.' % answer
                LOGGER.warning(msg)
                colors.append(settings.SURVEY_DEFAULT_PIE_COLOR)

        return '{%s}' % ', '.join(colors)

    def get_results(self):
        """ Return a formated string for a tikz pgf-pie chart. """
        pie = ''
        for answer, cardinality in list(self.cardinality.items()):
            if not answer:
                ans = _('Left blank')
            ans = Question2Tex.get_clean_answer(answer)
            pie += '{}/{},'.format(cardinality, ans)

        if not pie:
            return ''
        final_answers = []
        for answer in pie.split(','):
            if answer:
                final_answers.append(answer)

        return '            {}'.format(',\n            '.join(final_answers))

    def get_pie_options(self):
        r"""Return the options of the pie for: \pie[options]{data}"""
        options = ''
        if self.pos:
            options += 'pos={%s},' % self.pos
        if self.explode:
            options += 'explode={%s},' % self.explode
        if self.rotate:
            options += 'rotate={},'.format(self.rotate)
        if self.radius:
            options += 'radius={},'.format(self.radius)
        if self.color:
            options += 'color={},'.format(self.get_colors())
        if self.sum:
            options += 'sum={},'.format(self.sum)
        if self.after_number:
            options += 'after number={},'.format(self.after_number)
        if self.before_number:
            options += 'before number={},'.format(self.before_number)
        if self.scale_font:
            options += 'scale font, '
        if self.text:
            options += 'text={},'.format(self.text)
        if self.style:
            options += 'style={},'.format(self.style)
        if self.type:
            if self.type != 'pie':
                options += '{},'.format(self.type)
        options = options[:-1]
        if options:
            return '[{}]'.format(options)
        return ''

    def get_caption_specifics(self):
        return "%s '%s' " % (_('for the question'), Question2Tex.html2latex(self.question.text))

    def tex(self):
        r""" Return a pfg-pie pie chart of a question.

        You must use pgf-pie in your latex file for this to works ::
            \usepackage{pgf-pie}
        See http://pgf-pie.googlecode.com/ for detail and arguments doc. """
        results = self.get_results()
        if not results:
            return str(_('No answers for this question.'))
        return Question2TexChart.TEX_SKELETON % (
         self.get_pie_options(),
         results,
         self.question.pk,
         self.latex_label,
         self.get_caption())