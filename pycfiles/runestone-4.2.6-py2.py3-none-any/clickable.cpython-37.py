# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/clickableArea/clickable.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 6644 bytes
__author__ = 'isaiahmayerchak'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB
from runestone.common.runestonedirective import RunestoneIdDirective, RunestoneNode

def setup(app):
    app.add_directive('clickablearea', ClickableArea)
    app.add_node(ClickableAreaNode, html=(visit_ca_node, depart_ca_node))
    app.add_config_value('clickable_div_class', 'runestone alert alert-warning', 'html')


TEMPLATE = '\n<div class="runestone">\n<div data-component="clickablearea" class="%(divclass)s" id="%(divid)s" %(table)s %(correct)s %(incorrect)s>\n<span data-question>%(qnumber)s: %(question)s</span>%(feedback)s%(clickcode)s\n'
TEMPLATE_END = '\n</div>\n</div>\n'

class ClickableAreaNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(ClickableAreaNode, self).__init__)(**kwargs)
        self.ca_options = content


def visit_ca_node(self, node):
    res = TEMPLATE
    node.delimiter = '_start__{}_'.format(node.ca_options['divid'])
    self.body.append(node.delimiter)
    if 'feedback' in node.ca_options:
        node.ca_options['feedback'] = '<span data-feedback>' + node.ca_options['feedback'] + '</span>'
    else:
        node.ca_options['feedback'] = ''
    if 'iscode' not in node.ca_options:
        node.ca_options['correct'] = 'data-cc="' + node.ca_options['correct'] + '"'
        node.ca_options['incorrect'] = 'data-ci="' + node.ca_options['incorrect'] + '"'
    else:
        node.ca_options['correct'] = ''
        node.ca_options['incorrect'] = ''
    res = res % node.ca_options
    self.body.append(res)


def depart_ca_node(self, node):
    res = ''
    res = TEMPLATE_END % node.ca_options
    self.body.append(res)
    addHTMLToDB(node.ca_options['divid'], node.ca_options['basecourse'], ''.join(self.body[self.body.index(node.delimiter) + 1:]))
    self.body.remove(node.delimiter)


class ClickableArea(RunestoneIdDirective):
    __doc__ = "\n.. clickablearea:: identifier\n    :question: Question text\n    :feedback: Optional feedback for incorrect answer\n    :iscode: Boolean that if present will put the content into a <pre>\n    :table: Boolean that indicates that the content is a table.\n    :correct: An array of the indices of the correct elements, separated by semicolons--if this is a table, each item in the array is a tuple\n    with the first number being the row and the second number being the column--use a column number of 0 to make the whole row correct (ex: 1,2;3,0 makes the 2nd data cell in the first row correct as well as the entire 3rd row)\n    :incorrect: An array of the indices of the incorrect elements--same format as the correct elements.\n\n    --Content--\n\n\nconfig values (conf.py):\n\n- clickable_div_class - custom CSS class of the component's outermost div\n    "
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    final_argument_whitespace = True
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update({'question':directives.unchanged, 
     'feedback':directives.unchanged, 
     'iscode':directives.flag, 
     'correct':directives.unchanged, 
     'incorrect':directives.unchanged, 
     'table':directives.flag})

    def run(self):
        super(ClickableArea, self).run()
        addQuestionToDB(self)
        self.assert_has_content()
        if 'iscode' in self.options:
            source = '\n'.join(self.content)
            source = source.replace(':click-correct:', '<span data-correct>')
            source = source.replace(':click-incorrect:', '<span data-incorrect>')
            source = source.replace(':endclick:', '</span>')
            source = '<pre>' + source + '</pre>'
            self.options['clickcode'] = source
        else:
            self.options['clickcode'] = ''
        clickNode = ClickableAreaNode((self.options), rawsource=(self.block_text))
        clickNode.source, clickNode.line = self.state_machine.get_source_and_line(self.lineno)
        clickNode.template_start = TEMPLATE
        if 'table' in self.options:
            self.options['table'] = 'data-table'
        else:
            self.options['table'] = ''
        if 'iscode' not in self.options:
            self.state.nested_parse(self.content, self.content_offset, clickNode)
        env = self.state.document.settings.env
        self.options['divclass'] = env.config.clickable_div_class
        return [
         clickNode]