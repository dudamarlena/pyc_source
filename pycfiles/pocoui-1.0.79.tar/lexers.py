# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/highlight/lexers.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.pkg.highlight.lexers\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n    Lexers for highlighting package.\n\n    :copyright: 2006 by Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'
from pocoo.pkg.highlight.base import RegexLexer, Text, Comment, Operator, Keyword, Name, String, Number

class PythonLexer(RegexLexer):
    __module__ = __name__
    name = 'python'
    tokens = [('\\s+', Text), ('#.*?\\n', Comment), ('[]{}:(),.[]', Text), ('\\\\\\n', Text), ('in\\b|is\\b|and\\b|or\\b|not\\b|!=|==|[-+/*%=<>]', Operator), ('(assert|break|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|lambda|pass|print|raise|return|try|while|yield)\\b', Keyword), ('@[a-zA-Z0-9.]+', Keyword.Decorator), ('(?<!\\.)(__import__|abs|apply|basestring|bool|buffer|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|exit|file|filter|float|getattr|globals|hasattr|hash|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|min|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|round|setattr|slice|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\\b', Name.Builtin), ('(?<!\\.)(self|None|False|True)\\b', Name.Builtin.Pseudokeyword), ('[a-zA-Z_][a-zA-Z0-9_]*', Name), ('[0-9]+', Number), ('""".*?"""', String.Double), ("'''.*?'''", String.Single), ('"(\\\\\\\\|\\\\"|[^"])*"', String.Double), ("'(\\\\\\\\|\\\\'|[^'])*'", String.Single)]


class PHPLexer(RegexLexer):
    __module__ = __name__
    name = 'php'
    tokens = [('\\s+', Text), ('#.*?\\n', Comment), ('//.*?\\n', Comment), ('/[*].*?[*]/', Comment), ('[~!%^&*()+=|\\[\\]:;,.<>/?{}@-]', Text), ('(' + ('|').join(('and', 'E_PARSE', 'old_function', 'E_ERROR', 'or', 'as', 'E_WARNING',
                  'parent', 'eval', 'PHP_OS', 'break', 'exit', 'case', 'extends',
                  'PHP_VERSION', 'cfunction', 'FALSE', 'print', 'class', 'for', 'require',
                  'continue', 'foreach', 'require_once', 'declare', 'function', 'return',
                  'default', 'static', 'do', 'switch', 'die', 'stdClass', 'echo',
                  'else', 'TRUE', 'elseif', 'var', 'empty', 'if', 'xor', 'enddeclare',
                  'include', 'virtual', 'endfor', 'include_once', 'while', 'endforeach',
                  'global', '__FILE__', 'endif', 'list', '__LINE__', 'endswitch',
                  'new', '__sleep', 'endwhile', 'not', '__wakeup', 'E_ALL', 'NULL')) + ')\\b', Keyword), ('(true|false|null)\x08', Keyword.Constant), ('\\$[a-zA-Z_][a-zA-Z0-9_]*', Name.Variable), ('[a-zA-Z_][a-zA-Z0-9_]*', Name.Other), ('[0-9](\\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?', Number), ('"(\\\\\\\\|\\\\"|[^"])*"', String.Double), ("'(\\\\\\\\|\\\\'|[^'])*'", String.Single)]


class CppLexer(RegexLexer):
    __module__ = __name__
    name = 'cplusplus'
    tokens = [('\\s+', Text), ('\\\\\\n', Text), ('//.*?\\n', Comment), ('/[*].*?[*]/', Comment), ('(?<=\\n)\\s*#.*?(\\n|(?=/[*]))', Comment.Preproc), ('[~!%^&*()+=|\\[\\]:;,.<>/?-]', Text), ('[{}]', Keyword), ('"(\\\\\\\\|\\\\"|[^"])*"', String), ("'\\\\.'|'[^\\\\]'", String.Char), ('[0-9](\\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?', Number), ('(' + ('|').join(('struct', 'class', 'union', 'enum', 'int', 'float', 'double', 'signed',
                  'unsigned', 'char', 'short', 'void', 'bool', 'long', 'register',
                  'auto', 'operator', 'static', 'const', 'private', 'public', 'protected',
                  'virtual', 'explicit', 'new', 'delete', 'this', 'if', 'else', 'while',
                  'for', 'do', 'switch', 'case', 'default', 'sizeof', 'dynamic_cast',
                  'static_cast', 'const_cast', 'reinterpret_cast', 'typeid', 'try',
                  'catch', 'throw', 'throws', 'return', 'continue', 'break', 'goto')) + ')\\b', Keyword), ('(' + ('|').join(('extern', 'volatile', 'typedef', 'friend', '__declspec', 'inline',
                  '__asm', 'thread', 'naked', 'dllimport', 'dllexport', 'namespace',
                  'using', 'template', 'typename', 'goto')) + ')\\b', Keyword.Reserved), ('(true|false|NULL)\\b', Keyword.Constant), ('[a-zA-Z_][a-zA-Z0-9_]*', Name)]