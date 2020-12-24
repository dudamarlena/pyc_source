# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\zhpy\ext\pygmentplugin.py
# Compiled at: 2015-10-22 21:48:08
import re
try:
    set
except NameError:
    from sets import Set as set

from pygments.lexer import Lexer, RegexLexer, ExtendedRegexLexer, LexerContext, include, combined, do_insertions, bygroups, using
from pygments.token import Error, Text, Comment, Operator, Keyword, Name, String, Number, Generic, Punctuation
from pygments.util import get_bool_opt, get_list_opt, shebang_matches
from pygments import unistring as uni
from pygments.lexers.functional import SchemeLexer
line_re = re.compile('.*?\n')

class ZhpyLexer(RegexLexer):
    """
    for zhpy <zhpy.googlecode.com> source code
    """
    name = 'Zhpy'
    aliases = ['zhpy']
    filenames = ['*.twpy', '*.cnpy', '*.py']
    tokens = {'root': [
              (
               '\\n', Text),
              (
               '^(\\s*)("""(?:.|\\n)*?""")', bygroups(Text, String.Doc)),
              (
               "^(\\s*)('''(?:.|\\n)*?''')", bygroups(Text, String.Doc)),
              (
               '[^\\S\\n]+', Text),
              (
               '#.*$', Comment),
              (
               '[]{}:(),;[]', Punctuation),
              (
               '\\\\\\n', Text),
              (
               '\\\\', Text),
              (
               '(in|is|and|or|not)\\b', Operator.Word),
              (
               '!=|==|<<|>>|[-~+/*%=<>&^|.]', Operator),
              include('keywords'),
              (
               '(def)(\\s+)', bygroups(Keyword, Text), 'funcname'),
              (
               '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
              (
               '(from)(\\s+)', bygroups(Keyword, Text), 'fromimport'),
              (
               '(import)(\\s+)', bygroups(Keyword, Text), 'import'),
              include('builtins'),
              include('backtick'),
              (
               '(?:[rR]|[uU][rR]|[rR][uU])"""', String, 'tdqs'),
              (
               "(?:[rR]|[uU][rR]|[rR][uU])'''", String, 'tsqs'),
              (
               '(?:[rR]|[uU][rR]|[rR][uU])"', String, 'dqs'),
              (
               "(?:[rR]|[uU][rR]|[rR][uU])'", String, 'sqs'),
              (
               '[uU]?"""', String, combined('stringescape', 'tdqs')),
              (
               "[uU]?'''", String, combined('stringescape', 'tsqs')),
              (
               '[uU]?"', String, combined('stringescape', 'dqs')),
              (
               "[uU]?'", String, combined('stringescape', 'sqs')),
              include('name'),
              include('numbers')], 
       'keywords': [
                  (
                   '(assert|break|continue|del|elif|else|except|exec|finally|for|global|if|lambda|pass|print|raise|return|try|while|yield|as|with|印出|輸入)\\b',
                   Keyword)], 
       'builtins': [
                  (
                   '(?<!\\.)(__import__|abs|apply|basestring|bool|buffer|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|exit|file|filter|float|getattr|globals|hasattr|hash|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|min|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|round|setattr|slice|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\\b',
                   Name.Builtin),
                  (
                   '(?<!\\.)(self|None|Ellipsis|NotImplemented|False|True)\\b',
                   Name.Builtin.Pseudo),
                  (
                   '(?<!\\.)(ArithmeticError|AssertionError|AttributeError|BaseException|DeprecationWarning|EOFError|EnvironmentError|Exception|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError|ImportWarning|IndentationError|IndexError|KeyError|KeyboardInterrupt|LookupError|MemoryError|NameError|NotImplemented|NotImplementedError|OSError|OverflowError|OverflowWarning|PendingDeprecationWarning|ReferenceError|RuntimeError|RuntimeWarning|StandardError|StopIteration|SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|Warning|ZeroDivisionError)\\b',
                   Name.Exception)], 
       'numbers': [
                 (
                  '(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
                 (
                  '0\\d+', Number.Oct),
                 (
                  '0[xX][a-fA-F0-9]+', Number.Hex),
                 (
                  '\\d+L', Number.Integer.Long),
                 (
                  '\\d+', Number.Integer)], 
       'backtick': [
                  (
                   '`.*?`', String.Backtick)], 
       'name': [
              (
               '@[a-zA-Z0-9_]+', Name.Decorator),
              (
               '[a-zA-Z_][a-zA-Z0-9_u"\\u0080-\\ufe01]*', Name)], 
       'funcname': [
                  (
                   '[a-zA-Z_][a-zA-Z0-9_\\u0080-\\ufe01]*', Name.Function, '#pop')], 
       'classname': [
                   (
                    '[a-zA-Z_][a-zA-Z0-9_\\u0080-\\ufe01]*', Name.Class, '#pop')], 
       'import': [
                (
                 '(\\s+)(as)(\\s+)', bygroups(Text, Keyword, Text)),
                (
                 '[a-zA-Z_][a-zA-Z0-9_.\\u0080-\\ufe01]*', Name.Namespace),
                (
                 '(\\s*)(,)(\\s*)', bygroups(Text, Operator, Text)),
                (
                 '', Text, '#pop')], 
       'fromimport': [
                    (
                     '(\\s+)(import)\\b', bygroups(Text, Keyword), '#pop'),
                    (
                     '[a-zA-Z_.][a-zA-Z0-9_.]*', Name.Namespace)], 
       'stringescape': [
                      (
                       '\\\\([\\\\abfnrtv"\\\']|\\n|N{.*?}|u[a-fA-F0-9]{4}|U[a-fA-F0-9\\u0080-\\ufe01]{8}|x[a-fA-F0-9\\u0080-\\ufe01]{2}|[0-7]{1,3})',
                       String.Escape)], 
       'strings': [
                 (
                  '%(\\([a-zA-Z0-9\\u0080-\\ufe01]+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[diouxXeEfFgGcrs%]',
                  String.Interpol),
                 (
                  '[^\\\\\\\'"%\\n]+', String),
                 (
                  '[\\\'"\\\\]', String),
                 (
                  '%', String)], 
       'nl': [
            (
             '\\n', String)], 
       'dqs': [
             (
              '"', String, '#pop'),
             (
              '\\\\\\\\|\\\\"|\\\\\\n', String.Escape),
             include('strings')], 
       'sqs': [
             (
              "'", String, '#pop'),
             (
              "\\\\\\\\|\\\\'|\\\\\\n", String.Escape),
             include('strings')], 
       'tdqs': [
              (
               '"""', String, '#pop'),
              include('strings'),
              include('nl')], 
       'tsqs': [
              (
               "'''", String, '#pop'),
              include('strings'),
              include('nl')]}

    def analyse_text(text):
        return shebang_matches(text, 'pythonw?(2\\.\\d)?')