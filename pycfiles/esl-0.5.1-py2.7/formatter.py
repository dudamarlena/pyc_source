# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/esl/formatter.py
# Compiled at: 2016-04-16 02:22:25
from __future__ import absolute_import
import json, pygments.lexer, pygments.token, pygments.styles, pygments.lexers, pygments.style
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound
AVAILABLE_STYLES = set(pygments.styles.STYLE_MAP.keys())
AVAILABLE_STYLES.add('solarized')
DEFAULT_STYLE = 'solarized'

class ColorFormatter(object):
    """
    Colorize using Pygments

    This processor that applies syntax highlighting to the headers,
    and also to the body if its content type is recognized.

    """

    def __init__(self, explicit_json=False, color_scheme=DEFAULT_STYLE, **kwargs):
        super(ColorFormatter, self).__init__(**kwargs)
        self.explicit_json = explicit_json
        try:
            style_class = pygments.styles.get_style_by_name(color_scheme)
        except ClassNotFound:
            style_class = Solarized256Style

        self.formatter = Terminal256Formatter(style=style_class)

    def format_headers(self, headers):
        return pygments.highlight(headers, HTTPLexer(), self.formatter).strip()

    def format_body(self, body, mime):
        lexer = self.get_lexer(mime, body)
        if lexer:
            body = pygments.highlight(body, lexer, self.formatter)
        return body.strip()

    def get_lexer(self, mime, body):
        return get_lexer(mime=mime, explicit_json=self.explicit_json, body=body)


def get_lexer(mime, explicit_json=False, body=''):
    mime_types, lexer_names = [
     mime], []
    type_, subtype = mime.split('/', 1)
    if '+' not in subtype:
        lexer_names.append(subtype)
    else:
        subtype_name, subtype_suffix = subtype.split('+', 1)
        lexer_names.extend([subtype_name, subtype_suffix])
        mime_types.extend([
         '%s/%s' % (type_, subtype_name),
         '%s/%s' % (type_, subtype_suffix)])
    if 'json' in subtype:
        lexer_names.append('json')
    lexer = None
    for mime_type in mime_types:
        try:
            lexer = pygments.lexers.get_lexer_for_mimetype(mime_type)
            break
        except ClassNotFound:
            pass

    else:
        for name in lexer_names:
            try:
                lexer = pygments.lexers.get_lexer_by_name(name)
            except ClassNotFound:
                pass

        if explicit_json and body and (not lexer or isinstance(lexer, TextLexer)):
            try:
                json.loads(body)
            except ValueError:
                pass
            else:
                lexer = pygments.lexers.get_lexer_by_name('json')

        return lexer


class HTTPLexer(pygments.lexer.RegexLexer):
    """Simplified HTTP lexer for Pygments.

    It only operates on headers and provides a stronger contrast between
    their names and values than the original one bundled with Pygments
    (:class:`pygments.lexers.text import HttpLexer`), especially when
    Solarized color scheme is used.

    """
    name = 'HTTP'
    aliases = ['http']
    filenames = ['*.http']
    tokens = {'root': [
              (
               '([A-Z]+)( +)([^ ]+)( +)(HTTP)(/)(\\d+\\.\\d+)',
               pygments.lexer.bygroups(pygments.token.Name.Function, pygments.token.Text, pygments.token.Name.Namespace, pygments.token.Text, pygments.token.Keyword.Reserved, pygments.token.Operator, pygments.token.Number)),
              (
               '(HTTP)(/)(\\d+\\.\\d+)( +)(\\d{3})( +)(.+)',
               pygments.lexer.bygroups(pygments.token.Keyword.Reserved, pygments.token.Operator, pygments.token.Number, pygments.token.Text, pygments.token.Number, pygments.token.Text, pygments.token.Name.Exception)),
              (
               '(.*?)( *)(:)( *)(.+)',
               pygments.lexer.bygroups(pygments.token.Name.Attribute, pygments.token.Text, pygments.token.Operator, pygments.token.Text, pygments.token.String))]}


class Solarized256Style(pygments.style.Style):
    """
    solarized256
    ------------

    A Pygments style inspired by Solarized's 256 color mode.

    :copyright: (c) 2011 by Hank Gay, (c) 2012 by John Mastro.
    :license: BSD, see LICENSE for more details.

    """
    BASE03 = '#1c1c1c'
    BASE02 = '#262626'
    BASE01 = '#4e4e4e'
    BASE00 = '#585858'
    BASE0 = '#808080'
    BASE1 = '#8a8a8a'
    BASE2 = '#d7d7af'
    BASE3 = '#ffffd7'
    YELLOW = '#af8700'
    ORANGE = '#d75f00'
    RED = '#af0000'
    MAGENTA = '#af005f'
    VIOLET = '#5f5faf'
    BLUE = '#0087ff'
    CYAN = '#00afaf'
    GREEN = '#5f8700'
    background_color = BASE03
    styles = {pygments.token.Keyword: GREEN, 
       pygments.token.Keyword.Constant: ORANGE, 
       pygments.token.Keyword.Declaration: BLUE, 
       pygments.token.Keyword.Namespace: ORANGE, 
       pygments.token.Keyword.Reserved: BLUE, 
       pygments.token.Keyword.Type: RED, 
       pygments.token.Name.Attribute: BASE1, 
       pygments.token.Name.Builtin: BLUE, 
       pygments.token.Name.Builtin.Pseudo: BLUE, 
       pygments.token.Name.Class: BLUE, 
       pygments.token.Name.Constant: ORANGE, 
       pygments.token.Name.Decorator: BLUE, 
       pygments.token.Name.Entity: ORANGE, 
       pygments.token.Name.Exception: YELLOW, 
       pygments.token.Name.Function: BLUE, 
       pygments.token.Name.Tag: BLUE, 
       pygments.token.Name.Variable: BLUE, 
       pygments.token.String: CYAN, 
       pygments.token.String.Backtick: BASE01, 
       pygments.token.String.Char: CYAN, 
       pygments.token.String.Doc: CYAN, 
       pygments.token.String.Escape: RED, 
       pygments.token.String.Heredoc: CYAN, 
       pygments.token.String.Regex: RED, 
       pygments.token.Number: CYAN, 
       pygments.token.Operator: BASE1, 
       pygments.token.Operator.Word: GREEN, 
       pygments.token.Comment: BASE01, 
       pygments.token.Comment.Preproc: GREEN, 
       pygments.token.Comment.Special: GREEN, 
       pygments.token.Generic.Deleted: CYAN, 
       pygments.token.Generic.Emph: 'italic', 
       pygments.token.Generic.Error: RED, 
       pygments.token.Generic.Heading: ORANGE, 
       pygments.token.Generic.Inserted: GREEN, 
       pygments.token.Generic.Strong: 'bold', 
       pygments.token.Generic.Subheading: ORANGE, 
       pygments.token.Token: BASE1, 
       pygments.token.Token.Other: ORANGE}