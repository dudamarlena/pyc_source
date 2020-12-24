# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/functional.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.functional
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for functional languages.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, bygroups, include, do_insertions
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Literal, Generic
__all__ = [
 'SchemeLexer', 'CommonLispLexer', 'HaskellLexer', 'LiterateHaskellLexer',
 'OcamlLexer', 'ErlangLexer', 'ErlangShellLexer']

class SchemeLexer(RegexLexer):
    """
    A Scheme lexer, parsing a stream and outputting the tokens
    needed to highlight scheme code.
    This lexer could be most probably easily subclassed to parse
    other LISP-Dialects like Common Lisp, Emacs Lisp or AutoLisp.

    This parser is checked with pastes from the LISP pastebin
    at http://paste.lisp.org/ to cover as much syntax as possible.

    It supports the full Scheme syntax as defined in R5RS.

    *New in Pygments 0.6.*
    """
    name = 'Scheme'
    aliases = ['scheme', 'scm']
    filenames = ['*.scm']
    mimetypes = ['text/x-scheme', 'application/x-scheme']
    keywords = [
     'lambda', 'define', 'if', 'else', 'cond', 'and', 'or', 'case', 'let',
     'let*', 'letrec', 'begin', 'do', 'delay', 'set!', '=>', 'quote',
     'quasiquote', 'unquote', 'unquote-splicing', 'define-syntax',
     'let-syntax', 'letrec-syntax', 'syntax-rules']
    builtins = [
     '*', '+', '-', '/', '<', '<=', '=', '>', '>=', 'abs', 'acos', 'angle',
     'append', 'apply', 'asin', 'assoc', 'assq', 'assv', 'atan',
     'boolean?', 'caaaar', 'caaadr', 'caaar', 'caadar', 'caaddr', 'caadr',
     'caar', 'cadaar', 'cadadr', 'cadar', 'caddar', 'cadddr', 'caddr',
     'cadr', 'call-with-current-continuation', 'call-with-input-file',
     'call-with-output-file', 'call-with-values', 'call/cc', 'car',
     'cdaaar', 'cdaadr', 'cdaar', 'cdadar', 'cdaddr', 'cdadr', 'cdar',
     'cddaar', 'cddadr', 'cddar', 'cdddar', 'cddddr', 'cdddr', 'cddr',
     'cdr', 'ceiling', 'char->integer', 'char-alphabetic?', 'char-ci<=?',
     'char-ci<?', 'char-ci=?', 'char-ci>=?', 'char-ci>?', 'char-downcase',
     'char-lower-case?', 'char-numeric?', 'char-ready?', 'char-upcase',
     'char-upper-case?', 'char-whitespace?', 'char<=?', 'char<?', 'char=?',
     'char>=?', 'char>?', 'char?', 'close-input-port', 'close-output-port',
     'complex?', 'cons', 'cos', 'current-input-port', 'current-output-port',
     'denominator', 'display', 'dynamic-wind', 'eof-object?', 'eq?',
     'equal?', 'eqv?', 'eval', 'even?', 'exact->inexact', 'exact?', 'exp',
     'expt', 'floor', 'for-each', 'force', 'gcd', 'imag-part',
     'inexact->exact', 'inexact?', 'input-port?', 'integer->char',
     'integer?', 'interaction-environment', 'lcm', 'length', 'list',
     'list->string', 'list->vector', 'list-ref', 'list-tail', 'list?',
     'load', 'log', 'magnitude', 'make-polar', 'make-rectangular',
     'make-string', 'make-vector', 'map', 'max', 'member', 'memq', 'memv',
     'min', 'modulo', 'negative?', 'newline', 'not', 'null-environment',
     'null?', 'number->string', 'number?', 'numerator', 'odd?',
     'open-input-file', 'open-output-file', 'output-port?', 'pair?',
     'peek-char', 'port?', 'positive?', 'procedure?', 'quotient',
     'rational?', 'rationalize', 'read', 'read-char', 'real-part', 'real?',
     'remainder', 'reverse', 'round', 'scheme-report-environment',
     'set-car!', 'set-cdr!', 'sin', 'sqrt', 'string', 'string->list',
     'string->number', 'string->symbol', 'string-append', 'string-ci<=?',
     'string-ci<?', 'string-ci=?', 'string-ci>=?', 'string-ci>?',
     'string-copy', 'string-fill!', 'string-length', 'string-ref',
     'string-set!', 'string<=?', 'string<?', 'string=?', 'string>=?',
     'string>?', 'string?', 'substring', 'symbol->string', 'symbol?',
     'tan', 'transcript-off', 'transcript-on', 'truncate', 'values',
     'vector', 'vector->list', 'vector-fill!', 'vector-length',
     'vector-ref', 'vector-set!', 'vector?', 'with-input-from-file',
     'with-output-to-file', 'write', 'write-char', 'zero?']
    valid_name = '[a-zA-Z0-9!$%&*+,/:<=>?@^_~|-]+'
    tokens = {'root': [
              (
               ';.*$', Comment.Single),
              (
               '\\s+', Text),
              (
               '-?\\d+\\.\\d+', Number.Float),
              (
               '-?\\d+', Number.Integer),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               "'" + valid_name, String.Symbol),
              (
               '#\\\\([()/\'\\".\'_!§$%& ?=+-]{1}|[a-zA-Z0-9]+)', String.Char),
              (
               '(#t|#f)', Name.Constant),
              (
               "('|#|`|,@|,|\\.)", Operator),
              (
               '(%s)' % ('|').join([ re.escape(entry) + ' ' for entry in keywords ]),
               Keyword),
              (
               "(?<='\\()" + valid_name, Name.Variable),
              (
               '(?<=#\\()' + valid_name, Name.Variable),
              (
               '(?<=\\()(%s)' % ('|').join([ re.escape(entry) + ' ' for entry in builtins ]),
               Name.Builtin),
              (
               '(?<=\\()' + valid_name, Name.Function),
              (
               valid_name, Name.Variable),
              (
               '(\\(|\\))', Punctuation)]}


