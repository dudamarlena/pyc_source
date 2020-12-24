# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/compiled.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.compiled
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for compiled languages.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.scanner import Scanner
from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, this, combined
from pygments.util import get_bool_opt, get_list_opt
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
from pygments.lexers.functional import OcamlLexer
__all__ = [
 'CLexer', 'CppLexer', 'DLexer', 'DelphiLexer', 'JavaLexer',
 'ScalaLexer', 'DylanLexer', 'OcamlLexer', 'ObjectiveCLexer',
 'FortranLexer', 'GLShaderLexer', 'PrologLexer', 'CythonLexer',
 'ValaLexer', 'OocLexer', 'GoLexer', 'FelixLexer', 'AdaLexer',
 'Modula2Lexer', 'BlitzMaxLexer']

class CLexer(RegexLexer):
    """
    For C source code with preprocessor directives.
    """
    name = 'C'
    aliases = ['c']
    filenames = ['*.c', '*.h']
    mimetypes = ['text/x-chdr', 'text/x-csrc']
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'whitespace': [
                    (
                     '^#if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '^#', Comment.Preproc, 'macro'),
                    (
                     '^' + _ws + '#if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '^' + _ws + '#', Comment.Preproc, 'macro'),
                    (
                     '^(\\s*)([a-zA-Z_][a-zA-Z0-9_]*:(?!:))', bygroups(Text, Name.Label)),
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     '\\\\\\n', Text),
                    (
                     '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
                    (
                     '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline)], 
       'statements': [
                    (
                     'L?"', String, 'string'),
                    (
                     "L?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[LlUu]*', Number.Float),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
                    (
                     '0x[0-9a-fA-F]+[LlUu]*', Number.Hex),
                    (
                     '0[0-7]+[LlUu]*', Number.Oct),
                    (
                     '\\d+[LlUu]*', Number.Integer),
                    (
                     '\\*/', Error),
                    (
                     '[~!%^&*+=|?:<>/-]', Operator),
                    (
                     '[()\\[\\],.]', Punctuation),
                    (
                     '\\b(case)(.+?)(:)', bygroups(Keyword, using(this), Text)),
                    (
                     '(auto|break|case|const|continue|default|do|else|enum|extern|for|goto|if|register|restricted|return|sizeof|static|struct|switch|typedef|union|volatile|virtual|while)\\b',
                     Keyword),
                    (
                     '(int|long|float|short|double|char|unsigned|signed|void)\\b',
                     Keyword.Type),
                    (
                     '(_{0,2}inline|naked|restrict|thread|typename)\\b', Keyword.Reserved),
                    (
                     '__(asm|int8|based|except|int16|stdcall|cdecl|fastcall|int32|declspec|finally|int64|try|leave)\\b',
                     Keyword.Reserved),
                    (
                     '(true|false|NULL)\\b', Name.Builtin),
                    (
                     '[a-zA-Z_][a-zA-Z0-9_]*', Name)], 
       'root': [
              include('whitespace'),
              (
               '((?:[a-zA-Z0-9_*\\s])+?(?:\\s|[*]))([a-zA-Z_][a-zA-Z0-9_]*)(\\s*\\([^;]*?\\))(' + _ws + ')({)',
               bygroups(using(this), Name.Function, using(this), using(this), Punctuation),
               'function'),
              (
               '((?:[a-zA-Z0-9_*\\s])+?(?:\\s|[*]))([a-zA-Z_][a-zA-Z0-9_]*)(\\s*\\([^;]*?\\))(' + _ws + ')(;)',
               bygroups(using(this), Name.Function, using(this), using(this), Punctuation)),
              (
               '', Text, 'statement')], 
       'statement': [
                   include('whitespace'),
                   include('statements'),
                   (
                    '[{}]', Punctuation),
                   (
                    ';', Punctuation, '#pop')], 
       'function': [
                  include('whitespace'),
                  include('statements'),
                  (
                   ';', Punctuation),
                  (
                   '{', Punctuation, '#push'),
                  (
                   '}', Punctuation, '#pop')], 
       'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                (
                 '[^\\\\"\\n]+', String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\', String)], 
       'macro': [
               (
                '[^/\\n]+', Comment.Preproc),
               (
                '/[*](.|\\n)*?[*]/', Comment.Multiline),
               (
                '//.*?\\n', Comment.Single, '#pop'),
               (
                '/', Comment.Preproc),
               (
                '(?<=\\\\)\\n', Comment.Preproc),
               (
                '\\n', Comment.Preproc, '#pop')], 
       'if0': [
             (
              '^\\s*#if.*?(?<!\\\\)\\n', Comment.Preproc, '#push'),
             (
              '^\\s*#el(?:se|if).*\\n', Comment.Preproc, '#pop'),
             (
              '^\\s*#endif.*?(?<!\\\\)\\n', Comment.Preproc, '#pop'),
             (
              '.*?\\n', Comment)]}
    stdlib_types = [
     'size_t', 'ssize_t', 'off_t', 'wchar_t', 'ptrdiff_t',
     'sig_atomic_t', 'fpos_t', 'clock_t', 'time_t', 'va_list',
     'jmp_buf', 'FILE', 'DIR', 'div_t', 'ldiv_t', 'mbstate_t',
     'wctrans_t', 'wint_t', 'wctype_t']
    c99_types = ['_Bool', '_Complex', 'int8_t', 'int16_t', 'int32_t', 'int64_t',
     'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t', 'int_least8_t',
     'int_least16_t', 'int_least32_t', 'int_least64_t',
     'uint_least8_t', 'uint_least16_t', 'uint_least32_t',
     'uint_least64_t', 'int_fast8_t', 'int_fast16_t', 'int_fast32_t',
     'int_fast64_t', 'uint_fast8_t', 'uint_fast16_t', 'uint_fast32_t',
     'uint_fast64_t', 'intptr_t', 'uintptr_t', 'intmax_t', 'uintmax_t']

    def __init__(self, **options):
        self.stdlibhighlighting = get_bool_opt(options, 'stdlibhighlighting', True)
        self.c99highlighting = get_bool_opt(options, 'c99highlighting', True)
        RegexLexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if self.stdlibhighlighting and value in self.stdlib_types:
                    token = Keyword.Type
                elif self.c99highlighting and value in self.c99_types:
                    token = Keyword.Type
            yield (
             index, token, value)


class CppLexer(RegexLexer):
    """
    For C++ source code with preprocessor directives.
    """
    name = 'C++'
    aliases = ['cpp', 'c++']
    filenames = ['*.cpp', '*.hpp', '*.c++', '*.h++', '*.cc', '*.hh', '*.cxx', '*.hxx']
    mimetypes = ['text/x-c++hdr', 'text/x-c++src']
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'root': [
              (
               '^#if\\s+0', Comment.Preproc, 'if0'),
              (
               '^#', Comment.Preproc, 'macro'),
              (
               '^' + _ws + '#if\\s+0', Comment.Preproc, 'if0'),
              (
               '^' + _ws + '#', Comment.Preproc, 'macro'),
              (
               '\\n', Text),
              (
               '\\s+', Text),
              (
               '\\\\\\n', Text),
              (
               '/(\\\\\\n)?/(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
              (
               '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
              (
               '[{}]', Punctuation),
              (
               'L?"', String, 'string'),
              (
               "L?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char),
              (
               '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[LlUu]*', Number.Float),
              (
               '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
              (
               '0x[0-9a-fA-F]+[LlUu]*', Number.Hex),
              (
               '0[0-7]+[LlUu]*', Number.Oct),
              (
               '\\d+[LlUu]*', Number.Integer),
              (
               '\\*/', Error),
              (
               '[~!%^&*+=|?:<>/-]', Operator),
              (
               '[()\\[\\],.;]', Punctuation),
              (
               '(asm|auto|break|case|catch|const|const_cast|continue|default|delete|do|dynamic_cast|else|enum|explicit|export|extern|for|friend|goto|if|mutable|namespace|new|operator|private|protected|public|register|reinterpret_cast|return|restrict|sizeof|static|static_cast|struct|switch|template|this|throw|throws|try|typedef|typeid|typename|union|using|volatile|virtual|while)\\b',
               Keyword),
              (
               '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
              (
               '(bool|int|long|float|short|double|char|unsigned|signed|void|wchar_t)\\b',
               Keyword.Type),
              (
               '(_{0,2}inline|naked|thread)\\b', Keyword.Reserved),
              (
               '__(asm|int8|based|except|int16|stdcall|cdecl|fastcall|int32|declspec|finally|int64|try|leave|wchar_t|w64|virtual_inheritance|uuidof|unaligned|super|single_inheritance|raise|noop|multiple_inheritance|m128i|m128d|m128|m64|interface|identifier|forceinline|event|assume)\\b',
               Keyword.Reserved),
              (
               '(__offload|__blockingoffload|__outer)\\b', Keyword.Psuedo),
              (
               '(true|false)\\b', Keyword.Constant),
              (
               'NULL\\b', Name.Builtin),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*:(?!:)', Name.Label),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Name)], 
       'classname': [
                   (
                    '[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop'),
                   (
                    '\\s*(?=>)', Text, '#pop')], 
       'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                (
                 '[^\\\\"\\n]+', String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\', String)], 
       'macro': [
               (
                '[^/\\n]+', Comment.Preproc),
               (
                '/[*](.|\\n)*?[*]/', Comment.Multiline),
               (
                '//.*?\\n', Comment.Single, '#pop'),
               (
                '/', Comment.Preproc),
               (
                '(?<=\\\\)\\n', Comment.Preproc),
               (
                '\\n', Comment.Preproc, '#pop')], 
       'if0': [
             (
              '^\\s*#if.*?(?<!\\\\)\\n', Comment.Preproc, '#push'),
             (
              '^\\s*#endif.*?(?<!\\\\)\\n', Comment.Preproc, '#pop'),
             (
              '.*?\\n', Comment)]}


class DLexer(RegexLexer):
    """
    For D source.

    *New in Pygments 1.2.*
    """
    name = 'D'
    filenames = ['*.d', '*.di']
    aliases = ['d']
    mimetypes = ['text/x-dsrc']
    tokens = {'root': [
              (
               '\\n', Text),
              (
               '\\s+', Text),
              (
               '//(.*?)\\n', Comment.Single),
              (
               '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
              (
               '/\\+', Comment.Multiline, 'nested_comment'),
              (
               '(abstract|alias|align|asm|assert|auto|body|break|case|cast|catch|class|const|continue|debug|default|delegate|delete|deprecated|do|else|enum|export|extern|finally|final|foreach_reverse|foreach|for|function|goto|if|import|inout|interface|invariant|in|is|lazy|mixin|module|new|nothrow|out|override|package|pragma|private|protected|public|pure|ref|return|scope|static|struct|super|switch|synchronized|template|this|throw|try|typedef|typeid|typeof|union|unittest|version|volatile|while|with|__traits)\\b',
               Keyword),
              (
               '(bool|byte|cdouble|cent|cfloat|char|creal|dchar|double|float|idouble|ifloat|int|ireal|long|real|short|ubyte|ucent|uint|ulong|ushort|void|wchar)\\b',
               Keyword.Type),
              (
               '(false|true|null)\\b', Keyword.Constant),
              (
               'macro\\b', Keyword.Reserved),
              (
               '(string|wstring|dstring)\\b', Name.Builtin),
              (
               '0[xX]([0-9a-fA-F_]*\\.[0-9a-fA-F_]+|[0-9a-fA-F_]+)[pP][+\\-]?[0-9_]+[fFL]?[i]?',
               Number.Float),
              (
               '[0-9_]+(\\.[0-9_]+[eE][+\\-]?[0-9_]+|\\.[0-9_]*|[eE][+\\-]?[0-9_]+)[fFL]?[i]?',
               Number.Float),
              (
               '\\.(0|[1-9][0-9_]*)([eE][+\\-]?[0-9_]+)?[fFL]?[i]?', Number.Float),
              (
               '0[Bb][01_]+', Number),
              (
               '0[0-7_]+', Number.Oct),
              (
               '0[xX][0-9a-fA-F_]+', Number.Hex),
              (
               '(0|[1-9][0-9_]*)([LUu]|Lu|LU|uL|UL)?', Number.Integer),
              (
               '\'(\\\\[\'"?\\\\abfnrtv]|\\\\x[0-9a-fA-F]{2}|\\\\[0-7]{1,3}|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|\\\\&\\w+;|.)\'',
               String.Char),
              (
               'r"[^"]*"[cwd]?', String),
              (
               '`[^`]*`[cwd]?', String),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"[cwd]?', String),
              (
               '\\\\([\'\\"?\\\\abfnrtv]|x[0-9a-fA-F]{2}|[0-7]{1,3}|u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|&\\w+;)',
               String),
              (
               'x"[0-9a-fA-F_\\s]*"[cwd]?', String),
              (
               'q"\\[', String, 'delimited_bracket'),
              (
               'q"\\(', String, 'delimited_parenthesis'),
              (
               'q"<', String, 'delimited_angle'),
              (
               'q"{', String, 'delimited_curly'),
              (
               'q"([a-zA-Z_]\\w*)\\n.*?\\n\\1"', String),
              (
               'q"(.).*?\\1"', String),
              (
               'q{', String, 'token_string'),
              (
               '(~=|\\^=|%=|\\*=|==|!>=|!<=|!<>=|!<>|!<|!>|!=|>>>=|>>>|>>=|>>|>=|<>=|<>|<<=|<<|<=|\\+\\+|\\+=|--|-=|\\|\\||\\|=|&&|&=|\\.\\.\\.|\\.\\.|/=)|[/.&|\\-+<>!()\\[\\]{}?,;:$=*%^~]',
               Punctuation),
              (
               '[a-zA-Z_]\\w*', Name)], 
       'nested_comment': [
                        (
                         '[^+/]+', Comment.Multiline),
                        (
                         '/\\+', Comment.Multiline, '#push'),
                        (
                         '\\+/', Comment.Multiline, '#pop'),
                        (
                         '[+/]', Comment.Multiline)], 
       'token_string': [
                      (
                       '{', Punctuation, 'token_string_nest'),
                      (
                       '}', String, '#pop'),
                      include('root')], 
       'token_string_nest': [
                           (
                            '{', Punctuation, '#push'),
                           (
                            '}', Punctuation, '#pop'),
                           include('root')], 
       'delimited_bracket': [
                           (
                            '[^\\[\\]]+', String),
                           (
                            '\\[', String, 'delimited_inside_bracket'),
                           (
                            '\\]"', String, '#pop')], 
       'delimited_inside_bracket': [
                                  (
                                   '[^\\[\\]]+', String),
                                  (
                                   '\\[', String, '#push'),
                                  (
                                   '\\]', String, '#pop')], 
       'delimited_parenthesis': [
                               (
                                '[^\\(\\)]+', String),
                               (
                                '\\(', String, 'delimited_inside_parenthesis'),
                               (
                                '\\)"', String, '#pop')], 
       'delimited_inside_parenthesis': [
                                      (
                                       '[^\\(\\)]+', String),
                                      (
                                       '\\(', String, '#push'),
                                      (
                                       '\\)', String, '#pop')], 
       'delimited_angle': [
                         (
                          '[^<>]+', String),
                         (
                          '<', String, 'delimited_inside_angle'),
                         (
                          '>"', String, '#pop')], 
       'delimited_inside_angle': [
                                (
                                 '[^<>]+', String),
                                (
                                 '<', String, '#push'),
                                (
                                 '>', String, '#pop')], 
       'delimited_curly': [
                         (
                          '[^{}]+', String),
                         (
                          '{', String, 'delimited_inside_curly'),
                         (
                          '}"', String, '#pop')], 
       'delimited_inside_curly': [
                                (
                                 '[^{}]+', String),
                                (
                                 '{', String, '#push'),
                                (
                                 '}', String, '#pop')]}


class DelphiLexer(Lexer):
    """
    For `Delphi <http://www.borland.com/delphi/>`_ (Borland Object Pascal),
    Turbo Pascal and Free Pascal source code.

    Additional options accepted:

    `turbopascal`
        Highlight Turbo Pascal specific keywords (default: ``True``).
    `delphi`
        Highlight Borland Delphi specific keywords (default: ``True``).
    `freepascal`
        Highlight Free Pascal specific keywords (default: ``True``).
    `units`
        A list of units that should be considered builtin, supported are
        ``System``, ``SysUtils``, ``Classes`` and ``Math``.
        Default is to consider all of them builtin.
    """
    name = 'Delphi'
    aliases = ['delphi', 'pas', 'pascal', 'objectpascal']
    filenames = ['*.pas']
    mimetypes = ['text/x-pascal']
    TURBO_PASCAL_KEYWORDS = [
     'absolute', 'and', 'array', 'asm', 'begin', 'break', 'case',
     'const', 'constructor', 'continue', 'destructor', 'div', 'do',
     'downto', 'else', 'end', 'file', 'for', 'function', 'goto',
     'if', 'implementation', 'in', 'inherited', 'inline', 'interface',
     'label', 'mod', 'nil', 'not', 'object', 'of', 'on', 'operator',
     'or', 'packed', 'procedure', 'program', 'record', 'reintroduce',
     'repeat', 'self', 'set', 'shl', 'shr', 'string', 'then', 'to',
     'type', 'unit', 'until', 'uses', 'var', 'while', 'with', 'xor']
    DELPHI_KEYWORDS = [
     'as', 'class', 'except', 'exports', 'finalization', 'finally',
     'initialization', 'is', 'library', 'on', 'property', 'raise',
     'threadvar', 'try']
    FREE_PASCAL_KEYWORDS = [
     'dispose', 'exit', 'false', 'new', 'true']
    BLOCK_KEYWORDS = set([
     'begin', 'class', 'const', 'constructor', 'destructor', 'end',
     'finalization', 'function', 'implementation', 'initialization',
     'label', 'library', 'operator', 'procedure', 'program', 'property',
     'record', 'threadvar', 'type', 'unit', 'uses', 'var'])
    FUNCTION_MODIFIERS = set([
     'alias', 'cdecl', 'export', 'inline', 'interrupt', 'nostackframe',
     'pascal', 'register', 'safecall', 'softfloat', 'stdcall',
     'varargs', 'name', 'dynamic', 'near', 'virtual', 'external',
     'override', 'assembler'])
    DIRECTIVES = set([
     'absolute', 'abstract', 'assembler', 'cppdecl', 'default', 'far',
     'far16', 'forward', 'index', 'oldfpccall', 'private', 'protected',
     'published', 'public'])
    BUILTIN_TYPES = set([
     'ansichar', 'ansistring', 'bool', 'boolean', 'byte', 'bytebool',
     'cardinal', 'char', 'comp', 'currency', 'double', 'dword',
     'extended', 'int64', 'integer', 'iunknown', 'longbool', 'longint',
     'longword', 'pansichar', 'pansistring', 'pbool', 'pboolean',
     'pbyte', 'pbytearray', 'pcardinal', 'pchar', 'pcomp', 'pcurrency',
     'pdate', 'pdatetime', 'pdouble', 'pdword', 'pextended', 'phandle',
     'pint64', 'pinteger', 'plongint', 'plongword', 'pointer',
     'ppointer', 'pshortint', 'pshortstring', 'psingle', 'psmallint',
     'pstring', 'pvariant', 'pwidechar', 'pwidestring', 'pword',
     'pwordarray', 'pwordbool', 'real', 'real48', 'shortint',
     'shortstring', 'single', 'smallint', 'string', 'tclass', 'tdate',
     'tdatetime', 'textfile', 'thandle', 'tobject', 'ttime', 'variant',
     'widechar', 'widestring', 'word', 'wordbool'])
    BUILTIN_UNITS = {'System': [
                'abs', 'acquireexceptionobject', 'addr', 'ansitoutf8',
                'append', 'arctan', 'assert', 'assigned', 'assignfile',
                'beginthread', 'blockread', 'blockwrite', 'break', 'chdir',
                'chr', 'close', 'closefile', 'comptocurrency', 'comptodouble',
                'concat', 'continue', 'copy', 'cos', 'dec', 'delete',
                'dispose', 'doubletocomp', 'endthread', 'enummodules',
                'enumresourcemodules', 'eof', 'eoln', 'erase', 'exceptaddr',
                'exceptobject', 'exclude', 'exit', 'exp', 'filepos', 'filesize',
                'fillchar', 'finalize', 'findclasshinstance', 'findhinstance',
                'findresourcehinstance', 'flush', 'frac', 'freemem',
                'get8087cw', 'getdir', 'getlasterror', 'getmem',
                'getmemorymanager', 'getmodulefilename', 'getvariantmanager',
                'halt', 'hi', 'high', 'inc', 'include', 'initialize', 'insert',
                'int', 'ioresult', 'ismemorymanagerset', 'isvariantmanagerset',
                'length', 'ln', 'lo', 'low', 'mkdir', 'move', 'new', 'odd',
                'olestrtostring', 'olestrtostrvar', 'ord', 'paramcount',
                'paramstr', 'pi', 'pos', 'pred', 'ptr', 'pucs4chars', 'random',
                'randomize', 'read', 'readln', 'reallocmem',
                'releaseexceptionobject', 'rename', 'reset', 'rewrite', 'rmdir',
                'round', 'runerror', 'seek', 'seekeof', 'seekeoln',
                'set8087cw', 'setlength', 'setlinebreakstyle',
                'setmemorymanager', 'setstring', 'settextbuf',
                'setvariantmanager', 'sin', 'sizeof', 'slice', 'sqr', 'sqrt',
                'str', 'stringofchar', 'stringtoolestr', 'stringtowidechar',
                'succ', 'swap', 'trunc', 'truncate', 'typeinfo',
                'ucs4stringtowidestring', 'unicodetoutf8', 'uniquestring',
                'upcase', 'utf8decode', 'utf8encode', 'utf8toansi',
                'utf8tounicode', 'val', 'vararrayredim', 'varclear',
                'widecharlentostring', 'widecharlentostrvar',
                'widechartostring', 'widechartostrvar',
                'widestringtoucs4string', 'write', 'writeln'], 
       'SysUtils': [
                  'abort', 'addexitproc', 'addterminateproc', 'adjustlinebreaks',
                  'allocmem', 'ansicomparefilename', 'ansicomparestr',
                  'ansicomparetext', 'ansidequotedstr', 'ansiextractquotedstr',
                  'ansilastchar', 'ansilowercase', 'ansilowercasefilename',
                  'ansipos', 'ansiquotedstr', 'ansisamestr', 'ansisametext',
                  'ansistrcomp', 'ansistricomp', 'ansistrlastchar', 'ansistrlcomp',
                  'ansistrlicomp', 'ansistrlower', 'ansistrpos', 'ansistrrscan',
                  'ansistrscan', 'ansistrupper', 'ansiuppercase',
                  'ansiuppercasefilename', 'appendstr', 'assignstr', 'beep',
                  'booltostr', 'bytetocharindex', 'bytetocharlen', 'bytetype',
                  'callterminateprocs', 'changefileext', 'charlength',
                  'chartobyteindex', 'chartobytelen', 'comparemem', 'comparestr',
                  'comparetext', 'createdir', 'createguid', 'currentyear',
                  'currtostr', 'currtostrf', 'date', 'datetimetofiledate',
                  'datetimetostr', 'datetimetostring', 'datetimetosystemtime',
                  'datetimetotimestamp', 'datetostr', 'dayofweek', 'decodedate',
                  'decodedatefully', 'decodetime', 'deletefile', 'directoryexists',
                  'diskfree', 'disksize', 'disposestr', 'encodedate', 'encodetime',
                  'exceptionerrormessage', 'excludetrailingbackslash',
                  'excludetrailingpathdelimiter', 'expandfilename',
                  'expandfilenamecase', 'expanduncfilename', 'extractfiledir',
                  'extractfiledrive', 'extractfileext', 'extractfilename',
                  'extractfilepath', 'extractrelativepath', 'extractshortpathname',
                  'fileage', 'fileclose', 'filecreate', 'filedatetodatetime',
                  'fileexists', 'filegetattr', 'filegetdate', 'fileisreadonly',
                  'fileopen', 'fileread', 'filesearch', 'fileseek', 'filesetattr',
                  'filesetdate', 'filesetreadonly', 'filewrite', 'finalizepackage',
                  'findclose', 'findcmdlineswitch', 'findfirst', 'findnext',
                  'floattocurr', 'floattodatetime', 'floattodecimal', 'floattostr',
                  'floattostrf', 'floattotext', 'floattotextfmt', 'fmtloadstr',
                  'fmtstr', 'forcedirectories', 'format', 'formatbuf', 'formatcurr',
                  'formatdatetime', 'formatfloat', 'freeandnil', 'getcurrentdir',
                  'getenvironmentvariable', 'getfileversion', 'getformatsettings',
                  'getlocaleformatsettings', 'getmodulename', 'getpackagedescription',
                  'getpackageinfo', 'gettime', 'guidtostring', 'incamonth',
                  'includetrailingbackslash', 'includetrailingpathdelimiter',
                  'incmonth', 'initializepackage', 'interlockeddecrement',
                  'interlockedexchange', 'interlockedexchangeadd',
                  'interlockedincrement', 'inttohex', 'inttostr', 'isdelimiter',
                  'isequalguid', 'isleapyear', 'ispathdelimiter', 'isvalidident',
                  'languages', 'lastdelimiter', 'loadpackage', 'loadstr',
                  'lowercase', 'msecstotimestamp', 'newstr', 'nextcharindex', 'now',
                  'outofmemoryerror', 'quotedstr', 'raiselastoserror',
                  'raiselastwin32error', 'removedir', 'renamefile', 'replacedate',
                  'replacetime', 'safeloadlibrary', 'samefilename', 'sametext',
                  'setcurrentdir', 'showexception', 'sleep', 'stralloc', 'strbufsize',
                  'strbytetype', 'strcat', 'strcharlength', 'strcomp', 'strcopy',
                  'strdispose', 'strecopy', 'strend', 'strfmt', 'stricomp',
                  'stringreplace', 'stringtoguid', 'strlcat', 'strlcomp', 'strlcopy',
                  'strlen', 'strlfmt', 'strlicomp', 'strlower', 'strmove', 'strnew',
                  'strnextchar', 'strpas', 'strpcopy', 'strplcopy', 'strpos',
                  'strrscan', 'strscan', 'strtobool', 'strtobooldef', 'strtocurr',
                  'strtocurrdef', 'strtodate', 'strtodatedef', 'strtodatetime',
                  'strtodatetimedef', 'strtofloat', 'strtofloatdef', 'strtoint',
                  'strtoint64', 'strtoint64def', 'strtointdef', 'strtotime',
                  'strtotimedef', 'strupper', 'supports', 'syserrormessage',
                  'systemtimetodatetime', 'texttofloat', 'time', 'timestamptodatetime',
                  'timestamptomsecs', 'timetostr', 'trim', 'trimleft', 'trimright',
                  'tryencodedate', 'tryencodetime', 'tryfloattocurr', 'tryfloattodatetime',
                  'trystrtobool', 'trystrtocurr', 'trystrtodate', 'trystrtodatetime',
                  'trystrtofloat', 'trystrtoint', 'trystrtoint64', 'trystrtotime',
                  'unloadpackage', 'uppercase', 'widecomparestr', 'widecomparetext',
                  'widefmtstr', 'wideformat', 'wideformatbuf', 'widelowercase',
                  'widesamestr', 'widesametext', 'wideuppercase', 'win32check',
                  'wraptext'], 
       'Classes': [
                 'activateclassgroup', 'allocatehwnd', 'bintohex', 'checksynchronize',
                 'collectionsequal', 'countgenerations', 'deallocatehwnd', 'equalrect',
                 'extractstrings', 'findclass', 'findglobalcomponent', 'getclass',
                 'groupdescendantswith', 'hextobin', 'identtoint',
                 'initinheritedcomponent', 'inttoident', 'invalidpoint',
                 'isuniqueglobalcomponentname', 'linestart', 'objectbinarytotext',
                 'objectresourcetotext', 'objecttexttobinary', 'objecttexttoresource',
                 'pointsequal', 'readcomponentres', 'readcomponentresex',
                 'readcomponentresfile', 'rect', 'registerclass', 'registerclassalias',
                 'registerclasses', 'registercomponents', 'registerintegerconsts',
                 'registernoicon', 'registernonactivex', 'smallpoint', 'startclassgroup',
                 'teststreamformat', 'unregisterclass', 'unregisterclasses',
                 'unregisterintegerconsts', 'unregistermoduleclasses',
                 'writecomponentresfile'], 
       'Math': [
              'arccos', 'arccosh', 'arccot', 'arccoth', 'arccsc', 'arccsch', 'arcsec',
              'arcsech', 'arcsin', 'arcsinh', 'arctan2', 'arctanh', 'ceil',
              'comparevalue', 'cosecant', 'cosh', 'cot', 'cotan', 'coth', 'csc',
              'csch', 'cycletodeg', 'cycletograd', 'cycletorad', 'degtocycle',
              'degtograd', 'degtorad', 'divmod', 'doubledecliningbalance',
              'ensurerange', 'floor', 'frexp', 'futurevalue', 'getexceptionmask',
              'getprecisionmode', 'getroundmode', 'gradtocycle', 'gradtodeg',
              'gradtorad', 'hypot', 'inrange', 'interestpayment', 'interestrate',
              'internalrateofreturn', 'intpower', 'isinfinite', 'isnan', 'iszero',
              'ldexp', 'lnxp1', 'log10', 'log2', 'logn', 'max', 'maxintvalue',
              'maxvalue', 'mean', 'meanandstddev', 'min', 'minintvalue', 'minvalue',
              'momentskewkurtosis', 'netpresentvalue', 'norm', 'numberofperiods',
              'payment', 'periodpayment', 'poly', 'popnstddev', 'popnvariance',
              'power', 'presentvalue', 'radtocycle', 'radtodeg', 'radtograd',
              'randg', 'randomrange', 'roundto', 'samevalue', 'sec', 'secant',
              'sech', 'setexceptionmask', 'setprecisionmode', 'setroundmode',
              'sign', 'simpleroundto', 'sincos', 'sinh', 'slndepreciation', 'stddev',
              'sum', 'sumint', 'sumofsquares', 'sumsandsquares', 'syddepreciation',
              'tan', 'tanh', 'totalvariance', 'variance']}
    ASM_REGISTERS = set([
     'ah', 'al', 'ax', 'bh', 'bl', 'bp', 'bx', 'ch', 'cl', 'cr0',
     'cr1', 'cr2', 'cr3', 'cr4', 'cs', 'cx', 'dh', 'di', 'dl', 'dr0',
     'dr1', 'dr2', 'dr3', 'dr4', 'dr5', 'dr6', 'dr7', 'ds', 'dx',
     'eax', 'ebp', 'ebx', 'ecx', 'edi', 'edx', 'es', 'esi', 'esp',
     'fs', 'gs', 'mm0', 'mm1', 'mm2', 'mm3', 'mm4', 'mm5', 'mm6',
     'mm7', 'si', 'sp', 'ss', 'st0', 'st1', 'st2', 'st3', 'st4', 'st5',
     'st6', 'st7', 'xmm0', 'xmm1', 'xmm2', 'xmm3', 'xmm4', 'xmm5',
     'xmm6', 'xmm7'])
    ASM_INSTRUCTIONS = set([
     'aaa', 'aad', 'aam', 'aas', 'adc', 'add', 'and', 'arpl', 'bound',
     'bsf', 'bsr', 'bswap', 'bt', 'btc', 'btr', 'bts', 'call', 'cbw',
     'cdq', 'clc', 'cld', 'cli', 'clts', 'cmc', 'cmova', 'cmovae',
     'cmovb', 'cmovbe', 'cmovc', 'cmovcxz', 'cmove', 'cmovg',
     'cmovge', 'cmovl', 'cmovle', 'cmovna', 'cmovnae', 'cmovnb',
     'cmovnbe', 'cmovnc', 'cmovne', 'cmovng', 'cmovnge', 'cmovnl',
     'cmovnle', 'cmovno', 'cmovnp', 'cmovns', 'cmovnz', 'cmovo',
     'cmovp', 'cmovpe', 'cmovpo', 'cmovs', 'cmovz', 'cmp', 'cmpsb',
     'cmpsd', 'cmpsw', 'cmpxchg', 'cmpxchg486', 'cmpxchg8b', 'cpuid',
     'cwd', 'cwde', 'daa', 'das', 'dec', 'div', 'emms', 'enter', 'hlt',
     'ibts', 'icebp', 'idiv', 'imul', 'in', 'inc', 'insb', 'insd',
     'insw', 'int', 'int01', 'int03', 'int1', 'int3', 'into', 'invd',
     'invlpg', 'iret', 'iretd', 'iretw', 'ja', 'jae', 'jb', 'jbe',
     'jc', 'jcxz', 'jcxz', 'je', 'jecxz', 'jg', 'jge', 'jl', 'jle',
     'jmp', 'jna', 'jnae', 'jnb', 'jnbe', 'jnc', 'jne', 'jng', 'jnge',
     'jnl', 'jnle', 'jno', 'jnp', 'jns', 'jnz', 'jo', 'jp', 'jpe',
     'jpo', 'js', 'jz', 'lahf', 'lar', 'lcall', 'lds', 'lea', 'leave',
     'les', 'lfs', 'lgdt', 'lgs', 'lidt', 'ljmp', 'lldt', 'lmsw',
     'loadall', 'loadall286', 'lock', 'lodsb', 'lodsd', 'lodsw',
     'loop', 'loope', 'loopne', 'loopnz', 'loopz', 'lsl', 'lss', 'ltr',
     'mov', 'movd', 'movq', 'movsb', 'movsd', 'movsw', 'movsx',
     'movzx', 'mul', 'neg', 'nop', 'not', 'or', 'out', 'outsb', 'outsd',
     'outsw', 'pop', 'popa', 'popad', 'popaw', 'popf', 'popfd', 'popfw',
     'push', 'pusha', 'pushad', 'pushaw', 'pushf', 'pushfd', 'pushfw',
     'rcl', 'rcr', 'rdmsr', 'rdpmc', 'rdshr', 'rdtsc', 'rep', 'repe',
     'repne', 'repnz', 'repz', 'ret', 'retf', 'retn', 'rol', 'ror',
     'rsdc', 'rsldt', 'rsm', 'sahf', 'sal', 'salc', 'sar', 'sbb',
     'scasb', 'scasd', 'scasw', 'seta', 'setae', 'setb', 'setbe',
     'setc', 'setcxz', 'sete', 'setg', 'setge', 'setl', 'setle',
     'setna', 'setnae', 'setnb', 'setnbe', 'setnc', 'setne', 'setng',
     'setnge', 'setnl', 'setnle', 'setno', 'setnp', 'setns', 'setnz',
     'seto', 'setp', 'setpe', 'setpo', 'sets', 'setz', 'sgdt', 'shl',
     'shld', 'shr', 'shrd', 'sidt', 'sldt', 'smi', 'smint', 'smintold',
     'smsw', 'stc', 'std', 'sti', 'stosb', 'stosd', 'stosw', 'str',
     'sub', 'svdc', 'svldt', 'svts', 'syscall', 'sysenter', 'sysexit',
     'sysret', 'test', 'ud1', 'ud2', 'umov', 'verr', 'verw', 'wait',
     'wbinvd', 'wrmsr', 'wrshr', 'xadd', 'xbts', 'xchg', 'xlat',
     'xlatb', 'xor'])

    def __init__(self, **options):
        Lexer.__init__(self, **options)
        self.keywords = set()
        if get_bool_opt(options, 'turbopascal', True):
            self.keywords.update(self.TURBO_PASCAL_KEYWORDS)
        if get_bool_opt(options, 'delphi', True):
            self.keywords.update(self.DELPHI_KEYWORDS)
        if get_bool_opt(options, 'freepascal', True):
            self.keywords.update(self.FREE_PASCAL_KEYWORDS)
        self.builtins = set()
        for unit in get_list_opt(options, 'units', self.BUILTIN_UNITS.keys()):
            self.builtins.update(self.BUILTIN_UNITS[unit])

    def get_tokens_unprocessed(self, text):
        scanner = Scanner(text, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        stack = ['initial']
        in_function_block = False
        in_property_block = False
        was_dot = False
        next_token_is_function = False
        next_token_is_property = False
        collect_labels = False
        block_labels = set()
        brace_balance = [0, 0]
        while not scanner.eos:
            token = Error
            if stack[(-1)] == 'initial':
                if scanner.scan('\\s+'):
                    token = Text
                elif scanner.scan('\\{.*?\\}|\\(\\*.*?\\*\\)'):
                    if scanner.match.startswith('$'):
                        token = Comment.Preproc
                    else:
                        token = Comment.Multiline
                elif scanner.scan('//.*?$'):
                    token = Comment.Single
                elif scanner.scan('[-+*\\/=<>:;,.@\\^]'):
                    token = Operator
                    if collect_labels and scanner.match == ';':
                        collect_labels = False
                elif scanner.scan('[\\(\\)\\[\\]]+'):
                    token = Punctuation
                    next_token_is_function = False
                    if in_function_block or in_property_block:
                        if scanner.match == '(':
                            brace_balance[0] += 1
                        elif scanner.match == ')':
                            brace_balance[0] -= 1
                        elif scanner.match == '[':
                            brace_balance[1] += 1
                        elif scanner.match == ']':
                            brace_balance[1] -= 1
                elif scanner.scan('[A-Za-z_][A-Za-z_0-9]*'):
                    lowercase_name = scanner.match.lower()
                    if lowercase_name == 'result':
                        token = Name.Builtin.Pseudo
                    elif lowercase_name in self.keywords:
                        token = Keyword
                        if (in_function_block or in_property_block) and lowercase_name in self.BLOCK_KEYWORDS and brace_balance[0] <= 0 and brace_balance[1] <= 0:
                            in_function_block = False
                            in_property_block = False
                            brace_balance = [0, 0]
                            block_labels = set()
                        if lowercase_name in ('label', 'goto'):
                            collect_labels = True
                        elif lowercase_name == 'asm':
                            stack.append('asm')
                        elif lowercase_name == 'property':
                            in_property_block = True
                            next_token_is_property = True
                        elif lowercase_name in ('procedure', 'operator', 'function',
                                                'constructor', 'destructor'):
                            in_function_block = True
                            next_token_is_function = True
                    elif in_function_block and lowercase_name in self.FUNCTION_MODIFIERS:
                        token = Keyword.Pseudo
                    elif in_property_block and lowercase_name in ('read', 'write'):
                        token = Keyword.Pseudo
                        next_token_is_function = True
                    elif next_token_is_function:
                        if scanner.test('\\s*\\.\\s*'):
                            token = Name.Class
                        else:
                            token = Name.Function
                            next_token_is_function = False
                    elif next_token_is_property:
                        token = Name.Property
                        next_token_is_property = False
                    elif collect_labels:
                        token = Name.Label
                        block_labels.add(scanner.match.lower())
                    elif lowercase_name in block_labels:
                        token = Name.Label
                    elif lowercase_name in self.BUILTIN_TYPES:
                        token = Keyword.Type
                    elif lowercase_name in self.DIRECTIVES:
                        token = Keyword.Pseudo
                    elif not was_dot and lowercase_name in self.builtins:
                        token = Name.Builtin
                    else:
                        token = Name
                elif scanner.scan("'"):
                    token = String
                    stack.append('string')
                elif scanner.scan('\\#(\\d+|\\$[0-9A-Fa-f]+)'):
                    token = String.Char
                elif scanner.scan('\\$[0-9A-Fa-f]+'):
                    token = Number.Hex
                elif scanner.scan('\\d+(?![eE]|\\.[^.])'):
                    token = Number.Integer
                elif scanner.scan('\\d+(\\.\\d+([eE][+-]?\\d+)?|[eE][+-]?\\d+)'):
                    token = Number.Float
                else:
                    if len(stack) > 1:
                        stack.pop()
                    scanner.get_char()
            elif stack[(-1)] == 'string':
                if scanner.scan("''"):
                    token = String.Escape
                elif scanner.scan("'"):
                    token = String
                    stack.pop()
                elif scanner.scan("[^']*"):
                    token = String
                else:
                    scanner.get_char()
                    stack.pop()
            elif stack[(-1)] == 'asm':
                if scanner.scan('\\s+'):
                    token = Text
                elif scanner.scan('end'):
                    token = Keyword
                    stack.pop()
                elif scanner.scan('\\{.*?\\}|\\(\\*.*?\\*\\)'):
                    if scanner.match.startswith('$'):
                        token = Comment.Preproc
                    else:
                        token = Comment.Multiline
                elif scanner.scan('//.*?$'):
                    token = Comment.Single
                elif scanner.scan("'"):
                    token = String
                    stack.append('string')
                elif scanner.scan('@@[A-Za-z_][A-Za-z_0-9]*'):
                    token = Name.Label
                elif scanner.scan('[A-Za-z_][A-Za-z_0-9]*'):
                    lowercase_name = scanner.match.lower()
                    if lowercase_name in self.ASM_INSTRUCTIONS:
                        token = Keyword
                    elif lowercase_name in self.ASM_REGISTERS:
                        token = Name.Builtin
                    else:
                        token = Name
                elif scanner.scan('[-+*\\/=<>:;,.@\\^]+'):
                    token = Operator
                elif scanner.scan('[\\(\\)\\[\\]]+'):
                    token = Punctuation
                elif scanner.scan('\\$[0-9A-Fa-f]+'):
                    token = Number.Hex
                elif scanner.scan('\\d+(?![eE]|\\.[^.])'):
                    token = Number.Integer
                elif scanner.scan('\\d+(\\.\\d+([eE][+-]?\\d+)?|[eE][+-]?\\d+)'):
                    token = Number.Float
                else:
                    scanner.get_char()
                    stack.pop()
            if scanner.match.strip():
                was_dot = scanner.match == '.'
            yield (
             scanner.start_pos, token, scanner.match or '')


class JavaLexer(RegexLexer):
    """
    For `Java <http://www.sun.com/java/>`_ source code.
    """
    name = 'Java'
    aliases = ['java']
    filenames = ['*.java']
    mimetypes = ['text/x-java']
    flags = re.MULTILINE | re.DOTALL
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'root': [
              (
               '^(\\s*(?:[a-zA-Z_][a-zA-Z0-9_\\.\\[\\]]*\\s+)+?)([a-zA-Z_][a-zA-Z0-9_]*)(\\s*)(\\()',
               bygroups(using(this), Name.Function, Text, Operator)),
              (
               '[^\\S\\n]+', Text),
              (
               '//.*?\\n', Comment.Single),
              (
               '/\\*.*?\\*/', Comment.Multiline),
              (
               '@[a-zA-Z_][a-zA-Z0-9_\\.]*', Name.Decorator),
              (
               '(assert|break|case|catch|continue|default|do|else|finally|for|if|goto|instanceof|new|return|switch|this|throw|try|while)\\b',
               Keyword),
              (
               '(abstract|const|enum|extends|final|implements|native|private|protected|public|static|strictfp|super|synchronized|throws|transient|volatile)\\b',
               Keyword.Declaration),
              (
               '(boolean|byte|char|double|float|int|long|short|void)\\b',
               Keyword.Type),
              (
               '(package)(\\s+)', bygroups(Keyword.Namespace, Text)),
              (
               '(true|false|null)\\b', Keyword.Constant),
              (
               '(class|interface)(\\s+)', bygroups(Keyword.Declaration, Text), 'class'),
              (
               '(import)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               "'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-f]{4}'", String.Char),
              (
               '(\\.)([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Operator, Name.Attribute)),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*:', Name.Label),
              (
               '[a-zA-Z_\\$][a-zA-Z0-9_]*', Name),
              (
               '[~\\^\\*!%&\\[\\]\\(\\)\\{\\}<>\\|+=:;,./?-]', Operator),
              (
               '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
              (
               '0x[0-9a-f]+', Number.Hex),
              (
               '[0-9]+L?', Number.Integer),
              (
               '\\n', Text)], 
       'class': [
               (
                '[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop')], 
       'import': [
                (
                 '[a-zA-Z0-9_.]+\\*?', Name.Namespace, '#pop')]}


class ScalaLexer(RegexLexer):
    """
    For `Scala <http://www.scala-lang.org>`_ source code.
    """
    name = 'Scala'
    aliases = ['scala']
    filenames = ['*.scala']
    mimetypes = ['text/x-scala']
    flags = re.MULTILINE | re.DOTALL
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    op = '[-~\\^\\*!%&\\\\<>\\|+=:/?@¦-§©¬®°-±¶×÷϶҂؆-؈؎-؏۩۽-۾߶৺୰௳-௸௺౿ೱ-ೲ൹༁-༃༓-༗༚-༟༴༶༸྾-࿅࿇-࿏႞-႟፠᎐-᎙᥀᧠-᧿᭡-᭪᭴-᭼⁄⁒⁺-⁼₊-₌℀-℁℃-℆℈-℉℔№-℘℞-℣℥℧℩℮℺-℻⅀-⅄⅊-⅍⅏←-⌨⌫-⑊⒜-ⓩ─-❧➔-⟄⟇-⟥⟰-⦂⦙-⧗⧜-⧻⧾-⭔⳥-⳪⺀-⿻〄〒-〓〠〶-〷〾-〿㆐-㆑㆖-㆟㇀-㇣㈀-㈞㈪-㉐㉠-㉿㊊-㊰㋀-㏿䷀-䷿꒐-꓆꠨-꠫﬩﷽﹢﹤-﹦＋＜-＞｜～￢￤￨-￮￼-�]+'
    letter = '[a-zA-Z\\$_ªµºÀ-ÖØ-öø-ʯͰ-ͳͶ-ͷͻ-ͽΆΈ-ϵϷ-ҁҊ-Ֆա-ևא-ײء-ؿف-يٮ-ٯٱ-ۓەۮ-ۯۺ-ۼۿܐܒ-ܯݍ-ޥޱߊ-ߪऄ-हऽॐक़-ॡॲ-ॿঅ-হঽৎড়-ৡৰ-ৱਅ-ਹਖ਼-ਫ਼ੲ-ੴઅ-હઽૐ-ૡଅ-ହଽଡ଼-ୡୱஃ-ஹௐఅ-ఽౘ-ౡಅ-ಹಽೞ-ೡഅ-ഽൠ-ൡൺ-ൿඅ-ෆก-ะา-ำเ-ๅກ-ະາ-ຳຽ-ໄໜ-ༀཀ-ཬྈ-ྋက-ဪဿၐ-ၕၚ-ၝၡၥ-ၦၮ-ၰၵ-ႁႎႠ-ჺᄀ-ፚᎀ-ᎏᎠ-ᙬᙯ-ᙶᚁ-ᚚᚠ-ᛪᛮ-ᜑᜠ-ᜱᝀ-ᝑᝠ-ᝰក-ឳៜᠠ-ᡂᡄ-ᢨᢪ-ᤜᥐ-ᦩᧁ-ᧇᨀ-ᨖᬅ-ᬳᭅ-ᭋᮃ-ᮠᮮ-ᮯᰀ-ᰣᱍ-ᱏᱚ-ᱷᴀ-ᴫᵢ-ᵷᵹ-ᶚḀ-ᾼιῂ-ῌῐ-Ίῠ-Ῥῲ-ῼⁱⁿℂℇℊ-ℓℕℙ-ℝℤΩℨK-ℭℯ-ℹℼ-ℿⅅ-ⅉⅎⅠ-ↈⰀ-ⱼⲀ-ⳤⴀ-ⵥⶀ-ⷞ〆-〇〡-〩〸-〺〼ぁ-ゖゟァ-ヺヿ-ㆎㆠ-ㆷㇰ-ㇿ㐀-䶵一-ꀔꀖ-ꒌꔀ-ꘋꘐ-ꘟꘪ-ꙮꚀ-ꚗꜢ-ꝯꝱ-ꞇꞋ-ꠁꠃ-ꠅꠇ-ꠊꠌ-ꠢꡀ-ꡳꢂ-ꢳꤊ-ꤥꤰ-ꥆꨀ-ꨨꩀ-ꩂꩄ-ꩋ가-힣豈-יִײַ-ﬨשׁ-ﴽﵐ-ﷻﹰ-ﻼＡ-Ｚａ-ｚｦ-ｯｱ-ﾝﾠ-ￜ]'
    upper = '[A-Z\\$_À-ÖØ-ÞĀĂĄĆĈĊČĎĐĒĔĖĘĚĜĞĠĢĤĦĨĪĬĮİĲĴĶĹĻĽĿŁŃŅŇŊŌŎŐŒŔŖŘŚŜŞŠŢŤŦŨŪŬŮŰŲŴŶŸ-ŹŻŽƁ-ƂƄƆ-ƇƉ-ƋƎ-ƑƓ-ƔƖ-ƘƜ-ƝƟ-ƠƢƤƦ-ƧƩƬƮ-ƯƱ-ƳƵƷ-ƸƼǄǇǊǍǏǑǓǕǗǙǛǞǠǢǤǦǨǪǬǮǱǴǶ-ǸǺǼǾȀȂȄȆȈȊȌȎȐȒȔȖȘȚȜȞȠȢȤȦȨȪȬȮȰȲȺ-ȻȽ-ȾɁɃ-ɆɈɊɌɎͰͲͶΆΈ-ΏΑ-ΫϏϒ-ϔϘϚϜϞϠϢϤϦϨϪϬϮϴϷϹ-ϺϽ-ЯѠѢѤѦѨѪѬѮѰѲѴѶѸѺѼѾҀҊҌҎҐҒҔҖҘҚҜҞҠҢҤҦҨҪҬҮҰҲҴҶҸҺҼҾӀ-ӁӃӅӇӉӋӍӐӒӔӖӘӚӜӞӠӢӤӦӨӪӬӮӰӲӴӶӸӺӼӾԀԂԄԆԈԊԌԎԐԒԔԖԘԚԜԞԠԢԱ-ՖႠ-ჅḀḂḄḆḈḊḌḎḐḒḔḖḘḚḜḞḠḢḤḦḨḪḬḮḰḲḴḶḸḺḼḾṀṂṄṆṈṊṌṎṐṒṔṖṘṚṜṞṠṢṤṦṨṪṬṮṰṲṴṶṸṺṼṾẀẂẄẆẈẊẌẎẐẒẔẞẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸỺỼỾἈ-ἏἘ-ἝἨ-ἯἸ-ἿὈ-ὍὙ-ὟὨ-ὯᾸ-ΆῈ-ΉῘ-ΊῨ-ῬῸ-Ώℂℇℋ-ℍℐ-ℒℕℙ-ℝℤΩℨK-ℭℰ-ℳℾ-ℿⅅↃⰀ-ⰮⱠⱢ-ⱤⱧⱩⱫⱭ-ⱯⱲⱵⲀⲂⲄⲆⲈⲊⲌⲎⲐⲒⲔⲖⲘⲚⲜⲞⲠⲢⲤⲦⲨⲪⲬⲮⲰⲲⲴⲶⲸⲺⲼⲾⳀⳂⳄⳆⳈⳊⳌⳎⳐⳒⳔⳖⳘⳚⳜⳞⳠⳢꙀꙂꙄꙆꙈꙊꙌꙎꙐꙒꙔꙖꙘꙚꙜꙞꙢꙤꙦꙨꙪꙬꚀꚂꚄꚆꚈꚊꚌꚎꚐꚒꚔꚖꜢꜤꜦꜨꜪꜬꜮꜲꜴꜶꜸꜺꜼꜾꝀꝂꝄꝆꝈꝊꝌꝎꝐꝒꝔꝖꝘꝚꝜꝞꝠꝢꝤꝦꝨꝪꝬꝮꝹꝻꝽ-ꝾꞀꞂꞄꞆꞋＡ-Ｚ]'
    idrest = '%s(?:%s|[0-9])*(?:(?<=_)%s)?' % (letter, letter, op)
    tokens = {'root': [
              (
               '(class|trait|object)(\\s+)', bygroups(Keyword, Text), 'class'),
              (
               "'%s" % idrest, Text.Symbol),
              (
               '[^\\S\\n]+', Text),
              (
               '//.*?\\n', Comment.Single),
              (
               '/\\*', Comment.Multiline, 'comment'),
              (
               '@%s' % idrest, Name.Decorator),
              (
               '(abstract|ca(?:se|tch)|d(?:ef|o)|e(?:lse|xtends)|f(?:inal(?:ly)?|or(?:Some)?)|i(?:f|mplicit)|lazy|match|new|override|pr(?:ivate|otected)|re(?:quires|turn)|s(?:ealed|uper)|t(?:h(?:is|row)|ry)|va[lr]|w(?:hile|ith)|yield)\\b|(<[%:-]|=>|>:|[#=@_⇒←])(\x08|(?=\\s)|$)',
               Keyword),
              (
               ':(?!%s)' % op, Keyword, 'type'),
              (
               '%s%s\\b' % (upper, idrest), Name.Class),
              (
               '(true|false|null)\\b', Keyword.Constant),
              (
               '(import|package)(\\s+)', bygroups(Keyword, Text), 'import'),
              (
               '(type)(\\s+)', bygroups(Keyword, Text), 'type'),
              (
               '"""(?:.|\\n)*?"""', String),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               "'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-f]{4}'", String.Char),
              (
               idrest, Name),
              (
               '`[^`]+`', Name),
              (
               '\\[', Operator, 'typeparam'),
              (
               '[\\(\\)\\{\\};,.]', Operator),
              (
               op, Operator),
              (
               '([0-9][0-9]*\\.[0-9]*|\\.[0-9]+)([eE][+-]?[0-9]+)?[fFdD]?',
               Number.Float),
              (
               '0x[0-9a-f]+', Number.Hex),
              (
               '[0-9]+L?', Number.Integer),
              (
               '\\n', Text)], 
       'class': [
               (
                '(%s|%s|`[^`]+`)(\\s*)(\\[)' % (idrest, op),
                bygroups(Name.Class, Text, Operator), 'typeparam'),
               (
                '[\\s\\n]+', Text),
               (
                '{', Operator, '#pop'),
               (
                '\\(', Operator, '#pop'),
               (
                '%s|%s|`[^`]+`' % (idrest, op), Name.Class, '#pop')], 
       'type': [
              (
               '\\s+', Text),
              (
               '<[%:]|>:|[#_⇒]|forSome|type', Keyword),
              (
               '([,\\);}]|=>|=)([\\s\\n]*)', bygroups(Operator, Text), '#pop'),
              (
               '[\\(\\{]', Operator, '#push'),
              (
               '((?:%s|%s|`[^`]+`)(?:\\.(?:%s|%s|`[^`]+`))*)(\\s*)(\\[)' % (
                idrest, op, idrest, op),
               bygroups(Keyword.Type, Text, Operator), ('#pop', 'typeparam')),
              (
               '((?:%s|%s|`[^`]+`)(?:\\.(?:%s|%s|`[^`]+`))*)(\\s*)$' % (
                idrest, op, idrest, op),
               bygroups(Keyword.Type, Text), '#pop'),
              (
               '\\.|%s|%s|`[^`]+`' % (idrest, op), Keyword.Type)], 
       'typeparam': [
                   (
                    '[\\s\\n,]+', Text),
                   (
                    '<[%:]|=>|>:|[#_⇒]|forSome|type', Keyword),
                   (
                    '([\\]\\)\\}])', Operator, '#pop'),
                   (
                    '[\\(\\[\\{]', Operator, '#push'),
                   (
                    '\\.|%s|%s|`[^`]+`' % (idrest, op), Keyword.Type)], 
       'comment': [
                 (
                  '[^/\\*]+', Comment.Multiline),
                 (
                  '/\\*', Comment.Multiline, '#push'),
                 (
                  '\\*/', Comment.Multiline, '#pop'),
                 (
                  '[*/]', Comment.Multiline)], 
       'import': [
                (
                 '(%s|\\.)+' % idrest, Name.Namespace, '#pop')]}


class DylanLexer(RegexLexer):
    """
    For the `Dylan <http://www.opendylan.org/>`_ language.

    *New in Pygments 0.7.*
    """
    name = 'Dylan'
    aliases = ['dylan']
    filenames = ['*.dylan', '*.dyl']
    mimetypes = ['text/x-dylan']
    flags = re.DOTALL
    tokens = {'root': [
              (
               '\\b(subclass|abstract|block|c(on(crete|stant)|lass)|domain|ex(c(eption|lude)|port)|f(unction(|al))|generic|handler|i(n(herited|line|stance|terface)|mport)|library|m(acro|ethod)|open|primary|sealed|si(deways|ngleton)|slot|v(ariable|irtual))\\b',
               Name.Builtin),
              (
               '<\\w+>', Keyword.Type),
              (
               '//.*?\\n', Comment.Single),
              (
               '/\\*[\\w\\W]*?\\*/', Comment.Multiline),
              (
               '"', String, 'string'),
              (
               "'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char),
              (
               '=>|\\b(a(bove|fterwards)|b(e(gin|low)|y)|c(ase|leanup|reate)|define|else(|if)|end|f(inally|or|rom)|i[fn]|l(et|ocal)|otherwise|rename|s(elect|ignal)|t(hen|o)|u(n(less|til)|se)|wh(en|ile))\\b',
               Keyword),
              (
               '([ \\t])([!\\$%&\\*\\/:<=>\\?~_^a-zA-Z0-9.+\\-]*:)',
               bygroups(Text, Name.Variable)),
              (
               '([ \\t]*)(\\S+[^:])([ \\t]*)(\\()([ \\t]*)',
               bygroups(Text, Name.Function, Text, Punctuation, Text)),
              (
               '-?[0-9.]+', Number),
              (
               '[(),;]', Punctuation),
              (
               '\\$[a-zA-Z0-9-]+', Name.Constant),
              (
               '[!$%&*/:<>=?~^.+\\[\\]{}-]+', Operator),
              (
               '\\s+', Text),
              (
               '#[a-zA-Z0-9-]+', Keyword),
              (
               '[a-zA-Z0-9-]+', Name.Variable)], 
       'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                (
                 '[^\\\\"\\n]+', String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\', String)]}


class ObjectiveCLexer(RegexLexer):
    """
    For Objective-C source code with preprocessor directives.
    """
    name = 'Objective-C'
    aliases = ['objective-c', 'objectivec', 'obj-c', 'objc']
    filenames = [
     '*.m']
    mimetypes = ['text/x-objective-c']
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'whitespace': [
                    (
                     '^#if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '^#', Comment.Preproc, 'macro'),
                    (
                     '^' + _ws + '#if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '^' + _ws + '#', Comment.Preproc, 'macro'),
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     '\\\\\\n', Text),
                    (
                     '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
                    (
                     '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline)], 
       'statements': [
                    (
                     '(L|@)?"', String, 'string'),
                    (
                     "(L|@)?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'",
                     String.Char),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[lL]?', Number.Float),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
                    (
                     '0x[0-9a-fA-F]+[Ll]?', Number.Hex),
                    (
                     '0[0-7]+[Ll]?', Number.Oct),
                    (
                     '\\d+[Ll]?', Number.Integer),
                    (
                     '[~!%^&*+=|?:<>/-]', Operator),
                    (
                     '[()\\[\\],.]', Punctuation),
                    (
                     '(auto|break|case|const|continue|default|do|else|enum|extern|for|goto|if|register|restricted|return|sizeof|static|struct|switch|typedef|union|volatile|virtual|while|in|@selector|@private|@protected|@public|@encode|@synchronized|@try|@throw|@catch|@finally|@end|@property|@synthesize|@dynamic)\\b',
                     Keyword),
                    (
                     '(int|long|float|short|double|char|unsigned|signed|void|id|BOOL|IBOutlet|IBAction|SEL)\\b',
                     Keyword.Type),
                    (
                     '(_{0,2}inline|naked|restrict|thread|typename)\\b',
                     Keyword.Reserved),
                    (
                     '__(asm|int8|based|except|int16|stdcall|cdecl|fastcall|int32|declspec|finally|int64|try|leave)\\b',
                     Keyword.Reserved),
                    (
                     '(TRUE|FALSE|nil|NULL)\\b', Name.Builtin),
                    (
                     '[a-zA-Z$_][a-zA-Z0-9$_]*:(?!:)', Name.Label),
                    (
                     '[a-zA-Z$_][a-zA-Z0-9$_]*', Name)], 
       'root': [
              include('whitespace'),
              (
               '((?:[a-zA-Z0-9_*\\s])+?(?:\\s|[*]))([a-zA-Z$_][a-zA-Z0-9$_]*)(\\s*\\([^;]*?\\))(' + _ws + ')({)',
               bygroups(using(this), Name.Function, using(this), Text, Punctuation),
               'function'),
              (
               '((?:[a-zA-Z0-9_*\\s])+?(?:\\s|[*]))([a-zA-Z$_][a-zA-Z0-9$_]*)(\\s*\\([^;]*?\\))(' + _ws + ')(;)',
               bygroups(using(this), Name.Function, using(this), Text, Punctuation)),
              (
               '(@interface|@implementation)(\\s+)', bygroups(Keyword, Text),
               'classname'),
              (
               '(@class|@protocol)(\\s+)', bygroups(Keyword, Text),
               'forward_classname'),
              (
               '(\\s*)(@end)(\\s*)', bygroups(Text, Keyword, Text)),
              (
               '', Text, 'statement')], 
       'classname': [
                   (
                    '([a-zA-Z$_][a-zA-Z0-9$_]*)(\\s*:\\s*)([a-zA-Z$_][a-zA-Z0-9$_]*)?',
                    bygroups(Name.Class, Text, Name.Class), '#pop'),
                   (
                    '([a-zA-Z$_][a-zA-Z0-9$_]*)(\\s*)(\\([a-zA-Z$_][a-zA-Z0-9$_]*\\))',
                    bygroups(Name.Class, Text, Name.Label), '#pop'),
                   (
                    '([a-zA-Z$_][a-zA-Z0-9$_]*)', Name.Class, '#pop')], 
       'forward_classname': [
                           (
                            '([a-zA-Z$_][a-zA-Z0-9$_]*)(\\s*,\\s*)',
                            bygroups(Name.Class, Text), 'forward_classname'),
                           (
                            '([a-zA-Z$_][a-zA-Z0-9$_]*)(\\s*;?)',
                            bygroups(Name.Class, Text), '#pop')], 
       'statement': [
                   include('whitespace'),
                   include('statements'),
                   (
                    '[{}]', Punctuation),
                   (
                    ';', Punctuation, '#pop')], 
       'function': [
                  include('whitespace'),
                  include('statements'),
                  (
                   ';', Punctuation),
                  (
                   '{', Punctuation, '#push'),
                  (
                   '}', Punctuation, '#pop')], 
       'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                (
                 '[^\\\\"\\n]+', String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\', String)], 
       'macro': [
               (
                '[^/\\n]+', Comment.Preproc),
               (
                '/[*](.|\\n)*?[*]/', Comment.Multiline),
               (
                '//.*?\\n', Comment.Single, '#pop'),
               (
                '/', Comment.Preproc),
               (
                '(?<=\\\\)\\n', Comment.Preproc),
               (
                '\\n', Comment.Preproc, '#pop')], 
       'if0': [
             (
              '^\\s*#if.*?(?<!\\\\)\\n', Comment.Preproc, '#push'),
             (
              '^\\s*#endif.*?(?<!\\\\)\\n', Comment.Preproc, '#pop'),
             (
              '.*?\\n', Comment)]}

    def analyse_text(text):
        if '@"' in text:
            return True
        if re.match('\\[[a-zA-Z0-9.]:', text):
            return True
        return False


class FortranLexer(RegexLexer):
    """
    Lexer for FORTRAN 90 code.

    *New in Pygments 0.10.*
    """
    name = 'Fortran'
    aliases = ['fortran']
    filenames = ['*.f', '*.f90']
    mimetypes = ['text/x-fortran']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               '!.*\\n', Comment),
              include('strings'),
              include('core'),
              (
               '[a-z][a-z0-9_]*', Name.Variable),
              include('nums'),
              (
               '[\\s]+', Text)], 
       'core': [
              (
               '\\b(ACCEPT|ALLOCATABLE|ALLOCATE|ARRAY|ASSIGN|BACKSPACE|BLOCK DATA|BYTE|CALL|CASE|CLOSE|COMMON|CONTAINS|CONTINUE|CYCLE|DATA|DEALLOCATE|DECODE|DIMENSION|DO|ENCODE|END FILE|ENDIF|END|ENTRY|EQUIVALENCE|EXIT|EXTERNAL|EXTRINSIC|FORALL|FORMAT|FUNCTION|GOTO|IF|IMPLICIT|INCLUDE|INQUIRE|INTENT|INTERFACE|INTRINSIC|MODULE|NAMELIST|NULLIFY|NONE|OPEN|OPTIONAL|OPTIONS|PARAMETER|PAUSE|POINTER|PRINT|PRIVATE|PROGRAM|PUBLIC|PURE|READ|RECURSIVE|RETURN|REWIND|SAVE|SELECT|SEQUENCE|STOP|SUBROUTINE|TARGET|TYPE|USE|VOLATILE|WHERE|WRITE|WHILE|THEN|ELSE|ENDIF)\\s*\\b',
               Keyword),
              (
               '\\b(CHARACTER|COMPLEX|DOUBLE PRECISION|DOUBLE COMPLEX|INTEGER|LOGICAL|REAL)\\s*\\b',
               Keyword.Type),
              (
               '(\\*\\*|\\*|\\+|-|\\/|<|>|<=|>=|==|\\/=|=)', Operator),
              (
               '(::)', Keyword.Declaration),
              (
               '[(),:&%;]', Punctuation),
              (
               '\\b(Abort|Abs|Access|AChar|ACos|AdjustL|AdjustR|AImag|AInt|Alarm|All|Allocated|ALog|AMax|AMin|AMod|And|ANInt|Any|ASin|Associated|ATan|BesJ|BesJN|BesY|BesYN|Bit_Size|BTest|CAbs|CCos|Ceiling|CExp|Char|ChDir|ChMod|CLog|Cmplx|Complex|Conjg|Cos|CosH|Count|CPU_Time|CShift|CSin|CSqRt|CTime|DAbs|DACos|DASin|DATan|Date_and_Time|DbesJ|DbesJ|DbesJN|DbesY|DbesY|DbesYN|Dble|DCos|DCosH|DDiM|DErF|DErFC|DExp|Digits|DiM|DInt|DLog|DLog|DMax|DMin|DMod|DNInt|Dot_Product|DProd|DSign|DSinH|DSin|DSqRt|DTanH|DTan|DTime|EOShift|Epsilon|ErF|ErFC|ETime|Exit|Exp|Exponent|FDate|FGet|FGetC|Float|Floor|Flush|FNum|FPutC|FPut|Fraction|FSeek|FStat|FTell|GError|GetArg|GetCWD|GetEnv|GetGId|GetLog|GetPId|GetUId|GMTime|HostNm|Huge|IAbs|IAChar|IAnd|IArgC|IBClr|IBits|IBSet|IChar|IDate|IDiM|IDInt|IDNInt|IEOr|IErrNo|IFix|Imag|ImagPart|Index|Int|IOr|IRand|IsaTty|IShft|IShftC|ISign|ITime|Kill|Kind|LBound|Len|Len_Trim|LGe|LGt|Link|LLe|LLt|LnBlnk|Loc|Log|Log|Logical|Long|LShift|LStat|LTime|MatMul|Max|MaxExponent|MaxLoc|MaxVal|MClock|Merge|Min|MinExponent|MinLoc|MinVal|Mod|Modulo|MvBits|Nearest|NInt|Not|Or|Pack|PError|Precision|Present|Product|Radix|Rand|Random_Number|Random_Seed|Range|Real|RealPart|Rename|Repeat|Reshape|RRSpacing|RShift|Scale|Scan|Second|Selected_Int_Kind|Selected_Real_Kind|Set_Exponent|Shape|Short|Sign|Signal|SinH|Sin|Sleep|Sngl|Spacing|Spread|SqRt|SRand|Stat|Sum|SymLnk|System|System_Clock|Tan|TanH|Time|Tiny|Transfer|Transpose|Trim|TtyNam|UBound|UMask|Unlink|Unpack|Verify|XOr|ZAbs|ZCos|ZExp|ZLog|ZSin|ZSqRt)\\s*\\b',
               Name.Builtin),
              (
               '\\.(true|false)\\.', Name.Builtin),
              (
               '\\.(eq|ne|lt|le|gt|ge|not|and|or|eqv|neqv)\\.', Operator.Word)], 
       'strings': [
                 (
                  '(?s)"(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\])*"', String.Double),
                 (
                  "(?s)'(\\\\\\\\|\\\\[0-7]+|\\\\.|[^'\\\\])*'", String.Single)], 
       'nums': [
              (
               '\\d+(?![.Ee])', Number.Integer),
              (
               '[+-]?\\d*\\.\\d+([eE][-+]?\\d+)?', Number.Float),
              (
               '[+-]?\\d+\\.\\d*([eE][-+]?\\d+)?', Number.Float)]}


class GLShaderLexer(RegexLexer):
    """
    GLSL (OpenGL Shader) lexer.

    *New in Pygments 1.1.*
    """
    name = 'GLSL'
    aliases = ['glsl']
    filenames = ['*.vert', '*.frag', '*.geo']
    mimetypes = ['text/x-glslsrc']
    tokens = {'root': [
              (
               '^#.*', Comment.Preproc),
              (
               '//.*', Comment.Single),
              (
               '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
              (
               '\\+|-|~|!=?|\\*|/|%|<<|>>|<=?|>=?|==?|&&?|\\^|\\|\\|?',
               Operator),
              (
               '[?:]', Operator),
              (
               '\\bdefined\\b', Operator),
              (
               '[;{}(),\\[\\]]', Punctuation),
              (
               '[+-]?\\d*\\.\\d+([eE][-+]?\\d+)?', Number.Float),
              (
               '[+-]?\\d+\\.\\d*([eE][-+]?\\d+)?', Number.Float),
              (
               '0[xX][0-9a-fA-F]*', Number.Hex),
              (
               '0[0-7]*', Number.Oct),
              (
               '[1-9][0-9]*', Number.Integer),
              (
               '\\b(attribute|const|uniform|varying|centroid|break|continue|do|for|while|if|else|in|out|inout|float|int|void|bool|true|false|invariant|discard|return|mat[234]|mat[234]x[234]|vec[234]|[ib]vec[234]|sampler[123]D|samplerCube|sampler[12]DShadow|struct)\\b',
               Keyword),
              (
               '\\b(asm|class|union|enum|typedef|template|this|packed|goto|switch|default|inline|noinline|volatile|public|static|extern|external|interface|long|short|double|half|fixed|unsigned|lowp|mediump|highp|precision|input|output|hvec[234]|[df]vec[234]|sampler[23]DRect|sampler2DRectShadow|sizeof|cast|namespace|using)\\b',
               Keyword),
              (
               '[a-zA-Z_][a-zA-Z_0-9]*', Name),
              (
               '\\.', Punctuation),
              (
               '\\s+', Text)]}


class PrologLexer(RegexLexer):
    """
    Lexer for Prolog files.
    """
    name = 'Prolog'
    aliases = ['prolog']
    filenames = ['*.prolog', '*.pro', '*.pl']
    mimetypes = ['text/x-prolog']
    flags = re.UNICODE
    tokens = {'root': [
              (
               '^#.*', Comment.Single),
              (
               '/\\*', Comment.Multiline, 'nested-comment'),
              (
               '%.*', Comment.Single),
              (
               '[0-9]+', Number),
              (
               '[\\[\\](){}|.,;!]', Punctuation),
              (
               ':-|-->', Punctuation),
              (
               '"(?:\\\\x[0-9a-fA-F]+\\\\|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|\\\\[0-7]+\\\\|\\\\[\\w\\W]|[^"])*"',
               String.Double),
              (
               "'(?:''|[^'])*'", String.Atom),
              (
               '(is|<|>|=<|>=|==|=:=|=|/|//|\\*|\\+|-)(?=\\s|[a-zA-Z0-9\\[])',
               Operator),
              (
               '(mod|div|not)\\b', Operator),
              (
               '_', Keyword),
              (
               '([a-z]+)(:)', bygroups(Name.Namespace, Punctuation)),
              (
               '([a-zÀ-\u1fff\u3040-\ud7ff\ue000-\uffef][a-zA-Z0-9_$À-\u1fff\u3040-\ud7ff\ue000-\uffef]*)(\\s*)(:-|-->)',
               bygroups(Name.Function, Text, Operator)),
              (
               '([a-zÀ-\u1fff\u3040-\ud7ff\ue000-\uffef][a-zA-Z0-9_$À-\u1fff\u3040-\ud7ff\ue000-\uffef]*)(\\s*)(\\()',
               bygroups(Name.Function, Text, Punctuation)),
              (
               '[a-zÀ-\u1fff\u3040-\ud7ff\ue000-\uffef][a-zA-Z0-9_$À-\u1fff\u3040-\ud7ff\ue000-\uffef]*',
               String.Atom),
              (
               '[#&*+\\-./:<=>?@\\\\^~¡-¿‐-〿]+',
               String.Atom),
              (
               '[A-Z_][A-Za-z0-9_]*', Name.Variable),
              (
               '\\s+|[\u2000-\u200f\ufff0-\ufffe\uffef]', Text)], 
       'nested-comment': [
                        (
                         '\\*/', Comment.Multiline, '#pop'),
                        (
                         '/\\*', Comment.Multiline, '#push'),
                        (
                         '[^*/]+', Comment.Multiline),
                        (
                         '[*/]', Comment.Multiline)]}

    def analyse_text(text):
        return ':-' in text


class CythonLexer(RegexLexer):
    """
    For Pyrex and `Cython <http://cython.org>`_ source code.

    *New in Pygments 1.1.*
    """
    name = 'Cython'
    aliases = ['cython', 'pyx']
    filenames = ['*.pyx', '*.pxd', '*.pxi']
    mimetypes = ['text/x-cython', 'application/x-cython']
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
               '(<)([a-zA-Z0-9.?]+)(>)',
               bygroups(Punctuation, Keyword.Type, Punctuation)),
              (
               '!=|==|<<|>>|[-~+/*%=<>&^|.?]', Operator),
              (
               '(from)(\\d+)(<=)(\\s+)(<)(\\d+)(:)',
               bygroups(Keyword, Number.Integer, Operator, Name, Operator, Name, Punctuation)),
              include('keywords'),
              (
               '(def|property)(\\s+)', bygroups(Keyword, Text), 'funcname'),
              (
               '(cp?def)(\\s+)', bygroups(Keyword, Text), 'cdef'),
              (
               '(class|struct)(\\s+)', bygroups(Keyword, Text), 'classname'),
              (
               '(from)(\\s+)', bygroups(Keyword, Text), 'fromimport'),
              (
               '(c?import)(\\s+)', bygroups(Keyword, Text), 'import'),
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
                   '(assert|break|by|continue|ctypedef|del|elif|else|except\\??|exec|finally|for|gil|global|if|include|lambda|nogil|pass|print|raise|return|try|while|yield|as|with)\\b',
                   Keyword),
                  (
                   '(DEF|IF|ELIF|ELSE)\\b', Comment.Preproc)], 
       'builtins': [
                  (
                   '(?<!\\.)(__import__|abs|all|any|apply|basestring|bin|bool|buffer|bytearray|bytes|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|exit|file|filter|float|frozenset|getattr|globals|hasattr|hash|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|min|next|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\\b',
                   Name.Builtin),
                  (
                   '(?<!\\.)(self|None|Ellipsis|NotImplemented|False|True|NULL)\\b',
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
               '[a-zA-Z_][a-zA-Z0-9_]*', Name)], 
       'funcname': [
                  (
                   '[a-zA-Z_][a-zA-Z0-9_]*', Name.Function, '#pop')], 
       'cdef': [
              (
               '(public|readonly|extern|api|inline)\\b', Keyword.Reserved),
              (
               '(struct|enum|union|class)\\b', Keyword),
              (
               '([a-zA-Z_][a-zA-Z0-9_]*)(\\s*)(?=[(:#=]|$)',
               bygroups(Name.Function, Text), '#pop'),
              (
               '([a-zA-Z_][a-zA-Z0-9_]*)(\\s*)(,)',
               bygroups(Name.Function, Text, Punctuation)),
              (
               'from\\b', Keyword, '#pop'),
              (
               'as\\b', Keyword),
              (
               ':', Punctuation, '#pop'),
              (
               '(?=["\\\'])', Text, '#pop'),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Keyword.Type),
              (
               '.', Text)], 
       'classname': [
                   (
                    '[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop')], 
       'import': [
                (
                 '(\\s+)(as)(\\s+)', bygroups(Text, Keyword, Text)),
                (
                 '[a-zA-Z_][a-zA-Z0-9_.]*', Name.Namespace),
                (
                 '(\\s*)(,)(\\s*)', bygroups(Text, Operator, Text)),
                (
                 '', Text, '#pop')], 
       'fromimport': [
                    (
                     '(\\s+)(c?import)\\b', bygroups(Text, Keyword), '#pop'),
                    (
                     '[a-zA-Z_.][a-zA-Z0-9_.]*', Name.Namespace),
                    (
                     '', Text, '#pop')], 
       'stringescape': [
                      (
                       '\\\\([\\\\abfnrtv"\\\']|\\n|N{.*?}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
                       String.Escape)], 
       'strings': [
                 (
                  '%(\\([a-zA-Z0-9]+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[diouxXeEfFgGcrs%]',
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


class ValaLexer(RegexLexer):
    """
    For Vala source code with preprocessor directives.

    *New in Pygments 1.1.*
    """
    name = 'Vala'
    aliases = ['vala', 'vapi']
    filenames = ['*.vala', '*.vapi']
    mimetypes = ['text/x-vala']
    tokens = {'whitespace': [
                    (
                     '^\\s*#if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     '\\\\\\n', Text),
                    (
                     '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
                    (
                     '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline)], 
       'statements': [
                    (
                     'L?"', String, 'string'),
                    (
                     "L?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'",
                     String.Char),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[lL]?', Number.Float),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
                    (
                     '0x[0-9a-fA-F]+[Ll]?', Number.Hex),
                    (
                     '0[0-7]+[Ll]?', Number.Oct),
                    (
                     '\\d+[Ll]?', Number.Integer),
                    (
                     '[~!%^&*+=|?:<>/-]', Operator),
                    (
                     '(\\[)(Compact|Immutable|(?:Boolean|Simple)Type)(\\])',
                     bygroups(Punctuation, Name.Decorator, Punctuation)),
                    (
                     '(\\[)(CCode|(?:Integer|Floating)Type)',
                     bygroups(Punctuation, Name.Decorator)),
                    (
                     '[()\\[\\],.]', Punctuation),
                    (
                     '(as|base|break|case|catch|construct|continue|default|delete|do|else|enum|finally|for|foreach|get|if|in|is|lock|new|out|params|return|set|sizeof|switch|this|throw|try|typeof|while|yield)\\b',
                     Keyword),
                    (
                     '(abstract|const|delegate|dynamic|ensures|extern|inline|internal|override|owned|private|protected|public|ref|requires|signal|static|throws|unowned|var|virtual|volatile|weak|yields)\\b',
                     Keyword.Declaration),
                    (
                     '(namespace|using)(\\s+)', bygroups(Keyword.Namespace, Text),
                     'namespace'),
                    (
                     '(class|errordomain|interface|struct)(\\s+)',
                     bygroups(Keyword.Declaration, Text), 'class'),
                    (
                     '(\\.)([a-zA-Z_][a-zA-Z0-9_]*)',
                     bygroups(Operator, Name.Attribute)),
                    (
                     '(void|bool|char|double|float|int|int8|int16|int32|int64|long|short|size_t|ssize_t|string|time_t|uchar|uint|uint8|uint16|uint32|uint64|ulong|unichar|ushort)\\b',
                     Keyword.Type),
                    (
                     '(true|false|null)\\b', Name.Builtin),
                    (
                     '[a-zA-Z_][a-zA-Z0-9_]*', Name)], 
       'root': [
              include('whitespace'),
              (
               '', Text, 'statement')], 
       'statement': [
                   include('whitespace'),
                   include('statements'),
                   (
                    '[{}]', Punctuation),
                   (
                    ';', Punctuation, '#pop')], 
       'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                (
                 '[^\\\\"\\n]+', String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\', String)], 
       'if0': [
             (
              '^\\s*#if.*?(?<!\\\\)\\n', Comment.Preproc, '#push'),
             (
              '^\\s*#el(?:se|if).*\\n', Comment.Preproc, '#pop'),
             (
              '^\\s*#endif.*?(?<!\\\\)\\n', Comment.Preproc, '#pop'),
             (
              '.*?\\n', Comment)], 
       'class': [
               (
                '[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop')], 
       'namespace': [
                   (
                    '[a-zA-Z_][a-zA-Z0-9_.]*', Name.Namespace, '#pop')]}


class OocLexer(RegexLexer):
    """
    For `Ooc <http://ooc-lang.org/>`_ source code

    *New in Pygments 1.2.*
    """
    name = 'Ooc'
    aliases = ['ooc']
    filenames = ['*.ooc']
    mimetypes = ['text/x-ooc']
    tokens = {'root': [
              (
               '\\b(class|interface|implement|abstract|extends|from|this|super|new|const|final|static|import|use|extern|inline|proto|break|continue|fallthrough|operator|if|else|for|while|do|switch|case|as|in|version|return|true|false|null)\\b',
               Keyword),
              (
               'include\\b', Keyword, 'include'),
              (
               '(cover)([ \\t]+)(from)([ \\t]+)([a-zA-Z0-9_]+[*@]?)',
               bygroups(Keyword, Text, Keyword, Text, Name.Class)),
              (
               '(func)((?:[ \\t]|\\\\\\n)+)(~[a-z_][a-zA-Z0-9_]*)',
               bygroups(Keyword, Text, Name.Function)),
              (
               '\\bfunc\\b', Keyword),
              (
               '//.*', Comment),
              (
               '(?s)/\\*.*?\\*/', Comment.Multiline),
              (
               '(==?|\\+=?|-[=>]?|\\*=?|/=?|:=|!=?|%=?|\\?|>{1,3}=?|<{1,3}=?|\\.\\.|&&?|\\|\\|?|\\^=?)',
               Operator),
              (
               '(\\.)([ \\t]*)([a-z]\\w*)',
               bygroups(Operator, Text, Name.Function)),
              (
               '[A-Z][A-Z0-9_]+', Name.Constant),
              (
               '[A-Z][a-zA-Z0-9_]*([@*]|\\[[ \\t]*\\])?', Name.Class),
              (
               '([a-z][a-zA-Z0-9_]*(?:~[a-z][a-zA-Z0-9_]*)?)((?:[ \\t]|\\\\\\n)*)(?=\\()',
               bygroups(Name.Function, Text)),
              (
               '[a-z][a-zA-Z0-9_]*', Name.Variable),
              (
               '[:(){}\\[\\];,]', Punctuation),
              (
               '0x[0-9a-fA-F]+', Number.Hex),
              (
               '0c[0-9]+', Number.Oct),
              (
               '0b[01]+', Number.Binary),
              (
               '[0-9_]\\.[0-9_]*(?!\\.)', Number.Float),
              (
               '[0-9_]+', Number.Decimal),
              (
               '"(?:\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\"])*"',
               String.Double),
              (
               "'(?:\\\\.|\\\\[0-9]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'",
               String.Char),
              (
               '@', Punctuation),
              (
               '\\.', Punctuation),
              (
               '\\\\[ \\t\\n]', Text),
              (
               '[ \\t]+', Text)], 
       'include': [
                 (
                  '[\\w/]+', Name),
                 (
                  ',', Punctuation),
                 (
                  '[ \\t]', Text),
                 (
                  '[;\\n]', Text, '#pop')]}


class GoLexer(RegexLexer):
    """
    For `Go <http://golang.org>`_ source.
    """
    name = 'Go'
    filenames = ['*.go']
    aliases = ['go']
    mimetypes = ['text/x-gosrc']
    tokens = {'root': [
              (
               '\\n', Text),
              (
               '\\s+', Text),
              (
               '\\\\\\n', Text),
              (
               '//(.*?)\\n', Comment.Single),
              (
               '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
              (
               '(break|default|func|interface|select|case|defer|go|map|struct|chan|else|goto|package|switch|const|fallthrough|if|range|type|continue|for|import|return|var)\\b',
               Keyword),
              (
               '(uint8|uint16|uint32|uint64|int8|int16|int32|int64|float32|float64|byte|uint|int|float|uintptr|string|close|closed|len|cap|new|make)\\b',
               Name.Builtin),
              (
               '\\d+(\\.\\d+[eE][+\\-]?\\d+|\\.\\d*|[eE][+\\-]?\\d+)',
               Number.Float),
              (
               '\\.\\d+([eE][+\\-]?\\d+)?', Number.Float),
              (
               '0[0-7]+', Number.Oct),
              (
               '0[xX][0-9a-fA-F]+', Number.Hex),
              (
               '(0|[1-9][0-9]*)', Number.Integer),
              (
               '\'(\\\\[\'"\\\\abfnrtv]|\\\\x[0-9a-fA-F]{2}|\\\\[0-7]{1,3}|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|[^\\\\])\'',
               String.Char),
              (
               '`[^`]*`', String),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '(<<=|>>=|<<|>>|<=|>=|&\\^=|&\\^|\\+=|-=|\\*=|/=|%=|&=|\\|=|&&|\\|\\||<-|\\+\\+|--|==|!=|:=|\\.\\.\\.)|[+\\-*/%&|^<>=!()\\[\\]{}.,;:]',
               Punctuation),
              (
               '[a-zA-Z_]\\w*', Name)]}


class FelixLexer(RegexLexer):
    """
    For `Felix <http://www.felix-lang.org>`_ source code.

    *New in Pygments 1.2.*
    """
    name = 'Felix'
    aliases = ['felix', 'flx']
    filenames = ['*.flx', '*.flxh']
    mimetypes = ['text/x-felix']
    preproc = [
     'elif', 'else', 'endif', 'if', 'ifdef', 'ifndef']
    keywords = [
     '_', '_deref', 'all', 'as',
     'assert', 'attempt', 'call', 'callback', 'case', 'caseno', 'cclass',
     'code', 'compound', 'ctypes', 'do', 'done', 'downto', 'elif', 'else',
     'endattempt', 'endcase', 'endif', 'endmatch', 'enum', 'except',
     'exceptions', 'expect', 'finally', 'for', 'forall', 'forget', 'fork',
     'functor', 'goto', 'ident', 'if', 'incomplete', 'inherit', 'instance',
     'interface', 'jump', 'lambda', 'loop', 'match', 'module', 'namespace',
     'new', 'noexpand', 'nonterm', 'obj', 'of', 'open', 'parse', 'raise',
     'regexp', 'reglex', 'regmatch', 'rename', 'return', 'the', 'then',
     'to', 'type', 'typecase', 'typedef', 'typematch', 'typeof', 'upto',
     'when', 'whilst', 'with', 'yield']
    keyword_directives = [
     '_gc_pointer', '_gc_type', 'body', 'comment', 'const', 'export',
     'header', 'inline', 'lval', 'macro', 'noinline', 'noreturn',
     'package', 'private', 'pod', 'property', 'public', 'publish',
     'requires', 'todo', 'virtual', 'use']
    keyword_declarations = [
     'def', 'let', 'ref', 'val', 'var']
    keyword_types = [
     'unit', 'void', 'any', 'bool',
     'byte', 'offset',
     'address', 'caddress', 'cvaddress', 'vaddress',
     'tiny', 'short', 'int', 'long', 'vlong',
     'utiny', 'ushort', 'vshort', 'uint', 'ulong', 'uvlong',
     'int8', 'int16', 'int32', 'int64',
     'uint8', 'uint16', 'uint32', 'uint64',
     'float', 'double', 'ldouble',
     'complex', 'dcomplex', 'lcomplex',
     'imaginary', 'dimaginary', 'limaginary',
     'char', 'wchar', 'uchar',
     'charp', 'charcp', 'ucharp', 'ucharcp',
     'string', 'wstring', 'ustring',
     'cont',
     'array', 'varray', 'list',
     'lvalue', 'opt', 'slice']
    keyword_constants = [
     'false', 'true']
    operator_words = [
     'and', 'not', 'in', 'is', 'isin', 'or', 'xor']
    name_builtins = [
     '_svc', 'while']
    name_pseudo = [
     'root', 'self', 'this']
    decimal_suffixes = '([tTsSiIlLvV]|ll|LL|([iIuU])(8|16|32|64))?'
    tokens = {'root': [
              include('whitespace'),
              (
               '(axiom|ctor|fun|gen|proc|reduce|union)\\b', Keyword,
               'funcname'),
              (
               '(class|cclass|cstruct|obj|struct)\\b', Keyword, 'classname'),
              (
               '(instance|module|typeclass)\\b', Keyword, 'modulename'),
              (
               '(%s)\\b' % ('|').join(keywords), Keyword),
              (
               '(%s)\\b' % ('|').join(keyword_directives), Name.Decorator),
              (
               '(%s)\\b' % ('|').join(keyword_declarations), Keyword.Declaration),
              (
               '(%s)\\b' % ('|').join(keyword_types), Keyword.Type),
              (
               '(%s)\\b' % ('|').join(keyword_constants), Keyword.Constant),
              include('operators'),
              (
               '0[xX]([0-9a-fA-F_]*\\.[0-9a-fA-F_]+|[0-9a-fA-F_]+)[pP][+\\-]?[0-9_]+[lLfFdD]?',
               Number.Float),
              (
               '[0-9_]+(\\.[0-9_]+[eE][+\\-]?[0-9_]+|\\.[0-9_]*|[eE][+\\-]?[0-9_]+)[lLfFdD]?',
               Number.Float),
              (
               '\\.(0|[1-9][0-9_]*)([eE][+\\-]?[0-9_]+)?[lLfFdD]?',
               Number.Float),
              (
               '0[Bb][01_]+%s' % decimal_suffixes, Number),
              (
               '0[0-7_]+%s' % decimal_suffixes, Number.Oct),
              (
               '0[xX][0-9a-fA-F_]+%s' % decimal_suffixes, Number.Hex),
              (
               '(0|[1-9][0-9_]*)%s' % decimal_suffixes, Number.Integer),
              (
               '([rR][cC]?|[cC][rR])"""', String, 'tdqs'),
              (
               "([rR][cC]?|[cC][rR])'''", String, 'tsqs'),
              (
               '([rR][cC]?|[cC][rR])"', String, 'dqs'),
              (
               "([rR][cC]?|[cC][rR])'", String, 'sqs'),
              (
               '[cCfFqQwWuU]?"""', String, combined('stringescape', 'tdqs')),
              (
               "[cCfFqQwWuU]?'''", String, combined('stringescape', 'tsqs')),
              (
               '[cCfFqQwWuU]?"', String, combined('stringescape', 'dqs')),
              (
               "[cCfFqQwWuU]?'", String, combined('stringescape', 'sqs')),
              (
               '[\\[\\]{}:(),;?]', Punctuation),
              (
               '[a-zA-Z_]\\w*:>', Name.Label),
              (
               '(%s)\\b' % ('|').join(name_builtins), Name.Builtin),
              (
               '(%s)\\b' % ('|').join(name_pseudo), Name.Builtin.Pseudo),
              (
               '[a-zA-Z_]\\w*', Name)], 
       'whitespace': [
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    include('comment'),
                    (
                     '#\\s*if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '#', Comment.Preproc, 'macro')], 
       'operators': [
                   (
                    '(%s)\\b' % ('|').join(operator_words), Operator.Word),
                   (
                    '!=|==|<<|>>|\\|\\||&&|[-~+/*%=<>&^|.$]', Operator)], 
       'comment': [
                 (
                  '//(.*?)\\n', Comment.Single),
                 (
                  '/[*]', Comment.Multiline, 'comment2')], 
       'comment2': [
                  (
                   '[^\\/*]', Comment.Multiline),
                  (
                   '/[*]', Comment.Multiline, '#push'),
                  (
                   '[*]/', Comment.Multiline, '#pop'),
                  (
                   '[\\/*]', Comment.Multiline)], 
       'if0': [
             (
              '^\\s*#if.*?(?<!\\\\)\\n', Comment, '#push'),
             (
              '^\\s*#endif.*?(?<!\\\\)\\n', Comment, '#pop'),
             (
              '.*?\\n', Comment)], 
       'macro': [
               include('comment'),
               (
                '(import|include)(\\s+)(<[^>]*?>)',
                bygroups(Comment.Preproc, Text, String), '#pop'),
               (
                '(import|include)(\\s+)("[^"]*?")',
                bygroups(Comment.Preproc, Text, String), '#pop'),
               (
                "(import|include)(\\s+)('[^']*?')",
                bygroups(Comment.Preproc, Text, String), '#pop'),
               (
                '[^/\\n]+', Comment.Preproc),
               (
                '/', Comment.Preproc),
               (
                '(?<=\\\\)\\n', Comment.Preproc),
               (
                '\\n', Comment.Preproc, '#pop')], 
       'funcname': [
                  include('whitespace'),
                  (
                   '[a-zA-Z_]\\w*', Name.Function, '#pop'),
                  (
                   '(?=\\()', Text, '#pop')], 
       'classname': [
                   include('whitespace'),
                   (
                    '[a-zA-Z_]\\w*', Name.Class, '#pop'),
                   (
                    '(?=\\{)', Text, '#pop')], 
       'modulename': [
                    include('whitespace'),
                    (
                     '\\[', Punctuation, ('modulename2', 'tvarlist')),
                    (
                     '', Error, 'modulename2')], 
       'modulename2': [
                     include('whitespace'),
                     (
                      '([a-zA-Z_]\\w*)', Name.Namespace, '#pop:2')], 
       'tvarlist': [
                  include('whitespace'),
                  include('operators'),
                  (
                   '\\[', Punctuation, '#push'),
                  (
                   '\\]', Punctuation, '#pop'),
                  (
                   ',', Punctuation),
                  (
                   '(with|where)\\b', Keyword),
                  (
                   '[a-zA-Z_]\\w*', Name)], 
       'stringescape': [
                      (
                       '\\\\([\\\\abfnrtv"\\\']|\\n|N{.*?}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
                       String.Escape)], 
       'strings': [
                 (
                  '%(\\([a-zA-Z0-9]+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[diouxXeEfFgGcrs%]',
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


class AdaLexer(RegexLexer):
    """
    For Ada source code.

    *New in Pygments 1.3.*
    """
    name = 'Ada'
    aliases = ['ada', 'ada95ada2005']
    filenames = ['*.adb', '*.ads', '*.ada']
    mimetypes = ['text/x-ada']
    flags = re.MULTILINE | re.I
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'root': [
              (
               '[^\\S\\n]+', Text),
              (
               '--.*?\\n', Comment.Single),
              (
               '[^\\S\\n]+', Text),
              (
               'function|procedure|entry', Keyword.Declaration, 'subprogram'),
              (
               '(subtype|type)(\\s+)([a-z0-9_]+)',
               bygroups(Keyword.Declaration, Text, Keyword.Type), 'type_def'),
              (
               'task|protected', Keyword.Declaration),
              (
               '(subtype)(\\s+)', bygroups(Keyword.Declaration, Text)),
              (
               '(end)(\\s+)', bygroups(Keyword.Reserved, Text), 'end'),
              (
               '(pragma)(\\s+)([a-zA-Z0-9_]+)',
               bygroups(Keyword.Reserved, Text, Comment.Preproc)),
              (
               '(true|false|null)\\b', Keyword.Constant),
              (
               '(Byte|Character|Float|Integer|Long_Float|Long_Integer|Long_Long_Float|Long_Long_Integer|Natural|Positive|Short_Float|Short_Integer|Short_Short_Float|Short_Short_Integer|String|Wide_String|Duration)\\b',
               Keyword.Type),
              (
               '(and(\\s+then)?|in|mod|not|or(\\s+else)|rem)\\b', Operator.Word),
              (
               'generic|private', Keyword.Declaration),
              (
               'package', Keyword.Declaration, 'package'),
              (
               'array\\b', Keyword.Reserved, 'array_def'),
              (
               '(with|use)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'),
              (
               '([a-z0-9_]+)(\\s*)(:)(\\s*)(constant)',
               bygroups(Name.Constant, Text, Punctuation, Text, Keyword.Reserved)),
              (
               '<<[a-z0-9_]+>>', Name.Label),
              (
               '([a-z0-9_]+)(\\s*)(:)(\\s*)(declare|begin|loop|for|while)',
               bygroups(Name.Label, Text, Punctuation, Text, Keyword.Reserved)),
              (
               '\\b(abort|abs|abstract|accept|access|aliased|all|array|at|begin|body|case|constant|declare|delay|delta|digits|do|else|elsif|end|entry|exception|exit|interface|for|goto|if|is|limited|loop|new|null|of|or|others|out|overriding|pragma|protected|raise|range|record|renames|requeue|return|reverse|select|separate|subtype|synchronized|task|tagged|terminate|then|type|until|when|while|xor)\\b',
               Keyword.Reserved),
              (
               '"[^"]*"', String),
              include('attribute'),
              include('numbers'),
              (
               "'[^']'", String.Character),
              (
               '([a-z0-9_]+)(\\s*|[(,])', bygroups(Name, using(this))),
              (
               "(<>|=>|:=|[\\(\\)\\|:;,.'])", Punctuation),
              (
               '[*<>+=/&-]', Operator),
              (
               '\\n+', Text)], 
       'numbers': [
                 (
                  '[0-9_]+#[0-9a-f]+#', Number.Hex),
                 (
                  '[0-9_]+\\.[0-9_]*', Number.Float),
                 (
                  '[0-9_]+', Number.Integer)], 
       'attribute': [
                   (
                    "(')([a-zA-Z0-9_]+)", bygroups(Punctuation, Name.Attribute))], 
       'subprogram': [
                    (
                     '\\(', Punctuation, ('#pop', 'formal_part')),
                    (
                     ';', Punctuation, '#pop'),
                    (
                     'is\\b', Keyword.Reserved, '#pop'),
                    (
                     '"[^"]+"|[a-z0-9_]+', Name.Function),
                    include('root')], 
       'end': [
             (
              '(if|case|record|loop|select)', Keyword.Reserved),
             (
              '"[^"]+"|[a-zA-Z0-9_]+', Name.Function),
             (
              '[\n\\s]+', Text),
             (
              ';', Punctuation, '#pop')], 
       'type_def': [
                  (
                   ';', Punctuation, '#pop'),
                  (
                   '\\(', Punctuation, 'formal_part'),
                  (
                   'with|and|use', Keyword.Reserved),
                  (
                   'array\\b', Keyword.Reserved, ('#pop', 'array_def')),
                  (
                   'record\\b', Keyword.Reserved, 'formal_part'),
                  include('root')], 
       'array_def': [
                   (
                    ';', Punctuation, '#pop'),
                   (
                    '([a-z0-9_]+)(\\s+)(range)',
                    bygroups(Keyword.Type, Text, Keyword.Reserved)),
                   include('root')], 
       'import': [
                (
                 '[a-z0-9_.]+', Name.Namespace, '#pop')], 
       'formal_part': [
                     (
                      '\\)', Punctuation, '#pop'),
                     (
                      '([a-z0-9_]+)(\\s*)(,|:[^=])',
                      bygroups(Name.Variable, Text, Punctuation)),
                     (
                      '(in|not|null|out|access)\\b', Keyword.Reserved),
                     include('root')], 
       'package': [
                 (
                  'body', Keyword.Declaration),
                 (
                  'is\\s+new|renames', Keyword.Reserved),
                 (
                  'is', Keyword.Reserved, '#pop'),
                 (
                  ';', Punctuation, '#pop'),
                 (
                  '\\(', Punctuation, 'package_instantiation'),
                 (
                  '([a-zA-Z0-9_.]+)', Name.Class),
                 include('root')], 
       'package_instantiation': [
                               (
                                '("[^"]+"|[a-z0-9_]+)(\\s+)(=>)',
                                bygroups(Name.Variable, Text, Punctuation)),
                               (
                                '[a-z0-9._\\\'"]', Text),
                               (
                                '\\)', Punctuation, '#pop'),
                               include('root')]}


class Modula2Lexer(RegexLexer):
    """
    For `Modula-2 <http://www.modula2.org/>`_ source code.

    Additional options that determine which keywords are highlighted:

    `pim`
        Select PIM Modula-2 dialect (default: True).
    `iso`
        Select ISO Modula-2 dialect (default: False).
    `objm2`
        Select Objective Modula-2 dialect (default: False).
    `gm2ext`
        Also highlight GNU extensions (default: False).

    *New in Pygments 1.3.*
    """
    name = 'Modula-2'
    aliases = ['modula2', 'm2']
    filenames = ['*.def', '*.mod']
    mimetypes = ['text/x-modula2']
    flags = re.MULTILINE | re.DOTALL
    tokens = {'whitespace': [
                    (
                     '\\n+', Text),
                    (
                     '\\s+', Text)], 
       'identifiers': [
                     (
                      '([a-zA-Z_\\$][a-zA-Z0-9_\\$]*)', Name)], 
       'numliterals': [
                     (
                      '[01]+B', Number.Binary),
                     (
                      '[0-7]+B', Number.Oct),
                     (
                      '[0-7]+C', Number.Oct),
                     (
                      '[0-9A-F]+C', Number.Hex),
                     (
                      '[0-9A-F]+H', Number.Hex),
                     (
                      '[0-9]+\\.[0-9]+E[+-][0-9]+', Number.Float),
                     (
                      '[0-9]+\\.[0-9]+', Number.Float),
                     (
                      '[0-9]+', Number.Integer)], 
       'strings': [
                 (
                  "'(\\\\\\\\|\\\\'|[^'])*'", String),
                 (
                  '"(\\\\\\\\|\\\\"|[^"])*"', String)], 
       'operators': [
                   (
                    '[*/+=#~&<>\\^-]', Operator),
                   (
                    ':=', Operator),
                   (
                    '@', Operator),
                   (
                    '\\.\\.', Operator),
                   (
                    '`', Operator),
                   (
                    '::', Operator)], 
       'punctuation': [
                     (
                      '[\\(\\)\\[\\]{},.:;|]', Punctuation)], 
       'comments': [
                  (
                   '//.*?\\n', Comment.Single),
                  (
                   '/\\*(.*?)\\*/', Comment.Multiline),
                  (
                   '\\(\\*([^\\$].*?)\\*\\)', Comment.Multiline)], 
       'pragmas': [
                 (
                  '\\(\\*\\$(.*?)\\*\\)', Comment.Preproc),
                 (
                  '<\\*(.*?)\\*>', Comment.Preproc)], 
       'root': [
              include('whitespace'),
              include('comments'),
              include('pragmas'),
              include('identifiers'),
              include('numliterals'),
              include('strings'),
              include('operators'),
              include('punctuation')]}
    pim_reserved_words = [
     'AND', 'ARRAY', 'BEGIN', 'BY', 'CASE', 'CONST', 'DEFINITION',
     'DIV', 'DO', 'ELSE', 'ELSIF', 'END', 'EXIT', 'EXPORT', 'FOR',
     'FROM', 'IF', 'IMPLEMENTATION', 'IMPORT', 'IN', 'LOOP', 'MOD',
     'MODULE', 'NOT', 'OF', 'OR', 'POINTER', 'PROCEDURE', 'QUALIFIED',
     'RECORD', 'REPEAT', 'RETURN', 'SET', 'THEN', 'TO', 'TYPE',
     'UNTIL', 'VAR', 'WHILE', 'WITH']
    pim_pervasives = [
     'ABS', 'BITSET', 'BOOLEAN', 'CAP', 'CARDINAL', 'CHAR', 'CHR', 'DEC',
     'DISPOSE', 'EXCL', 'FALSE', 'FLOAT', 'HALT', 'HIGH', 'INC', 'INCL',
     'INTEGER', 'LONGINT', 'LONGREAL', 'MAX', 'MIN', 'NEW', 'NIL', 'ODD',
     'ORD', 'PROC', 'REAL', 'SIZE', 'TRUE', 'TRUNC', 'VAL']
    iso_reserved_words = [
     'AND', 'ARRAY', 'BEGIN', 'BY', 'CASE', 'CONST', 'DEFINITION', 'DIV',
     'DO', 'ELSE', 'ELSIF', 'END', 'EXCEPT', 'EXIT', 'EXPORT', 'FINALLY',
     'FOR', 'FORWARD', 'FROM', 'IF', 'IMPLEMENTATION', 'IMPORT', 'IN',
     'LOOP', 'MOD', 'MODULE', 'NOT', 'OF', 'OR', 'PACKEDSET', 'POINTER',
     'PROCEDURE', 'QUALIFIED', 'RECORD', 'REPEAT', 'REM', 'RETRY',
     'RETURN', 'SET', 'THEN', 'TO', 'TYPE', 'UNTIL', 'VAR', 'WHILE',
     'WITH']
    iso_pervasives = [
     'ABS', 'BITSET', 'BOOLEAN', 'CAP', 'CARDINAL', 'CHAR', 'CHR', 'CMPLX',
     'COMPLEX', 'DEC', 'DISPOSE', 'EXCL', 'FALSE', 'FLOAT', 'HALT', 'HIGH',
     'IM', 'INC', 'INCL', 'INT', 'INTEGER', 'INTERRUPTIBLE', 'LENGTH',
     'LFLOAT', 'LONGCOMPLEX', 'LONGINT', 'LONGREAL', 'MAX', 'MIN', 'NEW',
     'NIL', 'ODD', 'ORD', 'PROC', 'PROTECTION', 'RE', 'REAL', 'SIZE',
     'TRUE', 'TRUNC', 'UNINTERRUBTIBLE', 'VAL']
    objm2_reserved_words = [
     'AND', 'ARRAY', 'BEGIN', 'BY', 'CASE', 'CONST', 'DEFINITION', 'DIV',
     'DO', 'ELSE', 'ELSIF', 'END', 'ENUM', 'EXIT', 'FOR', 'FROM', 'IF',
     'IMMUTABLE', 'IMPLEMENTATION', 'IMPORT', 'IN', 'IS', 'LOOP', 'MOD',
     'MODULE', 'NOT', 'OF', 'OPAQUE', 'OR', 'POINTER', 'PROCEDURE',
     'RECORD', 'REPEAT', 'RETURN', 'SET', 'THEN', 'TO', 'TYPE',
     'UNTIL', 'VAR', 'VARIADIC', 'WHILE',
     'BYCOPY', 'BYREF', 'CLASS', 'CONTINUE', 'CRITICAL', 'INOUT', 'METHOD',
     'ON', 'OPTIONAL', 'OUT', 'PRIVATE', 'PROTECTED', 'PROTOCOL', 'PUBLIC',
     'SUPER', 'TRY']
    objm2_pervasives = [
     'ABS', 'BITSET', 'BOOLEAN', 'CARDINAL', 'CHAR', 'CHR', 'DISPOSE',
     'FALSE', 'HALT', 'HIGH', 'INTEGER', 'INRANGE', 'LENGTH', 'LONGCARD',
     'LONGINT', 'LONGREAL', 'MAX', 'MIN', 'NEG', 'NEW', 'NEXTV', 'NIL',
     'OCTET', 'ODD', 'ORD', 'PRED', 'PROC', 'READ', 'REAL', 'SUCC', 'TMAX',
     'TMIN', 'TRUE', 'TSIZE', 'UNICHAR', 'VAL', 'WRITE', 'WRITEF',
     'OBJECT', 'NO', 'YES']
    gnu_reserved_words = [
     'ASM', '__ATTRIBUTE__', '__BUILTIN__', '__COLUMN__', '__DATE__',
     '__FILE__', '__FUNCTION__', '__LINE__', '__MODULE__', 'VOLATILE']
    gnu_pervasives = [
     'BITSET8', 'BITSET16', 'BITSET32', 'CARDINAL8', 'CARDINAL16',
     'CARDINAL32', 'CARDINAL64', 'COMPLEX32', 'COMPLEX64', 'COMPLEX96',
     'COMPLEX128', 'INTEGER8', 'INTEGER16', 'INTEGER32', 'INTEGER64',
     'REAL8', 'REAL16', 'REAL32', 'REAL96', 'REAL128', 'THROW']

    def __init__(self, **options):
        self.reserved_words = set()
        self.pervasives = set()
        if get_bool_opt(options, 'iso', False):
            self.reserved_words.update(self.iso_reserved_words)
            self.pervasives.update(self.iso_pervasives)
        elif get_bool_opt(options, 'objm2', False):
            self.reserved_words.update(self.objm2_reserved_words)
            self.pervasives.update(self.objm2_pervasives)
        else:
            self.reserved_words.update(self.pim_reserved_words)
            self.pervasives.update(self.pim_pervasives)
        if get_bool_opt(options, 'gm2ext', False):
            self.reserved_words.update(self.gnu_reserved_words)
            self.pervasives.update(self.gnu_pervasives)
        RegexLexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if value in self.reserved_words:
                    token = Keyword.Reserved
                elif value in self.pervasives:
                    token = Keyword.Pervasive
            yield (
             index, token, value)


class BlitzMaxLexer(RegexLexer):
    """
    For `BlitzMax <http://blitzbasic.com>`_ source code.

    *New in Pygments 1.4.*
    """
    name = 'BlitzMax'
    aliases = ['blitzmax', 'bmax']
    filenames = ['*.bmx']
    mimetypes = ['text/x-bmx']
    bmax_vopwords = '\\b(Shl|Shr|Sar|Mod)\\b'
    bmax_sktypes = '@{1,2}|[!#$%]'
    bmax_lktypes = '\\b(Int|Byte|Short|Float|Double|Long)\\b'
    bmax_name = '[a-z_][a-z0-9_]*'
    bmax_var = '(%s)(?:(?:([ \\t]*)(%s)|([ \\t]*:[ \\t]*\\b(?:Shl|Shr|Sar|Mod)\\b)|([ \\t]*)([:])([ \\t]*)(?:%s|(%s)))(?:([ \\t]*)(Ptr))?)' % (bmax_name, bmax_sktypes, bmax_lktypes, bmax_name)
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
               '\\%[10]+', Number),
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
               '\\b(TNullMethodException|TNullFunctionException|TNullObjectException|TArrayBoundsException|TRuntimeException)\\b',
               Name.Exception),
              (
               '\\b(Strict|SuperStrict|Module|ModuleInfo|End|Return|Continue|Exit|Public|Private|Var|VarPtr|Chr|Len|Asc|SizeOf|Sgn|Abs|Min|Max|New|Release|Delete|Incbin|IncbinPtr|IncbinLen|Framework|Include|Import|Extern|EndExtern|Function|EndFunction|Type|EndType|Extends|Method|EndMethod|Abstract|Final|If|Then|Else|ElseIf|EndIf|For|To|Next|Step|EachIn|While|Wend|EndWhile|Repeat|Until|Forever|Select|Case|Default|EndSelect|Try|Catch|EndTry|Throw|Assert|Goto|DefData|ReadData|RestoreData)\\b',
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