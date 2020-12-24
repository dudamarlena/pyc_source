# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pygments_github_lexers/github.py
# Compiled at: 2015-01-20 20:55:41
# Size of source mod 2**32: 21007 bytes
__doc__ = '\n    pygments.lexers.github\n    ~~~~~~~~~~~~~~~~~~~\n\n    Custom lexers for GitHub.com\n\n    :copyright: Copyright 2012 by GitHub, Inc\n    :license: BSD, see LICENSE for details.\n'
import re
from pygments.lexer import RegexLexer, ExtendedRegexLexer, include, bygroups, using, DelegatingLexer
from pygments.token import Text, Name, Number, String, Comment, Punctuation, Other, Keyword, Operator, Literal, Whitespace
__all__ = [
 'Dasm16Lexer', 'PuppetLexer', 'AugeasLexer', 'TOMLLexer', 'SlashLexer']

class Dasm16Lexer(RegexLexer):
    """Dasm16Lexer"""
    name = 'dasm16'
    aliases = ['DASM16']
    filenames = ['*.dasm16', '*.dasm']
    mimetypes = ['text/x-dasm16']
    INSTRUCTIONS = [
     'SET',
     'ADD', 'SUB',
     'MUL', 'MLI',
     'DIV', 'DVI',
     'MOD', 'MDI',
     'AND', 'BOR', 'XOR',
     'SHR', 'ASR', 'SHL',
     'IFB', 'IFC', 'IFE', 'IFN', 'IFG', 'IFA', 'IFL', 'IFU',
     'ADX', 'SBX',
     'STI', 'STD',
     'JSR',
     'INT', 'IAG', 'IAS', 'RFI', 'IAQ', 'HWN', 'HWQ', 'HWI']
    REGISTERS = [
     'A', 'B', 'C',
     'X', 'Y', 'Z',
     'I', 'J',
     'SP', 'PC', 'EX',
     'POP', 'PEEK', 'PUSH']
    char = '[a-zA-Z$._0-9@]'
    identifier = '(?:[a-zA-Z$_]' + char + '*|\\.' + char + '+)'
    number = '[+-]?(?:0[xX][a-zA-Z0-9]+|\\d+)'
    binary_number = '0b[01_]+'
    instruction = '(?i)(' + '|'.join(INSTRUCTIONS) + ')'
    single_char = "'\\\\?" + char + "'"
    string = '"(\\\\"|[^"])*"'

    def guess_identifier(lexer, match):
        ident = match.group(0)
        klass = Name.Variable if ident.upper() in lexer.REGISTERS else Name.Label
        yield (match.start(), klass, ident)

    tokens = {'root': [
              include('whitespace'),
              (
               ':' + identifier, Name.Label),
              (
               identifier + ':', Name.Label),
              (
               instruction, Name.Function, 'instruction-args'),
              (
               '\\.' + identifier, Name.Function, 'data-args'),
              (
               '[\\r\\n]+', Text)], 
     'numeric': [
                 (
                  binary_number, Number.Integer),
                 (
                  number, Number.Integer),
                 (
                  single_char, String)], 
     'arg': [
             (
              identifier, guess_identifier),
             include('numeric')], 
     'deref': [
               (
                '\\+', Punctuation),
               (
                '\\]', Punctuation, '#pop'),
               include('arg'),
               include('whitespace')], 
     'instruction-line': [
                          (
                           '[\\r\\n]+', Text, '#pop'),
                          (
                           ';.*?$', Comment, '#pop'),
                          include('whitespace')], 
     'instruction-args': [
                          (
                           ',', Punctuation),
                          (
                           '\\[', Punctuation, 'deref'),
                          include('arg'),
                          include('instruction-line')], 
     'data-args': [
                   (
                    ',', Punctuation),
                   include('numeric'),
                   (
                    string, String),
                   include('instruction-line')], 
     'whitespace': [
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     ';.*?\\n', Comment)]}


