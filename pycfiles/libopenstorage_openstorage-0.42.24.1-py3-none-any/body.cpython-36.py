# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/docutils/docutils/parsers/rst/directives/body.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 9244 bytes
"""
Directives for additional body elements.

See `docutils.parsers.rst.directives` for API details.
"""
__docformat__ = 'reStructuredText'
import sys
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import set_classes
from docutils.utils.code_analyzer import Lexer, LexerError, NumberLines

class BasePseudoSection(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'class':directives.class_option,  'name':directives.unchanged}
    has_content = True
    node_class = None

    def run(self):
        if not (self.state_machine.match_titles or isinstance(self.state_machine.node, nodes.sidebar)):
            raise self.error('The "%s" directive may not be used within topics or body elements.' % self.name)
        else:
            self.assert_has_content()
            title_text = self.arguments[0]
            textnodes, messages = self.state.inline_text(title_text, self.lineno)
            titles = [(nodes.title)(title_text, '', *textnodes)]
            if 'subtitle' in self.options:
                textnodes, more_messages = self.state.inline_text(self.options['subtitle'], self.lineno)
                titles.append((nodes.subtitle)(self.options['subtitle'], '', *textnodes))
                messages.extend(more_messages)
            text = '\n'.join(self.content)
            node = (self.node_class)(text, *titles + messages)
            node['classes'] += self.options.get('class', [])
            self.add_name(node)
            if text:
                self.state.nested_parse(self.content, self.content_offset, node)
        return [
         node]


class Topic(BasePseudoSection):
    node_class = nodes.topic


class Sidebar(BasePseudoSection):
    node_class = nodes.sidebar
    option_spec = BasePseudoSection.option_spec.copy()
    option_spec['subtitle'] = directives.unchanged_required

    def run(self):
        if isinstance(self.state_machine.node, nodes.sidebar):
            raise self.error('The "%s" directive may not be used within a sidebar element.' % self.name)
        return BasePseudoSection.run(self)


class LineBlock(Directive):
    option_spec = {'class':directives.class_option, 
     'name':directives.unchanged}
    has_content = True

    def run(self):
        self.assert_has_content()
        block = nodes.line_block(classes=(self.options.get('class', [])))
        self.add_name(block)
        node_list = [block]
        for line_text in self.content:
            text_nodes, messages = self.state.inline_text(line_text.strip(), self.lineno + self.content_offset)
            line = (nodes.line)(line_text, '', *text_nodes)
            if line_text.strip():
                line.indent = len(line_text) - len(line_text.lstrip())
            block += line
            node_list.extend(messages)
            self.content_offset += 1

        self.state.nest_line_block_lines(block)
        return node_list


class ParsedLiteral(Directive):
    option_spec = {'class':directives.class_option, 
     'name':directives.unchanged}
    has_content = True

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = '\n'.join(self.content)
        text_nodes, messages = self.state.inline_text(text, self.lineno)
        node = (nodes.literal_block)(text, '', *text_nodes, **self.options)
        node.line = self.content_offset + 1
        self.add_name(node)
        return [node] + messages


class CodeBlock(Directive):
    __doc__ = "Parse and mark up content of a code block.\n\n    Configuration setting: syntax_highlight\n       Highlight Code content with Pygments?\n       Possible values: ('long', 'short', 'none')\n\n    "
    optional_arguments = 1
    option_spec = {'class':directives.class_option,  'name':directives.unchanged, 
     'number-lines':directives.unchanged}
    has_content = True

    def run(self):
        self.assert_has_content()
        if self.arguments:
            language = self.arguments[0]
        else:
            language = ''
        set_classes(self.options)
        classes = ['code']
        if language:
            classes.append(language)
        if 'classes' in self.options:
            classes.extend(self.options['classes'])
        try:
            tokens = Lexer('\n'.join(self.content), language, self.state.document.settings.syntax_highlight)
        except LexerError as error:
            raise self.warning(error)

        if 'number-lines' in self.options:
            try:
                startline = int(self.options['number-lines'] or 1)
            except ValueError:
                raise self.error(':number-lines: with non-integer start value')

            endline = startline + len(self.content)
            tokens = NumberLines(tokens, startline, endline)
        node = nodes.literal_block(('\n'.join(self.content)), classes=classes)
        self.add_name(node)
        if 'source' in self.options:
            node.attributes['source'] = self.options['source']
        for classes, value in tokens:
            if classes:
                node += nodes.inline(value, value, classes=classes)
            else:
                node += nodes.Text(value, value)

        return [
         node]


class MathBlock(Directive):
    option_spec = {'class':directives.class_option, 
     'name':directives.unchanged}
    has_content = True

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        content = '\n'.join(self.content).split('\n\n')
        _nodes = []
        for block in content:
            if not block:
                pass
            else:
                node = (nodes.math_block)((self.block_text), block, **self.options)
                node.line = self.content_offset + 1
                self.add_name(node)
                _nodes.append(node)

        return _nodes


class Rubric(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'class':directives.class_option,  'name':directives.unchanged}

    def run(self):
        set_classes(self.options)
        rubric_text = self.arguments[0]
        textnodes, messages = self.state.inline_text(rubric_text, self.lineno)
        rubric = (nodes.rubric)(rubric_text, '', *textnodes, **self.options)
        self.add_name(rubric)
        return [rubric] + messages


class BlockQuote(Directive):
    has_content = True
    classes = []

    def run(self):
        self.assert_has_content()
        elements = self.state.block_quote(self.content, self.content_offset)
        for element in elements:
            if isinstance(element, nodes.block_quote):
                element['classes'] += self.classes

        return elements


class Epigraph(BlockQuote):
    classes = [
     'epigraph']


class Highlights(BlockQuote):
    classes = [
     'highlights']


class PullQuote(BlockQuote):
    classes = [
     'pull-quote']


class Compound(Directive):
    option_spec = {'class':directives.class_option, 
     'name':directives.unchanged}
    has_content = True

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        node = nodes.compound(text)
        node['classes'] += self.options.get('class', [])
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class Container(Directive):
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'name': directives.unchanged}
    has_content = True

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        try:
            if self.arguments:
                classes = directives.class_option(self.arguments[0])
            else:
                classes = []
        except ValueError:
            raise self.error('Invalid class attribute value for "%s" directive: "%s".' % (
             self.name, self.arguments[0]))

        node = nodes.container(text)
        node['classes'].extend(classes)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]