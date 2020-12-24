# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/textfmts.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 10852 bytes
"""
    pygments.lexers.textfmts
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for various text formats.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Generic, Literal
from pygments.util import ClassNotFound
__all__ = [
 'IrcLogsLexer', 'TodotxtLexer', 'HttpLexer', 'GettextLexer']

class IrcLogsLexer(RegexLexer):
    __doc__ = '\n    Lexer for IRC logs in *irssi*, *xchat* or *weechat* style.\n    '
    name = 'IRC logs'
    aliases = ['irc']
    filenames = ['*.weechatlog']
    mimetypes = ['text/x-irclog']
    flags = re.VERBOSE | re.MULTILINE
    timestamp = '\n        (\n          # irssi / xchat and others\n          (?: \\[|\\()?                  # Opening bracket or paren for the timestamp\n            (?:                        # Timestamp\n                (?: (?:\\d{1,4} [-/])*  # Date as - or /-separated groups of digits\n                    (?:\\d{1,4})\n                 [T ])?                # Date/time separator: T or space\n                (?: \\d?\\d [:.])*       # Time as :/.-separated groups of 1 or 2 digits\n                    (?: \\d?\\d)\n            )\n          (?: \\]|\\))?\\s+               # Closing bracket or paren for the timestamp\n        |\n          # weechat\n          \\d{4}\\s\\w{3}\\s\\d{2}\\s        # Date\n          \\d{2}:\\d{2}:\\d{2}\\s+         # Time + Whitespace\n        |\n          # xchat\n          \\w{3}\\s\\d{2}\\s               # Date\n          \\d{2}:\\d{2}:\\d{2}\\s+         # Time + Whitespace\n        )?\n    '
    tokens = {'root': [
              (
               '^\\*\\*\\*\\*(.*)\\*\\*\\*\\*$', Comment),
              (
               '^' + timestamp + '(\\s*<[^>]*>\\s*)$', bygroups(Comment.Preproc, Name.Tag)),
              (
               '^' + timestamp + '\n                (\\s*<.*?>\\s*)          # Nick ',
               bygroups(Comment.Preproc, Name.Tag), 'msg'),
              (
               '^' + timestamp + '\n                (\\s*[*]\\s+)            # Star\n                (\\S+\\s+.*?\\n)          # Nick + rest of message ',
               bygroups(Comment.Preproc, Keyword, Generic.Inserted)),
              (
               '^' + timestamp + '\n                (\\s*(?:\\*{3}|<?-[!@=P]?->?)\\s*)  # Star(s) or symbols\n                (\\S+\\s+)                     # Nick + Space\n                (.*?\\n)                         # Rest of message ',
               bygroups(Comment.Preproc, Keyword, String, Comment)),
              (
               '^.*?\\n', Text)], 
     
     'msg': [
             (
              '\\S+:(?!//)', Name.Attribute),
             (
              '.*\\n', Text, '#pop')]}


class GettextLexer(RegexLexer):
    __doc__ = '\n    Lexer for Gettext catalog files.\n\n    .. versionadded:: 0.9\n    '
    name = 'Gettext Catalog'
    aliases = ['pot', 'po']
    filenames = ['*.pot', '*.po']
    mimetypes = ['application/x-gettext', 'text/x-gettext', 'text/gettext']
    tokens = {'root': [
              (
               '^#,\\s.*?$', Keyword.Type),
              (
               '^#:\\s.*?$', Keyword.Declaration),
              (
               '^(#|#\\.\\s|#\\|\\s|#~\\s|#\\s).*$', Comment.Single),
              (
               '^(")([A-Za-z-]+:)(.*")$',
               bygroups(String, Name.Property, String)),
              (
               '^".*"$', String),
              (
               '^(msgid|msgid_plural|msgstr|msgctxt)(\\s+)(".*")$',
               bygroups(Name.Variable, Text, String)),
              (
               '^(msgstr\\[)(\\d)(\\])(\\s+)(".*")$',
               bygroups(Name.Variable, Number.Integer, Name.Variable, Text, String))]}


class HttpLexer(RegexLexer):
    __doc__ = '\n    Lexer for HTTP sessions.\n\n    .. versionadded:: 1.5\n    '
    name = 'HTTP'
    aliases = ['http']
    flags = re.DOTALL

    def get_tokens_unprocessed(self, text, stack=('root', )):
        """Reset the content-type state."""
        self.content_type = None
        return RegexLexer.get_tokens_unprocessed(self, text, stack)

    def header_callback(self, match):
        if match.group(1).lower() == 'content-type':
            content_type = match.group(5).strip()
            if ';' in content_type:
                content_type = content_type[:content_type.find(';')].strip()
            self.content_type = content_type
        yield (
         match.start(1), Name.Attribute, match.group(1))
        yield (match.start(2), Text, match.group(2))
        yield (match.start(3), Operator, match.group(3))
        yield (match.start(4), Text, match.group(4))
        yield (match.start(5), Literal, match.group(5))
        yield (match.start(6), Text, match.group(6))

    def continuous_header_callback(self, match):
        yield (
         match.start(1), Text, match.group(1))
        yield (match.start(2), Literal, match.group(2))
        yield (match.start(3), Text, match.group(3))

    def content_callback(self, match):
        content_type = getattr(self, 'content_type', None)
        content = match.group()
        offset = match.start()
        if content_type:
            from pygments.lexers import get_lexer_for_mimetype
            possible_lexer_mimetypes = [
             content_type]
            if '+' in content_type:
                general_type = re.sub('^(.*)/.*\\+(.*)$', '\\1/\\2', content_type)
                possible_lexer_mimetypes.append(general_type)
            for i in possible_lexer_mimetypes:
                try:
                    lexer = get_lexer_for_mimetype(i)
                except ClassNotFound:
                    pass
                else:
                    for idx, token, value in lexer.get_tokens_unprocessed(content):
                        yield (
                         offset + idx, token, value)

                    return

        yield (
         offset, Text, content)

    tokens = {'root': [
              (
               '(GET|POST|PUT|DELETE|HEAD|OPTIONS|TRACE|PATCH)( +)([^ ]+)( +)(HTTP)(/)(1\\.[01])(\\r?\\n|\\Z)',
               bygroups(Name.Function, Text, Name.Namespace, Text, Keyword.Reserved, Operator, Number, Text),
               'headers'),
              (
               '(HTTP)(/)(1\\.[01])( +)(\\d{3})( +)([^\\r\\n]+)(\\r?\\n|\\Z)',
               bygroups(Keyword.Reserved, Operator, Number, Text, Number, Text, Name.Exception, Text),
               'headers')], 
     
     'headers': [
                 (
                  '([^\\s:]+)( *)(:)( *)([^\\r\\n]+)(\\r?\\n|\\Z)', header_callback),
                 (
                  '([\\t ]+)([^\\r\\n]+)(\\r?\\n|\\Z)', continuous_header_callback),
                 (
                  '\\r?\\n', Text, 'content')], 
     
     'content': [
                 (
                  '.+', content_callback)]}

    def analyse_text(text):
        return text.startswith(('GET /', 'POST /', 'PUT /', 'DELETE /', 'HEAD /', 'OPTIONS /',
                                'TRACE /', 'PATCH /'))


class TodotxtLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Todo.txt <http://todotxt.com/>`_ todo list format.\n\n    .. versionadded:: 2.0\n    '
    name = 'Todotxt'
    aliases = ['todotxt']
    filenames = [
     'todo.txt', '*.todotxt']
    mimetypes = ['text/x-todo']
    CompleteTaskText = Operator
    IncompleteTaskText = Text
    Priority = Generic.Heading
    Date = Generic.Subheading
    Project = Generic.Error
    Context = String
    date_regex = '\\d{4,}-\\d{2}-\\d{2}'
    priority_regex = '\\([A-Z]\\)'
    project_regex = '\\+\\S+'
    context_regex = '@\\S+'
    complete_one_date_regex = '(x )(' + date_regex + ')'
    complete_two_date_regex = complete_one_date_regex + '( )(' + date_regex + ')'
    priority_date_regex = '(' + priority_regex + ')( )(' + date_regex + ')'
    tokens = {'root': [
              (
               complete_two_date_regex,
               bygroups(CompleteTaskText, Date, CompleteTaskText, Date),
               'complete'),
              (
               complete_one_date_regex, bygroups(CompleteTaskText, Date),
               'complete'),
              (
               priority_date_regex, bygroups(Priority, IncompleteTaskText, Date),
               'incomplete'),
              (
               priority_regex, Priority, 'incomplete'),
              (
               date_regex, Date, 'incomplete'),
              (
               context_regex, Context, 'incomplete'),
              (
               project_regex, Project, 'incomplete'),
              (
               '\\S+', IncompleteTaskText, 'incomplete')], 
     
     'complete': [
                  (
                   '\\s*\\n', CompleteTaskText, '#pop'),
                  (
                   context_regex, Context),
                  (
                   project_regex, Project),
                  (
                   '\\S+', CompleteTaskText),
                  (
                   '\\s+', CompleteTaskText)], 
     
     'incomplete': [
                    (
                     '\\s*\\n', IncompleteTaskText, '#pop'),
                    (
                     context_regex, Context),
                    (
                     project_regex, Project),
                    (
                     '\\S+', IncompleteTaskText),
                    (
                     '\\s+', IncompleteTaskText)]}