class PuppetLexer(RegexLexer):
    name = 'Puppet'
    aliases = ['puppet']
    filenames = ['*.pp']
    tokens = {'root': [
              include('puppet')], 
     'puppet': [
                include('comments'),
                (
                 '(class)(\\s*)(\\{)', bygroups(Name.Class, Text, Punctuation), ('type', 'namevar')),
                (
                 '(class|define)', Keyword.Declaration, ('block', 'class_name')),
                (
                 'node', Keyword.Declaration, ('block', 'node_name')),
                (
                 'elsif', Keyword.Reserved, ('block', 'conditional')),
                (
                 'if', Keyword.Reserved, ('block', 'conditional')),
                (
                 'unless', Keyword.Reserved, ('block', 'conditional')),
                (
                 '(else)(\\s*)(\\{)', bygroups(Keyword.Reserved, Text, Punctuation), 'block'),
                (
                 'case', Keyword.Reserved, ('case', 'conditional')),
                (
                 '(::)?([A-Z][\\w:]+)+(\\s*)(<{1,2}\\|)', bygroups(Name.Class, Name.Class, Text, Punctuation), 'spaceinvader'),
                (
                 '(::)?([A-Z][\\w:]+)+(\\s*)(\\{)', bygroups(Name.Class, Name.Class, Text, Punctuation), 'type'),
                (
                 '(::)?([A-Z][\\w:]+)+(\\s*)(\\[)', bygroups(Name.Class, Name.Class, Text, Punctuation), ('type', 'override_name')),
                (
                 '(@{0,2}[\\w:]+)(\\s*)(\\{)(\\s*)', bygroups(Name.Class, Text, Punctuation, Text), ('type', 'namevar')),
                (
                 '\\$(::)?(\\w+::)*\\w+', Name.Variable, 'var_assign'),
                (
                 '(include|require)', Keyword.Namespace, 'include'),
                (
                 'import', Keyword.Namespace, 'import'),
                (
                 '(\\w+)(\\()', bygroups(Name.Function, Punctuation), 'function'),
                (
                 '\\s', Text)], 
     'block': [
               include('puppet'),
               (
                '\\}', Text, '#pop')], 
     'override_name': [
                       include('strings'),
                       include('variables'),
                       (
                        '\\]', Punctuation),
                       (
                        '\\s', Text),
                       (
                        '\\{', Punctuation, '#pop')], 
     'node_name': [
                   (
                    'inherits', Keyword.Declaration),
                   (
                    '[\\w\\.]+', String),
                   include('strings'),
                   include('variables'),
                   (
                    ',', Punctuation),
                   (
                    '\\s', Text),
                   (
                    '\\{', Punctuation, '#pop')], 
     'class_name': [
                    (
                     'inherits', Keyword.Declaration),
                    (
                     '[\\w:]+', Name.Class),
                    (
                     '\\s', Text),
                    (
                     '\\{', Punctuation, '#pop'),
                    (
                     '\\(', Punctuation, 'paramlist')], 
     'include': [
                 (
                  '\\n', Text, '#pop'),
                 (
                  '[\\w:-]+', Name.Class),
                 include('value'),
                 (
                  '\\s', Text)], 
     'import': [
                (
                 '\\n', Text, '#pop'),
                (
                 '[\\/\\w\\.]+', String),
                include('value'),
                (
                 '\\s', Text)], 
     'case': [
              (
               '(default)(:)(\\s*)(\\{)', bygroups(Keyword.Reserved, Punctuation, Text, Punctuation), 'block'),
              include('case_values'),
              (
               '(:)(\\s*)(\\{)', bygroups(Punctuation, Text, Punctuation), 'block'),
              (
               '\\s', Text),
              (
               '\\}', Punctuation, '#pop')], 
     'case_values': [
                     include('value'),
                     (
                      ',', Punctuation)], 
     'comments': [
                  (
                   '\\s*#.*\\n', Comment.Singleline)], 
     'strings': [
                 (
                  "'.*?'", String.Single),
                 (
                  '\\w+', String.Symbol),
                 (
                  '"', String.Double, 'dblstring'),
                 (
                  '\\/.+?\\/', String.Regex)], 
     'dblstring': [
                   (
                    '\\$\\{.+?\\}', String.Interpol),
                   (
                    '(?:\\\\(?:[bdefnrstv\\\'"\\$\\\\/]|[0-7][0-7]?[0-7]?|\\^[a-zA-Z]))', String.Escape),
                   (
                    '[^"\\\\\\$]+', String.Double),
                   (
                    '\\$', String.Double),
                   (
                    '"', String.Double, '#pop')], 
     'variables': [
                   (
                    '\\$(::)?(\\w+::)*\\w+', Name.Variable)], 
     'var_assign': [
                    (
                     '\\[', Punctuation, ('#pop', 'array')),
                    (
                     '\\{', Punctuation, ('#pop', 'hash')),
                    (
                     '(\\s*)(=)(\\s*)', bygroups(Text, Operator, Text)),
                    (
                     '(\\(|\\))', Punctuation),
                    include('operators'),
                    include('value'),
                    (
                     '\\s', Text, '#pop')], 
     'booleans': [
                  (
                   '(true|false)', Literal)], 
     'operators': [
                   (
                    '(\\s*)(==|=~|\\*|-|\\+|<<|>>|!=|!~|!|>=|<=|<|>|and|or|in)(\\s*)', bygroups(Text, Operator, Text))], 
     'conditional': [
                     include('operators'),
                     include('strings'),
                     include('variables'),
                     (
                      '\\[', Punctuation, 'array'),
                     (
                      '\\(', Punctuation, 'conditional'),
                     (
                      '\\{', Punctuation, '#pop'),
                     (
                      '\\)', Punctuation, '#pop'),
                     (
                      '\\s', Text)], 
     'spaceinvader': [
                      include('operators'),
                      include('strings'),
                      include('variables'),
                      (
                       '\\[', Punctuation, 'array'),
                      (
                       '\\(', Punctuation, 'conditional'),
                      (
                       '\\s', Text),
                      (
                       '\\|>{1,2}', Punctuation, '#pop')], 
     'namevar': [
                 include('value'),
                 (
                  '\\[', Punctuation, 'array'),
                 (
                  '\\s', Text),
                 (
                  ':', Punctuation, '#pop'),
                 (
                  '\\}', Punctuation, '#pop')], 
     'function': [
                  (
                   '\\[', Punctuation, 'array'),
                  include('value'),
                  (
                   ',', Punctuation),
                  (
                   '\\s', Text),
                  (
                   '\\)', Punctuation, '#pop')], 
     'paramlist': [
                   include('value'),
                   (
                    '=', Punctuation),
                   (
                    ',', Punctuation),
                   (
                    '\\s', Text),
                   (
                    '\\[', Punctuation, 'array'),
                   (
                    '\\)', Punctuation, '#pop')], 
     'type': [
              (
               '(\\w+)(\\s*)(=>)(\\s*)', bygroups(Name.Tag, Text, Punctuation, Text), 'param_value'),
              (
               '\\}', Punctuation, '#pop'),
              (
               '\\s', Text),
              include('comments'),
              (
               '', Text, 'namevar')], 
     'value': [
               (
                '[\\d\\.]', Number),
               (
                '([A-Z][\\w:]+)+(\\[)', bygroups(Name.Class, Punctuation), 'array'),
               (
                '(\\w+)(\\()', bygroups(Name.Function, Punctuation), 'function'),
               include('strings'),
               include('variables'),
               include('comments'),
               include('booleans'),
               (
                '(\\s*)(\\?)(\\s*)(\\{)', bygroups(Text, Punctuation, Text, Punctuation), 'selector'),
               (
                '\\{', Punctuation, 'hash')], 
     'selector': [
                  (
                   'default', Keyword.Reserved),
                  include('value'),
                  (
                   '=>', Punctuation),
                  (
                   ',', Punctuation),
                  (
                   '\\s', Text),
                  (
                   '\\}', Punctuation, '#pop')], 
     'param_value': [
                     include('value'),
                     (
                      '\\[', Punctuation, 'array'),
                     (
                      ',', Punctuation, '#pop'),
                     (
                      ';', Punctuation, '#pop'),
                     (
                      '\\s', Text, '#pop'),
                     (
                      '', Text, '#pop')], 
     'array': [
               include('value'),
               (
                '\\[', Punctuation, 'array'),
               (
                ',', Punctuation),
               (
                '\\s', Text),
               (
                '\\]', Punctuation, '#pop')], 
     'hash': [
              include('value'),
              (
               '\\s', Text),
              (
               '=>', Punctuation),
              (
               ',', Punctuation),
              (
               '\\}', Punctuation, '#pop')]}


