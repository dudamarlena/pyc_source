# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/docutils/docutils/parsers/rst/directives/admonitions.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 2413 bytes
"""
Admonition directives.
"""
__docformat__ = 'reStructuredText'
from docutils.parsers.rst import Directive
from docutils.parsers.rst import states, directives
from docutils.parsers.rst.roles import set_classes
from docutils import nodes

class BaseAdmonition(Directive):
    final_argument_whitespace = True
    option_spec = {'class':directives.class_option,  'name':directives.unchanged}
    has_content = True
    node_class = None

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = '\n'.join(self.content)
        admonition_node = (self.node_class)(text, **self.options)
        self.add_name(admonition_node)
        if self.node_class is nodes.admonition:
            title_text = self.arguments[0]
            textnodes, messages = self.state.inline_text(title_text, self.lineno)
            title = (nodes.title)(title_text, '', *textnodes)
            title.source, title.line = self.state_machine.get_source_and_line(self.lineno)
            admonition_node += title
            admonition_node += messages
            if 'classes' not in self.options:
                admonition_node['classes'] += [
                 'admonition-' + nodes.make_id(title_text)]
        self.state.nested_parse(self.content, self.content_offset, admonition_node)
        return [admonition_node]


class Admonition(BaseAdmonition):
    required_arguments = 1
    node_class = nodes.admonition


class Attention(BaseAdmonition):
    node_class = nodes.attention


class Caution(BaseAdmonition):
    node_class = nodes.caution


class Danger(BaseAdmonition):
    node_class = nodes.danger


class Error(BaseAdmonition):
    node_class = nodes.error


class Hint(BaseAdmonition):
    node_class = nodes.hint


class Important(BaseAdmonition):
    node_class = nodes.important


class Note(BaseAdmonition):
    node_class = nodes.note


class Tip(BaseAdmonition):
    node_class = nodes.tip


class Warning(BaseAdmonition):
    node_class = nodes.warning