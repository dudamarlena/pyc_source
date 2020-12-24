# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/click/click/_textwrap.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 1198 bytes
import textwrap
from contextlib import contextmanager

class TextWrapper(textwrap.TextWrapper):

    def _handle_long_word(self, reversed_chunks, cur_line, cur_len, width):
        space_left = max(width - cur_len, 1)
        if self.break_long_words:
            last = reversed_chunks[(-1)]
            cut = last[:space_left]
            res = last[space_left:]
            cur_line.append(cut)
            reversed_chunks[-1] = res
        elif not cur_line:
            cur_line.append(reversed_chunks.pop())

    @contextmanager
    def extra_indent(self, indent):
        old_initial_indent = self.initial_indent
        old_subsequent_indent = self.subsequent_indent
        self.initial_indent += indent
        self.subsequent_indent += indent
        try:
            yield
        finally:
            self.initial_indent = old_initial_indent
            self.subsequent_indent = old_subsequent_indent

    def indent_only(self, text):
        rv = []
        for idx, line in enumerate(text.splitlines()):
            indent = self.initial_indent
            if idx > 0:
                indent = self.subsequent_indent
            rv.append(indent + line)

        return '\n'.join(rv)