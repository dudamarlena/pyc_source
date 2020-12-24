# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/int_fiction.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 55779 bytes
"""
    pygments.lexers.int_fiction
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for interactive fiction languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, using, this, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error, Generic
__all__ = [
 'Inform6Lexer', 'Inform6TemplateLexer', 'Inform7Lexer',
 'Tads3Lexer']

class Inform6Lexer(RegexLexer):
    __doc__ = '\n    For `Inform 6 <http://inform-fiction.org/>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Inform 6'
    aliases = ['inform6', 'i6']
    filenames = ['*.inf']
    flags = re.MULTILINE | re.DOTALL | re.UNICODE
    _name = '[a-zA-Z_]\\w*'
    _dash = '\\-‐-—'
    _dquote = '"“”'
    _squote = "'‘’"
    _newline = '\\n\x85\u2028\u2029'
    tokens = {'root':[
      (
       '\\A(!%%[^%s]*[%s])+' % (_newline, _newline), Comment.Preproc,
       'directive'),
      default('directive')], 
     '_whitespace':[
      (
       '\\s+', Text),
      (
       '![^%s]*' % _newline, Comment.Single)], 
     'default':[
      include('_whitespace'),
      (
       '\\[', Punctuation, 'many-values'),
      (
       ':|(?=;)', Punctuation, '#pop'),
      (
       '<', Punctuation),
      default(('expression', '_expression'))], 
     '_expression':[
      include('_whitespace'),
      (
       '(?=sp\\b)', Text, '#pop'),
      (
       '(?=[%s%s$0-9#a-zA-Z_])' % (_dquote, _squote), Text,
       ('#pop', 'value')),
      (
       '\\+\\+|[%s]{1,2}(?!>)|~~?' % _dash, Operator),
      (
       '(?=[()\\[%s,?@{:;])' % _dash, Text, '#pop')], 
     'expression':[
      include('_whitespace'),
      (
       '\\(', Punctuation, ('expression', '_expression')),
      (
       '\\)', Punctuation, '#pop'),
      (
       '\\[', Punctuation, ('#pop', 'statements', 'locals')),
      (
       '>(?=(\\s+|(![^%s]*))*[>;])' % _newline, Punctuation),
      (
       '\\+\\+|[%s]{2}(?!>)' % _dash, Operator),
      (
       ',', Punctuation, '_expression'),
      (
       '&&?|\\|\\|?|[=~><]?=|[%s]{1,2}>?|\\.\\.?[&#]?|::|[<>+*/%%]' % _dash,
       Operator, '_expression'),
      (
       '(has|hasnt|in|notin|ofclass|or|provides)\\b', Operator.Word,
       '_expression'),
      (
       'sp\\b', Name),
      (
       '\\?~?', Name.Label, 'label?'),
      (
       '[@{]', Error),
      default('#pop')], 
     '_assembly-expression':[
      (
       '\\(', Punctuation, ('#push', '_expression')),
      (
       '[\\[\\]]', Punctuation),
      (
       '[%s]>' % _dash, Punctuation, '_expression'),
      (
       'sp\\b', Keyword.Pseudo),
      (
       ';', Punctuation, '#pop:3'),
      include('expression')], 
     '_for-expression':[
      (
       '\\)', Punctuation, '#pop:2'),
      (
       ':', Punctuation, '#pop'),
      include('expression')], 
     '_keyword-expression':[
      (
       '(from|near|to)\\b', Keyword, '_expression'),
      include('expression')], 
     '_list-expression':[
      (
       ',', Punctuation, '#pop'),
      include('expression')], 
     '_object-expression':[
      (
       'has\\b', Keyword.Declaration, '#pop'),
      include('_list-expression')], 
     'value':[
      include('_whitespace'),
      (
       '[%s][^@][%s]' % (_squote, _squote), String.Char, '#pop'),
      (
       '([%s])(@\\{[0-9a-fA-F]{1,4}\\})([%s])' % (_squote, _squote),
       bygroups(String.Char, String.Escape, String.Char), '#pop'),
      (
       '([%s])(@.{2})([%s])' % (_squote, _squote),
       bygroups(String.Char, String.Escape, String.Char), '#pop'),
      (
       '[%s]' % _squote, String.Single, ('#pop', 'dictionary-word')),
      (
       '[%s]' % _dquote, String.Double, ('#pop', 'string')),
      (
       '\\$[+%s][0-9]*\\.?[0-9]*([eE][+%s]?[0-9]+)?' % (_dash, _dash),
       Number.Float, '#pop'),
      (
       '\\$[0-9a-fA-F]+', Number.Hex, '#pop'),
      (
       '\\$\\$[01]+', Number.Bin, '#pop'),
      (
       '[0-9]+', Number.Integer, '#pop'),
      (
       '(##|#a\\$)(%s)' % _name, bygroups(Operator, Name), '#pop'),
      (
       '(#g\\$)(%s)' % _name,
       bygroups(Operator, Name.Variable.Global), '#pop'),
      (
       '#[nw]\\$', Operator, ('#pop', 'obsolete-dictionary-word')),
      (
       '(#r\\$)(%s)' % _name, bygroups(Operator, Name.Function), '#pop'),
      (
       '#', Name.Builtin, ('#pop', 'system-constant')),
      (
       words(('child', 'children', 'elder', 'eldest', 'glk', 'indirect', 'metaclass', 'parent',
       'random', 'sibling', 'younger', 'youngest'),
         suffix='\\b'),
       Name.Builtin, '#pop'),
      (
       '(?i)(Class|Object|Routine|String)\\b', Name.Builtin, '#pop'),
      (
       words(('Box__Routine', 'CA__Pr', 'CDefArt', 'CInDefArt', 'Cl__Ms', 'Copy__Primitive',
       'CP__Tab', 'DA__Pr', 'DB__Pr', 'DefArt', 'Dynam__String', 'EnglishNumber',
       'Glk__Wrap', 'IA__Pr', 'IB__Pr', 'InDefArt', 'Main__', 'Meta__class', 'OB__Move',
       'OB__Remove', 'OC__Cl', 'OP__Pr', 'Print__Addr', 'Print__PName', 'PrintShortName',
       'RA__Pr', 'RA__Sc', 'RL__Pr', 'R_Process', 'RT__ChG', 'RT__ChGt', 'RT__ChLDB',
       'RT__ChLDW', 'RT__ChPR', 'RT__ChPrintA', 'RT__ChPrintC', 'RT__ChPrintO', 'RT__ChPrintS',
       'RT__ChPS', 'RT__ChR', 'RT__ChSTB', 'RT__ChSTW', 'RT__ChT', 'RT__Err', 'RT__TrPS',
       'RV__Pr', 'Symb__Tab', 'Unsigned__Compare', 'WV__Pr', 'Z__Region'),
         prefix='(?i)',
         suffix='\\b'),
       Name.Builtin, '#pop'),
      (
       words(('call', 'copy', 'create', 'DEBUG', 'destroy', 'DICT_CHAR_SIZE', 'DICT_ENTRY_BYTES',
       'DICT_IS_UNICODE', 'DICT_WORD_SIZE', 'false', 'FLOAT_INFINITY', 'FLOAT_NAN',
       'FLOAT_NINFINITY', 'GOBJFIELD_CHAIN', 'GOBJFIELD_CHILD', 'GOBJFIELD_NAME',
       'GOBJFIELD_PARENT', 'GOBJFIELD_PROPTAB', 'GOBJFIELD_SIBLING', 'GOBJ_EXT_START',
       'GOBJ_TOTAL_LENGTH', 'Grammar__Version', 'INDIV_PROP_START', 'INFIX', 'infix__watching',
       'MODULE_MODE', 'name', 'nothing', 'NUM_ATTR_BYTES', 'print', 'print_to_array',
       'recreate', 'remaining', 'self', 'sender', 'STRICT_MODE', 'sw__var', 'sys__glob0',
       'sys__glob1', 'sys__glob2', 'sys_statusline_flag', 'TARGET_GLULX', 'TARGET_ZCODE',
       'temp__global2', 'temp__global3', 'temp__global4', 'temp_global', 'true',
       'USE_MODULES', 'WORDSIZE'),
         prefix='(?i)',
         suffix='\\b'),
       Name.Builtin, '#pop'),
      (
       _name, Name, '#pop')], 
     'dictionary-word':[
      (
       '[~^]+', String.Escape),
      (
       '[^~^\\\\@({%s]+' % _squote, String.Single),
      (
       '[({]', String.Single),
      (
       '@\\{[0-9a-fA-F]{,4}\\}', String.Escape),
      (
       '@.{2}', String.Escape),
      (
       '[%s]' % _squote, String.Single, '#pop')], 
     'string':[
      (
       '[~^]+', String.Escape),
      (
       '[^~^\\\\@({%s]+' % _dquote, String.Double),
      (
       '[({]', String.Double),
      (
       '\\\\', String.Escape),
      (
       '@(\\\\\\s*[%s]\\s*)*@((\\\\\\s*[%s]\\s*)*[0-9])*' % (
        _newline, _newline), String.Escape),
      (
       '@(\\\\\\s*[%s]\\s*)*\\{((\\\\\\s*[%s]\\s*)*[0-9a-fA-F]){,4}(\\\\\\s*[%s]\\s*)*\\}' % (
        _newline, _newline, _newline),
       String.Escape),
      (
       '@(\\\\\\s*[%s]\\s*)*.(\\\\\\s*[%s]\\s*)*.' % (_newline, _newline),
       String.Escape),
      (
       '[%s]' % _dquote, String.Double, '#pop')], 
     'plain-string':[
      (
       '[^~^\\\\({\\[\\]%s]+' % _dquote, String.Double),
      (
       '[~^({\\[\\]]', String.Double),
      (
       '\\\\', String.Escape),
      (
       '[%s]' % _dquote, String.Double, '#pop')], 
     '_constant':[
      include('_whitespace'),
      (
       _name, Name.Constant, '#pop'),
      include('value')], 
     '_global':[
      include('_whitespace'),
      (
       _name, Name.Variable.Global, '#pop'),
      include('value')], 
     'label?':[
      include('_whitespace'),
      (
       _name, Name.Label, '#pop'),
      default('#pop')], 
     'variable?':[
      include('_whitespace'),
      (
       _name, Name.Variable, '#pop'),
      default('#pop')], 
     'obsolete-dictionary-word':[
      (
       '\\S\\w*', String.Other, '#pop')], 
     'system-constant':[
      include('_whitespace'),
      (
       _name, Name.Builtin, '#pop')], 
     'directive':[
      include('_whitespace'),
      (
       '#', Punctuation),
      (
       ';', Punctuation, '#pop'),
      (
       '\\[', Punctuation,
       ('default', 'statements', 'locals', 'routine-name?')),
      (
       words(('abbreviate', 'endif', 'dictionary', 'ifdef', 'iffalse', 'ifndef', 'ifnot',
       'iftrue', 'ifv3', 'ifv5', 'release', 'serial', 'switches', 'system_file',
       'version'),
         prefix='(?i)', suffix='\\b'),
       Keyword, 'default'),
      (
       '(?i)(array|global)\\b', Keyword,
       ('default', 'directive-keyword?', '_global')),
      (
       '(?i)attribute\\b', Keyword, ('default', 'alias?', '_constant')),
      (
       '(?i)class\\b', Keyword,
       ('object-body', 'duplicates', 'class-name')),
      (
       '(?i)(constant|default)\\b', Keyword,
       ('default', 'expression', '_constant')),
      (
       '(?i)(end\\b)(.*)', bygroups(Keyword, Text)),
      (
       '(?i)(extend|verb)\\b', Keyword, 'grammar'),
      (
       '(?i)fake_action\\b', Keyword, ('default', '_constant')),
      (
       '(?i)import\\b', Keyword, 'manifest'),
      (
       '(?i)(include|link)\\b', Keyword,
       ('default', 'before-plain-string')),
      (
       '(?i)(lowstring|undef)\\b', Keyword, ('default', '_constant')),
      (
       '(?i)message\\b', Keyword, ('default', 'diagnostic')),
      (
       '(?i)(nearby|object)\\b', Keyword,
       ('object-body', '_object-head')),
      (
       '(?i)property\\b', Keyword,
       ('default', 'alias?', '_constant', 'property-keyword*')),
      (
       '(?i)replace\\b', Keyword,
       ('default', 'routine-name?', 'routine-name?')),
      (
       '(?i)statusline\\b', Keyword, ('default', 'directive-keyword?')),
      (
       '(?i)stub\\b', Keyword, ('default', 'routine-name?')),
      (
       '(?i)trace\\b', Keyword,
       ('default', 'trace-keyword?', 'trace-keyword?')),
      (
       '(?i)zcharacter\\b', Keyword,
       ('default', 'directive-keyword?', 'directive-keyword?')),
      (
       _name, Name.Class, ('object-body', '_object-head'))], 
     'routine-name?':[
      include('_whitespace'),
      (
       _name, Name.Function, '#pop'),
      default('#pop')], 
     'locals':[
      include('_whitespace'),
      (
       ';', Punctuation, '#pop'),
      (
       '\\*', Punctuation),
      (
       '"', String.Double, 'plain-string'),
      (
       _name, Name.Variable)], 
     'many-values':[
      include('_whitespace'),
      (
       ';', Punctuation),
      (
       '\\]', Punctuation, '#pop'),
      (
       ':', Error),
      default(('expression', '_expression'))], 
     'alias?':[
      include('_whitespace'),
      (
       'alias\\b', Keyword, ('#pop', '_constant')),
      default('#pop')], 
     'class-name':[
      include('_whitespace'),
      (
       '(?=[,;]|(class|has|private|with)\\b)', Text, '#pop'),
      (
       _name, Name.Class, '#pop')], 
     'duplicates':[
      include('_whitespace'),
      (
       '\\(', Punctuation, ('#pop', 'expression', '_expression')),
      default('#pop')], 
     '_object-head':[
      (
       '[%s]>' % _dash, Punctuation),
      (
       '(class|has|private|with)\\b', Keyword.Declaration, '#pop'),
      include('_global')], 
     'object-body':[
      include('_whitespace'),
      (
       ';', Punctuation, '#pop:2'),
      (
       ',', Punctuation),
      (
       'class\\b', Keyword.Declaration, 'class-segment'),
      (
       '(has|private|with)\\b', Keyword.Declaration),
      (
       ':', Error),
      default(('_object-expression', '_expression'))], 
     'class-segment':[
      include('_whitespace'),
      (
       '(?=[,;]|(class|has|private|with)\\b)', Text, '#pop'),
      (
       _name, Name.Class),
      default('value')], 
     'grammar':[
      include('_whitespace'),
      (
       '=', Punctuation, ('#pop', 'default')),
      (
       '\\*', Punctuation, ('#pop', 'grammar-line')),
      default('_directive-keyword')], 
     'grammar-line':[
      include('_whitespace'),
      (
       ';', Punctuation, '#pop'),
      (
       '[/*]', Punctuation),
      (
       '[%s]>' % _dash, Punctuation, 'value'),
      (
       '(noun|scope)\\b', Keyword, '=routine'),
      default('_directive-keyword')], 
     '=routine':[
      include('_whitespace'),
      (
       '=', Punctuation, 'routine-name?'),
      default('#pop')], 
     'manifest':[
      include('_whitespace'),
      (
       ';', Punctuation, '#pop'),
      (
       ',', Punctuation),
      (
       '(?i)global\\b', Keyword, '_global'),
      default('_global')], 
     'diagnostic':[
      include('_whitespace'),
      (
       '[%s]' % _dquote, String.Double, ('#pop', 'message-string')),
      default(('#pop', 'before-plain-string', 'directive-keyword?'))], 
     'before-plain-string':[
      include('_whitespace'),
      (
       '[%s]' % _dquote, String.Double, ('#pop', 'plain-string'))], 
     'message-string':[
      (
       '[~^]+', String.Escape),
      include('plain-string')], 
     '_directive-keyword!':[
      include('_whitespace'),
      (
       words(('additive', 'alias', 'buffer', 'class', 'creature', 'data', 'error', 'fatalerror',
       'first', 'has', 'held', 'initial', 'initstr', 'last', 'long', 'meta', 'multi',
       'multiexcept', 'multiheld', 'multiinside', 'noun', 'number', 'only', 'private',
       'replace', 'reverse', 'scope', 'score', 'special', 'string', 'table', 'terminating',
       'time', 'topic', 'warning', 'with'),
         suffix='\\b'),
       Keyword, '#pop'),
      (
       '[%s]{1,2}>|[+=]' % _dash, Punctuation, '#pop')], 
     '_directive-keyword':[
      include('_directive-keyword!'),
      include('value')], 
     'directive-keyword?':[
      include('_directive-keyword!'),
      default('#pop')], 
     'property-keyword*':[
      include('_whitespace'),
      (
       '(additive|long)\\b', Keyword),
      default('#pop')], 
     'trace-keyword?':[
      include('_whitespace'),
      (
       words(('assembly', 'dictionary', 'expressions', 'lines', 'linker', 'objects', 'off',
       'on', 'symbols', 'tokens', 'verbs'),
         suffix='\\b'),
       Keyword, '#pop'),
      default('#pop')], 
     'statements':[
      include('_whitespace'),
      (
       '\\]', Punctuation, '#pop'),
      (
       '[;{}]', Punctuation),
      (
       words(('box', 'break', 'continue', 'default', 'give', 'inversion', 'new_line', 'quit',
       'read', 'remove', 'return', 'rfalse', 'rtrue', 'spaces', 'string', 'until'),
         suffix='\\b'),
       Keyword, 'default'),
      (
       '(do|else)\\b', Keyword),
      (
       '(font|style)\\b', Keyword,
       ('default', 'miscellaneous-keyword?')),
      (
       'for\\b', Keyword, ('for', '(?')),
      (
       '(if|switch|while)', Keyword,
       ('expression', '_expression', '(?')),
      (
       '(jump|save|restore)\\b', Keyword, ('default', 'label?')),
      (
       'objectloop\\b', Keyword,
       ('_keyword-expression', 'variable?', '(?')),
      (
       'print(_ret)?\\b|(?=[%s])' % _dquote, Keyword, 'print-list'),
      (
       '\\.', Name.Label, 'label?'),
      (
       '@', Keyword, 'opcode'),
      (
       '#(?![agrnw]\\$|#)', Punctuation, 'directive'),
      (
       '<', Punctuation, 'default'),
      (
       'move\\b', Keyword,
       ('default', '_keyword-expression', '_expression')),
      default(('default', '_keyword-expression', '_expression'))], 
     'miscellaneous-keyword?':[
      include('_whitespace'),
      (
       '(bold|fixed|from|near|off|on|reverse|roman|to|underline)\\b',
       Keyword, '#pop'),
      (
       '(a|A|an|address|char|name|number|object|property|string|the|The)\\b(?=(\\s+|(![^%s]*))*\\))' % _newline, Keyword.Pseudo,
       '#pop'),
      (
       '%s(?=(\\s+|(![^%s]*))*\\))' % (_name, _newline), Name.Function,
       '#pop'),
      default('#pop')], 
     '(?':[
      include('_whitespace'),
      (
       '\\(', Punctuation, '#pop'),
      default('#pop')], 
     'for':[
      include('_whitespace'),
      (
       ';', Punctuation, ('_for-expression', '_expression')),
      default(('_for-expression', '_expression'))], 
     'print-list':[
      include('_whitespace'),
      (
       ';', Punctuation, '#pop'),
      (
       ':', Error),
      default(('_list-expression', '_expression', '_list-expression', 'form'))], 
     'form':[
      include('_whitespace'),
      (
       '\\(', Punctuation, ('#pop', 'miscellaneous-keyword?')),
      default('#pop')], 
     'opcode':[
      include('_whitespace'),
      (
       '[%s]' % _dquote, String.Double, ('operands', 'plain-string')),
      (
       _name, Keyword, 'operands')], 
     'operands':[
      (
       ':', Error),
      default(('_assembly-expression', '_expression'))]}

    def get_tokens_unprocessed(self, text):
        objectloop_queue = []
        objectloop_token_count = -1
        previous_token = None
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            if previous_token is Name.Variable:
                if value == 'in':
                    objectloop_queue = [
                     [
                      index, token, value]]
                    objectloop_token_count = 2
                else:
                    if objectloop_token_count > 0:
                        if token not in Comment:
                            if token not in Text:
                                objectloop_token_count -= 1
                        objectloop_queue.append((index, token, value))
                    else:
                        if objectloop_token_count == 0:
                            if objectloop_queue[(-1)][2] == ')':
                                objectloop_queue[0][1] = Keyword
                            while objectloop_queue:
                                yield objectloop_queue.pop(0)

                            objectloop_token_count = -1
                        yield (
                         index, token, value)
                if token not in Comment and token not in Text:
                    previous_token = token

        while objectloop_queue:
            yield objectloop_queue.pop(0)


class Inform7Lexer(RegexLexer):
    __doc__ = '\n    For `Inform 7 <http://inform7.com/>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Inform 7'
    aliases = ['inform7', 'i7']
    filenames = ['*.ni', '*.i7x']
    flags = re.MULTILINE | re.DOTALL | re.UNICODE
    _dash = Inform6Lexer._dash
    _dquote = Inform6Lexer._dquote
    _newline = Inform6Lexer._newline
    _start = '\\A|(?<=[%s])' % _newline
    tokens = {}
    token_variants = [
     '+i6t-not-inline', '+i6t-inline', '+i6t-use-option']
    for level in token_variants:
        tokens[level] = {'+i6-root':list(Inform6Lexer.tokens['root']), 
         '+i6t-root':[
          (
           '[^%s]*' % Inform6Lexer._newline, Comment.Preproc,
           ('directive', '+p'))], 
         'root':[
          (
           '(\\|?\\s)+', Text),
          (
           '\\[', Comment.Multiline, '+comment'),
          (
           '[%s]' % _dquote, Generic.Heading,
           ('+main', '+titling', '+titling-string')),
          default(('+main', '+heading?'))], 
         '+titling-string':[
          (
           '[^%s]+' % _dquote, Generic.Heading),
          (
           '[%s]' % _dquote, Generic.Heading, '#pop')], 
         '+titling':[
          (
           '\\[', Comment.Multiline, '+comment'),
          (
           '[^%s.;:|%s]+' % (_dquote, _newline), Generic.Heading),
          (
           '[%s]' % _dquote, Generic.Heading, '+titling-string'),
          (
           '[%s]{2}|(?<=[\\s%s])\\|[\\s%s]' % (_newline, _dquote, _dquote),
           Text, ('#pop', '+heading?')),
          (
           '[.;:]|(?<=[\\s%s])\\|' % _dquote, Text, '#pop'),
          (
           '[|%s]' % _newline, Generic.Heading)], 
         '+main':[
          (
           '(?i)[^%s:a\\[(|%s]+' % (_dquote, _newline), Text),
          (
           '[%s]' % _dquote, String.Double, '+text'),
          (
           ':', Text, '+phrase-definition'),
          (
           '(?i)\\bas\\b', Text, '+use-option'),
          (
           '\\[', Comment.Multiline, '+comment'),
          (
           '(\\([%s])(.*?)([%s]\\))' % (_dash, _dash),
           bygroups(Punctuation, using(this, state=('+i6-root', 'directive'), i6t='+i6t-not-inline'), Punctuation)),
          (
           '(%s|(?<=[\\s;:.%s]))\\|\\s|[%s]{2,}' % (
            _start, _dquote, _newline), Text, '+heading?'),
          (
           '(?i)[a(|%s]' % _newline, Text)], 
         '+phrase-definition':[
          (
           '\\s+', Text),
          (
           '\\[', Comment.Multiline, '+comment'),
          (
           '(\\([%s])(.*?)([%s]\\))' % (_dash, _dash),
           bygroups(Punctuation, using(this, state=('+i6-root', 'directive', 'default', 'statements'),
             i6t='+i6t-inline'), Punctuation), '#pop'),
          default('#pop')], 
         '+use-option':[
          (
           '\\s+', Text),
          (
           '\\[', Comment.Multiline, '+comment'),
          (
           '(\\([%s])(.*?)([%s]\\))' % (_dash, _dash),
           bygroups(Punctuation, using(this, state=('+i6-root', 'directive'), i6t='+i6t-use-option'), Punctuation), '#pop'),
          default('#pop')], 
         '+comment':[
          (
           '[^\\[\\]]+', Comment.Multiline),
          (
           '\\[', Comment.Multiline, '#push'),
          (
           '\\]', Comment.Multiline, '#pop')], 
         '+text':[
          (
           '[^\\[%s]+' % _dquote, String.Double),
          (
           '\\[.*?\\]', String.Interpol),
          (
           '[%s]' % _dquote, String.Double, '#pop')], 
         '+heading?':[
          (
           '(\\|?\\s)+', Text),
          (
           '\\[', Comment.Multiline, '+comment'),
          (
           '[%s]{4}\\s+' % _dash, Text, '+documentation-heading'),
          (
           '[%s]{1,3}' % _dash, Text),
          (
           '(?i)(volume|book|part|chapter|section)\\b[^%s]*' % _newline,
           Generic.Heading, '#pop'),
          default('#pop')], 
         '+documentation-heading':[
          (
           '\\s+', Text),
          (
           '\\[', Comment.Multiline, '+comment'),
          (
           '(?i)documentation\\s+', Text, '+documentation-heading2'),
          default('#pop')], 
         '+documentation-heading2':[
          (
           '\\s+', Text),
          (
           '\\[', Comment.Multiline, '+comment'),
          (
           '[%s]{4}\\s' % _dash, Text, '+documentation'),
          default('#pop:2')], 
         '+documentation':[
          (
           '(?i)(%s)\\s*(chapter|example)\\s*:[^%s]*' % (
            _start, _newline), Generic.Heading),
          (
           '(?i)(%s)\\s*section\\s*:[^%s]*' % (_start, _newline),
           Generic.Subheading),
          (
           '((%s)\\t.*?[%s])+' % (_start, _newline),
           using(this, state='+main')),
          (
           '[^%s\\[]+|[%s\\[]' % (_newline, _newline), Text),
          (
           '\\[', Comment.Multiline, '+comment')], 
         '+i6t-not-inline':[
          (
           '(%s)@c( .*?)?([%s]|\\Z)' % (_start, _newline),
           Comment.Preproc),
          (
           '(%s)@([%s]+|Purpose:)[^%s]*' % (_start, _dash, _newline),
           Comment.Preproc),
          (
           '(%s)@p( .*?)?([%s]|\\Z)' % (_start, _newline),
           Generic.Heading, '+p')], 
         '+i6t-use-option':[
          include('+i6t-not-inline'),
          (
           '(\\{)(N)(\\})', bygroups(Punctuation, Text, Punctuation))], 
         '+i6t-inline':[
          (
           '(\\{)(\\S[^}]*)?(\\})',
           bygroups(Punctuation, using(this, state='+main'), Punctuation))], 
         '+i6t':[
          (
           '(\\{[%s])(![^}]*)(\\}?)' % _dash,
           bygroups(Punctuation, Comment.Single, Punctuation)),
          (
           '(\\{[%s])(lines)(:)([^}]*)(\\}?)' % _dash,
           bygroups(Punctuation, Keyword, Punctuation, Text, Punctuation), '+lines'),
          (
           '(\\{[%s])([^:}]*)(:?)([^}]*)(\\}?)' % _dash,
           bygroups(Punctuation, Keyword, Punctuation, Text, Punctuation)),
          (
           '(\\(\\+)(.*?)(\\+\\)|\\Z)',
           bygroups(Punctuation, using(this, state='+main'), Punctuation))], 
         '+p':[
          (
           '[^@]+', Comment.Preproc),
          (
           '(%s)@c( .*?)?([%s]|\\Z)' % (_start, _newline),
           Comment.Preproc, '#pop'),
          (
           '(%s)@([%s]|Purpose:)' % (_start, _dash), Comment.Preproc),
          (
           '(%s)@p( .*?)?([%s]|\\Z)' % (_start, _newline),
           Generic.Heading),
          (
           '@', Comment.Preproc)], 
         '+lines':[
          (
           '(%s)@c( .*?)?([%s]|\\Z)' % (_start, _newline),
           Comment.Preproc),
          (
           '(%s)@([%s]|Purpose:)[^%s]*' % (_start, _dash, _newline),
           Comment.Preproc),
          (
           '(%s)@p( .*?)?([%s]|\\Z)' % (_start, _newline),
           Generic.Heading, '+p'),
          (
           '(%s)@\\w*[ %s]' % (_start, _newline), Keyword),
          (
           '![^%s]*' % _newline, Comment.Single),
          (
           '(\\{)([%s]endlines)(\\})' % _dash,
           bygroups(Punctuation, Keyword, Punctuation), '#pop'),
          (
           '[^@!{]+?([%s]|\\Z)|.' % _newline, Text)]}
        for token in Inform6Lexer.tokens:
            if token == 'root':
                pass
            else:
                tokens[level][token] = list(Inform6Lexer.tokens[token])
                if not token.startswith('_'):
                    tokens[level][token][:0] = [
                     include('+i6t'), include(level)]

    def __init__(self, **options):
        level = options.get('i6t', '+i6t-not-inline')
        if level not in self._all_tokens:
            self._tokens = self.__class__.process_tokendef(level)
        else:
            self._tokens = self._all_tokens[level]
        (RegexLexer.__init__)(self, **options)


class Inform6TemplateLexer(Inform7Lexer):
    __doc__ = '\n    For `Inform 6 template\n    <http://inform7.com/sources/src/i6template/Woven/index.html>`_ code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Inform 6 template'
    aliases = ['i6t']
    filenames = ['*.i6t']

    def get_tokens_unprocessed(self, text, stack=('+i6t-root',)):
        return Inform7Lexer.get_tokens_unprocessed(self, text, stack)


class Tads3Lexer(RegexLexer):
    __doc__ = '\n    For `TADS 3 <http://www.tads.org/>`_ source code.\n    '
    name = 'TADS 3'
    aliases = ['tads3']
    filenames = ['*.t']
    flags = re.DOTALL | re.MULTILINE
    _comment_single = '(?://(?:[^\\\\\\n]|\\\\+[\\w\\W])*$)'
    _comment_multiline = '(?:/\\*(?:[^*]|\\*(?!/))*\\*/)'
    _escape = '(?:\\\\(?:[\\n\\\\<>"\\\'^v bnrt]|u[\\da-fA-F]{,4}|x[\\da-fA-F]{,2}|[0-3]?[0-7]{1,2}))'
    _name = '(?:[_a-zA-Z]\\w*)'
    _no_quote = '(?=\\s|\\\\?>)'
    _operator = '(?:&&|\\|\\||\\+\\+|--|\\?\\?|::|[.,@\\[\\]~]|(?:[=+\\-*/%!&|^]|<<?|>>?>?)=?)'
    _ws = '(?:\\\\|\\s|%s|%s)' % (_comment_single, _comment_multiline)
    _ws_pp = '(?:\\\\\\n|[^\\S\\n]|%s|%s)' % (_comment_single, _comment_multiline)

    def _make_string_state(triple, double, verbatim=None, _escape=_escape):
        if verbatim:
            verbatim = ''.join(['(?:%s|%s)' % (re.escape(c.lower()), re.escape(c.upper())) for c in verbatim])
        else:
            char = '"' if double else "'"
            token = String.Double if double else String.Single
            escaped_quotes = '+|%s(?!%s{2})' % (char, char) if triple else ''
            prefix = '%s%s' % ('t' if triple else '', 'd' if double else 's')
            tag_state_name = '%sqt' % prefix
            state = []
            if triple:
                state += [
                 (
                  '%s{3,}' % char, token, '#pop'),
                 (
                  '\\\\%s+' % char, String.Escape),
                 (
                  char, token)]
            else:
                state.append((char, token, '#pop'))
            state += [
             include('s/verbatim'),
             (
              '[^\\\\<&{}%s]+' % char, token)]
            if verbatim:
                state.append((
                 '\\\\?<(/|\\\\\\\\|(?!%s)\\\\)%s(?=[\\s=>])' % (
                  _escape, verbatim),
                 Name.Tag, ('#pop', '%sqs' % prefix, tag_state_name)))
            else:
                state += [
                 (
                  '\\\\?<!([^><\\\\%s]|<(?!<)|\\\\%s%s|%s|\\\\.)*>?' % (
                   char, char, escaped_quotes, _escape), Comment.Multiline),
                 (
                  '(?i)\\\\?<listing(?=[\\s=>]|\\\\>)', Name.Tag,
                  (
                   '#pop', '%sqs/listing' % prefix, tag_state_name)),
                 (
                  '(?i)\\\\?<xmp(?=[\\s=>]|\\\\>)', Name.Tag,
                  (
                   '#pop', '%sqs/xmp' % prefix, tag_state_name)),
                 (
                  '\\\\?<([^\\s=><\\\\%s]|<(?!<)|\\\\%s%s|%s|\\\\.)*' % (
                   char, char, escaped_quotes, _escape), Name.Tag,
                  tag_state_name),
                 include('s/entity')]
        state += [
         include('s/escape'),
         (
          '\\{([^}<\\\\%s]|<(?!<)|\\\\%s%s|%s|\\\\.)*\\}' % (
           char, char, escaped_quotes, _escape), String.Interpol),
         (
          '[\\\\&{}<]', token)]
        return state

    def _make_tag_state(triple, double, _escape=_escape):
        char = '"' if double else "'"
        quantifier = '{3,}' if triple else ''
        state_name = '%s%sqt' % ('t' if triple else '', 'd' if double else 's')
        token = String.Double if double else String.Single
        escaped_quotes = '+|%s(?!%s{2})' % (char, char) if triple else ''
        return [
         (
          '%s%s' % (char, quantifier), token, '#pop:2'),
         (
          '(\\s|\\\\\\n)+', Text),
         (
          '(=)(\\\\?")', bygroups(Punctuation, String.Double),
          'dqs/%s' % state_name),
         (
          "(=)(\\\\?')", bygroups(Punctuation, String.Single),
          'sqs/%s' % state_name),
         (
          '=', Punctuation, 'uqs/%s' % state_name),
         (
          '\\\\?>', Name.Tag, '#pop'),
         (
          '\\{([^}<\\\\%s]|<(?!<)|\\\\%s%s|%s|\\\\.)*\\}' % (
           char, char, escaped_quotes, _escape), String.Interpol),
         (
          '([^\\s=><\\\\%s]|<(?!<)|\\\\%s%s|%s|\\\\.)+' % (
           char, char, escaped_quotes, _escape), Name.Attribute),
         include('s/escape'),
         include('s/verbatim'),
         include('s/entity'),
         (
          '[\\\\{}&]', Name.Attribute)]

    def _make_attribute_value_state(terminator, host_triple, host_double, _escape=_escape):
        token = String.Double if terminator == '"' else String.Single if terminator == "'" else String.Other
        host_char = '"' if host_double else "'"
        host_quantifier = '{3,}' if host_triple else ''
        host_token = String.Double if host_double else String.Single
        escaped_quotes = '+|%s(?!%s{2})' % (host_char, host_char) if host_triple else ''
        return [
         (
          '%s%s' % (host_char, host_quantifier), host_token, '#pop:3'),
         (
          '%s%s' % ('' if token is String.Other else '\\\\?', terminator),
          token, '#pop'),
         include('s/verbatim'),
         include('s/entity'),
         (
          '\\{([^}<\\\\%s]|<(?!<)|\\\\%s%s|%s|\\\\.)*\\}' % (
           host_char, host_char, escaped_quotes, _escape), String.Interpol),
         (
          '([^\\s"\\\'<%s{}\\\\&])+' % ('>' if token is String.Other else ''),
          token),
         include('s/escape'),
         (
          '["\\\'\\s&{<}\\\\]', token)]

    tokens = {'root':[
      (
       '\ufeff', Text),
      (
       '\\{', Punctuation, 'object-body'),
      (
       ';+', Punctuation),
      (
       '(?=(argcount|break|case|catch|continue|default|definingobj|delegated|do|else|for|foreach|finally|goto|if|inherited|invokee|local|nil|new|operator|replaced|return|self|switch|targetobj|targetprop|throw|true|try|while)\\b)',
       Text, 'block'),
      (
       '(%s)(%s*)(\\()' % (_name, _ws),
       bygroups(Name.Function, using(this, state='whitespace'), Punctuation),
       ('block?/root', 'more/parameters', 'main/parameters')),
      include('whitespace'),
      (
       '\\++', Punctuation),
      (
       '[^\\s!"%-(*->@-_a-z{-~]+', Error),
      (
       '(?!\\Z)', Text, 'main/root')], 
     'main/root':[
      include('main/basic'),
      default(('#pop', 'object-body/no-braces', 'classes', 'class'))], 
     'object-body/no-braces':[
      (
       ';', Punctuation, '#pop'),
      (
       '\\{', Punctuation, ('#pop', 'object-body')),
      include('object-body')], 
     'object-body':[
      (
       ';', Punctuation),
      (
       '\\{', Punctuation, '#push'),
      (
       '\\}', Punctuation, '#pop'),
      (
       ':', Punctuation, ('classes', 'class')),
      (
       '(%s?)(%s*)(\\()' % (_name, _ws),
       bygroups(Name.Function, using(this, state='whitespace'), Punctuation),
       ('block?', 'more/parameters', 'main/parameters')),
      (
       '(%s)(%s*)(\\{)' % (_name, _ws),
       bygroups(Name.Function, using(this, state='whitespace'), Punctuation), 'block'),
      (
       '(%s)(%s*)(:)' % (_name, _ws),
       bygroups(Name.Variable, using(this, state='whitespace'), Punctuation),
       ('object-body/no-braces', 'classes', 'class')),
      include('whitespace'),
      (
       '->|%s' % _operator, Punctuation, 'main'),
      default('main/object-body')], 
     'main/object-body':[
      include('main/basic'),
      (
       '(%s)(%s*)(=?)' % (_name, _ws),
       bygroups(Name.Variable, using(this, state='whitespace'), Punctuation), ('#pop', 'more', 'main')),
      default('#pop:2')], 
     'block?/root':[
      (
       '\\{', Punctuation, ('#pop', 'block')),
      include('whitespace'),
      (
       '(?=[\\[\\\'"<(:])', Text,
       ('#pop', 'object-body/no-braces', 'grammar', 'grammar-rules')),
      default(('#pop', 'object-body/no-braces'))], 
     'block?':[
      (
       '\\{', Punctuation, ('#pop', 'block')),
      include('whitespace'),
      default('#pop')], 
     'block/basic':[
      (
       '[;:]+', Punctuation),
      (
       '\\{', Punctuation, '#push'),
      (
       '\\}', Punctuation, '#pop'),
      (
       'default\\b', Keyword.Reserved),
      (
       '(%s)(%s*)(:)' % (_name, _ws),
       bygroups(Name.Label, using(this, state='whitespace'), Punctuation)),
      include('whitespace')], 
     'block':[
      include('block/basic'),
      (
       '(?!\\Z)', Text, ('more', 'main'))], 
     'block/embed':[
      (
       '>>', String.Interpol, '#pop'),
      include('block/basic'),
      (
       '(?!\\Z)', Text, ('more/embed', 'main'))], 
     'main/basic':[
      include('whitespace'),
      (
       '\\(', Punctuation, ('#pop', 'more', 'main')),
      (
       '\\[', Punctuation, ('#pop', 'more/list', 'main')),
      (
       '\\{', Punctuation,
       ('#pop', 'more/inner', 'main/inner', 'more/parameters', 'main/parameters')),
      (
       '\\*|\\.{3}', Punctuation, '#pop'),
      (
       '(?i)0x[\\da-f]+', Number.Hex, '#pop'),
      (
       '(\\d+\\.(?!\\.)\\d*|\\.\\d+)([eE][-+]?\\d+)?|\\d+[eE][-+]?\\d+',
       Number.Float, '#pop'),
      (
       '0[0-7]+', Number.Oct, '#pop'),
      (
       '\\d+', Number.Integer, '#pop'),
      (
       '"""', String.Double, ('#pop', 'tdqs')),
      (
       "'''", String.Single, ('#pop', 'tsqs')),
      (
       '"', String.Double, ('#pop', 'dqs')),
      (
       "'", String.Single, ('#pop', 'sqs')),
      (
       'R"""', String.Regex, ('#pop', 'tdqr')),
      (
       "R'''", String.Regex, ('#pop', 'tsqr')),
      (
       'R"', String.Regex, ('#pop', 'dqr')),
      (
       "R'", String.Regex, ('#pop', 'sqr')),
      (
       '(extern)(%s+)(object\\b)' % _ws,
       bygroups(Keyword.Reserved, using(this, state='whitespace'), Keyword.Reserved)),
      (
       '(function|method)(%s*)(\\()' % _ws,
       bygroups(Keyword.Reserved, using(this, state='whitespace'), Punctuation),
       ('#pop', 'block?', 'more/parameters', 'main/parameters')),
      (
       '(modify)(%s+)(grammar\\b)' % _ws,
       bygroups(Keyword.Reserved, using(this, state='whitespace'), Keyword.Reserved),
       ('#pop', 'object-body/no-braces', ':', 'grammar')),
      (
       '(new)(%s+(?=(?:function|method)\\b))' % _ws,
       bygroups(Keyword.Reserved, using(this, state='whitespace'))),
      (
       '(object)(%s+)(template\\b)' % _ws,
       bygroups(Keyword.Reserved, using(this, state='whitespace'), Keyword.Reserved), ('#pop', 'template')),
      (
       '(string)(%s+)(template\\b)' % _ws,
       bygroups(Keyword, using(this, state='whitespace'), Keyword.Reserved), ('#pop', 'function-name')),
      (
       '(argcount|definingobj|invokee|replaced|targetobj|targetprop)\\b',
       Name.Builtin, '#pop'),
      (
       '(break|continue|goto)\\b', Keyword.Reserved, ('#pop', 'label')),
      (
       '(case|extern|if|intrinsic|return|static|while)\\b',
       Keyword.Reserved),
      (
       'catch\\b', Keyword.Reserved, ('#pop', 'catch')),
      (
       'class\\b', Keyword.Reserved,
       ('#pop', 'object-body/no-braces', 'class')),
      (
       '(default|do|else|finally|try)\\b', Keyword.Reserved, '#pop'),
      (
       '(dictionary|property)\\b', Keyword.Reserved,
       ('#pop', 'constants')),
      (
       'enum\\b', Keyword.Reserved, ('#pop', 'enum')),
      (
       'export\\b', Keyword.Reserved, ('#pop', 'main')),
      (
       '(for|foreach)\\b', Keyword.Reserved,
       ('#pop', 'more/inner', 'main/inner')),
      (
       '(function|method)\\b', Keyword.Reserved,
       ('#pop', 'block?', 'function-name')),
      (
       'grammar\\b', Keyword.Reserved,
       ('#pop', 'object-body/no-braces', 'grammar')),
      (
       'inherited\\b', Keyword.Reserved, ('#pop', 'inherited')),
      (
       'local\\b', Keyword.Reserved,
       ('#pop', 'more/local', 'main/local')),
      (
       '(modify|replace|switch|throw|transient)\\b', Keyword.Reserved,
       '#pop'),
      (
       'new\\b', Keyword.Reserved, ('#pop', 'class')),
      (
       '(nil|true)\\b', Keyword.Constant, '#pop'),
      (
       'object\\b', Keyword.Reserved, ('#pop', 'object-body/no-braces')),
      (
       'operator\\b', Keyword.Reserved, ('#pop', 'operator')),
      (
       'propertyset\\b', Keyword.Reserved,
       ('#pop', 'propertyset', 'main')),
      (
       'self\\b', Name.Builtin.Pseudo, '#pop'),
      (
       'template\\b', Keyword.Reserved, ('#pop', 'template')),
      (
       '(__objref|defined)(%s*)(\\()' % _ws,
       bygroups(Operator.Word, using(this, state='whitespace'), Operator), ('#pop', 'more/__objref', 'main')),
      (
       'delegated\\b', Operator.Word),
      (
       '(__DATE__|__DEBUG|__LINE__|__FILE__|__TADS_MACRO_FORMAT_VERSION|__TADS_SYS_\\w*|__TADS_SYSTEM_NAME|__TADS_VERSION_MAJOR|__TADS_VERSION_MINOR|__TADS3|__TIME__|construct|finalize|grammarInfo|grammarTag|lexicalParent|miscVocab|sourceTextGroup|sourceTextGroupName|sourceTextGroupOrder|sourceTextOrder)\\b',
       Name.Builtin, '#pop')], 
     'main':[
      include('main/basic'),
      (
       _name, Name, '#pop'),
      default('#pop')], 
     'more/basic':[
      (
       '\\(', Punctuation, ('more/list', 'main')),
      (
       '\\[', Punctuation, ('more', 'main')),
      (
       '\\.{3}', Punctuation),
      (
       '->|\\.\\.', Punctuation, 'main'),
      (
       '(?=;)|[:)\\]]', Punctuation, '#pop'),
      include('whitespace'),
      (
       _operator, Operator, 'main'),
      (
       '\\?', Operator, ('main', 'more/conditional', 'main')),
      (
       '(is|not)(%s+)(in\\b)' % _ws,
       bygroups(Operator.Word, using(this, state='whitespace'), Operator.Word)),
      (
       '[^\\s!"%-_a-z{-~]+', Error)], 
     'more':[
      include('more/basic'),
      default('#pop')], 
     'more/conditional':[
      (
       ':(?!:)', Operator, '#pop'),
      include('more')], 
     'more/embed':[
      (
       '>>', String.Interpol, '#pop:2'),
      include('more')], 
     'main/inner':[
      (
       '\\(', Punctuation, ('#pop', 'more/inner', 'main/inner')),
      (
       'local\\b', Keyword.Reserved, ('#pop', 'main/local')),
      include('main')], 
     'more/inner':[
      (
       '\\}', Punctuation, '#pop'),
      (
       ',', Punctuation, 'main/inner'),
      (
       '(in|step)\\b', Keyword, 'main/inner'),
      include('more')], 
     'main/local':[
      (
       _name, Name.Variable, '#pop'),
      include('whitespace')], 
     'more/local':[
      (
       ',', Punctuation, 'main/local'),
      include('more')], 
     'more/list':[
      (
       '[,:]', Punctuation, 'main'),
      include('more')], 
     'main/parameters':[
      (
       '(%s)(%s*)(?=:)' % (_name, _ws),
       bygroups(Name.Variable, using(this, state='whitespace')), '#pop'),
      (
       '(%s)(%s+)(%s)' % (_name, _ws, _name),
       bygroups(Name.Class, using(this, state='whitespace'), Name.Variable), '#pop'),
      (
       '\\[+', Punctuation),
      include('main/basic'),
      (
       _name, Name.Variable, '#pop'),
      default('#pop')], 
     'more/parameters':[
      (
       '(:)(%s*(?=[?=,:)]))' % _ws,
       bygroups(Punctuation, using(this, state='whitespace'))),
      (
       '[?\\]]+', Punctuation),
      (
       '[:)]', Punctuation, ('#pop', 'multimethod?')),
      (
       ',', Punctuation, 'main/parameters'),
      (
       '=', Punctuation, ('more/parameter', 'main')),
      include('more')], 
     'more/parameter':[
      (
       '(?=[,)])', Text, '#pop'),
      include('more')], 
     'multimethod?':[
      (
       'multimethod\\b', Keyword, '#pop'),
      include('whitespace'),
      default('#pop')], 
     'more/__objref':[
      (
       ',', Punctuation, 'mode'),
      (
       '\\)', Operator, '#pop'),
      include('more')], 
     'mode':[
      (
       '(error|warn)\\b', Keyword, '#pop'),
      include('whitespace')], 
     'catch':[
      (
       '\\(+', Punctuation),
      (
       _name, Name.Exception, ('#pop', 'variables')),
      include('whitespace')], 
     'enum':[
      include('whitespace'),
      (
       'token\\b', Keyword, ('#pop', 'constants')),
      default(('#pop', 'constants'))], 
     'grammar':[
      (
       '\\)+', Punctuation),
      (
       '\\(', Punctuation, 'grammar-tag'),
      (
       ':', Punctuation, 'grammar-rules'),
      (
       _name, Name.Class),
      include('whitespace')], 
     'grammar-tag':[
      include('whitespace'),
      (
       '"""([^\\\\"<]|""?(?!")|\\\\"+|\\\\.|<(?!<))+("{3,}|<<)|R"""([^\\\\"]|""?(?!")|\\\\"+|\\\\.)+"{3,}|\'\'\'([^\\\\\'<]|\'\'?(?!\')|\\\\\'+|\\\\.|<(?!<))+(\'{3,}|<<)|R\'\'\'([^\\\\\']|\'\'?(?!\')|\\\\\'+|\\\\.)+\'{3,}|"([^\\\\"<]|\\\\.|<(?!<))+("|<<)|R"([^\\\\"]|\\\\.)+"|\'([^\\\\\'<]|\\\\.|<(?!<))+(\'|<<)|R\'([^\\\\\']|\\\\.)+\'|([^)\\s\\\\/]|/(?![/*]))+|\\)',
       String.Other, '#pop')], 
     'grammar-rules':[
      include('string'),
      include('whitespace'),
      (
       '(\\[)(%s*)(badness)' % _ws,
       bygroups(Punctuation, using(this, state='whitespace'), Keyword),
       'main'),
      (
       '->|%s|[()]' % _operator, Punctuation),
      (
       _name, Name.Constant),
      default('#pop:2')], 
     ':':[
      (
       ':', Punctuation, '#pop')], 
     'function-name':[
      (
       '(<<([^>]|>>>|>(?!>))*>>)+', String.Interpol),
      (
       '(?=%s?%s*[({])' % (_name, _ws), Text, '#pop'),
      (
       _name, Name.Function, '#pop'),
      include('whitespace')], 
     'inherited':[
      (
       '<', Punctuation, ('#pop', 'classes', 'class')),
      include('whitespace'),
      (
       _name, Name.Class, '#pop'),
      default('#pop')], 
     'operator':[
      (
       'negate\\b', Operator.Word, '#pop'),
      include('whitespace'),
      (
       _operator, Operator),
      default('#pop')], 
     'propertyset':[
      (
       '\\(', Punctuation, ('more/parameters', 'main/parameters')),
      (
       '\\{', Punctuation, ('#pop', 'object-body')),
      include('whitespace')], 
     'template':[
      (
       '(?=;)', Text, '#pop'),
      include('string'),
      (
       'inherited\\b', Keyword.Reserved),
      include('whitespace'),
      (
       '->|\\?|%s' % _operator, Punctuation),
      (
       _name, Name.Variable)], 
     'class':[
      (
       '\\*|\\.{3}', Punctuation, '#pop'),
      (
       'object\\b', Keyword.Reserved, '#pop'),
      (
       'transient\\b', Keyword.Reserved),
      (
       _name, Name.Class, '#pop'),
      include('whitespace'),
      default('#pop')], 
     'classes':[
      (
       '[:,]', Punctuation, 'class'),
      include('whitespace'),
      (
       '>', Punctuation, '#pop'),
      default('#pop')], 
     'constants':[
      (
       ',+', Punctuation),
      (
       ';', Punctuation, '#pop'),
      (
       'property\\b', Keyword.Reserved),
      (
       _name, Name.Constant),
      include('whitespace')], 
     'label':[
      (
       _name, Name.Label, '#pop'),
      include('whitespace'),
      default('#pop')], 
     'variables':[
      (
       ',+', Punctuation),
      (
       '\\)', Punctuation, '#pop'),
      include('whitespace'),
      (
       _name, Name.Variable)], 
     'whitespace':[
      (
       '^%s*#(%s|[^\\n]|(?<=\\\\)\\n)*\\n?' % (_ws_pp, _comment_multiline),
       Comment.Preproc),
      (
       _comment_single, Comment.Single),
      (
       _comment_multiline, Comment.Multiline),
      (
       '\\\\+\\n+%s*#?|\\n+|([^\\S\\n]|\\\\)+' % _ws_pp, Text)], 
     'string':[
      (
       '"""', String.Double, 'tdqs'),
      (
       "'''", String.Single, 'tsqs'),
      (
       '"', String.Double, 'dqs'),
      (
       "'", String.Single, 'sqs')], 
     's/escape':[
      (
       '\\{\\{|\\}\\}|%s' % _escape, String.Escape)], 
     's/verbatim':[
      (
       '<<\\s*(as\\s+decreasingly\\s+likely\\s+outcomes|cycling|else|end|first\\s+time|one\\s+of|only|or|otherwise|(sticky|(then\\s+)?(purely\\s+)?at)\\s+random|stopping|(then\\s+)?(half\\s+)?shuffled|\\|\\|)\\s*>>',
       String.Interpol),
      (
       '<<(%%(_(%s|\\\\?.)|[\\-+ ,#]|\\[\\d*\\]?)*\\d*\\.?\\d*(%s|\\\\?.)|\\s*((else|otherwise)\\s+)?(if|unless)\\b)?' % (
        _escape, _escape),
       String.Interpol, ('block/embed', 'more/embed', 'main'))], 
     's/entity':[
      (
       '(?i)&(#(x[\\da-f]+|\\d+)|[a-z][\\da-z]*);?', Name.Entity)], 
     'tdqs':_make_string_state(True, True), 
     'tsqs':_make_string_state(True, False), 
     'dqs':_make_string_state(False, True), 
     'sqs':_make_string_state(False, False), 
     'tdqs/listing':_make_string_state(True, True, 'listing'), 
     'tsqs/listing':_make_string_state(True, False, 'listing'), 
     'dqs/listing':_make_string_state(False, True, 'listing'), 
     'sqs/listing':_make_string_state(False, False, 'listing'), 
     'tdqs/xmp':_make_string_state(True, True, 'xmp'), 
     'tsqs/xmp':_make_string_state(True, False, 'xmp'), 
     'dqs/xmp':_make_string_state(False, True, 'xmp'), 
     'sqs/xmp':_make_string_state(False, False, 'xmp'), 
     'tdqt':_make_tag_state(True, True), 
     'tsqt':_make_tag_state(True, False), 
     'dqt':_make_tag_state(False, True), 
     'sqt':_make_tag_state(False, False), 
     'dqs/tdqt':_make_attribute_value_state('"', True, True), 
     'dqs/tsqt':_make_attribute_value_state('"', True, False), 
     'dqs/dqt':_make_attribute_value_state('"', False, True), 
     'dqs/sqt':_make_attribute_value_state('"', False, False), 
     'sqs/tdqt':_make_attribute_value_state("'", True, True), 
     'sqs/tsqt':_make_attribute_value_state("'", True, False), 
     'sqs/dqt':_make_attribute_value_state("'", False, True), 
     'sqs/sqt':_make_attribute_value_state("'", False, False), 
     'uqs/tdqt':_make_attribute_value_state(_no_quote, True, True), 
     'uqs/tsqt':_make_attribute_value_state(_no_quote, True, False), 
     'uqs/dqt':_make_attribute_value_state(_no_quote, False, True), 
     'uqs/sqt':_make_attribute_value_state(_no_quote, False, False), 
     'tdqr':[
      (
       '[^\\\\"]+', String.Regex),
      (
       '\\\\"*', String.Regex),
      (
       '"{3,}', String.Regex, '#pop'),
      (
       '"', String.Regex)], 
     'tsqr':[
      (
       "[^\\\\']+", String.Regex),
      (
       "\\\\'*", String.Regex),
      (
       "'{3,}", String.Regex, '#pop'),
      (
       "'", String.Regex)], 
     'dqr':[
      (
       '[^\\\\"]+', String.Regex),
      (
       '\\\\"?', String.Regex),
      (
       '"', String.Regex, '#pop')], 
     'sqr':[
      (
       "[^\\\\']+", String.Regex),
      (
       "\\\\'?", String.Regex),
      (
       "'", String.Regex, '#pop')]}

    def get_tokens_unprocessed(self, text, **kwargs):
        pp = '^%s*#%s*' % (self._ws_pp, self._ws_pp)
        if_false_level = 0
        for index, token, value in (RegexLexer.get_tokens_unprocessed)(self, text, **kwargs):
            if if_false_level == 0:
                if token is Comment.Preproc:
                    if re.match('%sif%s+(0|nil)%s*$\\n?' % (
                     pp, self._ws_pp, self._ws_pp), value):
                        if_false_level = 1
            else:
                if token is Comment.Preproc:
                    if if_false_level == 1:
                        if re.match('%sel(if|se)\\b' % pp, value):
                            if_false_level = 0
                    if re.match('%sif' % pp, value):
                        if_false_level += 1
                    elif re.match('%sendif\\b' % pp, value):
                        if_false_level -= 1
                else:
                    token = Comment
            yield (
             index, token, value)