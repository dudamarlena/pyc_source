# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/mime.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 7975 bytes
"""
    pygments.lexers.mime
    ~~~~~~~~~~~~~~~~~~~~

    Lexer for Multipurpose Internet Mail Extensions (MIME) data.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include
from pygments.lexers import get_lexer_for_mimetype
from pygments.token import Text, Name, String, Operator, Comment, Other
from pygments.util import get_int_opt, ClassNotFound
__all__ = [
 'MIMELexer']

class MIMELexer(RegexLexer):
    __doc__ = '\n    Lexer for Multipurpose Internet Mail Extensions (MIME) data. This lexer is\n    designed to process the nested mulitpart data.\n\n    It assumes that the given data contains both header and body (and is\n    splitted by empty line). If no valid header is found, then the entire data\n    would be treated as body.\n\n    Additional options accepted:\n\n    `MIME-max-level`\n        Max recurssion level for nested MIME structure. Any negative number\n        would treated as unlimited. (default: -1)\n\n    `Content-Type`\n        Treat the data as specific content type. Useful when header is\n        missing, or this lexer would try to parse from header. (default:\n        `text/plain`)\n\n    `Multipart-Boundary`\n        Set the default multipart boundary delimiter. This option is only used\n        when `Content-Type` is `multipart` and header is missing. This lexer\n        would try to parse from header by default. (default: None)\n\n    `Content-Transfer-Encoding`\n        Treat the data as specific encoding. Or this lexer would try to parse\n        from header by default. (default: None)\n\n    .. versionadded:: 2.5\n    '
    name = 'MIME'
    aliases = ['mime']
    mimetypes = ['multipart/mixed',
     'multipart/related',
     'multipart/alternative']

    def __init__(self, **options):
        (super(MIMELexer, self).__init__)(**options)
        self.boundary = options.get('Multipart-Boundary')
        self.content_transfer_encoding = options.get('Content_Transfer_Encoding')
        self.content_type = options.get('Content_Type', 'text/plain')
        self.max_nested_level = get_int_opt(options, 'MIME-max-level', -1)

    def analyse_text(text):
        try:
            header, body = text.strip().split('\n\n', 1)
            if not body.strip():
                return 0.1
            else:
                invalid_headers = MIMELexer.tokens['header'].sub('', header)
                if invalid_headers.strip():
                    return 0.1
                return 1
        except ValueError:
            return 0.1

    def get_header_tokens(self, match):
        field = match.group(1)
        if field.lower() in self.attention_headers:
            yield (
             match.start(1), Name.Tag, field + ':')
            yield (match.start(2), Text.Whitespace, match.group(2))
            pos = match.end(2)
            body = match.group(3)
            for i, t, v in self.get_tokens_unprocessed(body, ('root', field.lower())):
                yield (
                 pos + i, t, v)

        else:
            yield (
             match.start(), Comment, match.group())

    def get_body_tokens(self, match):
        pos_body_start = match.start()
        entire_body = match.group()
        if entire_body[0] == '\n':
            yield (
             pos_body_start, Text.Whitespace, '\n')
            pos_body_start = pos_body_start + 1
            entire_body = entire_body[1:]
        else:
            if not self.content_type.startswith('multipart') or not self.boundary:
                for i, t, v in self.get_bodypart_tokens(entire_body):
                    yield (
                     pos_body_start + i, t, v)

                return
            bdry_pattern = '^--%s(--)?\\n' % re.escape(self.boundary)
            bdry_matcher = re.compile(bdry_pattern, re.MULTILINE)
            m = bdry_matcher.search(entire_body)
            if m:
                pos_part_start = pos_body_start + m.end()
                pos_iter_start = lpos_end = m.end()
                yield (pos_body_start, Text, entire_body[:m.start()])
                yield (pos_body_start + lpos_end, String.Delimiter, m.group())
            else:
                pos_part_start = pos_body_start
            pos_iter_start = 0
        for m in bdry_matcher.finditer(entire_body, pos_iter_start):
            lpos_start = pos_part_start - pos_body_start
            lpos_end = m.start()
            part = entire_body[lpos_start:lpos_end]
            for i, t, v in self.get_bodypart_tokens(part):
                yield (
                 pos_part_start + i, t, v)

            yield (
             pos_body_start + lpos_end, String.Delimiter, m.group())
            pos_part_start = pos_body_start + m.end()

        lpos_start = pos_part_start - pos_body_start
        if lpos_start != len(entire_body):
            yield (
             pos_part_start, Text, entire_body[lpos_start:])

    def get_bodypart_tokens(self, text):
        if not text.strip() or not self.content_type:
            return [(0, Other, text)]
        else:
            cte = self.content_transfer_encoding
            if cte:
                if cte not in frozenset({'7bit', '8bit', 'quoted-printable'}):
                    return [
                     (
                      0, Other, text)]
            if self.max_nested_level == 0:
                return [
                 (
                  0, Other, text)]
            try:
                lexer = get_lexer_for_mimetype(self.content_type)
            except ClassNotFound:
                return [
                 (
                  0, Other, text)]

            if isinstance(lexer, type(self)):
                lexer.max_nested_level = self.max_nested_level - 1
            return lexer.get_tokens_unprocessed(text)

    def store_content_type(self, match):
        self.content_type = match.group(1)
        prefix_len = match.start(1) - match.start(0)
        yield (match.start(0), Text.Whitespace, match.group(0)[:prefix_len])
        yield (match.start(1), Name.Label, match.group(2))
        yield (match.end(2), String.Delimiter, '/')
        yield (match.start(3), Name.Label, match.group(3))

    def get_content_type_subtokens(self, match):
        yield (
         match.start(1), Text, match.group(1))
        yield (match.start(2), Text.Whitespace, match.group(2))
        yield (match.start(3), Name.Attribute, match.group(3))
        yield (match.start(4), Operator, match.group(4))
        yield (match.start(5), String, match.group(5))
        if match.group(3).lower() == 'boundary':
            boundary = match.group(5).strip()
            if boundary[0] == '"':
                if boundary[(-1)] == '"':
                    boundary = boundary[1:-1]
            self.boundary = boundary

    def store_content_transfer_encoding(self, match):
        self.content_transfer_encoding = match.group(0).lower()
        yield (match.start(0), Name.Constant, match.group(0))

    attention_headers = {
     'content-type', 'content-transfer-encoding'}
    tokens = {'root':[
      (
       '^([\\w-]+):( *)([\\s\\S]*?\\n)(?![ \\t])', get_header_tokens),
      (
       '^$[\\s\\S]+', get_body_tokens)], 
     'header':[
      (
       '\\n[ \\t]', Text.Whitespace),
      (
       '\\n(?![ \\t])', Text.Whitespace, '#pop')], 
     'content-type':[
      include('header'),
      (
       '^\\s*((multipart|application|audio|font|image|model|text|video|message)/([\\w-]+))',
       store_content_type),
      (
       '(;)((?:[ \\t]|\\n[ \\t])*)([\\w:-]+)(=)([\\s\\S]*?)(?=;|\\n(?![ \\t]))',
       get_content_type_subtokens),
      (
       ';[ \\t]*\\n(?![ \\t])', Text, '#pop')], 
     'content-transfer-encoding':[
      include('header'),
      (
       '([\\w-]+)', store_content_transfer_encoding)]}