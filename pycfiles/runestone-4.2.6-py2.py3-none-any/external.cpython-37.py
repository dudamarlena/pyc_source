# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/external/external.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 3452 bytes
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB
from runestone.common.runestonedirective import RunestoneIdDirective, RunestoneNode
try:
    from html import escape
except ImportError:
    from cgi import escape

__author__ = 'jczetta'

def setup(app):
    app.add_directive('external', ExternalDirective)
    app.add_node(ExternalNode, html=(visit_external_node, depart_external_node))


class ExternalNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(ExternalNode, self).__init__)(**kwargs)
        self.external_options = content


def visit_external_node(self, node):
    node.delimiter = '_start__{}_'.format(node.external_options['divid'])
    self.body.append(node.delimiter)
    res = TEMPLATE_START % node.external_options
    self.body.append(res)


def depart_external_node(self, node):
    res = TEMPLATE_END % node.external_options
    self.body.append(res)
    addHTMLToDB(node.external_options['divid'], node.external_options['basecourse'], ''.join(''))
    self.body.remove(node.delimiter)


TEMPLATE_START = '\n    <div data-component="external" class="full-width container external" id="%(divid)s" >\n    <li class="alert alert-warning">\n\n    '
TEMPLATE_END = '\n    </li>\n    </div>\n    '

class ExternalDirective(RunestoneIdDirective):
    __doc__ = '\n.. external:: identifier\n\n   Content  Everything here is part of the activity\n   Content  Can include links...\n    '
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update({'number': directives.positive_int})

    def run(self):
        super(ExternalDirective, self).run()
        addQuestionToDB(self)
        self.assert_has_content()
        self.options['name'] = self.arguments[0].strip()
        external_node = ExternalNode((self.options), rawsource=(self.block_text))
        external_node.source, external_node.line = self.state_machine.get_source_and_line(self.lineno)
        self.add_name(external_node)
        self.state.nested_parse(self.content, self.content_offset, external_node)
        return [
         external_node]