# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/question/question.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 3249 bytes
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneIdDirective, RunestoneNode
__author__ = 'bmiller'

def setup(app):
    app.add_directive('question', QuestionDirective)
    app.add_node(QuestionNode, html=(visit_question_node, depart_question_node))


class QuestionNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(QuestionNode, self).__init__)(**kwargs)
        self.question_options = content


def visit_question_node(self, node):
    env = node.document.settings.env
    if not hasattr(env, 'questioncounter'):
        env.questioncounter = 0
    elif 'number' in node.question_options:
        env.questioncounter = int(node.question_options['number'])
    else:
        env.questioncounter += 1
    node.question_options['number'] = 'start={}'.format(env.questioncounter)
    res = TEMPLATE_START % node.question_options
    self.body.append(res)


def depart_question_node(self, node):
    res = TEMPLATE_END % node.question_options
    delimiter = '_start__{}_'.format(node.question_options['divid'])
    self.body.append(res)


TEMPLATE_START = '\n    <div data-component="question" class="full-width container question" id="%(divid)s" >\n    <ol %(number)s class=arabic><li class="alert alert-warning">\n\n    '
TEMPLATE_END = '\n    </li></ol>\n    </div>\n    '

class QuestionDirective(RunestoneIdDirective):
    __doc__ = '\n.. question:: identifier\n   :number: Force a number for this question\n\n   Content  everything here is part of the question\n   Content  It can be a lot...\n    '
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update({'number': directives.positive_int})

    def run(self):
        super(QuestionDirective, self).run()
        self.assert_has_content()
        self.options['name'] = self.arguments[0].strip()
        question_node = QuestionNode((self.options), rawsource=(self.block_text))
        question_node.source, question_node.line = self.state_machine.get_source_and_line(self.lineno)
        self.add_name(question_node)
        self.state.nested_parse(self.content, self.content_offset, question_node)
        return [
         question_node]