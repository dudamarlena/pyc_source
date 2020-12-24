# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/python.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 37722 bytes
"""
    pygments.lexers.python
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Python and related languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, default, words, combined, do_insertions
from pygments.util import get_bool_opt, shebang_matches
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic, Other, Error
from pygments import unistring as uni
__all__ = [
 'PythonLexer', 'PythonConsoleLexer', 'PythonTracebackLexer',
 'Python3Lexer', 'Python3TracebackLexer', 'CythonLexer',
 'DgLexer', 'NumPyLexer']
line_re = re.compile('.*?\n')

class PythonLexer(RegexLexer):
    __doc__ = '\n    For `Python <http://www.python.org>`_ source code.\n    '
    name = 'Python'
    aliases = ['python', 'py', 'sage']
    filenames = ['*.py', '*.pyw', '*.sc', 'SConstruct', 'SConscript', '*.tac', '*.sage']
    mimetypes = ['text/x-python', 'application/x-python']

    def innerstring_rules(ttype):
        return [
         (
          '%(\\(\\w+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[diouxXeEfFgGcrs%]',
          String.Interpol),
         (
          '[^\\\\\\\'"%\\n]+', ttype),
         (
          '[\\\'"\\\\]', ttype),
         (
          '%', ttype)]

    tokens = {'root': [
              (
               '\\n', Text),
              (
               '^(\\s*)([rRuU]{,2}"""(?:.|\\n)*?""")', bygroups(Text, String.Doc)),
              (
               "^(\\s*)([rRuU]{,2}'''(?:.|\\n)*?''')", bygroups(Text, String.Doc)),
              (
               '[^\\S\\n]+', Text),
              (
               '\\A#!.+$', Comment.Hashbang),
              (
               '#.*$', Comment.Single),
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
               '(def)((?:\\s|\\\\\\s)+)', bygroups(Keyword, Text), 'funcname'),
              (
               '(class)((?:\\s|\\\\\\s)+)', bygroups(Keyword, Text), 'classname'),
              (
               '(from)((?:\\s|\\\\\\s)+)', bygroups(Keyword.Namespace, Text),
               'fromimport'),
              (
               '(import)((?:\\s|\\\\\\s)+)', bygroups(Keyword.Namespace, Text),
               'import'),
              include('builtins'),
              include('backtick'),
              (
               '(?:[rR]|[uU][rR]|[rR][uU])"""', String.Double, 'tdqs'),
              (
               "(?:[rR]|[uU][rR]|[rR][uU])'''", String.Single, 'tsqs'),
              (
               '(?:[rR]|[uU][rR]|[rR][uU])"', String.Double, 'dqs'),
              (
               "(?:[rR]|[uU][rR]|[rR][uU])'", String.Single, 'sqs'),
              (
               '[uU]?"""', String.Double, combined('stringescape', 'tdqs')),
              (
               "[uU]?'''", String.Single, combined('stringescape', 'tsqs')),
              (
               '[uU]?"', String.Double, combined('stringescape', 'dqs')),
              (
               "[uU]?'", String.Single, combined('stringescape', 'sqs')),
              include('name'),
              include('numbers')], 
     
     'keywords': [
                  (
                   words(('assert', 'break', 'continue', 'del', 'elif', 'else', 'except', 'exec', 'finally',
       'for', 'global', 'if', 'lambda', 'pass', 'print', 'raise', 'return', 'try',
       'while', 'yield', 'yield from', 'as', 'with'), suffix='\\b'),
                   Keyword)], 
     
     'builtins': [
                  (
                   words(('__import__', 'abs', 'all', 'any', 'apply', 'basestring', 'bin', 'bool', 'buffer',
       'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile',
       'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile',
       'exit', 'file', 'filter', 'float', 'frozenset', 'getattr', 'globals', 'hasattr',
       'hash', 'hex', 'id', 'input', 'int', 'intern', 'isinstance', 'issubclass',
       'iter', 'len', 'list', 'locals', 'long', 'map', 'max', 'min', 'next', 'object',
       'oct', 'open', 'ord', 'pow', 'property', 'range', 'raw_input', 'reduce', 'reload',
       'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod',
       'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange',
       'zip'), prefix='(?<!\\.)', suffix='\\b'),
                   Name.Builtin),
                  (
                   '(?<!\\.)(self|None|Ellipsis|NotImplemented|False|True)\\b',
                   Name.Builtin.Pseudo),
                  (
                   words(('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'DeprecationWarning',
       'EOFError', 'EnvironmentError', 'Exception', 'FloatingPointError', 'FutureWarning',
       'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError',
       'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError',
       'NameError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
       'OverflowWarning', 'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError',
       'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 'SyntaxWarning',
       'SystemError', 'SystemExit', 'TabError', 'TypeError', 'UnboundLocalError',
       'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
       'UnicodeWarning', 'UserWarning', 'ValueError', 'VMSError', 'Warning', 'WindowsError',
       'ZeroDivisionError'), prefix='(?<!\\.)', suffix='\\b'),
                   Name.Exception)], 
     
     'numbers': [
                 (
                  '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
                 (
                  '\\d+[eE][+-]?[0-9]+j?', Number.Float),
                 (
                  '0[0-7]+j?', Number.Oct),
                 (
                  '0[bB][01]+', Number.Bin),
                 (
                  '0[xX][a-fA-F0-9]+', Number.Hex),
                 (
                  '\\d+L', Number.Integer.Long),
                 (
                  '\\d+j?', Number.Integer)], 
     
     'backtick': [
                  (
                   '`.*?`', String.Backtick)], 
     
     'name': [
              (
               '@[\\w.]+', Name.Decorator),
              (
               '[a-zA-Z_]\\w*', Name)], 
     
     'funcname': [
                  (
                   '[a-zA-Z_]\\w*', Name.Function, '#pop')], 
     
     'classname': [
                   (
                    '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     
     'import': [
                (
                 '(?:[ \\t]|\\\\\\n)+', Text),
                (
                 'as\\b', Keyword.Namespace),
                (
                 ',', Operator),
                (
                 '[a-zA-Z_][\\w.]*', Name.Namespace),
                default('#pop')], 
     
     'fromimport': [
                    (
                     '(?:[ \\t]|\\\\\\n)+', Text),
                    (
                     'import\\b', Keyword.Namespace, '#pop'),
                    (
                     'None\\b', Name.Builtin.Pseudo, '#pop'),
                    (
                     '[a-zA-Z_.][\\w.]*', Name.Namespace),
                    default('#pop')], 
     
     'stringescape': [
                      (
                       '\\\\([\\\\abfnrtv"\\\']|\\n|N\\{.*?\\}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
                       String.Escape)], 
     
     'strings-single': innerstring_rules(String.Single), 
     'strings-double': innerstring_rules(String.Double), 
     'dqs': [
             (
              '"', String.Double, '#pop'),
             (
              '\\\\\\\\|\\\\"|\\\\\\n', String.Escape),
             include('strings-double')], 
     
     'sqs': [
             (
              "'", String.Single, '#pop'),
             (
              "\\\\\\\\|\\\\'|\\\\\\n", String.Escape),
             include('strings-single')], 
     
     'tdqs': [
              (
               '"""', String.Double, '#pop'),
              include('strings-double'),
              (
               '\\n', String.Double)], 
     
     'tsqs': [
              (
               "'''", String.Single, '#pop'),
              include('strings-single'),
              (
               '\\n', String.Single)]}

    def analyse_text(text):
        return shebang_matches(text, 'pythonw?(2(\\.\\d)?)?') or 'import ' in text[:1000]


class Python3Lexer(RegexLexer):
    __doc__ = '\n    For `Python <http://www.python.org>`_ source code (version 3.0).\n\n    .. versionadded:: 0.10\n    '
    name = 'Python 3'
    aliases = ['python3', 'py3']
    filenames = []
    mimetypes = ['text/x-python3', 'application/x-python3']
    flags = re.MULTILINE | re.UNICODE
    uni_name = '[%s][%s]*' % (uni.xid_start, uni.xid_continue)

    def innerstring_rules(ttype):
        return [
         (
          '%(\\(\\w+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[diouxXeEfFgGcrs%]',
          String.Interpol),
         (
          '\\{((\\w+)((\\.\\w+)|(\\[[^\\]]+\\]))*)?(\\![sra])?(\\:(.?[<>=\\^])?[-+ ]?#?0?(\\d+)?,?(\\.\\d+)?[bcdeEfFgGnosxX%]?)?\\}',
          String.Interpol),
         (
          '[^\\\\\\\'"%\\{\\n]+', ttype),
         (
          '[\\\'"\\\\]', ttype),
         (
          '%|(\\{{1,2})', ttype)]

    tokens = PythonLexer.tokens.copy()
    tokens['keywords'] = [
     (
      words(('assert', 'async', 'await', 'break', 'continue', 'del', 'elif', 'else', 'except',
       'finally', 'for', 'global', 'if', 'lambda', 'pass', 'raise', 'nonlocal', 'return',
       'try', 'while', 'yield', 'yield from', 'as', 'with'), suffix='\\b'),
      Keyword),
     (
      words(('True', 'False', 'None'), suffix='\\b'),
      Keyword.Constant)]
    tokens['builtins'] = [
     (
      words(('__import__', 'abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes', 'chr',
       'classmethod', 'cmp', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod',
       'enumerate', 'eval', 'filter', 'float', 'format', 'frozenset', 'getattr',
       'globals', 'hasattr', 'hash', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
       'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next',
       'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr',
       'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod',
       'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'), prefix='(?<!\\.)', suffix='\\b'),
      Name.Builtin),
     (
      '(?<!\\.)(self|Ellipsis|NotImplemented)\\b', Name.Builtin.Pseudo),
     (
      words(('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError',
       'BytesWarning', 'DeprecationWarning', 'EOFError', 'EnvironmentError', 'Exception',
       'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError',
       'ImportWarning', 'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt',
       'LookupError', 'MemoryError', 'NameError', 'NotImplementedError', 'OSError',
       'OverflowError', 'PendingDeprecationWarning', 'ReferenceError', 'ResourceWarning',
       'RuntimeError', 'RuntimeWarning', 'StopIteration', 'SyntaxError', 'SyntaxWarning',
       'SystemError', 'SystemExit', 'TabError', 'TypeError', 'UnboundLocalError',
       'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
       'UnicodeWarning', 'UserWarning', 'ValueError', 'VMSError', 'Warning', 'WindowsError',
       'ZeroDivisionError', 'BlockingIOError', 'ChildProcessError', 'ConnectionError',
       'BrokenPipeError', 'ConnectionAbortedError', 'ConnectionRefusedError', 'ConnectionResetError',
       'FileExistsError', 'FileNotFoundError', 'InterruptedError', 'IsADirectoryError',
       'NotADirectoryError', 'PermissionError', 'ProcessLookupError', 'TimeoutError'), prefix='(?<!\\.)', suffix='\\b'),
      Name.Exception)]
    tokens['numbers'] = [
     (
      '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
     (
      '0[oO][0-7]+', Number.Oct),
     (
      '0[bB][01]+', Number.Bin),
     (
      '0[xX][a-fA-F0-9]+', Number.Hex),
     (
      '\\d+', Number.Integer)]
    tokens['backtick'] = []
    tokens['name'] = [
     (
      '@\\w+', Name.Decorator),
     (
      '@', Operator),
     (
      uni_name, Name)]
    tokens['funcname'] = [
     (
      uni_name, Name.Function, '#pop')]
    tokens['classname'] = [
     (
      uni_name, Name.Class, '#pop')]
    tokens['import'] = [
     (
      '(\\s+)(as)(\\s+)', bygroups(Text, Keyword, Text)),
     (
      '\\.', Name.Namespace),
     (
      uni_name, Name.Namespace),
     (
      '(\\s*)(,)(\\s*)', bygroups(Text, Operator, Text)),
     default('#pop')]
    tokens['fromimport'] = [
     (
      '(\\s+)(import)\\b', bygroups(Text, Keyword), '#pop'),
     (
      '\\.', Name.Namespace),
     (
      uni_name, Name.Namespace),
     default('#pop')]
    tokens['strings-single'] = innerstring_rules(String.Single)
    tokens['strings-double'] = innerstring_rules(String.Double)

    def analyse_text(text):
        return shebang_matches(text, 'pythonw?3(\\.\\d)?')


class PythonConsoleLexer(Lexer):
    __doc__ = '\n    For Python console output or doctests, such as:\n\n    .. sourcecode:: pycon\n\n        >>> a = \'foo\'\n        >>> print a\n        foo\n        >>> 1 / 0\n        Traceback (most recent call last):\n          File "<stdin>", line 1, in <module>\n        ZeroDivisionError: integer division or modulo by zero\n\n    Additional options:\n\n    `python3`\n        Use Python 3 lexer for code.  Default is ``False``.\n\n        .. versionadded:: 1.0\n    '
    name = 'Python console session'
    aliases = ['pycon']
    mimetypes = ['text/x-python-doctest']

    def __init__(self, **options):
        self.python3 = get_bool_opt(options, 'python3', False)
        Lexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        if self.python3:
            pylexer = Python3Lexer(**self.options)
            tblexer = Python3TracebackLexer(**self.options)
        else:
            pylexer = PythonLexer(**self.options)
            tblexer = PythonTracebackLexer(**self.options)
        curcode = ''
        insertions = []
        curtb = ''
        tbindex = 0
        tb = 0
        for match in line_re.finditer(text):
            line = match.group()
            if line.startswith('>>> ') or line.startswith('... '):
                tb = 0
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, line[:4])]))
                curcode += line[4:]
            elif line.rstrip() == '...' and not tb:
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, '...')]))
                curcode += line[3:]
            else:
                if curcode:
                    for item in do_insertions(insertions, pylexer.get_tokens_unprocessed(curcode)):
                        yield item

                    curcode = ''
                    insertions = []
                if line.startswith('Traceback (most recent call last):') or re.match('  File "[^"]+", line \\d+\\n$', line):
                    tb = 1
                    curtb = line
                    tbindex = match.start()
                else:
                    if line == 'KeyboardInterrupt\n':
                        yield (
                         match.start(), Name.Class, line)
                    else:
                        if tb:
                            curtb += line
                            if not (line.startswith(' ') or line.strip() == '...'):
                                tb = 0
                                for i, t, v in tblexer.get_tokens_unprocessed(curtb):
                                    yield (
                                     tbindex + i, t, v)

                                curtb = ''
                        else:
                            yield (
                             match.start(), Generic.Output, line)

        if curcode:
            for item in do_insertions(insertions, pylexer.get_tokens_unprocessed(curcode)):
                yield item

        if curtb:
            for i, t, v in tblexer.get_tokens_unprocessed(curtb):
                yield (
                 tbindex + i, t, v)


