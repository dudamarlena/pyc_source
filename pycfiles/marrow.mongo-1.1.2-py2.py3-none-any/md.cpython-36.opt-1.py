# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/md.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 1072 bytes
from __future__ import unicode_literals
from misaka import Markdown, HtmlRenderer
from misaka import HTML_ESCAPE, HTML_HARD_WRAP
from misaka import EXT_FENCED_CODE, EXT_NO_INTRA_EMPHASIS, EXT_AUTOLINK, EXT_SPACE_HEADERS, EXT_STRIKETHROUGH, EXT_SUPERSCRIPT
from .string import String
from ....schema.compat import unicode, py3
md = Markdown(HtmlRenderer(flags=(HTML_ESCAPE | HTML_HARD_WRAP)),
  extensions=(EXT_FENCED_CODE | EXT_NO_INTRA_EMPHASIS | EXT_AUTOLINK | EXT_SPACE_HEADERS | EXT_STRIKETHROUGH | EXT_SUPERSCRIPT))

class MarkdownString(unicode):

    def __html__(self):
        return md(self)


class Markdown(String):

    def to_foreign(self, obj, name, value):
        if hasattr(value, '__markdown__'):
            return value.__markdown__()
        else:
            if hasattr(value, 'as_markdown'):
                return value.as_markdown
            return super(Markdown, self).to_foreign(obj, name, value)

    def to_native(self, obj, name, value):
        return MarkdownString(value)