class AugeasLexer(RegexLexer):
    name = 'Augeas'
    aliases = ['augeas']
    filenames = ['*.aug']
    tokens = {'root': [
              (
               '(module)(\\s*)([^\\s=]+)', bygroups(Keyword.Namespace, Text, Name.Namespace)),
              (
               '(let)(\\s*)([^\\s=]+)', bygroups(Keyword.Declaration, Text, Name.Variable)),
              (
               '(del|store|value|counter|seq|key|label|autoload|incl|excl|transform|test|get|put)(\\s+)', bygroups(Name.Builtin, Text)),
              (
               '(\\()([^\\:]+)(\\:)(unit|string|regexp|lens|tree|filter)(\\))', bygroups(Punctuation, Name.Variable, Punctuation, Keyword.Type, Punctuation)),
              (
               '\\(\\*', Comment.Multiline, 'comment'),
              (
               '[\\+=\\|\\.\\*\\;\\?-]', Operator),
              (
               '[\\[\\]\\(\\)\\{\\}]', Operator),
              (
               '"', String.Double, 'string'),
              (
               '\\/', String.Regex, 'regex'),
              (
               '([A-Z]\\w*)(\\.)(\\w+)', bygroups(Name.Namespace, Punctuation, Name.Variable)),
              (
               '.', Name.Variable),
              (
               '\\s', Text)], 
     'string': [
                (
                 '\\\\.', String.Escape),
                (
                 '[^"]', String.Double),
                (
                 '"', String.Double, '#pop')], 
     'regex': [
               (
                '\\\\.', String.Escape),
               (
                '[^\\/]', String.Regex),
               (
                '\\/', String.Regex, '#pop')], 
     'comment': [
                 (
                  '[^*\\)]', Comment.Multiline),
                 (
                  '\\(\\*', Comment.Multiline, '#push'),
                 (
                  '\\*\\)', Comment.Multiline, '#pop'),
                 (
                  '[\\*\\)]', Comment.Multiline)]}


