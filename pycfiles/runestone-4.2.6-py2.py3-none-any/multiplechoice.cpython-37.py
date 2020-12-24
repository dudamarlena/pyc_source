# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/mchoice/multiplechoice.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 16578 bytes
__author__ = 'bmiller'
from docutils import nodes
from docutils.parsers.rst import directives
from .assessbase import Assessment
from runestone.common.runestonedirective import RunestoneNode, get_node_line
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB

class MChoiceNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(MChoiceNode, self).__init__)(**kwargs)
        self.mc_options = content


def visit_mc_node(self, node):
    node.delimiter = '_start__{}_'.format(node.mc_options['divid'])
    self.body.append(node.delimiter)
    res = ''
    if 'random' in node.mc_options:
        node.mc_options['random'] = 'data-random'
    else:
        node.mc_options['random'] = ''
    if 'multiple_answers' in node.mc_options or ',' in node.mc_options['correct']:
        node.mc_options['multipleAnswers'] = 'true'
    else:
        node.mc_options['multipleAnswers'] = 'false'
    res = node.template_start % node.mc_options
    self.body.append(res)


def depart_mc_node(self, node):
    res = ''
    currFeedback = ''
    okeys = list(node.mc_options.keys())
    okeys.sort()
    for k in okeys:
        if 'answer_' in k:
            x, label = k.split('_')
            node.mc_options['alabel'] = label
            node.mc_options['atext'] = node.mc_options[k]
            currFeedback = 'feedback_' + label
            node.mc_options['feedtext'] = node.mc_options.get(currFeedback, '')
            if label in node.mc_options['correct']:
                node.mc_options['is_correct'] = 'data-correct'
            else:
                node.mc_options['is_correct'] = ''
            res += node.template_option % node.mc_options

    res += node.template_end % node.mc_options
    self.body.append(res)
    addHTMLToDB(node.mc_options['divid'], node.mc_options['basecourse'], ''.join(self.body[self.body.index(node.delimiter) + 1:]))
    self.body.remove(node.delimiter)


class MChoice(Assessment):
    __doc__ = "\n    The syntax for a multiple-choice question is:\n\n    .. mchoice:: uniqueid\n        :multiple_answers: [optional]. Implied if ``:correct:`` contains a list.\n        :random: [optional]\n\n        The following arguments supply answers and feedback. See below for an alternative method of specification.\n\n        :correct: letter of correct answer or list of correct answer letters (in case of multiple answers)\n        :answer_a: possible answer  -- what follows the _ is the answer's label.\n        :answer_b: possible answer\n        :answer_c: possible answer\n        :answer_d: possible answer\n        :answer_e: possible answer\n        :feedback_a: displayed if a is picked\n        :feedback_b: displayed if b is picked\n        :feedback_c: displayed if c is picked\n        :feedback_d: displayed if d is picked\n        :feedback_e: displayed if e is picked\n\n        Question text; this may contain multiple paragraphs with any markup.\n\n        An alternative method of specifying answers and feedback: Place an `unordered list <http://www.sphinx-doc.org/en/stable/rest.html#lists-and-quote-like-blocks>`_ at the end of the question text, in the following format. Note: If your question text happens to end with an unordered list, then place a comment, consisting of a paragraph containing only ``..`` at the end of the list. For example:\n\n        -   This list is still part of the question text.\n\n        ..\n\n        -   Text for answer A.\n\n            Your text may be multiple paragraphs, including `images <http://www.sphinx-doc.org/en/stable/rest.html#images>`_\n            and any other `inline <http://www.sphinx-doc.org/en/stable/rest.html#inline-markup>`_ or block markup. For example: :math:`\\sqrt(2)/2`. As earlier, if your feedback contains an unordered list, end it with a comment.\n\n            -   For example, this is part of the answer text.\n\n            ..\n\n            +   This is feedback for answer A. This is a correct answer because the bullet is a ``+``.\n\n                This may also span multiple paragraphs and include any markup.\n                However, there can be only one item in this unordered list.\n\n        -   Text for answer B.\n\n            -   Feedback for answer B. This is an incorrect answer, because the bullet is not a ``+``.\n        -   Text for answer C. Note that the empty line between a sublist and a list may be omitted.\n\n            +   Feedback for answer C, which is a correct answer. However, the empty line is required between a list and a sublist.\n\n        -   ... and so on.\n\n            -   Up to 26 answers and feedback pairs may be provided.\n\n    config values (conf.py): \n\n    - mchoice_div_class - custom CSS class of the component's outermost div\n    "
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    option_spec = Assessment.option_spec.copy()
    option_spec.update({'answer_a':directives.unchanged, 
     'answer_b':directives.unchanged, 
     'answer_c':directives.unchanged, 
     'answer_d':directives.unchanged, 
     'answer_e':directives.unchanged, 
     'correct':directives.unchanged, 
     'feedback_a':directives.unchanged, 
     'feedback_b':directives.unchanged, 
     'feedback_c':directives.unchanged, 
     'feedback_d':directives.unchanged, 
     'feedback_e':directives.unchanged, 
     'random':directives.flag, 
     'multiple_answers':directives.flag})

    def run(self):
        super(MChoice, self).run()
        TEMPLATE_START = '\n            <div class="%(divclass)s">\n            <ul data-component="multiplechoice" data-multipleanswers="%(multipleAnswers)s" %(random)s id="%(divid)s">\n            '
        OPTION = '\n            <li data-component="answer" %(is_correct)s id="%(divid)s_opt_%(alabel)s">%(atext)s</li><li data-component="feedback">%(feedtext)s</li>\n            '
        TEMPLATE_END = '\n\n            </ul>\n            </div>\n            '
        addQuestionToDB(self)
        mcNode = MChoiceNode((self.options), rawsource=(self.block_text))
        mcNode.source, mcNode.line = self.state_machine.get_source_and_line(self.lineno)
        mcNode.template_start = TEMPLATE_START
        mcNode.template_option = OPTION
        mcNode.template_end = TEMPLATE_END
        self.updateContent()
        self.state.nested_parse(self.content, self.content_offset, mcNode)
        env = self.state.document.settings.env
        self.options['divclass'] = env.config.mchoice_div_class
        answers_bullet_list = mcNode[(-1)] if len(mcNode) else None
        if isinstance(answers_bullet_list, nodes.bullet_list):
            if 'answer_a' not in self.options:
                if 'correct' not in self.options:
                    correct_answers = []
                    for answer_list_item in answers_bullet_list:
                        assert isinstance(answer_list_item, nodes.list_item)
                        feedback_bullet_list = answer_list_item[(-1)]
                        if not isinstance(feedback_bullet_list, nodes.bullet_list) or len(feedback_bullet_list) != 1:
                            raise self.error('On line {}, a single-item list must be nested under each answer.'.format(get_node_line(feedback_bullet_list)))
                        feedback_list_item = feedback_bullet_list[0]
                        assert isinstance(feedback_list_item, nodes.list_item)
                        if feedback_bullet_list['bullet'] == '+':
                            correct_answers.append(chr(answer_list_item.parent.index(answer_list_item) + ord('a')))
                        feedback_list_item.replace_self(FeedbackListItem(
 feedback_list_item.rawsource, *(feedback_list_item.children), **feedback_list_item.attributes))
                        feedback_bullet_list.replace_self(FeedbackBulletList(
 feedback_bullet_list.rawsource, *(feedback_bullet_list.children), **feedback_bullet_list.attributes))
                        answer_list_item.replace_self(AnswerListItem(
 answer_list_item.rawsource, *(answer_list_item.children), **answer_list_item.attributes))

                    answers_bullet_list.replace_self(AnswersBulletList(
 answers_bullet_list.rawsource, *(answers_bullet_list.children), **answers_bullet_list.attributes))
                    self.options['correct'] = ','.join(correct_answers)
        if not self.options.get('correct'):
            raise self.error('No correct answer specified.')
        return [
         mcNode]


