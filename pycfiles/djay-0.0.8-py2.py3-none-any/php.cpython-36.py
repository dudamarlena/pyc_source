# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/php.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 10821 bytes
"""
    pygments.lexers.php
    ~~~~~~~~~~~~~~~~~~~

    Lexers for PHP and related languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, default, using, this, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Other
from pygments.util import get_bool_opt, get_list_opt, iteritems, shebang_matches
__all__ = [
 'ZephirLexer', 'PhpLexer']

class ZephirLexer(RegexLexer):
    __doc__ = '\n    For `Zephir language <http://zephir-lang.com/>`_ source code.\n\n    Zephir is a compiled high level language aimed\n    to the creation of C-extensions for PHP.\n\n    .. versionadded:: 2.0\n    '
    name = 'Zephir'
    aliases = ['zephir']
    filenames = ['*.zep']
    zephir_keywords = [
     'fetch', 'echo', 'isset', 'empty']
    zephir_type = ['bit', 'bits', 'string']
    flags = re.DOTALL | re.MULTILINE
    tokens = {'commentsandwhitespace':[
      (
       '\\s+', Text),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*.*?\\*/', Comment.Multiline)], 
     'slashstartsregex':[
      include('commentsandwhitespace'),
      (
       '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
       String.Regex, '#pop'),
      default('#pop')], 
     'badregex':[
      (
       '\\n', Text, '#pop')], 
     'root':[
      (
       '^(?=\\s|/|<!--)', Text, 'slashstartsregex'),
      include('commentsandwhitespace'),
      (
       '\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|->|[-<>+*%&|^/])=?',
       Operator, 'slashstartsregex'),
      (
       '[{(\\[;,]', Punctuation, 'slashstartsregex'),
      (
       '[})\\].]', Punctuation),
      (
       '(for|in|while|do|break|return|continue|switch|case|default|if|else|loop|require|inline|throw|try|catch|finally|new|delete|typeof|instanceof|void|namespace|use|extends|this|fetch|isset|unset|echo|fetch|likely|unlikely|empty)\\b',
       Keyword, 'slashstartsregex'),
      (
       '(var|let|with|function)\\b', Keyword.Declaration, 'slashstartsregex'),
      (
       '(abstract|boolean|bool|char|class|const|double|enum|export|extends|final|native|goto|implements|import|int|string|interface|long|ulong|char|uchar|float|unsigned|private|protected|public|short|static|self|throws|reverse|transient|volatile)\\b',
       Keyword.Reserved),
      (
       '(true|false|null|undefined)\\b', Keyword.Constant),
      (
       '(Array|Boolean|Date|_REQUEST|_COOKIE|_SESSION|_GET|_POST|_SERVER|this|stdClass|range|count|iterator|window)\\b',
       Name.Builtin),
      (
       '[$a-zA-Z_][\\w\\\\]*', Name.Other),
      (
       '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '[0-9]+', Number.Integer),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
      (
       "'(\\\\\\\\|\\\\'|[^'])*'", String.Single)]}


class PhpLexer(RegexLexer):
    __doc__ = "\n    For `PHP <http://www.php.net/>`_ source code.\n    For PHP embedded in HTML, use the `HtmlPhpLexer`.\n\n    Additional options accepted:\n\n    `startinline`\n        If given and ``True`` the lexer starts highlighting with\n        php code (i.e.: no starting ``<?php`` required).  The default\n        is ``False``.\n    `funcnamehighlighting`\n        If given and ``True``, highlight builtin function names\n        (default: ``True``).\n    `disabledmodules`\n        If given, must be a list of module names whose function names\n        should not be highlighted. By default all modules are highlighted\n        except the special ``'unknown'`` module that includes functions\n        that are known to php but are undocumented.\n\n        To get a list of allowed modules have a look into the\n        `_php_builtins` module:\n\n        .. sourcecode:: pycon\n\n            >>> from pygments.lexers._php_builtins import MODULES\n            >>> MODULES.keys()\n            ['PHP Options/Info', 'Zip', 'dba', ...]\n\n        In fact the names of those modules match the module names from\n        the php documentation.\n    "
    name = 'PHP'
    aliases = ['php', 'php3', 'php4', 'php5']
    filenames = ['*.php', '*.php[345]', '*.inc']
    mimetypes = ['text/x-php']
    _ident_char = '[\\\\\\w]|[^\\x00-\\x7f]'
    _ident_begin = '(?:[\\\\_a-z]|[^\\x00-\\x7f])'
    _ident_end = '(?:' + _ident_char + ')*'
    _ident_inner = _ident_begin + _ident_end
    flags = re.IGNORECASE | re.DOTALL | re.MULTILINE
    tokens = {'root':[
      (
       '<\\?(php)?', Comment.Preproc, 'php'),
      (
       '[^<]+', Other),
      (
       '<', Other)], 
     'php':[
      (
       '\\?>', Comment.Preproc, '#pop'),
      (
       '(<<<)([\\\'"]?)(' + _ident_inner + ')(\\2\\n.*?\\n\\s*)(\\3)(;?)(\\n)',
       bygroups(String, String, String.Delimiter, String, String.Delimiter, Punctuation, Text)),
      (
       '\\s+', Text),
      (
       '#.*?\\n', Comment.Single),
      (
       '//.*?\\n', Comment.Single),
      (
       '/\\*\\*/', Comment.Multiline),
      (
       '/\\*\\*.*?\\*/', String.Doc),
      (
       '/\\*.*?\\*/', Comment.Multiline),
      (
       '(->|::)(\\s*)(' + _ident_inner + ')',
       bygroups(Operator, Text, Name.Attribute)),
      (
       '[~!%^&*+=|:.<>/@-]+', Operator),
      (
       '\\?', Operator),
      (
       '[\\[\\]{}();,]+', Punctuation),
      (
       '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
      (
       '(function)(\\s*)(?=\\()', bygroups(Keyword, Text)),
      (
       '(function)(\\s+)(&?)(\\s*)',
       bygroups(Keyword, Text, Operator, Text), 'functionname'),
      (
       '(const)(\\s+)(' + _ident_inner + ')',
       bygroups(Keyword, Text, Name.Constant)),
      (
       '(and|E_PARSE|old_function|E_ERROR|or|as|E_WARNING|parent|eval|PHP_OS|break|exit|case|extends|PHP_VERSION|cfunction|FALSE|print|for|require|continue|foreach|require_once|declare|return|default|static|do|switch|die|stdClass|echo|else|TRUE|elseif|var|empty|if|xor|enddeclare|include|virtual|endfor|include_once|while|endforeach|global|endif|list|endswitch|new|endwhile|not|array|E_ALL|NULL|final|php_user_filter|interface|implements|public|private|protected|abstract|clone|try|catch|throw|this|use|namespace|trait|yield|finally)\\b',
       Keyword),
      (
       '(true|false|null)\\b', Keyword.Constant),
      include('magicconstants'),
      (
       '\\$\\{\\$+' + _ident_inner + '\\}', Name.Variable),
      (
       '\\$+' + _ident_inner, Name.Variable),
      (
       _ident_inner, Name.Other),
      (
       '(\\d+\\.\\d*|\\d*\\.\\d+)(e[+-]?[0-9]+)?', Number.Float),
      (
       '\\d+e[+-]?[0-9]+', Number.Float),
      (
       '0[0-7]+', Number.Oct),
      (
       '0x[a-f0-9]+', Number.Hex),
      (
       '\\d+', Number.Integer),
      (
       '0b[01]+', Number.Bin),
      (
       "'([^'\\\\]*(?:\\\\.[^'\\\\]*)*)'", String.Single),
      (
       '`([^`\\\\]*(?:\\\\.[^`\\\\]*)*)`', String.Backtick),
      (
       '"', String.Double, 'string')], 
     'magicfuncs':[
      (
       words(('__construct', '__destruct', '__call', '__callStatic', '__get', '__set', '__isset',
       '__unset', '__sleep', '__wakeup', '__toString', '__invoke', '__set_state',
       '__clone', '__debugInfo'),
         suffix='\\b'),
       Name.Function.Magic)], 
     'magicconstants':[
      (
       words(('__LINE__', '__FILE__', '__DIR__', '__FUNCTION__', '__CLASS__', '__TRAIT__',
       '__METHOD__', '__NAMESPACE__'),
         suffix='\\b'),
       Name.Constant)], 
     'classname':[
      (
       _ident_inner, Name.Class, '#pop')], 
     'functionname':[
      include('magicfuncs'),
      (
       _ident_inner, Name.Function, '#pop'),
      default('#pop')], 
     'string':[
      (
       '"', String.Double, '#pop'),
      (
       '[^{$"\\\\]+', String.Double),
      (
       '\\\\([nrt"$\\\\]|[0-7]{1,3}|x[0-9a-f]{1,2})', String.Escape),
      (
       '\\$' + _ident_inner + '(\\[\\S+?\\]|->' + _ident_inner + ')?',
       String.Interpol),
      (
       '(\\{\\$\\{)(.*?)(\\}\\})',
       bygroups(String.Interpol, using(this, _startinline=True), String.Interpol)),
      (
       '(\\{)(\\$.*?)(\\})',
       bygroups(String.Interpol, using(this, _startinline=True), String.Interpol)),
      (
       '(\\$\\{)(\\S+)(\\})',
       bygroups(String.Interpol, Name.Variable, String.Interpol)),
      (
       '[${\\\\]', String.Double)]}

    def __init__(self, **options):
        self.funcnamehighlighting = get_bool_opt(options, 'funcnamehighlighting', True)
        self.disabledmodules = get_list_opt(options, 'disabledmodules', ['unknown'])
        self.startinline = get_bool_opt(options, 'startinline', False)
        if '_startinline' in options:
            self.startinline = options.pop('_startinline')
        self._functions = set()
        if self.funcnamehighlighting:
            from pygments.lexers._php_builtins import MODULES
            for key, value in iteritems(MODULES):
                if key not in self.disabledmodules:
                    self._functions.update(value)

        (RegexLexer.__init__)(self, **options)

    def get_tokens_unprocessed(self, text):
        stack = [
         'root']
        if self.startinline:
            stack.append('php')
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name.Other:
                if value in self._functions:
                    yield (
                     index, Name.Builtin, value)
                    continue
            yield (
             index, token, value)

    def analyse_text(text):
        if shebang_matches(text, 'php'):
            return True
        else:
            rv = 0.0
            if re.search('<\\?(?!xml)', text):
                rv += 0.3
            return rv