class CommonLispLexer(RegexLexer):
    """
    A Common Lisp lexer.

    *New in Pygments 0.9.*
    """
    name = 'Common Lisp'
    aliases = ['common-lisp', 'cl']
    filenames = ['*.cl', '*.lisp', '*.el']
    mimetypes = ['text/x-common-lisp']
    flags = re.IGNORECASE | re.MULTILINE
    nonmacro = '\\\\.|[a-zA-Z0-9!$%&*+-/<=>?@\\[\\]^_{}~]'
    constituent = nonmacro + '|[#.:]'
    terminated = '(?=[ "()\\\'\\n,;`])'
    symbol = '(\\|[^|]+\\||(?:%s)(?:%s)*)' % (nonmacro, constituent)

    def __init__(self, **options):
        from pygments.lexers._clbuiltins import BUILTIN_FUNCTIONS, SPECIAL_FORMS, MACROS, LAMBDA_LIST_KEYWORDS, DECLARATIONS, BUILTIN_TYPES, BUILTIN_CLASSES
        self.builtin_function = BUILTIN_FUNCTIONS
        self.special_forms = SPECIAL_FORMS
        self.macros = MACROS
        self.lambda_list_keywords = LAMBDA_LIST_KEYWORDS
        self.declarations = DECLARATIONS
        self.builtin_types = BUILTIN_TYPES
        self.builtin_classes = BUILTIN_CLASSES
        RegexLexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        stack = [
         'root']
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name.Variable:
                if value in self.builtin_function:
                    yield (
                     index, Name.Builtin, value)
                    continue
                if value in self.special_forms:
                    yield (
                     index, Keyword, value)
                    continue
                if value in self.macros:
                    yield (
                     index, Name.Builtin, value)
                    continue
                if value in self.lambda_list_keywords:
                    yield (
                     index, Keyword, value)
                    continue
                if value in self.declarations:
                    yield (
                     index, Keyword, value)
                    continue
                if value in self.builtin_types:
                    yield (
                     index, Keyword.Type, value)
                    continue
                if value in self.builtin_classes:
                    yield (
                     index, Name.Class, value)
                    continue
            yield (
             index, token, value)

    tokens = {'root': [
              (
               '', Text, 'body')], 
       'multiline-comment': [
                           (
                            '#\\|', Comment.Multiline, '#push'),
                           (
                            '\\|#', Comment.Multiline, '#pop'),
                           (
                            '[^|#]+', Comment.Multiline),
                           (
                            '[|#]', Comment.Multiline)], 
       'commented-form': [
                        (
                         '\\(', Comment.Preproc, '#push'),
                        (
                         '\\)', Comment.Preproc, '#pop'),
                        (
                         '[^()]+', Comment.Preproc)], 
       'body': [
              (
               '\\s+', Text),
              (
               ';.*$', Comment.Single),
              (
               '#\\|', Comment.Multiline, 'multiline-comment'),
              (
               '#\\d*Y.*$', Comment.Special),
              (
               '"(\\\\.|[^"\\\\])*"', String),
              (
               ':' + symbol, String.Symbol),
              (
               "'" + symbol, String.Symbol),
              (
               "'", Operator),
              (
               '`', Operator),
              (
               '[-+]?\\d+\\.?' + terminated, Number.Integer),
              (
               '[-+]?\\d+/\\d+' + terminated, Number),
              (
               '[-+]?(\\d*\\.\\d+([defls][-+]?\\d+)?|\\d+(\\.\\d*)?[defls][-+]?\\d+)' + terminated, Number.Float),
              (
               '#\\\\.' + terminated, String.Char),
              (
               '#\\\\' + symbol, String.Char),
              (
               '#\\(', Operator, 'body'),
              (
               '#\\d*\\*[01]*', Literal.Other),
              (
               '#:' + symbol, String.Symbol),
              (
               '#[.,]', Operator),
              (
               "#\\'", Name.Function),
              (
               '#[bB][+-]?[01]+(/[01]+)?', Number),
              (
               '#[oO][+-]?[0-7]+(/[0-7]+)?', Number.Oct),
              (
               '#[xX][+-]?[0-9a-fA-F]+(/[0-9a-fA-F]+)?', Number.Hex),
              (
               '#\\d+[rR][+-]?[0-9a-zA-Z]+(/[0-9a-zA-Z]+)?', Number),
              (
               '(#[cC])(\\()', bygroups(Number, Punctuation), 'body'),
              (
               '(#\\d+[aA])(\\()', bygroups(Literal.Other, Punctuation), 'body'),
              (
               '(#[sS])(\\()', bygroups(Literal.Other, Punctuation), 'body'),
              (
               '#[pP]?"(\\\\.|[^"])*"', Literal.Other),
              (
               '#\\d+=', Operator),
              (
               '#\\d+#', Operator),
              (
               '#+nil' + terminated + '\\s*\\(', Comment.Preproc, 'commented-form'),
              (
               '#[+-]', Operator),
              (
               '(,@|,|\\.)', Operator),
              (
               '(t|nil)' + terminated, Name.Constant),
              (
               '\\*' + symbol + '\\*', Name.Variable.Global),
              (
               symbol, Name.Variable),
              (
               '\\(', Punctuation, 'body'),
              (
               '\\)', Punctuation, '#pop')]}


