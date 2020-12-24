# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/basic.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 20306 bytes
"""
    pygments.lexers.basic
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for BASIC like languages (other than VB.net).

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, default, words, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'BlitzBasicLexer', 'BlitzMaxLexer', 'MonkeyLexer', 'CbmBasicV2Lexer',
 'QBasicLexer']

class BlitzMaxLexer(RegexLexer):
    __doc__ = '\n    For `BlitzMax <http://blitzbasic.com>`_ source code.\n\n    .. versionadded:: 1.4\n    '
    name = 'BlitzMax'
    aliases = ['blitzmax', 'bmax']
    filenames = ['*.bmx']
    mimetypes = ['text/x-bmx']
    bmax_vopwords = '\\b(Shl|Shr|Sar|Mod)\\b'
    bmax_sktypes = '@{1,2}|[!#$%]'
    bmax_lktypes = '\\b(Int|Byte|Short|Float|Double|Long)\\b'
    bmax_name = '[a-z_]\\w*'
    bmax_var = '(%s)(?:(?:([ \\t]*)(%s)|([ \\t]*:[ \\t]*\\b(?:Shl|Shr|Sar|Mod)\\b)|([ \\t]*)(:)([ \\t]*)(?:%s|(%s)))(?:([ \\t]*)(Ptr))?)' % (
     bmax_name, bmax_sktypes, bmax_lktypes, bmax_name)
    bmax_func = bmax_var + '?((?:[ \\t]|\\.\\.\\n)*)([(])'
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [
              (
               '[ \\t]+', Text),
              (
               '\\.\\.\\n', Text),
              (
               "'.*?\\n", Comment.Single),
              (
               '([ \\t]*)\\bRem\\n(\\n|.)*?\\s*\\bEnd([ \\t]*)Rem', Comment.Multiline),
              (
               '"', String.Double, 'string'),
              (
               '[0-9]+\\.[0-9]*(?!\\.)', Number.Float),
              (
               '\\.[0-9]*(?!\\.)', Number.Float),
              (
               '[0-9]+', Number.Integer),
              (
               '\\$[0-9a-f]+', Number.Hex),
              (
               '\\%[10]+', Number.Bin),
              (
               '(?:(?:(:)?([ \\t]*)(:?%s|([+\\-*/&|~]))|Or|And|Not|[=<>^]))' % bmax_vopwords, Operator),
              (
               '[(),.:\\[\\]]', Punctuation),
              (
               '(?:#[\\w \\t]*)', Name.Label),
              (
               '(?:\\?[\\w \\t]*)', Comment.Preproc),
              (
               '\\b(New)\\b([ \\t]?)([(]?)(%s)' % bmax_name,
               bygroups(Keyword.Reserved, Text, Punctuation, Name.Class)),
              (
               '\\b(Import|Framework|Module)([ \\t]+)(%s\\.%s)' % (
                bmax_name, bmax_name),
               bygroups(Keyword.Reserved, Text, Keyword.Namespace)),
              (
               bmax_func,
               bygroups(Name.Function, Text, Keyword.Type, Operator, Text, Punctuation, Text, Keyword.Type, Name.Class, Text, Keyword.Type, Text, Punctuation)),
              (
               bmax_var,
               bygroups(Name.Variable, Text, Keyword.Type, Operator, Text, Punctuation, Text, Keyword.Type, Name.Class, Text, Keyword.Type)),
              (
               '\\b(Type|Extends)([ \\t]+)(%s)' % bmax_name,
               bygroups(Keyword.Reserved, Text, Name.Class)),
              (
               '\\b(Ptr)\\b', Keyword.Type),
              (
               '\\b(Pi|True|False|Null|Self|Super)\\b', Keyword.Constant),
              (
               '\\b(Local|Global|Const|Field)\\b', Keyword.Declaration),
              (
               words(('TNullMethodException', 'TNullFunctionException', 'TNullObjectException', 'TArrayBoundsException',
       'TRuntimeException'), prefix='\\b', suffix='\\b'), Name.Exception),
              (
               words(('Strict', 'SuperStrict', 'Module', 'ModuleInfo', 'End', 'Return', 'Continue',
       'Exit', 'Public', 'Private', 'Var', 'VarPtr', 'Chr', 'Len', 'Asc', 'SizeOf',
       'Sgn', 'Abs', 'Min', 'Max', 'New', 'Release', 'Delete', 'Incbin', 'IncbinPtr',
       'IncbinLen', 'Framework', 'Include', 'Import', 'Extern', 'EndExtern', 'Function',
       'EndFunction', 'Type', 'EndType', 'Extends', 'Method', 'EndMethod', 'Abstract',
       'Final', 'If', 'Then', 'Else', 'ElseIf', 'EndIf', 'For', 'To', 'Next', 'Step',
       'EachIn', 'While', 'Wend', 'EndWhile', 'Repeat', 'Until', 'Forever', 'Select',
       'Case', 'Default', 'EndSelect', 'Try', 'Catch', 'EndTry', 'Throw', 'Assert',
       'Goto', 'DefData', 'ReadData', 'RestoreData'), prefix='\\b', suffix='\\b'),
               Keyword.Reserved),
              (
               '(%s)' % bmax_name, Name.Variable)], 
     
     'string': [
                (
                 '""', String.Double),
                (
                 '"C?', String.Double, '#pop'),
                (
                 '[^"]+', String.Double)]}


class BlitzBasicLexer(RegexLexer):
    __doc__ = '\n    For `BlitzBasic <http://blitzbasic.com>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'BlitzBasic'
    aliases = ['blitzbasic', 'b3d', 'bplus']
    filenames = ['*.bb', '*.decls']
    mimetypes = ['text/x-bb']
    bb_sktypes = '@{1,2}|[#$%]'
    bb_name = '[a-z]\\w*'
    bb_var = '(%s)(?:([ \\t]*)(%s)|([ \\t]*)([.])([ \\t]*)(?:(%s)))?' % (
     bb_name, bb_sktypes, bb_name)
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [
              (
               '[ \\t]+', Text),
              (
               ';.*?\\n', Comment.Single),
              (
               '"', String.Double, 'string'),
              (
               '[0-9]+\\.[0-9]*(?!\\.)', Number.Float),
              (
               '\\.[0-9]+(?!\\.)', Number.Float),
              (
               '[0-9]+', Number.Integer),
              (
               '\\$[0-9a-f]+', Number.Hex),
              (
               '\\%[10]+', Number.Bin),
              (
               words(('Shl', 'Shr', 'Sar', 'Mod', 'Or', 'And', 'Not', 'Abs', 'Sgn', 'Handle', 'Int',
       'Float', 'Str', 'First', 'Last', 'Before', 'After'), prefix='\\b', suffix='\\b'),
               Operator),
              (
               '([+\\-*/~=<>^])', Operator),
              (
               '[(),:\\[\\]\\\\]', Punctuation),
              (
               '\\.([ \\t]*)(%s)' % bb_name, Name.Label),
              (
               '\\b(New)\\b([ \\t]+)(%s)' % bb_name,
               bygroups(Keyword.Reserved, Text, Name.Class)),
              (
               '\\b(Gosub|Goto)\\b([ \\t]+)(%s)' % bb_name,
               bygroups(Keyword.Reserved, Text, Name.Label)),
              (
               '\\b(Object)\\b([ \\t]*)([.])([ \\t]*)(%s)\\b' % bb_name,
               bygroups(Operator, Text, Punctuation, Text, Name.Class)),
              (
               '\\b%s\\b([ \\t]*)(\\()' % bb_var,
               bygroups(Name.Function, Text, Keyword.Type, Text, Punctuation, Text, Name.Class, Text, Punctuation)),
              (
               '\\b(Function)\\b([ \\t]+)%s' % bb_var,
               bygroups(Keyword.Reserved, Text, Name.Function, Text, Keyword.Type, Text, Punctuation, Text, Name.Class)),
              (
               '\\b(Type)([ \\t]+)(%s)' % bb_name,
               bygroups(Keyword.Reserved, Text, Name.Class)),
              (
               '\\b(Pi|True|False|Null)\\b', Keyword.Constant),
              (
               '\\b(Local|Global|Const|Field|Dim)\\b', Keyword.Declaration),
              (
               words(('End', 'Return', 'Exit', 'Chr', 'Len', 'Asc', 'New', 'Delete', 'Insert', 'Include',
       'Function', 'Type', 'If', 'Then', 'Else', 'ElseIf', 'EndIf', 'For', 'To',
       'Next', 'Step', 'Each', 'While', 'Wend', 'Repeat', 'Until', 'Forever', 'Select',
       'Case', 'Default', 'Goto', 'Gosub', 'Data', 'Read', 'Restore'), prefix='\\b', suffix='\\b'),
               Keyword.Reserved),
              (
               bb_var,
               bygroups(Name.Variable, Text, Keyword.Type, Text, Punctuation, Text, Name.Class))], 
     
     'string': [
                (
                 '""', String.Double),
                (
                 '"C?', String.Double, '#pop'),
                (
                 '[^"]+', String.Double)]}


class MonkeyLexer(RegexLexer):
    __doc__ = '\n    For\n    `Monkey <https://en.wikipedia.org/wiki/Monkey_(programming_language)>`_\n    source code.\n\n    .. versionadded:: 1.6\n    '
    name = 'Monkey'
    aliases = ['monkey']
    filenames = ['*.monkey']
    mimetypes = ['text/x-monkey']
    name_variable = '[a-z_]\\w*'
    name_function = '[A-Z]\\w*'
    name_constant = '[A-Z_][A-Z0-9_]*'
    name_class = '[A-Z]\\w*'
    name_module = '[a-z0-9_]*'
    keyword_type = '(?:Int|Float|String|Bool|Object|Array|Void)'
    keyword_type_special = '[?%#$]'
    flags = re.MULTILINE
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               "'.*", Comment),
              (
               '(?i)^#rem\\b', Comment.Multiline, 'comment'),
              (
               '(?i)^(?:#If|#ElseIf|#Else|#EndIf|#End|#Print|#Error)\\b', Comment.Preproc),
              (
               '^#', Comment.Preproc, 'variables'),
              (
               '"', String.Double, 'string'),
              (
               '[0-9]+\\.[0-9]*(?!\\.)', Number.Float),
              (
               '\\.[0-9]+(?!\\.)', Number.Float),
              (
               '[0-9]+', Number.Integer),
              (
               '\\$[0-9a-fA-Z]+', Number.Hex),
              (
               '\\%[10]+', Number.Bin),
              (
               '\\b%s\\b' % keyword_type, Keyword.Type),
              (
               '(?i)\\b(?:Try|Catch|Throw)\\b', Keyword.Reserved),
              (
               'Throwable', Name.Exception),
              (
               '(?i)\\b(?:Null|True|False)\\b', Name.Builtin),
              (
               '(?i)\\b(?:Self|Super)\\b', Name.Builtin.Pseudo),
              (
               '\\b(?:HOST|LANG|TARGET|CONFIG)\\b', Name.Constant),
              (
               '(?i)^(Import)(\\s+)(.*)(\\n)',
               bygroups(Keyword.Namespace, Text, Name.Namespace, Text)),
              (
               '(?i)^Strict\\b.*\\n', Keyword.Reserved),
              (
               '(?i)(Const|Local|Global|Field)(\\s+)',
               bygroups(Keyword.Declaration, Text), 'variables'),
              (
               '(?i)(New|Class|Interface|Extends|Implements)(\\s+)',
               bygroups(Keyword.Reserved, Text), 'classname'),
              (
               '(?i)(Function|Method)(\\s+)',
               bygroups(Keyword.Reserved, Text), 'funcname'),
              (
               '(?i)(?:End|Return|Public|Private|Extern|Property|Final|Abstract)\\b',
               Keyword.Reserved),
              (
               '(?i)(?:If|Then|Else|ElseIf|EndIf|Select|Case|Default|While|Wend|Repeat|Until|Forever|For|To|Until|Step|EachIn|Next|Exit|Continue)\\s+',
               Keyword.Reserved),
              (
               '(?i)\\b(?:Module|Inline)\\b', Keyword.Reserved),
              (
               '[\\[\\]]', Punctuation),
              (
               '<=|>=|<>|\\*=|/=|\\+=|-=|&=|~=|\\|=|[-&*/^+=<>|~]', Operator),
              (
               '(?i)(?:Not|Mod|Shl|Shr|And|Or)', Operator.Word),
              (
               '[(){}!#,.:]', Punctuation),
              (
               '%s\\b' % name_constant, Name.Constant),
              (
               '%s\\b' % name_function, Name.Function),
              (
               '%s\\b' % name_variable, Name.Variable)], 
     
     'funcname': [
                  (
                   '(?i)%s\\b' % name_function, Name.Function),
                  (
                   ':', Punctuation, 'classname'),
                  (
                   '\\s+', Text),
                  (
                   '\\(', Punctuation, 'variables'),
                  (
                   '\\)', Punctuation, '#pop')], 
     
     'classname': [
                   (
                    '%s\\.' % name_module, Name.Namespace),
                   (
                    '%s\\b' % keyword_type, Keyword.Type),
                   (
                    '%s\\b' % name_class, Name.Class),
                   (
                    '(\\[)(\\s*)(\\d*)(\\s*)(\\])',
                    bygroups(Punctuation, Text, Number.Integer, Text, Punctuation)),
                   (
                    '\\s+(?!<)', Text, '#pop'),
                   (
                    '<', Punctuation, '#push'),
                   (
                    '>', Punctuation, '#pop'),
                   (
                    '\\n', Text, '#pop'),
                   default('#pop')], 
     
     'variables': [
                   (
                    '%s\\b' % name_constant, Name.Constant),
                   (
                    '%s\\b' % name_variable, Name.Variable),
                   (
                    '%s' % keyword_type_special, Keyword.Type),
                   (
                    '\\s+', Text),
                   (
                    ':', Punctuation, 'classname'),
                   (
                    ',', Punctuation, '#push'),
                   default('#pop')], 
     
     'string': [
                (
                 '[^"~]+', String.Double),
                (
                 '~q|~n|~r|~t|~z|~~', String.Escape),
                (
                 '"', String.Double, '#pop')], 
     
     'comment': [
                 (
                  '(?i)^#rem.*?', Comment.Multiline, '#push'),
                 (
                  '(?i)^#end.*?', Comment.Multiline, '#pop'),
                 (
                  '\\n', Comment.Multiline),
                 (
                  '.+', Comment.Multiline)]}


class CbmBasicV2Lexer(RegexLexer):
    __doc__ = '\n    For CBM BASIC V2 sources.\n\n    .. versionadded:: 1.6\n    '
    name = 'CBM BASIC V2'
    aliases = ['cbmbas']
    filenames = ['*.bas']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               'rem.*\\n', Comment.Single),
              (
               '\\s+', Text),
              (
               'new|run|end|for|to|next|step|go(to|sub)?|on|return|stop|cont|if|then|input#?|read|wait|load|save|verify|poke|sys|print#?|list|clr|cmd|open|close|get#?',
               Keyword.Reserved),
              (
               'data|restore|dim|let|def|fn', Keyword.Declaration),
              (
               'tab|spc|sgn|int|abs|usr|fre|pos|sqr|rnd|log|exp|cos|sin|tan|atn|peek|len|val|asc|(str|chr|left|right|mid)\\$',
               Name.Builtin),
              (
               '[-+*/^<>=]', Operator),
              (
               'not|and|or', Operator.Word),
              (
               '"[^"\\n]*.', String),
              (
               '\\d+|[-+]?\\d*\\.\\d*(e[-+]?\\d+)?', Number.Float),
              (
               '[(),:;]', Punctuation),
              (
               '\\w+[$%]?', Name)]}

    def analyse_text(self, text):
        if re.match('\\d+', text):
            return 0.2


class QBasicLexer(RegexLexer):
    __doc__ = '\n    For\n    `QBasic <http://en.wikipedia.org/wiki/QBasic>`_\n    source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'QBasic'
    aliases = ['qbasic', 'basic']
    filenames = ['*.BAS', '*.bas']
    mimetypes = ['text/basic']
    declarations = ('DATA', 'LET')
    functions = ('ABS', 'ASC', 'ATN', 'CDBL', 'CHR$', 'CINT', 'CLNG', 'COMMAND$', 'COS',
                 'CSNG', 'CSRLIN', 'CVD', 'CVDMBF', 'CVI', 'CVL', 'CVS', 'CVSMBF',
                 'DATE$', 'ENVIRON$', 'EOF', 'ERDEV', 'ERDEV$', 'ERL', 'ERR', 'EXP',
                 'FILEATTR', 'FIX', 'FRE', 'FREEFILE', 'HEX$', 'INKEY$', 'INP', 'INPUT$',
                 'INSTR', 'INT', 'IOCTL$', 'LBOUND', 'LCASE$', 'LEFT$', 'LEN', 'LOC',
                 'LOF', 'LOG', 'LPOS', 'LTRIM$', 'MID$', 'MKD$', 'MKDMBF$', 'MKI$',
                 'MKL$', 'MKS$', 'MKSMBF$', 'OCT$', 'PEEK', 'PEN', 'PLAY', 'PMAP',
                 'POINT', 'POS', 'RIGHT$', 'RND', 'RTRIM$', 'SADD', 'SCREEN', 'SEEK',
                 'SETMEM', 'SGN', 'SIN', 'SPACE$', 'SPC', 'SQR', 'STICK', 'STR$',
                 'STRIG', 'STRING$', 'TAB', 'TAN', 'TIME$', 'TIMER', 'UBOUND', 'UCASE$',
                 'VAL', 'VARPTR', 'VARPTR$', 'VARSEG')
    metacommands = ('$DYNAMIC', '$INCLUDE', '$STATIC')
    operators = ('AND', 'EQV', 'IMP', 'NOT', 'OR', 'XOR')
    statements = ('BEEP', 'BLOAD', 'BSAVE', 'CALL', 'CALL ABSOLUTE', 'CALL INTERRUPT',
                  'CALLS', 'CHAIN', 'CHDIR', 'CIRCLE', 'CLEAR', 'CLOSE', 'CLS', 'COLOR',
                  'COM', 'COMMON', 'CONST', 'DATA', 'DATE$', 'DECLARE', 'DEF FN',
                  'DEF SEG', 'DEFDBL', 'DEFINT', 'DEFLNG', 'DEFSNG', 'DEFSTR', 'DEF',
                  'DIM', 'DO', 'LOOP', 'DRAW', 'END', 'ENVIRON', 'ERASE', 'ERROR',
                  'EXIT', 'FIELD', 'FILES', 'FOR', 'NEXT', 'FUNCTION', 'GET', 'GOSUB',
                  'GOTO', 'IF', 'THEN', 'INPUT', 'INPUT #', 'IOCTL', 'KEY', 'KEY',
                  'KILL', 'LET', 'LINE', 'LINE INPUT', 'LINE INPUT #', 'LOCATE',
                  'LOCK', 'UNLOCK', 'LPRINT', 'LSET', 'MID$', 'MKDIR', 'NAME', 'ON COM',
                  'ON ERROR', 'ON KEY', 'ON PEN', 'ON PLAY', 'ON STRIG', 'ON TIMER',
                  'ON UEVENT', 'ON', 'OPEN', 'OPEN COM', 'OPTION BASE', 'OUT', 'PAINT',
                  'PALETTE', 'PCOPY', 'PEN', 'PLAY', 'POKE', 'PRESET', 'PRINT', 'PRINT #',
                  'PRINT USING', 'PSET', 'PUT', 'PUT', 'RANDOMIZE', 'READ', 'REDIM',
                  'REM', 'RESET', 'RESTORE', 'RESUME', 'RETURN', 'RMDIR', 'RSET',
                  'RUN', 'SCREEN', 'SEEK', 'SELECT CASE', 'SHARED', 'SHELL', 'SLEEP',
                  'SOUND', 'STATIC', 'STOP', 'STRIG', 'SUB', 'SWAP', 'SYSTEM', 'TIME$',
                  'TIMER', 'TROFF', 'TRON', 'TYPE', 'UEVENT', 'UNLOCK', 'VIEW', 'WAIT',
                  'WHILE', 'WEND', 'WIDTH', 'WINDOW', 'WRITE')
    keywords = ('ACCESS', 'ALIAS', 'ANY', 'APPEND', 'AS', 'BASE', 'BINARY', 'BYVAL',
                'CASE', 'CDECL', 'DOUBLE', 'ELSE', 'ELSEIF', 'ENDIF', 'INTEGER',
                'IS', 'LIST', 'LOCAL', 'LONG', 'LOOP', 'MOD', 'NEXT', 'OFF', 'ON',
                'OUTPUT', 'RANDOM', 'SIGNAL', 'SINGLE', 'STEP', 'STRING', 'THEN',
                'TO', 'UNTIL', 'USING', 'WEND')
    tokens = {'root': [
              (
               '\\n+', Text),
              (
               '\\s+', Text.Whitespace),
              (
               '^(\\s*)(\\d*)(\\s*)(REM .*)$',
               bygroups(Text.Whitespace, Name.Label, Text.Whitespace, Comment.Single)),
              (
               '^(\\s*)(\\d+)(\\s*)',
               bygroups(Text.Whitespace, Name.Label, Text.Whitespace)),
              (
               '(?=[\\s]*)(\\w+)(?=[\\s]*=)', Name.Variable.Global),
              (
               '(?=[^"]*)\\\'.*$', Comment.Single),
              (
               '"[^\\n"]*"', String.Double),
              (
               '(END)(\\s+)(FUNCTION|IF|SELECT|SUB)',
               bygroups(Keyword.Reserved, Text.Whitespace, Keyword.Reserved)),
              (
               '(DECLARE)(\\s+)([A-Z]+)(\\s+)(\\S+)',
               bygroups(Keyword.Declaration, Text.Whitespace, Name.Variable, Text.Whitespace, Name)),
              (
               '(DIM)(\\s+)(SHARED)(\\s+)([^\\s(]+)',
               bygroups(Keyword.Declaration, Text.Whitespace, Name.Variable, Text.Whitespace, Name.Variable.Global)),
              (
               '(DIM)(\\s+)([^\\s(]+)',
               bygroups(Keyword.Declaration, Text.Whitespace, Name.Variable.Global)),
              (
               '^(\\s*)([a-zA-Z_]+)(\\s*)(\\=)',
               bygroups(Text.Whitespace, Name.Variable.Global, Text.Whitespace, Operator)),
              (
               '(GOTO|GOSUB)(\\s+)(\\w+\\:?)',
               bygroups(Keyword.Reserved, Text.Whitespace, Name.Label)),
              (
               '(SUB)(\\s+)(\\w+\\:?)',
               bygroups(Keyword.Reserved, Text.Whitespace, Name.Label)),
              include('declarations'),
              include('functions'),
              include('metacommands'),
              include('operators'),
              include('statements'),
              include('keywords'),
              (
               '[a-zA-Z_]\\w*[$@#&!]', Name.Variable.Global),
              (
               '[a-zA-Z_]\\w*\\:', Name.Label),
              (
               '\\-?\\d*\\.\\d+[@|#]?', Number.Float),
              (
               '\\-?\\d+[@|#]', Number.Float),
              (
               '\\-?\\d+#?', Number.Integer.Long),
              (
               '\\-?\\d+#?', Number.Integer),
              (
               '!=|==|:=|\\.=|<<|>>|[-~+/\\\\*%=<>&^|?:!.]', Operator),
              (
               '[\\[\\]{}(),;]', Punctuation),
              (
               '[\\w]+', Name.Variable.Global)], 
     
     'declarations': [
                      (
                       '\\b(%s)(?=\\(|\\b)' % '|'.join(map(re.escape, declarations)),
                       Keyword.Declaration)], 
     
     'functions': [
                   (
                    '\\b(%s)(?=\\(|\\b)' % '|'.join(map(re.escape, functions)),
                    Keyword.Reserved)], 
     
     'metacommands': [
                      (
                       '\\b(%s)(?=\\(|\\b)' % '|'.join(map(re.escape, metacommands)),
                       Keyword.Constant)], 
     
     'operators': [
                   (
                    '\\b(%s)(?=\\(|\\b)' % '|'.join(map(re.escape, operators)), Operator.Word)], 
     
     'statements': [
                    (
                     '\\b(%s)\\b' % '|'.join(map(re.escape, statements)),
                     Keyword.Reserved)], 
     
     'keywords': [
                  (
                   '\\b(%s)\\b' % '|'.join(keywords), Keyword)]}

    def analyse_text(text):
        if '$DYNAMIC' in text or '$STATIC' in text:
            return 0.9