class TOMLLexer(RegexLexer):
    """TOMLLexer"""
    name = 'TOML'
    aliases = ['toml']
    filenames = ['*.toml']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '#.*?$', Comment.Single),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '(true|false)$', Keyword.Constant),
              (
               '[a-zA-Z_][a-zA-Z0-9_\\-]*', Name),
              (
               '\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z', Number.Integer),
              (
               '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
              (
               '\\d+[eE][+-]?[0-9]+j?', Number.Float),
              (
               '\\-?\\d+', Number.Integer),
              (
               '[]{}:(),;[]', Punctuation),
              (
               '\\.', Punctuation),
              (
               '=', Operator)]}


class SlashLanguageLexer(ExtendedRegexLexer):
    _nkw = '(?=[^a-zA-Z_0-9])'

    def move_state(new_state):
        return (
         '#pop', new_state)

    def right_angle_bracket(lexer, match, ctx):
        if len(ctx.stack) > 1 and ctx.stack[(-2)] == 'string':
            ctx.stack.pop()
        yield (
         match.start(), String.Interpol, '}')
        ctx.pos = match.end()

    tokens = {'root': [
              (
               '<%=', Comment.Preproc, move_state('slash')),
              (
               '<%!!', Comment.Preproc, move_state('slash')),
              (
               '<%#.*?%>', Comment.Multiline),
              (
               '<%', Comment.Preproc, move_state('slash')),
              (
               '.|\\n', Other)], 
     'string': [
                (
                 '\\\\', String.Escape, move_state('string_e')),
                (
                 '\\"', String, move_state('slash')),
                (
                 '#\\{', String.Interpol, 'slash'),
                (
                 '.|\\n', String)], 
     'string_e': [
                  (
                   'n', String.Escape, move_state('string')),
                  (
                   't', String.Escape, move_state('string')),
                  (
                   'r', String.Escape, move_state('string')),
                  (
                   'e', String.Escape, move_state('string')),
                  (
                   'x[a-fA-F0-9]{2}', String.Escape, move_state('string')),
                  (
                   '.', String.Escape, move_state('string'))], 
     'regexp': [
                (
                 '}[a-z]*', String.Regex, move_state('slash')),
                (
                 '\\\\(.|\\n)', String.Regex),
                (
                 '{', String.Regex, 'regexp_r'),
                (
                 '.|\\n', String.Regex)], 
     'regexp_r': [
                  (
                   '}[a-z]*', String.Regex, '#pop'),
                  (
                   '\\\\(.|\\n)', String.Regex),
                  (
                   '{', String.Regex, 'regexp_r')], 
     'slash': [
               (
                '%>', Comment.Preproc, move_state('root')),
               (
                '\\"', String, move_state('string')),
               (
                "'[a-zA-Z0-9_]+", String),
               (
                '%r{', String.Regex, move_state('regexp')),
               (
                '/\\*.*?\\*/', Comment.Multiline),
               (
                '(#|//).*?\\n', Comment.Single),
               (
                '-?[0-9]+e[+-]?[0-9]+', Number.Float),
               (
                '-?[0-9]+\\.[0-9]+(e[+-]?[0-9]+)?', Number.Float),
               (
                '-?[0-9]+', Number.Integer),
               (
                'nil' + _nkw, Name.Builtin),
               (
                'true' + _nkw, Name.Builtin),
               (
                'false' + _nkw, Name.Builtin),
               (
                'self' + _nkw, Name.Builtin),
               (
                "(class)(\\s+)([A-Z][a-zA-Z0-9_\\']*)",
                bygroups(Keyword, Whitespace, Name.Class)),
               (
                'class' + _nkw, Keyword),
               (
                'extends' + _nkw, Keyword),
               (
                "(def)(\\s+)(self)(\\s*)(\\.)(\\s*)([a-z_][a-zA-Z0-9_\\']*=?|<<|>>|==|<=>|<=|<|>=|>|\\+|-(self)?|~(self)?|\\*|/|%|^|&&|&|\\||\\[\\]=?)",
                bygroups(Keyword, Whitespace, Name.Builtin, Whitespace, Punctuation, Whitespace, Name.Function)),
               (
                "(def)(\\s+)([a-z_][a-zA-Z0-9_\\']*=?|<<|>>|==|<=>|<=|<|>=|>|\\+|-(self)?|~(self)?|\\*|/|%|^|&&|&|\\||\\[\\]=?)",
                bygroups(Keyword, Whitespace, Name.Function)),
               (
                'def' + _nkw, Keyword),
               (
                'if' + _nkw, Keyword),
               (
                'elsif' + _nkw, Keyword),
               (
                'else' + _nkw, Keyword),
               (
                'unless' + _nkw, Keyword),
               (
                'for' + _nkw, Keyword),
               (
                'in' + _nkw, Keyword),
               (
                'while' + _nkw, Keyword),
               (
                'until' + _nkw, Keyword),
               (
                'and' + _nkw, Keyword),
               (
                'or' + _nkw, Keyword),
               (
                'not' + _nkw, Keyword),
               (
                'lambda' + _nkw, Keyword),
               (
                'try' + _nkw, Keyword),
               (
                'catch' + _nkw, Keyword),
               (
                'return' + _nkw, Keyword),
               (
                'next' + _nkw, Keyword),
               (
                'last' + _nkw, Keyword),
               (
                'throw' + _nkw, Keyword),
               (
                'use' + _nkw, Keyword),
               (
                'switch' + _nkw, Keyword),
               (
                '\\\\', Keyword),
               (
                'λ', Keyword),
               (
                '__FILE__' + _nkw, Name.Builtin.Pseudo),
               (
                '__LINE__' + _nkw, Name.Builtin.Pseudo),
               (
                "[A-Z][a-zA-Z0-9_\\']*" + _nkw, Name.Constant),
               (
                "[a-z_][a-zA-Z0-9_\\']*" + _nkw, Name),
               (
                "@[a-z_][a-zA-Z0-9_\\']*" + _nkw, Name.Variable.Instance),
               (
                "@@[a-z_][a-zA-Z0-9_\\']*" + _nkw, Name.Variable.Class),
               (
                '\\(', Punctuation),
               (
                '\\)', Punctuation),
               (
                '\\[', Punctuation),
               (
                '\\]', Punctuation),
               (
                '\\{', Punctuation),
               (
                '\\}', right_angle_bracket),
               (
                ';', Punctuation),
               (
                ',', Punctuation),
               (
                '<<=', Operator),
               (
                '>>=', Operator),
               (
                '<<', Operator),
               (
                '>>', Operator),
               (
                '==', Operator),
               (
                '!=', Operator),
               (
                '=>', Operator),
               (
                '=', Operator),
               (
                '<=>', Operator),
               (
                '<=', Operator),
               (
                '>=', Operator),
               (
                '<', Operator),
               (
                '>', Operator),
               (
                '\\+\\+', Operator),
               (
                '\\+=', Operator),
               (
                '-=', Operator),
               (
                '\\*\\*=', Operator),
               (
                '\\*=', Operator),
               (
                '\\*\\*', Operator),
               (
                '\\*', Operator),
               (
                '/=', Operator),
               (
                '\\+', Operator),
               (
                '-', Operator),
               (
                '/', Operator),
               (
                '%=', Operator),
               (
                '%', Operator),
               (
                '^=', Operator),
               (
                '&&=', Operator),
               (
                '&=', Operator),
               (
                '&&', Operator),
               (
                '&', Operator),
               (
                '\\|\\|=', Operator),
               (
                '\\|=', Operator),
               (
                '\\|\\|', Operator),
               (
                '\\|', Operator),
               (
                '!', Operator),
               (
                '\\.\\.\\.', Operator),
               (
                '\\.\\.', Operator),
               (
                '\\.', Operator),
               (
                '::', Operator),
               (
                ':', Operator),
               (
                '(\\s|\\n)+', Whitespace),
               (
                "[a-z_][a-zA-Z0-9_\\']*", Name.Variable)]}


class SlashLexer(DelegatingLexer):
    """SlashLexer"""
    name = 'Slash'
    aliases = ['slash']
    filenames = ['*.sl']

    def __init__(self, **options):
        from pygments.lexers.web import HtmlLexer
        super(SlashLexer, self).__init__(HtmlLexer, SlashLanguageLexer, **options)