class PythonTracebackLexer(RegexLexer):
    __doc__ = '\n    For Python tracebacks.\n\n    .. versionadded:: 0.7\n    '
    name = 'Python Traceback'
    aliases = ['pytb']
    filenames = ['*.pytb']
    mimetypes = ['text/x-python-traceback']
    tokens = {'root': [
              (
               '^(\\^C)?(Traceback.*\\n)',
               bygroups(Text, Generic.Traceback), 'intb'),
              (
               '^(?=  File "[^"]+", line \\d+)', Generic.Traceback, 'intb'),
              (
               '^.*\\n', Other)], 
     
     'intb': [
              (
               '^(  File )("[^"]+")(, line )(\\d+)(, in )(.+)(\\n)',
               bygroups(Text, Name.Builtin, Text, Number, Text, Name, Text)),
              (
               '^(  File )("[^"]+")(, line )(\\d+)(\\n)',
               bygroups(Text, Name.Builtin, Text, Number, Text)),
              (
               '^(    )(.+)(\\n)',
               bygroups(Text, using(PythonLexer), Text)),
              (
               '^([ \\t]*)(\\.\\.\\.)(\\n)',
               bygroups(Text, Comment, Text)),
              (
               '^([^:]+)(: )(.+)(\\n)',
               bygroups(Generic.Error, Text, Name, Text), '#pop'),
              (
               '^([a-zA-Z_]\\w*)(:?\\n)',
               bygroups(Generic.Error, Text), '#pop')]}


