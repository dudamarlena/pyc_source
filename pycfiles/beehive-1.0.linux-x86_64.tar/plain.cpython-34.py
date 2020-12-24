# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/plain.py
# Compiled at: 2014-10-31 06:38:11
# Size of source mod 2**32: 4898 bytes
from beehive.formatter.base import Formatter
from beehive.model_describe import ModelPrinter
from beehive.textutil import make_indentation

class PlainFormatter(Formatter):
    __doc__ = '\n    Provides a simple plain formatter without coloring/formatting.\n    The formatter displays now also:\n\n       * multi-line text (doc-strings)\n       * table\n       * tags (maybe)\n    '
    name = 'plain'
    description = 'Very basic formatter with maximum compatibility'
    SHOW_MULTI_LINE = True
    SHOW_TAGS = False
    SHOW_ALIGNED_KEYWORDS = False
    DEFAULT_INDENT_SIZE = 2

    def __init__(self, stream_opener, config, **kwargs):
        super(PlainFormatter, self).__init__(stream_opener, config)
        self.steps = []
        self.show_timings = config.show_timings
        self.show_multiline = config.show_multiline and self.SHOW_MULTI_LINE
        self.show_aligned_keywords = self.SHOW_ALIGNED_KEYWORDS
        self.show_tags = self.SHOW_TAGS
        self.indent_size = self.DEFAULT_INDENT_SIZE
        self.stream = self.open()
        self.printer = ModelPrinter(self.stream)
        self._multiline_indentation = None

    @property
    def multiline_indentation(self):
        if self._multiline_indentation is None:
            offset = 0
            if self.show_aligned_keywords:
                offset = 2
            indentation = make_indentation(3 * self.indent_size + offset)
            self._multiline_indentation = indentation
        return self._multiline_indentation

    def reset_steps(self):
        self.steps = []

    def write_tags(self, tags, indent=None):
        if tags:
            if self.show_tags:
                indent = indent or ''
                text = ' @'.join(tags)
                self.stream.write('%s@%s\n' % (indent, text))

    def feature(self, feature):
        self.reset_steps()
        self.write_tags(feature.tags)
        self.stream.write('%s: %s\n' % (feature.keyword, feature.name))

    def background(self, background):
        self.reset_steps()
        indent = make_indentation(self.indent_size)
        text = '%s%s: %s\n' % (indent, background.keyword, background.name)
        self.stream.write(text)

    def scenario(self, scenario):
        self.reset_steps()
        self.stream.write('\n')
        indent = make_indentation(self.indent_size)
        text = '%s%s: %s\n' % (indent, scenario.keyword, scenario.name)
        self.write_tags(scenario.tags, indent)
        self.stream.write(text)

    def scenario_outline(self, outline):
        self.reset_steps()
        indent = make_indentation(self.indent_size)
        text = '%s%s: %s\n' % (indent, outline.keyword, outline.name)
        self.write_tags(outline.tags, indent)
        self.stream.write(text)

    def step(self, step):
        self.steps.append(step)

    def result(self, result):
        """
        Process the result of a step (after step execution).

        :param result:
        """
        step = self.steps.pop(0)
        indent = make_indentation(2 * self.indent_size)
        if self.show_aligned_keywords:
            text = '%s%6s %s ... ' % (indent, step.keyword, step.name)
        else:
            text = '%s%s %s ... ' % (indent, step.keyword, step.name)
        self.stream.write(text)
        status = result.status
        if self.show_timings:
            status += ' in %0.3fs' % step.duration
        if result.error_message:
            self.stream.write('%s\n%s\n' % (status, result.error_message))
        else:
            self.stream.write('%s\n' % status)
        if self.show_multiline:
            if step.text:
                self.doc_string(step.text)
            if step.table:
                self.table(step.table)

    def eof(self):
        self.stream.write('\n')

    def doc_string(self, doc_string):
        self.printer.print_docstring(doc_string, self.multiline_indentation)

    def table(self, table):
        self.printer.print_table(table, self.multiline_indentation)


class Plain0Formatter(PlainFormatter):
    __doc__ = '\n    Similar to old plain formatter without support for:\n\n      * multi-line text\n      * tables\n      * tags\n    '
    name = 'plain0'
    description = 'Very basic formatter with maximum compatibility'
    SHOW_MULTI_LINE = False
    SHOW_TAGS = False
    SHOW_ALIGNED_KEYWORDS = False