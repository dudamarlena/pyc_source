# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/reveal/reveal.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 5414 bytes
__author__ = 'isaiahmayerchak'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneIdDirective, RunestoneNode

def setup(app):
    app.add_directive('reveal', RevealDirective)
    app.add_node(RevealNode, html=(visit_reveal_node, depart_reveal_node))


class RevealNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(RevealNode, self).__init__)(**kwargs)
        self.reveal_options = content


def visit_reveal_node(self, node):
    if 'modal' in node.reveal_options:
        node.reveal_options['modal'] = 'data-modal'
    else:
        node.reveal_options['modal'] = ''
    if 'modaltitle' in node.reveal_options:
        temp = node.reveal_options['modaltitle']
        node.reveal_options['modaltitle'] = 'data-title="' + temp + '"'
    else:
        node.reveal_options['modaltitle'] = ''
    if node.reveal_options['instructoronly'] and node.reveal_options['is_dynamic']:
        res = DYNAMIC_PREFIX
    else:
        res = ''
    res += TEMPLATE_START % node.reveal_options
    self.body.append(res)


def depart_reveal_node(self, node):
    res = TEMPLATE_END % node.reveal_options
    if node.reveal_options['instructoronly']:
        if node.reveal_options['is_dynamic']:
            res += DYNAMIC_SUFFIX
    self.body.append(res)


DYNAMIC_PREFIX = '\n{{ if is_instructor: }}\n'
TEMPLATE_START = '\n    <div data-component="reveal" id="%(divid)s" %(modal)s %(modaltitle)s %(showtitle)s %(hidetitle)s %(instructoronly)s>\n    '
TEMPLATE_END = '\n    </div>\n    '
DYNAMIC_SUFFIX = '\n{{ pass }}\n'

class RevealDirective(RunestoneIdDirective):
    __doc__ = '\n.. reveal:: identifier\n   :showtitle: Text on the \'show\' button--default is "Show"\n   :hidetitle: Text on the \'hide\' button--default is "Hide"\n   :modal: Boolean--if included, revealed display will be a modal\n   :modaltitle: Title of modal dialog window--default is "Message from the author"\n   :instructoronly: Only show button and contents to instructors\n\n   Content  everything here will be hidden until revealed\n   Content  It can be a lot...\n    '
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update({'showtitle':directives.unchanged, 
     'hidetitle':directives.unchanged, 
     'modal':directives.flag, 
     'modaltitle':directives.unchanged, 
     'instructoronly':directives.flag})

    def run(self):
        super(RevealDirective, self).run()
        env = self.state.document.settings.env
        self.assert_has_content()
        if 'showtitle' not in self.options:
            self.options['showtitle'] = 'data-showtitle="Show"'
        else:
            self.options['showtitle'] = 'data-showtitle="' + self.options['showtitle'] + '"'
        if 'hidetitle' not in self.options:
            self.options['hidetitle'] = 'data-hidetitle="Hide"'
        else:
            self.options['hidetitle'] = 'data-hidetitle="' + self.options['hidetitle'] + '"'
        if 'instructoronly' in self.options:
            self.options['instructoronly'] = 'data-instructoronly style="display: none;"'
        else:
            self.options['instructoronly'] = ''
        is_dynamic = env.config.html_context.get('dynamic_pages', False)
        self.options['is_dynamic'] = is_dynamic
        reveal_node = RevealNode((self.options), rawsource=(self.block_text))
        reveal_node.source, reveal_node.line = self.state_machine.get_source_and_line(self.lineno)
        self.state.nested_parse(self.content, self.content_offset, reveal_node)
        return [
         reveal_node]