class HaskellLexer(RegexLexer):
    """
    A Haskell lexer based on the lexemes defined in the Haskell 98 Report.

    *New in Pygments 0.8.*
    """
    name = 'Haskell'
    aliases = ['haskell', 'hs']
    filenames = ['*.hs']
    mimetypes = ['text/x-haskell']
    reserved = [
     'case', 'class', 'data', 'default', 'deriving', 'do', 'else',
     'if', 'in', 'infix[lr]?', 'instance',
     'let', 'newtype', 'of', 'then', 'type', 'where', '_']
    ascii = ['NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK',
     'BEL', 'BS', 'HT', 'LF', 'VT', 'FF', 'CR', 'S[OI]', 'DLE',
     'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN',
     'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '--(?![!#$%&*+./<=>?@\\^|_~]).*?$', Comment.Single),
              (
               '{-', Comment.Multiline, 'comment'),
              (
               '\\bimport\\b', Keyword.Reserved, 'import'),
              (
               '\\bmodule\\b', Keyword.Reserved, 'module'),
              (
               '\\berror\\b', Name.Exception),
              (
               "\\b(%s)(?!\\')\\b" % ('|').join(reserved), Keyword.Reserved),
              (
               "^[_a-z][\\w\\']*", Name.Function),
              (
               "[_a-z][\\w\\']*", Name),
              (
               "[A-Z][\\w\\']*", Keyword.Type),
              (
               '\\\\(?![:!#$%&*+.\\\\/<=>?@^|~-]+)', Name.Function),
              (
               '(<-|::|->|=>|=)(?![:!#$%&*+.\\\\/<=>?@^|~-]+)', Operator.Word),
              (
               ':[:!#$%&*+.\\\\/<=>?@^|~-]*', Keyword.Type),
              (
               '[:!#$%&*+.\\\\/<=>?@^|~-]+', Operator),
              (
               '\\d+[eE][+-]?\\d+', Number.Float),
              (
               '\\d+\\.\\d+([eE][+-]?\\d+)?', Number.Float),
              (
               '0[oO][0-7]+', Number.Oct),
              (
               '0[xX][\\da-fA-F]+', Number.Hex),
              (
               '\\d+', Number.Integer),
              (
               "'", String.Char, 'character'),
              (
               '"', String, 'string'),
              (
               '\\[\\]', Keyword.Type),
              (
               '\\(\\)', Name.Builtin),
              (
               '[][(),;`{}]', Punctuation)], 
       'import': [
                (
                 '\\s+', Text),
                (
                 '"', String, 'string'),
                (
                 '\\)', Punctuation, '#pop'),
                (
                 'qualified\\b', Keyword),
                (
                 '([A-Z][a-zA-Z0-9_.]*)(\\s+)(as)(\\s+)([A-Z][a-zA-Z0-9_.]*)',
                 bygroups(Name.Namespace, Text, Keyword, Text, Name), '#pop'),
                (
                 '([A-Z][a-zA-Z0-9_.]*)(\\s+)(hiding)(\\s+)(\\()',
                 bygroups(Name.Namespace, Text, Keyword, Text, Punctuation), 'funclist'),
                (
                 '([A-Z][a-zA-Z0-9_.]*)(\\s+)(\\()',
                 bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
                (
                 '[a-zA-Z0-9_.]+', Name.Namespace, '#pop')], 
       'module': [
                (
                 '\\s+', Text),
                (
                 '([A-Z][a-zA-Z0-9_.]*)(\\s+)(\\()',
                 bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
                (
                 '[A-Z][a-zA-Z0-9_.]*', Name.Namespace, '#pop')], 
       'funclist': [
                  (
                   '\\s+', Text),
                  (
                   '[A-Z][a-zA-Z0-9_]*', Keyword.Type),
                  (
                   "[_a-z][\\w\\']+", Name.Function),
                  (
                   '--.*$', Comment.Single),
                  (
                   '{-', Comment.Multiline, 'comment'),
                  (
                   ',', Punctuation),
                  (
                   '[:!#$%&*+.\\\\/<=>?@^|~-]+', Operator),
                  (
                   '\\(', Punctuation, ('funclist', 'funclist')),
                  (
                   '\\)', Punctuation, '#pop:2')], 
       'comment': [
                 (
                  '[^-{}]+', Comment.Multiline),
                 (
                  '{-', Comment.Multiline, '#push'),
                 (
                  '-}', Comment.Multiline, '#pop'),
                 (
                  '[-{}]', Comment.Multiline)], 
       'character': [
                   (
                    "[^\\\\']", String.Char),
                   (
                    '\\\\', String.Escape, 'escape'),
                   (
                    "'", String.Char, '#pop')], 
       'string': [
                (
                 '[^\\\\"]+', String),
                (
                 '\\\\', String.Escape, 'escape'),
                (
                 '"', String, '#pop')], 
       'escape': [
                (
                 '[abfnrtv"\\\'&\\\\]', String.Escape, '#pop'),
                (
                 '\\^[][A-Z@\\^_]', String.Escape, '#pop'),
                (
                 ('|').join(ascii), String.Escape, '#pop'),
                (
                 'o[0-7]+', String.Escape, '#pop'),
                (
                 'x[\\da-fA-F]+', String.Escape, '#pop'),
                (
                 '\\d+', String.Escape, '#pop'),
                (
                 '\\s+\\\\', String.Escape, '#pop')]}


line_re = re.compile('.*?\n')
bird_re = re.compile('(>[ \\t]*)(.*\\n)')

class LiterateHaskellLexer(Lexer):
    """
    For Literate Haskell (Bird-style or LaTeX) source.

    Additional options accepted:

    `litstyle`
        If given, must be ``"bird"`` or ``"latex"``.  If not given, the style
        is autodetected: if the first non-whitespace character in the source
        is a backslash or percent character, LaTeX is assumed, else Bird.

    *New in Pygments 0.9.*
    """
    name = 'Literate Haskell'
    aliases = ['lhs', 'literate-haskell']
    filenames = ['*.lhs']
    mimetypes = ['text/x-literate-haskell']

    def get_tokens_unprocessed(self, text):
        hslexer = HaskellLexer(**self.options)
        style = self.options.get('litstyle')
        if style is None:
            style = text.lstrip()[0:1] in '%\\' and 'latex' or 'bird'
        code = ''
        insertions = []
        if style == 'bird':
            for match in line_re.finditer(text):
                line = match.group()
                m = bird_re.match(line)
                if m:
                    insertions.append((len(code),
                     [
                      (
                       0, Comment.Special, m.group(1))]))
                    code += m.group(2)
                else:
                    insertions.append((len(code), [(0, Text, line)]))

        else:
            from pygments.lexers.text import TexLexer
            lxlexer = TexLexer(**self.options)
            codelines = 0
            latex = ''
            for match in line_re.finditer(text):
                line = match.group()
                if codelines:
                    if line.lstrip().startswith('\\end{code}'):
                        codelines = 0
                        latex += line
                    else:
                        code += line
                elif line.lstrip().startswith('\\begin{code}'):
                    codelines = 1
                    latex += line
                    insertions.append((len(code),
                     list(lxlexer.get_tokens_unprocessed(latex))))
                    latex = ''
                else:
                    latex += line

            insertions.append((len(code),
             list(lxlexer.get_tokens_unprocessed(latex))))
        for item in do_insertions(insertions, hslexer.get_tokens_unprocessed(code)):
            yield item

        return


class OcamlLexer(RegexLexer):
    """
    For the OCaml language.

    *New in Pygments 0.7.*
    """
    name = 'OCaml'
    aliases = ['ocaml']
    filenames = ['*.ml', '*.mli', '*.mll', '*.mly']
    mimetypes = ['text/x-ocaml']
    keywords = [
     'as', 'assert', 'begin', 'class', 'constraint', 'do', 'done',
     'downto', 'else', 'end', 'exception', 'external', 'false',
     'for', 'fun', 'function', 'functor', 'if', 'in', 'include',
     'inherit', 'initializer', 'lazy', 'let', 'match', 'method',
     'module', 'mutable', 'new', 'object', 'of', 'open', 'private',
     'raise', 'rec', 'sig', 'struct', 'then', 'to', 'true', 'try',
     'type', 'val', 'virtual', 'when', 'while', 'with']
    keyopts = [
     '!=', '#', '&', '&&', '\\(', '\\)', '\\*', '\\+', ',', '-',
     '-\\.', '->', '\\.', '\\.\\.', ':', '::', ':=', ':>', ';', ';;', '<',
     '<-', '=', '>', '>]', '>}', '\\?', '\\?\\?', '\\[', '\\[<', '\\[>', '\\[\\|',
     ']', '_', '`', '{', '{<', '\\|', '\\|]', '}', '~']
    operators = '[!$%&*+\\./:<=>?@^|~-]'
    word_operators = ['and', 'asr', 'land', 'lor', 'lsl', 'lxor', 'mod', 'or']
    prefix_syms = '[!?~]'
    infix_syms = '[=<>@^|&+\\*/$%-]'
    primitives = ['unit', 'int', 'float', 'bool', 'string', 'char', 'list', 'array']
    tokens = {'escape-sequence': [
                         (
                          '\\\\[\\\\\\"\\\'ntbr]', String.Escape),
                         (
                          '\\\\[0-9]{3}', String.Escape),
                         (
                          '\\\\x[0-9a-fA-F]{2}', String.Escape)], 
       'root': [
              (
               '\\s+', Text),
              (
               'false|true|\\(\\)|\\[\\]', Name.Builtin.Pseudo),
              (
               "\\b([A-Z][A-Za-z0-9_\\']*)(?=\\s*\\.)",
               Name.Namespace, 'dotted'),
              (
               "\\b([A-Z][A-Za-z0-9_\\']*)", Name.Class),
              (
               '\\(\\*', Comment, 'comment'),
              (
               '\\b(%s)\\b' % ('|').join(keywords), Keyword),
              (
               '(%s)' % ('|').join(keyopts), Operator),
              (
               '(%s|%s)?%s' % (infix_syms, prefix_syms, operators), Operator),
              (
               '\\b(%s)\\b' % ('|').join(word_operators), Operator.Word),
              (
               '\\b(%s)\\b' % ('|').join(primitives), Keyword.Type),
              (
               "[^\\W\\d][\\w']*", Name),
              (
               '\\d[\\d_]*', Number.Integer),
              (
               '0[xX][\\da-fA-F][\\da-fA-F_]*', Number.Hex),
              (
               '0[oO][0-7][0-7_]*', Number.Oct),
              (
               '0[bB][01][01_]*', Number.Binary),
              (
               '-?\\d[\\d_]*(.[\\d_]*)?([eE][+\\-]?\\d[\\d_]*)', Number.Float),
              (
               '\'(?:(\\\\[\\\\\\"\'ntbr ])|(\\\\[0-9]{3})|(\\\\x[0-9a-fA-F]{2}))\'',
               String.Char),
              (
               "'.'", String.Char),
              (
               "'", Keyword),
              (
               '"', String.Double, 'string'),
              (
               "[~?][a-z][\\w\\']*:", Name.Variable)], 
       'comment': [
                 (
                  '[^(*)]+', Comment),
                 (
                  '\\(\\*', Comment, '#push'),
                 (
                  '\\*\\)', Comment, '#pop'),
                 (
                  '[(*)]', Comment)], 
       'string': [
                (
                 '[^\\\\"]+', String.Double),
                include('escape-sequence'),
                (
                 '\\\\\\n', String.Double),
                (
                 '"', String.Double, '#pop')], 
       'dotted': [
                (
                 '\\s+', Text),
                (
                 '\\.', Punctuation),
                (
                 "[A-Z][A-Za-z0-9_\\']*(?=\\s*\\.)", Name.Namespace),
                (
                 "[A-Z][A-Za-z0-9_\\']*", Name.Class, '#pop'),
                (
                 "[a-z_][A-Za-z0-9_\\']*", Name, '#pop')]}


class ErlangLexer(RegexLexer):
    """
    For the Erlang functional programming language.

    Blame Jeremy Thurgood (http://jerith.za.net/).

    *New in Pygments 0.9.*
    """
    name = 'Erlang'
    aliases = ['erlang']
    filenames = ['*.erl', '*.hrl']
    mimetypes = ['text/x-erlang']
    keywords = [
     'after', 'begin', 'case', 'catch', 'cond', 'end', 'fun', 'if',
     'let', 'of', 'query', 'receive', 'try', 'when']
    builtins = [
     'abs', 'append_element', 'apply', 'atom_to_list', 'binary_to_list',
     'bitstring_to_list', 'binary_to_term', 'bit_size', 'bump_reductions',
     'byte_size', 'cancel_timer', 'check_process_code', 'delete_module',
     'demonitor', 'disconnect_node', 'display', 'element', 'erase', 'exit',
     'float', 'float_to_list', 'fun_info', 'fun_to_list',
     'function_exported', 'garbage_collect', 'get', 'get_keys',
     'group_leader', 'hash', 'hd', 'integer_to_list', 'iolist_to_binary',
     'iolist_size', 'is_atom', 'is_binary', 'is_bitstring', 'is_boolean',
     'is_builtin', 'is_float', 'is_function', 'is_integer', 'is_list',
     'is_number', 'is_pid', 'is_port', 'is_process_alive', 'is_record',
     'is_reference', 'is_tuple', 'length', 'link', 'list_to_atom',
     'list_to_binary', 'list_to_bitstring', 'list_to_existing_atom',
     'list_to_float', 'list_to_integer', 'list_to_pid', 'list_to_tuple',
     'load_module', 'localtime_to_universaltime', 'make_tuple', 'md5',
     'md5_final', 'md5_update', 'memory', 'module_loaded', 'monitor',
     'monitor_node', 'node', 'nodes', 'open_port', 'phash', 'phash2',
     'pid_to_list', 'port_close', 'port_command', 'port_connect',
     'port_control', 'port_call', 'port_info', 'port_to_list',
     'process_display', 'process_flag', 'process_info', 'purge_module',
     'put', 'read_timer', 'ref_to_list', 'register', 'resume_process',
     'round', 'send', 'send_after', 'send_nosuspend', 'set_cookie',
     'setelement', 'size', 'spawn', 'spawn_link', 'spawn_monitor',
     'spawn_opt', 'split_binary', 'start_timer', 'statistics',
     'suspend_process', 'system_flag', 'system_info', 'system_monitor',
     'system_profile', 'term_to_binary', 'tl', 'trace', 'trace_delivered',
     'trace_info', 'trace_pattern', 'trunc', 'tuple_size', 'tuple_to_list',
     'universaltime_to_localtime', 'unlink', 'unregister', 'whereis']
    operators = '(\\+|-|\\*|/|<|>|=|==|/=|=:=|=/=|=<|>=|\\+\\+|--|<-|!)'
    word_operators = [
     'and', 'andalso', 'band', 'bnot', 'bor', 'bsl', 'bsr', 'bxor',
     'div', 'not', 'or', 'orelse', 'rem', 'xor']
    atom_re = "(?:[a-z][a-zA-Z0-9_]*|'[^\\n']*[^\\\\]')"
    variable_re = '(?:[A-Z_][a-zA-Z0-9_]*)'
    escape_re = '(?:\\\\(?:[bdefnrstv\\\'"\\\\/]|[0-7][0-7]?[0-7]?|\\^[a-zA-Z]))'
    macro_re = '(?:' + variable_re + '|' + atom_re + ')'
    base_re = '(?:[2-9]|[12][0-9]|3[0-6])'
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '%.*\\n', Comment),
              (
               '(' + ('|').join(keywords) + ')\\b', Keyword),
              (
               '(' + ('|').join(builtins) + ')\\b', Name.Builtin),
              (
               '(' + ('|').join(word_operators) + ')\\b', Operator.Word),
              (
               '^-', Punctuation, 'directive'),
              (
               operators, Operator),
              (
               '"', String, 'string'),
              (
               '<<', Name.Label),
              (
               '>>', Name.Label),
              (
               '(' + atom_re + ')(:)', bygroups(Name.Namespace, Punctuation)),
              (
               '^(' + atom_re + ')(\\s*)(\\()', bygroups(Name.Function, Text, Punctuation)),
              (
               '[+-]?' + base_re + '#[0-9a-zA-Z]+', Number.Integer),
              (
               '[+-]?\\d+', Number.Integer),
              (
               '[+-]?\\d+.\\d+', Number.Float),
              (
               '[]\\[:_@\\".{}()|;,]', Punctuation),
              (
               variable_re, Name.Variable),
              (
               atom_re, Name),
              (
               '\\?' + macro_re, Name.Constant),
              (
               '\\$(?:' + escape_re + '|\\\\[ %]|[^\\\\])', String.Char),
              (
               '#' + atom_re + '(:?\\.' + atom_re + ')?', Name.Label)], 
       'string': [
                (
                 escape_re, String.Escape),
                (
                 '"', String, '#pop'),
                (
                 '~[0-9.*]*[~#+bBcdefginpPswWxX]', String.Interpol),
                (
                 '[^"\\\\~]+', String),
                (
                 '~', String)], 
       'directive': [
                   (
                    '(define)(\\s*)(\\()(' + macro_re + ')',
                    bygroups(Name.Entity, Text, Punctuation, Name.Constant), '#pop'),
                   (
                    '(record)(\\s*)(\\()(' + macro_re + ')',
                    bygroups(Name.Entity, Text, Punctuation, Name.Label), '#pop'),
                   (
                    atom_re, Name.Entity, '#pop')]}


class ErlangShellLexer(Lexer):
    """
    Shell sessions in erl (for Erlang code).

    *New in Pygments 1.1.*
    """
    name = 'Erlang erl session'
    aliases = ['erl']
    filenames = ['*.erl-sh']
    mimetypes = ['text/x-erl-shellsession']
    _prompt_re = re.compile('\\d+>(?=\\s|\\Z)')

    def get_tokens_unprocessed(self, text):
        erlexer = ErlangLexer(**self.options)
        curcode = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            m = self._prompt_re.match(line)
            if m is not None:
                end = m.end()
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, line[:end])]))
                curcode += line[end:]
            else:
                if curcode:
                    for item in do_insertions(insertions, erlexer.get_tokens_unprocessed(curcode)):
                        yield item

                    curcode = ''
                    insertions = []
                if line.startswith('*'):
                    yield (
                     match.start(), Generic.Traceback, line)
                else:
                    yield (
                     match.start(), Generic.Output, line)

        if curcode:
            for item in do_insertions(insertions, erlexer.get_tokens_unprocessed(curcode)):
                yield item

        return