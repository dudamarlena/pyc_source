# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/fitb/fitb.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 15254 bytes
__author__ = 'isaiahmayerchak'
import json, ast
from numbers import Number
import re
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util import logging
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB
from runestone.common import RunestoneIdDirective, RunestoneNode, get_node_line
from runestone.common.runestonedirective import add_i18n_js

def setup(app):
    app.add_directive('fillintheblank', FillInTheBlank)
    app.add_role('blank', BlankRole)
    app.add_node(FITBNode, html=(visit_fitb_node, depart_fitb_node))
    app.add_node(BlankNode, html=(visit_blank_node, depart_blank_node))
    app.add_node(FITBFeedbackNode,
      html=(visit_fitb_feedback_node, depart_fitb_feedback_node))
    app.add_config_value('fitb_div_class', 'runestone', 'html')


class FITBNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(FITBNode, self).__init__)(**kwargs)
        self.fitb_options = content
        self.feedbackArray = []


def visit_fitb_node(self, node):
    node.delimiter = '_start__{}_'.format(node.fitb_options['divid'])
    self.body.append(node.delimiter)
    res = node.template_start % node.fitb_options
    self.body.append(res)


def depart_fitb_node(self, node):
    blankCount = 0
    for _ in node.traverse(BlankNode):
        blankCount += 1

    while blankCount < len(node.feedbackArray):
        visit_blank_node(self, None)
        blankCount += 1

    if len(node.feedbackArray) < blankCount:
        logger = logging.getLogger(__name__)
        logger.warning('Not enough feedback for the number of blanks supplied.',
          location=node)
    json_feedback = json.dumps(node.feedbackArray)
    node_with_document = node
    while not node_with_document.document:
        node_with_document = node_with_document.parent

    node.fitb_options['json'] = 'false' if node_with_document.document.settings.env.config.runestone_server_side_grading else json_feedback
    res = node.template_end % node.fitb_options
    self.body.append(res)
    addHTMLToDB(node.fitb_options['divid'], node.fitb_options['basecourse'], ''.join(self.body[self.body.index(node.delimiter) + 1:]), json_feedback)
    self.body.remove(node.delimiter)


class FillInTheBlank(RunestoneIdDirective):
    __doc__ = "\n    .. fillintheblank:: some_unique_id_here\n\n        Complete the sentence: |blank| had a |blank| lamb. One plus one is: (note that if there aren't enough blanks for the feedback given, they're added to the end of the problem. So, we don't **need** to specify a blank here.)\n\n        -   :Mary: Is the correct answer.\n            :Sue: Is wrong.\n            :x: Try again. (Note: the last item of feedback matches anything, regardless of the string it's given.)\n        -   :little: That's right.\n            :.*: Nope.\n        -   :2: Right on! Numbers can be given in decimal, hex (0x10 == 16), octal (0o10 == 8), binary (0b10 == 2), or using scientific notation (1e1 == 10), both here and by the user when answering the question.\n            :2 1: Close.... (The second number is a tolerance, so this matches 1 or 3.)\n            :x: Nope. (As earlier, this matches anything.)\n\n    config values (conf.py):\n\n    - fitb_div_class - custom CSS class of the component's outermost div\n    "
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update({'blankid':directives.unchanged, 
     'casei':directives.flag})

    def run(self):
        super(FillInTheBlank, self).run()
        TEMPLATE_START = '\n        <div class="%(divclass)s">\n        <div data-component="fillintheblank" id="%(divid)s">\n            '
        TEMPLATE_END = '\n        <script type="application/json">\n            %(json)s\n        </script>\n\n        </div>\n        </div>\n            '
        addQuestionToDB(self)
        fitbNode = FITBNode((self.options), rawsource=(self.block_text))
        fitbNode.source, fitbNode.line = self.state_machine.get_source_and_line(self.lineno)
        fitbNode.template_start = TEMPLATE_START
        fitbNode.template_end = TEMPLATE_END
        self.updateContent()
        self.state.nested_parse(self.content, self.content_offset, fitbNode)
        env = self.state.document.settings.env
        self.options['divclass'] = env.config.fitb_div_class
        self.assert_has_content()
        feedback_bullet_list = fitbNode.pop()
        if not isinstance(feedback_bullet_list, nodes.bullet_list):
            raise self.error('On line {}, the last item in a fill-in-the-blank question must be a bulleted list.'.format(get_node_line(feedback_bullet_list)))
        for feedback_list_item in feedback_bullet_list.children:
            assert isinstance(feedback_list_item, nodes.list_item)
            feedback_field_list = feedback_list_item[0]
            if not len(feedback_list_item) != 1:
                if not isinstance(feedback_field_list, nodes.field_list):
                    raise self.error('On line {}, each list item in a fill-in-the-blank problems must contain only one item, a field list.'.format(get_node_line(feedback_list_item)))
                blankArray = []
                for feedback_field in feedback_field_list:
                    if not isinstance(feedback_field, nodes.field):
                        raise AssertionError
                    else:
                        feedback_field_name = feedback_field[0]
                        assert isinstance(feedback_field_name, nodes.field_name)
                        feedback_field_name_raw = feedback_field_name.rawsource
                        try:
                            tmp = feedback_field_name_raw.split()
                            str_num = tmp[0]
                            list_tol = tmp[1:]
                            num = ast.literal_eval(str_num)
                            assert isinstance(num, Number)
                            if len(list_tol) == 0:
                                tol = 0
                            else:
                                assert len(list_tol) == 1
                            tol = ast.literal_eval(list_tol[0])
                            assert isinstance(tol, Number)
                            blankFeedbackDict = {'number': [num - tol, num + tol]}
                        except (SyntaxError, ValueError, AssertionError):
                            regex = '^\\s*' + feedback_field_name.rawsource.replace(' ', '\\s+') + '\\s*$'
                            blankFeedbackDict = {'regex':regex, 
                             'regexFlags':'i' if 'casei' in self.options else ''}
                            try:
                                re.compile(regex)
                            except Exception as ex:
                                try:
                                    raise self.error('Error when compiling regex "{}": {}.'.format(regex, str(ex)))
                                finally:
                                    ex = None
                                    del ex

                    blankArray.append(blankFeedbackDict)
                    feedback_field_body = feedback_field[1]
                    assert isinstance(feedback_field_body, nodes.field_body)
                    ffn = FITBFeedbackNode(
 feedback_field_body.rawsource, *(feedback_field_body.children), **feedback_field_body.attributes)
                    ffn.blankFeedbackDict = blankFeedbackDict
                    fitbNode += ffn

                fitbNode.feedbackArray.append(blankArray)

        return [
         fitbNode]


def BlankRole(roleName, rawtext, text, lineno, inliner, options={}, content=[]):
    blank_node = BlankNode(rawtext)
    blank_node.line = lineno
    return ([blank_node], [])


class BlankNode(nodes.Inline, nodes.TextElement, RunestoneNode):
    pass


def visit_blank_node(self, node):
    self.body.append('<input type="text">')


def depart_blank_node(self, node):
    pass


class FITBFeedbackNode(nodes.General, nodes.Element, RunestoneNode):
    pass


def visit_fitb_feedback_node(self, node):
    self.context.append(self.body)
    self.body = []


def depart_fitb_feedback_node(self, node):
    node.blankFeedbackDict['feedback'] = ''.join(self.body)
    self.body = self.context.pop()