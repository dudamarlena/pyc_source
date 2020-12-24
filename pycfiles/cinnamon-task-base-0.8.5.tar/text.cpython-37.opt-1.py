# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/inline/text.py
# Compiled at: 2019-03-06 14:36:30
# Size of source mod 2**32: 6922 bytes
import ast
from collections import namedtuple
from ..util import pypy, iterate, chunk as chunk_, Line, ensure_buffer
Pair = namedtuple('Pair', ('prefix', 'suffix'))
WrapFormat = namedtuple('WrapFormat', ('single', 'multiple', 'intra', 'indent'))
BARE_FORMAT = WrapFormat(Pair('', ''), Pair('', ''), Pair('', ''), 0)
UNBUFFERED_FORMAT = WrapFormat(Pair('yield ', ''), Pair('yield ', ''), Pair('yield ', ''), 0)
if pypy:
    BUFFERED_FORMAT = WrapFormat(Pair('_buffer.append(', ')'), Pair('_buffer.extend((', '))'), Pair('', ','), 1)
else:
    BUFFERED_FORMAT = WrapFormat(Pair('__ws(', ')'), Pair('__w((', '))'), Pair('', ','), 1)

class Text(object):
    """Text"""
    UNBUFFERED = UNBUFFERED_FORMAT
    BUFFERED = BUFFERED_FORMAT
    priority = -25

    def match(self, context, line):
        """Identify if a line to be processed can be processed by this transformer."""
        return line.kind == 'text'

    @staticmethod
    def wrap(scope, lines, format=BARE_FORMAT):
        """Wrap a stream of lines in armour.
                
                Takes a stream of lines, for example, the following single line:
                
                        Line(1, "Lorem ipsum dolor.")
                
                Or the following multiple lines:
                
                        Line(1, "Lorem ipsum")
                        Line(2, "dolor")
                        Line(3, "sit amet.")
                
                Provides a generator of wrapped lines.  For a single line, the following format is utilized:
                
                        {format.single.prefix}{line.stripped}{format.single.suffix}
                
                In the above multi-line example, the following format would be utilized:
                
                        {format.multiple.prefix}{line[1].stripped}{format.intra.suffix}
                        {format.intra.prefix}{line[2].stripped}{format.intra.suffix}
                        {format.intra.prefix}{line[3].stripped}{format.multiple.suffix}
                """
        for line in iterate(lines):
            prefix = suffix = ''
            if line.first and line.last:
                prefix = format.single.prefix
                suffix = format.single.suffix
            else:
                prefix = format.multiple.prefix if line.first else format.intra.prefix
                suffix = format.multiple.suffix if line.last else format.intra.suffix
            yield line.value.clone(line=(prefix + line.value.stripped + suffix), scope=(scope + (0 if line.first else format.indent)))

    @staticmethod
    def gather(input):
        """Collect contiguous lines of text, preserving line numbers."""
        try:
            line = input.next()
        except StopIteration:
            return
        else:
            lead = True
            buffer = []
            while line.kind == 'text':
                value = line.line.rstrip().rstrip('\\') + ('' if line.continued else '\n')
                if lead and line.stripped:
                    yield Line(line.number, value)
                    lead = False
                elif not lead:
                    if line.stripped:
                        for buf in buffer:
                            yield buf

                        buffer = []
                        yield Line(line.number, value)
                    else:
                        buffer.append(Line(line.number, value))
                try:
                    line = input.next()
                except StopIteration:
                    line = None
                    break

            if line:
                input.push(line)

    def process(self, context, lines):
        """Chop up individual lines into static and dynamic parts.
                
                Applies light optimizations, such as empty chunk removal, and calls out to other methods to process different
                chunk types.
                
                The processor protocol here requires the method to accept values by yielding resulting lines while accepting
                sent chunks. Deferral of multiple chunks is possible by yielding None. The processor will be sent None to
                be given a chance to yield a final line and perform any clean-up.
                """
        handler = None
        for line in lines:
            for chunk in chunk_(line):
                if 'strip' in context.flag:
                    chunk.line = chunk.stripped
                else:
                    if not chunk.line:
                        continue
                    if not handler or handler[0] != chunk.kind:
                        if handler:
                            try:
                                result = next(handler[1])
                            except StopIteration:
                                result = None

                            if result:
                                yield result
                        handler = getattr(self, 'process_' + chunk.kind, self.process_generic)(chunk.kind, context)
                        handler = (chunk.kind, handler)
                        try:
                            next(handler[1])
                        except StopIteration:
                            return

                result = handler[1].send(chunk)
                if result:
                    yield result
                handler = (
                 None, handler[1])

        if handler:
            try:
                result = next(handler[1])
            except StopIteration:
                return
            else:
                if result:
                    yield result

    def process_text(self, kind, context):
        """Combine multiple lines of bare text and emit as a Python string literal."""
        result = None
        while True:
            chunk = yield
            if chunk is None:
                if result:
                    yield result.clone(line=(repr(result.line)))
                return
            if not result:
                result = chunk
                continue
            result.line += chunk.line

    def process_generic(self, kind, context):
        """Transform otherwise unhandled kinds of chunks by calling an underscore prefixed function by that name."""
        result = None
        while True:
            chunk = yield result
            if chunk is None:
                return
            result = chunk.clone(line=('_' + kind + '(' + chunk.line + ')'))

    def process_format(self, kind, context):
        """Handle transforming format string + arguments into Python code."""
        result = None
        while True:
            chunk = yield result
            if chunk is None:
                return
            split = -1
            line = chunk.line
            try:
                ast.parse(line)
            except SyntaxError as e:
                try:
                    split = line.rfind(' ', 0, e.offset)
                finally:
                    e = None
                    del e

            result = chunk.clone(line=('_bless(' + line[:split].rstrip() + ').format(' + line[split:].lstrip() + ')'))

    def __call__(self, context):
        for i in ensure_buffer(context):
            yield i

        dirty = False
        lines = self.gather(context.input)
        lines = self.process(context, lines)
        lines = self.wrap(context.scope, lines, self.BUFFERED if 'buffer' in context.flag else self.UNBUFFERED)
        for line in lines:
            dirty = True
            yield line

        if dirty:
            if 'text' in context.flag:
                if 'dirty' not in context.flag:
                    context.flag.add('dirty')