class AnswersBulletList(nodes.bullet_list, RunestoneNode):
    pass


class AnswerListItem(nodes.list_item, RunestoneNode):
    pass


class FeedbackBulletList(nodes.bullet_list, RunestoneNode):
    pass


class FeedbackListItem(nodes.list_item, RunestoneNode):
    pass


def visit_answers_bullet_node(self, node):
    self.context.append((self.compact_simple, self.compact_p))
    self.compact_p = None
    self.compact_simple = True


def depart_answers_bullet_node(self, node):
    self.compact_simple, self.compact_p = self.context.pop()


def visit_answer_list_item(self, node):
    mcNode = node.parent.parent
    label = chr(node.parent.index(node) + ord('a'))
    mcNode.mc_options['alabel'] = label
    if label in mcNode.mc_options['correct']:
        mcNode.mc_options['is_correct'] = 'data-correct'
    else:
        mcNode.mc_options['is_correct'] = ''
    self.body.append('<li data-component="answer" %(is_correct)s id="%(divid)s_opt_%(alabel)s">' % mcNode.mc_options)


def depart_answer_list_item(self, node):
    pass


def visit_feedback_bullet_node(self, node):
    pass


def depart_feedback_bullet_node(self, node):
    pass


def visit_feedback_list_item(self, node):
    answer_list_item = node.parent.parent
    mcNode = answer_list_item.parent.parent
    label = chr(answer_list_item.parent.index(answer_list_item) + ord('a'))
    mcNode.mc_options['alabel'] = label
    self.body.append('</li><li data-component="feedback" id="%(divid)s_opt_%(alabel)s">\n' % mcNode.mc_options)


def depart_feedback_list_item(self, node):
    self.body.append('</li>')


class MChoiceMF(MChoice):

    def run(self):
        raise self.error("This directive has been depreciated. Please convert to the new directive 'mchoice'")
        mcmfNode = super(MChoiceMF, self).run()[0]
        return [
         mcmfNode]


class MChoiceMA(MChoice):

    def run(self):
        self.options['multiple_answers'] = 'multipleAnswers'
        raise self.error("This directive has been depreciated. Please convert to the new directive 'mchoice'")
        mchoicemaNode = super(MChoiceMA, self).run()[0]
        return [
         mchoicemaNode]


class MChoiceRandomMF(MChoice):

    def run(self):
        self.options['random'] = 'random'
        raise self.error("This directive has been depreciated. Please convert to the new directive 'mchoice'")
        mchoicerandommfNode = super(MChoiceRandomMF, self).run()[0]
        return [
         mchoicerandommfNode]