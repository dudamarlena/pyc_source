# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/shortanswer/shortanswer.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 4036 bytes
__author__ = 'isaiahmayerchak'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.mchoice import Assessment
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB
from runestone.common.runestonedirective import RunestoneDirective, RunestoneNode

def setup(app):
    app.add_directive('shortanswer', JournalDirective)
    app.add_node(JournalNode, html=(visit_journal_node, depart_journal_node))
    app.add_config_value('shortanswer_div_class', 'journal alert alert-warning', 'html')
    app.add_config_value('shortanswer_optional_div_class', 'journal alert alert-success', 'html')


TEXT_START = '\n<div class="runestone">\n<div data-component="shortanswer" class="%(divclass)s" id=%(divid)s %(optional)s %(mathjax)s>\n'
TEXT_END = '\n</div>\n</div> <!-- end of runestone div -->\n'

class JournalNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, options, **kwargs):
        (super(JournalNode, self).__init__)(**kwargs)
        self.journalnode_components = options


def visit_journal_node(self, node):
    div_id = node.journalnode_components['divid']
    components = dict(node.journalnode_components)
    components.update({'divid': div_id})
    node.delimiter = '_start__{}_'.format(node.journalnode_components['divid'])
    self.body.append(node.delimiter)
    res = TEXT_START % components
    self.body.append(res)


def depart_journal_node(self, node):
    components = dict(node.journalnode_components)
    res = TEXT_END % components
    self.body.append(res)
    addHTMLToDB(node.journalnode_components['divid'], components['basecourse'], ''.join(self.body[self.body.index(node.delimiter) + 1:]))
    self.body.remove(node.delimiter)


class JournalDirective(Assessment):
    __doc__ = "\n.. shortanswer:: uniqueid\n   :optional:\n\n   text of the question goes here\n\n\nconfig values (conf.py):\n\n- shortanswer_div_class - custom CSS class of the component's outermost div\n    "
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = Assessment.option_spec.copy()
    option_spec.update({'optional': directives.flag})
    option_spec.update({'mathjax': directives.flag})
    node_class = JournalNode

    def run(self):
        super(JournalDirective, self).run()
        addQuestionToDB(self)
        self.assert_has_content()
        self.options['optional'] = 'data-optional' if 'optional' in self.options else ''
        self.options['mathjax'] = 'data-mathjax' if 'mathjax' in self.options else ''
        journal_node = JournalNode((self.options), rawsource=(self.block_text))
        journal_node.source, journal_node.line = self.state_machine.get_source_and_line(self.lineno)
        self.updateContent()
        self.state.nested_parse(self.content, self.content_offset, journal_node)
        env = self.state.document.settings.env
        if self.options['optional']:
            self.options['divclass'] = env.config.shortanswer_optional_div_class
        else:
            self.options['divclass'] = env.config.shortanswer_div_class
        return [journal_node]