class Python3TracebackLexer(RegexLexer):
    __doc__ = '\n    For Python 3.0 tracebacks, with support for chained exceptions.\n\n    .. versionadded:: 1.0\n    '
    name = 'Python 3.0 Traceback'
    aliases = ['py3tb']
    filenames = ['*.py3tb']
    mimetypes = ['text/x-python3-traceback']
    tokens = {'root': [
              (
               '\\n', Text),
              (
               '^Traceback \\(most recent call last\\):\\n', Generic.Traceback, 'intb'),
              (
               '^During handling of the above exception, another exception occurred:\\n\\n',
               Generic.Traceback),
              (
               '^The above exception was the direct cause of the following exception:\\n\\n',
               Generic.Traceback),
              (
               '^(?=  File "[^"]+", line \\d+)', Generic.Traceback, 'intb')], 
     
     'intb': [
              (
               '^(  File )("[^"]+")(, line )(\\d+)(, in )(.+)(\\n)',
               bygroups(Text, Name.Builtin, Text, Number, Text, Name, Text)),
              (
               '^(  File )("[^"]+")(, line )(\\d+)(\\n)',
               bygroups(Text, Name.Builtin, Text, Number, Text)),
              (
               '^(    )(.+)(\\n)',
               bygroups(Text, using(Python3Lexer), Text)),
              (
               '^([ \\t]*)(\\.\\.\\.)(\\n)',
               bygroups(Text, Comment, Text)),
              (
               '^([^:]+)(: )(.+)(\\n)',
               bygroups(Generic.Error, Text, Name, Text), '#pop'),
              (
               '^([a-zA-Z_]\\w*)(:?\\n)',
               bygroups(Generic.Error, Text), '#pop')]}


