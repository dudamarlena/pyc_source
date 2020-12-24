# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/email.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 5207 bytes
"""
    pygments.lexers.email
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for the raw E-mail.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, DelegatingLexer, bygroups
from pygments.lexers.mime import MIMELexer
from pygments.token import Text, Keyword, Name, String, Number, Comment
from pygments.util import get_bool_opt
__all__ = [
 'EmailLexer']

class EmailHeaderLexer(RegexLexer):
    __doc__ = '\n    Sub-lexer for raw E-mail. This lexer only process header part of e-mail.\n\n    .. versionadded:: 2.5\n    '

    def __init__(self, **options):
        (super(EmailHeaderLexer, self).__init__)(**options)
        self.highlight_x = get_bool_opt(options, 'highlight-X-header', False)

    def get_x_header_tokens(self, match):
        if self.highlight_x:
            yield (match.start(1), Name.Tag, match.group(1))
            default_actions = self.get_tokens_unprocessed((match.group(2)),
              stack=('root', 'header'))
            for item in default_actions:
                yield item

        else:
            yield (
             match.start(1), Comment.Special, match.group(1))
            yield (match.start(2), Comment.Multiline, match.group(2))

    tokens = {'root':[
      (
       '^(?:[A-WYZ]|X400)[\\w\\-]*:', Name.Tag, 'header'),
      (
       '^(X-(?:\\w[\\w\\-]*:))([\\s\\S]*?\\n)(?![ \\t])', get_x_header_tokens)], 
     'header':[
      (
       '\\n[ \\t]', Text.Whitespace),
      (
       '\\n(?![ \\t])', Text.Whitespace, '#pop'),
      (
       '\\bE?SMTPS?\\b', Keyword),
      (
       '\\b(?:HE|EH)LO\\b', Keyword),
      (
       '[\\w\\.\\-\\+=]+@[\\w\\.\\-]+', Name.Label),
      (
       '<[\\w\\.\\-\\+=]+@[\\w\\.\\-]+>', Name.Label),
      (
       '\\b(\\w[\\w\\.-]*\\.[\\w\\.-]*\\w[a-zA-Z]+)\\b', Name.Function),
      (
       '(?<=\\b)(?:(?:25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)(?=\\b)',
       Number.Integer),
      (
       '(?<=\\b)([0-9a-fA-F]{1,4}:){1,7}:(?!\\b)', Number.Hex),
      (
       '(?<=\\b):((:[0-9a-fA-F]{1,4}){1,7}|:)(?=\\b)', Number.Hex),
      (
       '(?<=\\b)([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}(?=\\b)', Number.Hex),
      (
       '(?<=\\b)([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}(?=\\b)', Number.Hex),
      (
       '(?<=\\b)[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})(?=\\b)', Number.Hex),
      (
       '(?<=\\b)fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}(?=\\b)', Number.Hex),
      (
       '(?<=\\b)([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}(?=\\b)', Number.Hex),
      (
       '(?<=\\b)([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}(?=\\b)',
       Number.Hex),
      (
       '(?<=\\b)([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}(?=\\b)',
       Number.Hex),
      (
       '(?<=\\b)([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}(?=\\b)',
       Number.Hex),
      (
       '(?<=\\b)::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])(?=\\b)',
       Number.Hex),
      (
       '(?<=\\b)([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])(?=\\b)',
       Number.Hex),
      (
       '(?:(Sun|Mon|Tue|Wed|Thu|Fri|Sat),\\s+)?(0[1-9]|[1-2]?[0-9]|3[01])\\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+(19[0-9]{2}|[2-9][0-9]{3})\\s+(2[0-3]|[0-1][0-9]):([0-5][0-9])(?::(60|[0-5][0-9]))?(?:\\.\\d{1,5})?\\s+([-\\+][0-9]{2}[0-5][0-9]|\\(?(?:UTC?|GMT|(?:E|C|M|P)(?:ST|ET|DT)|[A-IK-Z])\\)?)',
       Name.Decorator),
      (
       '(=\\?)([\\w-]+)(\\?)([BbQq])(\\?)([\\[\\w!\\"#$%&\\\'()*+,-./:;<=>@[\\\\\\]^_`{|}~]+)(\\?=)',
       bygroups(String.Affix, Name.Constant, String.Affix, Keyword.Constant, String.Affix, Number.Hex, String.Affix)),
      (
       '[\\s]+', Text.Whitespace),
      (
       '[\\S]', Text)]}


class EmailLexer(DelegatingLexer):
    __doc__ = '\n    Lexer for raw E-mail.\n\n    Additional options accepted:\n\n    `highlight-X-header`\n        Highlight the fields of ``X-`` user-defined email header. (default:\n        ``False``).\n\n    .. versionadded:: 2.5\n    '
    name = 'E-mail'
    aliases = ['email', 'eml']
    filenames = ['*.eml']
    mimetypes = ['message/rfc822']

    def __init__(self, **options):
        (super(EmailLexer, self).__init__)(
         EmailHeaderLexer, MIMELexer, Comment, **options)