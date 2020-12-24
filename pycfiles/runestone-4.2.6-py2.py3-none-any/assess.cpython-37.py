# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/mchoice/assess.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 3758 bytes
__author__ = 'bmiller'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneDirective, RunestoneIdDirective, add_i18n_js
from .assessbase import Assessment
from .multiplechoice import *

def setup(app):
    app.add_directive('mchoice', MChoice)
    app.add_directive('mchoicemf', MChoiceMF)
    app.add_directive('mchoicema', MChoiceMA)
    app.add_directive('mchoicerandommf', MChoiceRandomMF)
    app.add_directive('addbutton', AddButton)
    app.add_directive('qnum', QuestionNumber)
    app.add_config_value('mchoice_div_class', 'runestone alert alert-warning', 'html')
    app.add_node(MChoiceNode, html=(visit_mc_node, depart_mc_node))
    app.add_node(AnswersBulletList,
      html=(visit_answers_bullet_node, depart_answers_bullet_node))
    app.add_node(AnswerListItem, html=(visit_answer_list_item, depart_answer_list_item))
    app.add_node(FeedbackBulletList,
      html=(
     visit_feedback_bullet_node, depart_feedback_bullet_node))
    app.add_node(FeedbackListItem,
      html=(visit_feedback_list_item, depart_feedback_list_item))


class AddButton(RunestoneIdDirective):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True

    def run(self):
        super(AddButton, self).run()
        TEMPLATE_START = '\n            <div id="%(divid)s" class="alert alert-warning">\n            <form name="%(divid)s_form" method="get" action="" onsubmit="return false;">\n            '
        TEMPLATE_END = '\n            <button class=\'btn btn-inverse\' name="reset" onclick="resetPage(\'%(divid)s\')">Forget My Answers</button>\n            </form>\n            </div>\n            '
        res = ''
        res = TEMPLATE_START % self.options
        res += TEMPLATE_END % self.options
        rawnode = nodes.raw((self.block_text), res, format='html')
        rawnode.source, rawnode.line = self.state_machine.get_source_and_line(self.lineno)
        return [
         rawnode]


class QuestionNumber(RunestoneDirective):
    __doc__ = "Set Parameters for Question Numbering\n.. qnum::\n   'prefix': character prefix before the number\n   'suffix': character prefix after the number\n   'start': start numbering with this value\n\n.. qnum::\n   :prefix: turtle-\n   :start: 10\n    "
    required_arguments = 0
    optional_arguments = 3
    has_content = False
    option_spec = {'prefix':directives.unchanged, 
     'suffix':directives.unchanged, 
     'start':directives.positive_int}

    def run(self):
        env = self.state.document.settings.env
        if 'start' in self.options:
            env.assesscounter = self.options['start'] - 1
        if 'prefix' in self.options:
            env.assessprefix = self.options['prefix']
        if 'suffix' in self.options:
            env.assesssuffix = self.options['suffix']
        return []