class CythonLexer(RegexLexer):
    __doc__ = '\n    For Pyrex and `Cython <http://cython.org>`_ source code.\n\n    .. versionadded:: 1.1\n    '
    name = 'Cython'
    aliases = ['cython', 'pyx', 'pyrex']
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
               '(cdef)(:)', bygroups(Keyword, Punctuation)),
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
                   words(('assert', 'break', 'by', 'continue', 'ctypedef', 'del', 'elif', 'else', 'except',
       'except?', 'exec', 'finally', 'for', 'fused', 'gil', 'global', 'if', 'include',
       'lambda', 'nogil', 'pass', 'print', 'raise', 'return', 'try', 'while', 'yield',
       'as', 'with'), suffix='\\b'),
                   Keyword),
                  (
                   '(DEF|IF|ELIF|ELSE)\\b', Comment.Preproc)], 
     
     'builtins': [
                  (
                   words(('__import__', 'abs', 'all', 'any', 'apply', 'basestring', 'bin', 'bool', 'buffer',
       'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile',
       'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile',
       'exit', 'file', 'filter', 'float', 'frozenset', 'getattr', 'globals', 'hasattr',
       'hash', 'hex', 'id', 'input', 'int', 'intern', 'isinstance', 'issubclass',
       'iter', 'len', 'list', 'locals', 'long', 'map', 'max', 'min', 'next', 'object',
       'oct', 'open', 'ord', 'pow', 'property', 'range', 'raw_input', 'reduce', 'reload',
       'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod',
       'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'unsigned', 'vars',
       'xrange', 'zip'), prefix='(?<!\\.)', suffix='\\b'),
                   Name.Builtin),
                  (
                   '(?<!\\.)(self|None|Ellipsis|NotImplemented|False|True|NULL)\\b',
                   Name.Builtin.Pseudo),
                  (
                   words(('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'DeprecationWarning',
       'EOFError', 'EnvironmentError', 'Exception', 'FloatingPointError', 'FutureWarning',
       'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError',
       'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError',
       'NameError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
       'OverflowWarning', 'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError',
       'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 'SyntaxWarning',
       'SystemError', 'SystemExit', 'TabError', 'TypeError', 'UnboundLocalError',
       'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
       'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError'), prefix='(?<!\\.)', suffix='\\b'),
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
               '@\\w+', Name.Decorator),
              (
               '[a-zA-Z_]\\w*', Name)], 
     
     'funcname': [
                  (
                   '[a-zA-Z_]\\w*', Name.Function, '#pop')], 
     
     'cdef': [
              (
               '(public|readonly|extern|api|inline)\\b', Keyword.Reserved),
              (
               '(struct|enum|union|class)\\b', Keyword),
              (
               '([a-zA-Z_]\\w*)(\\s*)(?=[(:#=]|$)',
               bygroups(Name.Function, Text), '#pop'),
              (
               '([a-zA-Z_]\\w*)(\\s*)(,)',
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
               '[a-zA-Z_]\\w*', Keyword.Type),
              (
               '.', Text)], 
     
     'classname': [
                   (
                    '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     
     'import': [
                (
                 '(\\s+)(as)(\\s+)', bygroups(Text, Keyword, Text)),
                (
                 '[a-zA-Z_][\\w.]*', Name.Namespace),
                (
                 '(\\s*)(,)(\\s*)', bygroups(Text, Operator, Text)),
                default('#pop')], 
     
     'fromimport': [
                    (
                     '(\\s+)(c?import)\\b', bygroups(Text, Keyword), '#pop'),
                    (
                     '[a-zA-Z_.][\\w.]*', Name.Namespace),
                    default('#pop')], 
     
     'stringescape': [
                      (
                       '\\\\([\\\\abfnrtv"\\\']|\\n|N\\{.*?\\}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
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


class DgLexer(RegexLexer):
    __doc__ = '\n    Lexer for `dg <http://pyos.github.com/dg>`_,\n    a functional and object-oriented programming language\n    running on the CPython 3 VM.\n\n    .. versionadded:: 1.6\n    '
    name = 'dg'
    aliases = ['dg']
    filenames = ['*.dg']
    mimetypes = ['text/x-dg']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '#.*?$', Comment.Single),
              (
               '(?i)0b[01]+', Number.Bin),
              (
               '(?i)0o[0-7]+', Number.Oct),
              (
               '(?i)0x[0-9a-f]+', Number.Hex),
              (
               '(?i)[+-]?[0-9]+\\.[0-9]+(e[+-]?[0-9]+)?j?', Number.Float),
              (
               '(?i)[+-]?[0-9]+e[+-]?\\d+j?', Number.Float),
              (
               '(?i)[+-]?[0-9]+j?', Number.Integer),
              (
               "(?i)(br|r?b?)'''", String, combined('stringescape', 'tsqs', 'string')),
              (
               '(?i)(br|r?b?)"""', String, combined('stringescape', 'tdqs', 'string')),
              (
               "(?i)(br|r?b?)'", String, combined('stringescape', 'sqs', 'string')),
              (
               '(?i)(br|r?b?)"', String, combined('stringescape', 'dqs', 'string')),
              (
               "`\\w+'*`", Operator),
              (
               '\\b(and|in|is|or|where)\\b', Operator.Word),
              (
               '[!$%&*+\\-./:<-@\\\\^|~;,]+', Operator),
              (
               words(('bool', 'bytearray', 'bytes', 'classmethod', 'complex', 'dict', "dict'", 'float',
       'frozenset', 'int', 'list', "list'", 'memoryview', 'object', 'property', 'range',
       'set', "set'", 'slice', 'staticmethod', 'str', 'super', 'tuple', "tuple'",
       'type'), prefix='(?<!\\.)', suffix="(?![\\'\\w])"),
               Name.Builtin),
              (
               words(('__import__', 'abs', 'all', 'any', 'bin', 'bind', 'chr', 'cmp', 'compile', 'complex',
       'delattr', 'dir', 'divmod', 'drop', 'dropwhile', 'enumerate', 'eval', 'exhaust',
       'filter', 'flip', 'foldl1?', 'format', 'fst', 'getattr', 'globals', 'hasattr',
       'hash', 'head', 'hex', 'id', 'init', 'input', 'isinstance', 'issubclass',
       'iter', 'iterate', 'last', 'len', 'locals', 'map', 'max', 'min', 'next', 'oct',
       'open', 'ord', 'pow', 'print', 'repr', 'reversed', 'round', 'setattr', 'scanl1?',
       'snd', 'sorted', 'sum', 'tail', 'take', 'takewhile', 'vars', 'zip'), prefix='(?<!\\.)', suffix="(?![\\'\\w])"),
               Name.Builtin),
              (
               "(?<!\\.)(self|Ellipsis|NotImplemented|None|True|False)(?!['\\w])",
               Name.Builtin.Pseudo),
              (
               "(?<!\\.)[A-Z]\\w*(Error|Exception|Warning)'*(?!['\\w])",
               Name.Exception),
              (
               "(?<!\\.)(Exception|GeneratorExit|KeyboardInterrupt|StopIteration|SystemExit)(?!['\\w])",
               Name.Exception),
              (
               "(?<![\\w.])(except|finally|for|if|import|not|otherwise|raise|subclass|while|with|yield)(?!['\\w])",
               Keyword.Reserved),
              (
               "[A-Z_]+'*(?!['\\w])", Name),
              (
               "[A-Z]\\w+'*(?!['\\w])", Keyword.Type),
              (
               "\\w+'*", Name),
              (
               '[()]', Punctuation),
              (
               '.', Error)], 
     
     'stringescape': [
                      (
                       '\\\\([\\\\abfnrtv"\\\']|\\n|N\\{.*?\\}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
                       String.Escape)], 
     
     'string': [
                (
                 '%(\\(\\w+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[diouxXeEfFgGcrs%]',
                 String.Interpol),
                (
                 '[^\\\\\\\'"%\\n]+', String),
                (
                 '[\\\'"\\\\]', String),
                (
                 '%', String),
                (
                 '\\n', String)], 
     
     'dqs': [
             (
              '"', String, '#pop')], 
     
     'sqs': [
             (
              "'", String, '#pop')], 
     
     'tdqs': [
              (
               '"""', String, '#pop')], 
     
     'tsqs': [
              (
               "'''", String, '#pop')]}


class NumPyLexer(PythonLexer):
    __doc__ = '\n    A Python lexer recognizing Numerical Python builtins.\n\n    .. versionadded:: 0.10\n    '
    name = 'NumPy'
    aliases = ['numpy']
    mimetypes = []
    filenames = []
    EXTRA_KEYWORDS = set(('abs', 'absolute', 'accumulate', 'add', 'alen', 'all', 'allclose',
                          'alltrue', 'alterdot', 'amax', 'amin', 'angle', 'any',
                          'append', 'apply_along_axis', 'apply_over_axes', 'arange',
                          'arccos', 'arccosh', 'arcsin', 'arcsinh', 'arctan', 'arctan2',
                          'arctanh', 'argmax', 'argmin', 'argsort', 'argwhere', 'around',
                          'array', 'array2string', 'array_equal', 'array_equiv',
                          'array_repr', 'array_split', 'array_str', 'arrayrange',
                          'asanyarray', 'asarray', 'asarray_chkfinite', 'ascontiguousarray',
                          'asfarray', 'asfortranarray', 'asmatrix', 'asscalar', 'astype',
                          'atleast_1d', 'atleast_2d', 'atleast_3d', 'average', 'bartlett',
                          'base_repr', 'beta', 'binary_repr', 'bincount', 'binomial',
                          'bitwise_and', 'bitwise_not', 'bitwise_or', 'bitwise_xor',
                          'blackman', 'bmat', 'broadcast', 'byte_bounds', 'bytes',
                          'byteswap', 'c_', 'can_cast', 'ceil', 'choose', 'clip',
                          'column_stack', 'common_type', 'compare_chararrays', 'compress',
                          'concatenate', 'conj', 'conjugate', 'convolve', 'copy',
                          'corrcoef', 'correlate', 'cos', 'cosh', 'cov', 'cross',
                          'cumprod', 'cumproduct', 'cumsum', 'delete', 'deprecate',
                          'diag', 'diagflat', 'diagonal', 'diff', 'digitize', 'disp',
                          'divide', 'dot', 'dsplit', 'dstack', 'dtype', 'dump', 'dumps',
                          'ediff1d', 'empty', 'empty_like', 'equal', 'exp', 'expand_dims',
                          'expm1', 'extract', 'eye', 'fabs', 'fastCopyAndTranspose',
                          'fft', 'fftfreq', 'fftshift', 'fill', 'finfo', 'fix', 'flat',
                          'flatnonzero', 'flatten', 'fliplr', 'flipud', 'floor',
                          'floor_divide', 'fmod', 'frexp', 'fromarrays', 'frombuffer',
                          'fromfile', 'fromfunction', 'fromiter', 'frompyfunc', 'fromstring',
                          'generic', 'get_array_wrap', 'get_include', 'get_numarray_include',
                          'get_numpy_include', 'get_printoptions', 'getbuffer', 'getbufsize',
                          'geterr', 'geterrcall', 'geterrobj', 'getfield', 'gradient',
                          'greater', 'greater_equal', 'gumbel', 'hamming', 'hanning',
                          'histogram', 'histogram2d', 'histogramdd', 'hsplit', 'hstack',
                          'hypot', 'i0', 'identity', 'ifft', 'imag', 'index_exp',
                          'indices', 'inf', 'info', 'inner', 'insert', 'int_asbuffer',
                          'interp', 'intersect1d', 'intersect1d_nu', 'inv', 'invert',
                          'iscomplex', 'iscomplexobj', 'isfinite', 'isfortran', 'isinf',
                          'isnan', 'isneginf', 'isposinf', 'isreal', 'isrealobj',
                          'isscalar', 'issctype', 'issubclass_', 'issubdtype', 'issubsctype',
                          'item', 'itemset', 'iterable', 'ix_', 'kaiser', 'kron',
                          'ldexp', 'left_shift', 'less', 'less_equal', 'lexsort',
                          'linspace', 'load', 'loads', 'loadtxt', 'log', 'log10',
                          'log1p', 'log2', 'logical_and', 'logical_not', 'logical_or',
                          'logical_xor', 'logspace', 'lstsq', 'mat', 'matrix', 'max',
                          'maximum', 'maximum_sctype', 'may_share_memory', 'mean',
                          'median', 'meshgrid', 'mgrid', 'min', 'minimum', 'mintypecode',
                          'mod', 'modf', 'msort', 'multiply', 'nan', 'nan_to_num',
                          'nanargmax', 'nanargmin', 'nanmax', 'nanmin', 'nansum',
                          'ndenumerate', 'ndim', 'ndindex', 'negative', 'newaxis',
                          'newbuffer', 'newbyteorder', 'nonzero', 'not_equal', 'obj2sctype',
                          'ogrid', 'ones', 'ones_like', 'outer', 'permutation', 'piecewise',
                          'pinv', 'pkgload', 'place', 'poisson', 'poly', 'poly1d',
                          'polyadd', 'polyder', 'polydiv', 'polyfit', 'polyint',
                          'polymul', 'polysub', 'polyval', 'power', 'prod', 'product',
                          'ptp', 'put', 'putmask', 'r_', 'randint', 'random_integers',
                          'random_sample', 'ranf', 'rank', 'ravel', 'real', 'real_if_close',
                          'recarray', 'reciprocal', 'reduce', 'remainder', 'repeat',
                          'require', 'reshape', 'resize', 'restoredot', 'right_shift',
                          'rint', 'roll', 'rollaxis', 'roots', 'rot90', 'round',
                          'round_', 'row_stack', 's_', 'sample', 'savetxt', 'sctype2char',
                          'searchsorted', 'seed', 'select', 'set_numeric_ops', 'set_printoptions',
                          'set_string_function', 'setbufsize', 'setdiff1d', 'seterr',
                          'seterrcall', 'seterrobj', 'setfield', 'setflags', 'setmember1d',
                          'setxor1d', 'shape', 'show_config', 'shuffle', 'sign',
                          'signbit', 'sin', 'sinc', 'sinh', 'size', 'slice', 'solve',
                          'sometrue', 'sort', 'sort_complex', 'source', 'split',
                          'sqrt', 'square', 'squeeze', 'standard_normal', 'std',
                          'subtract', 'sum', 'svd', 'swapaxes', 'take', 'tan', 'tanh',
                          'tensordot', 'test', 'tile', 'tofile', 'tolist', 'tostring',
                          'trace', 'transpose', 'trapz', 'tri', 'tril', 'trim_zeros',
                          'triu', 'true_divide', 'typeDict', 'typename', 'uniform',
                          'union1d', 'unique', 'unique1d', 'unravel_index', 'unwrap',
                          'vander', 'var', 'vdot', 'vectorize', 'view', 'vonmises',
                          'vsplit', 'vstack', 'weibull', 'where', 'who', 'zeros',
                          'zeros_like'))

    def get_tokens_unprocessed(self, text):
        for index, token, value in PythonLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield (
                 index, Keyword.Pseudo, value)
            else:
                yield (
                 index, token, value)

    def analyse_text(text):
        return (shebang_matches(text, 'pythonw?(2(\\.\\d)?)?') or 'import ' in text[:1000]) and ('import numpy' in text or 'from numpy import' in text)