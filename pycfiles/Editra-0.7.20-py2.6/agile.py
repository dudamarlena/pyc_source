# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/agile.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.agile
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for agile languages.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, ExtendedRegexLexer, LexerContext, include, combined, do_insertions, bygroups, using
from pygments.token import Error, Text, Other, Comment, Operator, Keyword, Name, String, Number, Generic, Punctuation
from pygments.util import get_bool_opt, get_list_opt, shebang_matches
from pygments import unistring as uni
__all__ = [
 'PythonLexer', 'PythonConsoleLexer', 'PythonTracebackLexer',
 'RubyLexer', 'RubyConsoleLexer', 'PerlLexer', 'LuaLexer',
 'MiniDLexer', 'IoLexer', 'TclLexer', 'ClojureLexer',
 'Python3Lexer', 'Python3TracebackLexer', 'FactorLexer', 'IokeLexer']
from pygments.lexers.functional import SchemeLexer
line_re = re.compile('.*?\n')

class PythonLexer(RegexLexer):
    """
    For `Python <http://www.python.org>`_ source code.
    """
    name = 'Python'
    aliases = ['python', 'py']
    filenames = ['*.py', '*.pyw', '*.sc', 'SConstruct', 'SConscript', '*.tac']
    mimetypes = ['text/x-python', 'application/x-python']
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
               '(def)((?:\\s|\\\\\\s)+)', bygroups(Keyword, Text), 'funcname'),
              (
               '(class)((?:\\s|\\\\\\s)+)', bygroups(Keyword, Text), 'classname'),
              (
               '(from)((?:\\s|\\\\\\s)+)', bygroups(Keyword.Namespace, Text), 'fromimport'),
              (
               '(import)((?:\\s|\\\\\\s)+)', bygroups(Keyword.Namespace, Text), 'import'),
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
                   '(assert|break|continue|del|elif|else|except|exec|finally|for|global|if|lambda|pass|print|raise|return|try|while|yield|as|with)\\b',
                   Keyword)], 
       'builtins': [
                  (
                   '(?<!\\.)(__import__|abs|all|any|apply|basestring|bin|bool|buffer|bytearray|bytes|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|exit|file|filter|float|frozenset|getattr|globals|hasattr|hash|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|min|next|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\\b',
                   Name.Builtin),
                  (
                   '(?<!\\.)(self|None|Ellipsis|NotImplemented|False|True)\\b',
                   Name.Builtin.Pseudo),
                  (
                   '(?<!\\.)(ArithmeticError|AssertionError|AttributeError|BaseException|DeprecationWarning|EOFError|EnvironmentError|Exception|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError|ImportWarning|IndentationError|IndexError|KeyError|KeyboardInterrupt|LookupError|MemoryError|NameError|NotImplemented|NotImplementedError|OSError|OverflowError|OverflowWarning|PendingDeprecationWarning|ReferenceError|RuntimeError|RuntimeWarning|StandardError|StopIteration|SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|VMSError|Warning|WindowsError|ZeroDivisionError)\\b',
                   Name.Exception)], 
       'numbers': [
                 (
                  '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
                 (
                  '\\d+[eE][+-]?[0-9]+', Number.Float),
                 (
                  '0[0-7]+', Number.Oct),
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
               '@[a-zA-Z0-9_.]+', Name.Decorator),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Name)], 
       'funcname': [
                  (
                   '[a-zA-Z_][a-zA-Z0-9_]*', Name.Function, '#pop')], 
       'classname': [
                   (
                    '[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop')], 
       'import': [
                (
                 '((?:\\s|\\\\\\s)+)(as)((?:\\s|\\\\\\s)+)',
                 bygroups(Text, Keyword.Namespace, Text)),
                (
                 '[a-zA-Z_][a-zA-Z0-9_.]*', Name.Namespace),
                (
                 '(\\s*)(,)(\\s*)', bygroups(Text, Operator, Text)),
                (
                 '', Text, '#pop')], 
       'fromimport': [
                    (
                     '((?:\\s|\\\\\\s)+)(import)\\b', bygroups(Text, Keyword.Namespace), '#pop'),
                    (
                     '[a-zA-Z_.][a-zA-Z0-9_.]*', Name.Namespace)], 
       'stringescape': [
                      (
                       '\\\\([\\\\abfnrtv"\\\']|\\n|N{.*?}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})',
                       String.Escape)], 
       'strings': [
                 (
                  '%(\\([a-zA-Z0-9_]+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[diouxXeEfFgGcrs%]',
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


class Python3Lexer(RegexLexer):
    """
    For `Python <http://www.python.org>`_ source code (version 3.0).

    *New in Pygments 0.10.*
    """
    name = 'Python 3'
    aliases = ['python3', 'py3']
    filenames = []
    mimetypes = ['text/x-python3', 'application/x-python3']
    flags = re.MULTILINE | re.UNICODE
    uni_name = '[%s][%s]*' % (uni.xid_start, uni.xid_continue)
    tokens = PythonLexer.tokens.copy()
    tokens['keywords'] = [
     (
      '(assert|break|continue|del|elif|else|except|finally|for|global|if|lambda|pass|raise|return|try|while|yield|as|with|True|False|None)\\b',
      Keyword)]
    tokens['builtins'] = [
     (
      '(?<!\\.)(__import__|abs|all|any|bin|bool|bytearray|bytes|chr|classmethod|cmp|compile|complex|delattr|dict|dir|divmod|enumerate|eval|filter|float|format|frozenset|getattr|globals|hasattr|hash|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip)\\b',
      Name.Builtin),
     (
      '(?<!\\.)(self|Ellipsis|NotImplemented)\\b', Name.Builtin.Pseudo),
     (
      '(?<!\\.)(ArithmeticError|AssertionError|AttributeError|BaseException|BufferError|BytesWarning|DeprecationWarning|EOFError|EnvironmentError|Exception|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError|ImportWarning|IndentationError|IndexError|KeyError|KeyboardInterrupt|LookupError|MemoryError|NameError|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning|ReferenceError|RuntimeError|RuntimeWarning|StopIteration|SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|VMSError|Warning|WindowsError|ZeroDivisionError)\\b',
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
      '@[a-zA-Z0-9_]+', Name.Decorator),
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
     (
      '', Text, '#pop')]
    tokens['fromimport'] = [
     (
      '(\\s+)(import)\\b', bygroups(Text, Keyword), '#pop'),
     (
      '\\.', Name.Namespace),
     (
      uni_name, Name.Namespace)]
    tokens['strings'] = [
     (
      '[^\\\\\\\'"%\\n]+', String),
     (
      '[\\\'"\\\\]', String),
     (
      '%', String)]

    def analyse_text(text):
        return shebang_matches(text, 'pythonw?3(\\.\\d)?')


class PythonConsoleLexer(Lexer):
    """
    For Python console output or doctests, such as:

    .. sourcecode:: pycon

        >>> a = 'foo'
        >>> print a
        foo
        >>> 1 / 0
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        ZeroDivisionError: integer division or modulo by zero

    Additional options:

    `python3`
        Use Python 3 lexer for code.  Default is ``False``.
        *New in Pygments 1.0.*
    """
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
                elif line == 'KeyboardInterrupt\n':
                    yield (
                     match.start(), Name.Class, line)
                elif tb:
                    curtb += line
                    if not (line.startswith(' ') or line.strip() == '...'):
                        tb = 0
                        for (i, t, v) in tblexer.get_tokens_unprocessed(curtb):
                            yield (
                             tbindex + i, t, v)

                else:
                    yield (
                     match.start(), Generic.Output, line)

        if curcode:
            for item in do_insertions(insertions, pylexer.get_tokens_unprocessed(curcode)):
                yield item


class PythonTracebackLexer(RegexLexer):
    """
    For Python tracebacks.

    *New in Pygments 0.7.*
    """
    name = 'Python Traceback'
    aliases = ['pytb']
    filenames = ['*.pytb']
    mimetypes = ['text/x-python-traceback']
    tokens = {'root': [
              (
               '^Traceback \\(most recent call last\\):\\n', Generic.Traceback, 'intb'),
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
               '^([ \\t]*)(...)(\\n)',
               bygroups(Text, Comment, Text)),
              (
               '^(.+)(: )(.+)(\\n)',
               bygroups(Generic.Error, Text, Name, Text), '#pop'),
              (
               '^([a-zA-Z_][a-zA-Z0-9_]*)(:?\\n)',
               bygroups(Generic.Error, Text), '#pop')]}


class Python3TracebackLexer(RegexLexer):
    """
    For Python 3.0 tracebacks, with support for chained exceptions.

    *New in Pygments 1.0.*
    """
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
               Generic.Traceback)], 
       'intb': [
              (
               '^(  File )("[^"]+")(, line )(\\d+)(, in )(.+)(\\n)',
               bygroups(Text, Name.Builtin, Text, Number, Text, Name, Text)),
              (
               '^(    )(.+)(\\n)',
               bygroups(Text, using(Python3Lexer), Text)),
              (
               '^([ \\t]*)(...)(\\n)',
               bygroups(Text, Comment, Text)),
              (
               '^(.+)(: )(.+)(\\n)',
               bygroups(Generic.Error, Text, Name, Text), '#pop'),
              (
               '^([a-zA-Z_][a-zA-Z0-9_]*)(:?\\n)',
               bygroups(Generic.Error, Text), '#pop')]}


class RubyLexer(ExtendedRegexLexer):
    """
    For `Ruby <http://www.ruby-lang.org>`_ source code.
    """
    name = 'Ruby'
    aliases = ['rb', 'ruby', 'duby']
    filenames = ['*.rb', '*.rbw', 'Rakefile', '*.rake', '*.gemspec',
     '*.rbx', '*.duby']
    mimetypes = ['text/x-ruby', 'application/x-ruby']
    flags = re.DOTALL | re.MULTILINE

    def heredoc_callback(self, match, ctx):
        start = match.start(1)
        yield (start, Operator, match.group(1))
        yield (match.start(2), String.Heredoc, match.group(2))
        yield (match.start(3), Name.Constant, match.group(3))
        yield (match.start(4), String.Heredoc, match.group(4))
        heredocstack = ctx.__dict__.setdefault('heredocstack', [])
        outermost = not bool(heredocstack)
        heredocstack.append((match.group(1) == '<<-', match.group(3)))
        ctx.pos = match.start(5)
        ctx.end = match.end(5)
        for (i, t, v) in self.get_tokens_unprocessed(context=ctx):
            yield (i, t, v)

        ctx.pos = match.end()
        if outermost:
            for (tolerant, hdname) in heredocstack:
                lines = []
                for match in line_re.finditer(ctx.text, ctx.pos):
                    if tolerant:
                        check = match.group().strip()
                    else:
                        check = match.group().rstrip()
                    if check == hdname:
                        for amatch in lines:
                            yield (
                             amatch.start(), String.Heredoc, amatch.group())

                        yield (
                         match.start(), Name.Constant, match.group())
                        ctx.pos = match.end()
                        break
                    else:
                        lines.append(match)
                else:
                    for amatch in lines:
                        yield (
                         amatch.start(), Error, amatch.group())

            ctx.end = len(ctx.text)
            del heredocstack[:]

    def gen_rubystrings_rules():

        def intp_regex_callback(self, match, ctx):
            yield (
             match.start(1), String.Regex, match.group(1))
            nctx = LexerContext(match.group(3), 0, ['interpolated-regex'])
            for (i, t, v) in self.get_tokens_unprocessed(context=nctx):
                yield (
                 match.start(3) + i, t, v)

            yield (
             match.start(4), String.Regex, match.group(4))
            ctx.pos = match.end()

        def intp_string_callback(self, match, ctx):
            yield (
             match.start(1), String.Other, match.group(1))
            nctx = LexerContext(match.group(3), 0, ['interpolated-string'])
            for (i, t, v) in self.get_tokens_unprocessed(context=nctx):
                yield (
                 match.start(3) + i, t, v)

            yield (
             match.start(4), String.Other, match.group(4))
            ctx.pos = match.end()

        states = {}
        states['strings'] = [
         (
          '\\:([a-zA-Z_][\\w_]*[\\!\\?]?|\\*\\*?|[-+]@?|[/%&|^`~]|\\[\\]=?|<<|>>|<=?>|>=?|===?)',
          String.Symbol),
         (
          ":'(\\\\\\\\|\\\\'|[^'])*'", String.Symbol),
         (
          "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
         (
          ':"', String.Symbol, 'simple-sym'),
         (
          '"', String.Double, 'simple-string'),
         (
          '(?<!\\.)`', String.Backtick, 'simple-backtick')]
        for (name, ttype, end) in (('string', String.Double, '"'),
         (
          'sym', String.Symbol, '"'),
         (
          'backtick', String.Backtick, '`')):
            states['simple-' + name] = [include('string-intp-escaped'),
             (
              '[^\\\\%s#]+' % end, ttype),
             (
              '[\\\\#]', ttype),
             (
              end, ttype, '#pop')]

        for (lbrace, rbrace, name) in (('\\{', '\\}', 'cb'),
         ('\\[', '\\]', 'sb'),
         ('\\(', '\\)', 'pa'),
         ('<', '>', 'ab')):
            states[name + '-intp-string'] = [('\\\\[\\\\' + lbrace + rbrace + ']', String.Other),
             (
              '(?<!\\\\)' + lbrace, String.Other, '#push'),
             (
              '(?<!\\\\)' + rbrace, String.Other, '#pop'),
             include('string-intp-escaped'),
             (
              '[\\\\#' + lbrace + rbrace + ']', String.Other),
             (
              '[^\\\\#' + lbrace + rbrace + ']+', String.Other)]
            states['strings'].append(('%[QWx]?' + lbrace, String.Other,
             name + '-intp-string'))
            states[name + '-string'] = [
             (
              '\\\\[\\\\' + lbrace + rbrace + ']', String.Other),
             (
              '(?<!\\\\)' + lbrace, String.Other, '#push'),
             (
              '(?<!\\\\)' + rbrace, String.Other, '#pop'),
             (
              '[\\\\#' + lbrace + rbrace + ']', String.Other),
             (
              '[^\\\\#' + lbrace + rbrace + ']+', String.Other)]
            states['strings'].append(('%[qsw]' + lbrace, String.Other,
             name + '-string'))
            states[name + '-regex'] = [
             (
              '\\\\[\\\\' + lbrace + rbrace + ']', String.Regex),
             (
              '(?<!\\\\)' + lbrace, String.Regex, '#push'),
             (
              '(?<!\\\\)' + rbrace + '[mixounse]*', String.Regex, '#pop'),
             include('string-intp'),
             (
              '[\\\\#' + lbrace + rbrace + ']', String.Regex),
             (
              '[^\\\\#' + lbrace + rbrace + ']+', String.Regex)]
            states['strings'].append(('%r' + lbrace, String.Regex,
             name + '-regex'))

        states['strings'] += [
         (
          '(%r([^a-zA-Z0-9]))((?:\\\\\\2|(?!\\2).)*)(\\2[mixounse]*)',
          intp_regex_callback),
         (
          '%[qsw]([^a-zA-Z0-9])((?:\\\\\\1|(?!\\1).)*)\\1', String.Other),
         (
          '(%[QWx]([^a-zA-Z0-9]))((?:\\\\\\2|(?!\\2).)*)(\\2)',
          intp_string_callback),
         (
          '(?<=[-+/*%=<>&!^|~,(])(\\s*)(%([\\t ])(?:(?:\\\\\\3|(?!\\3).)*)\\3)',
          bygroups(Text, String.Other, None)),
         (
          '^(\\s*)(%([\\t ])(?:(?:\\\\\\3|(?!\\3).)*)\\3)',
          bygroups(Text, String.Other, None)),
         (
          '(%([^a-zA-Z0-9\\s]))((?:\\\\\\2|(?!\\2).)*)(\\2)',
          intp_string_callback)]
        return states

    tokens = {'root': [
              (
               '#.*?$', Comment.Single),
              (
               '=begin\\s.*?\\n=end', Comment.Multiline),
              (
               '(BEGIN|END|alias|begin|break|case|defined\\?|do|else|elsif|end|ensure|for|if|in|next|redo|rescue|raise|retry|return|super|then|undef|unless|until|when|while|yield)\\b',
               Keyword),
              (
               '(module)(\\s+)([a-zA-Z_][a-zA-Z0-9_]*(::[a-zA-Z_][a-zA-Z0-9_]*)*)',
               bygroups(Keyword, Text, Name.Namespace)),
              (
               '(def)(\\s+)', bygroups(Keyword, Text), 'funcname'),
              (
               'def(?=[*%&^`~+-/\\[<>=])', Keyword, 'funcname'),
              (
               '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
              (
               '(initialize|new|loop|include|extend|raise|attr_reader|attr_writer|attr_accessor|attr|catch|throw|private|module_function|public|protected|true|false|nil)\\b',
               Keyword.Pseudo),
              (
               '(not|and|or)\\b', Operator.Word),
              (
               '(autoload|block_given|const_defined|eql|equal|frozen|include|instance_of|is_a|iterator|kind_of|method_defined|nil|private_method_defined|protected_method_defined|public_method_defined|respond_to|tainted)\\?',
               Name.Builtin),
              (
               '(chomp|chop|exit|gsub|sub)!', Name.Builtin),
              (
               '(?<!\\.)(Array|Float|Integer|String|__id__|__send__|abort|ancestors|at_exit|autoload|binding|callcc|caller|catch|chomp|chop|class_eval|class_variables|clone|const_defined\\?|const_get|const_missing|const_set|constants|display|dup|eval|exec|exit|extend|fail|fork|format|freeze|getc|gets|global_variables|gsub|hash|id|included_modules|inspect|instance_eval|instance_method|instance_methods|instance_variable_get|instance_variable_set|instance_variables|lambda|load|local_variables|loop|method|method_missing|methods|module_eval|name|object_id|open|p|print|printf|private_class_method|private_instance_methods|private_methods|proc|protected_instance_methods|protected_methods|public_class_method|public_instance_methods|public_methods|putc|puts|raise|rand|readline|readlines|require|scan|select|self|send|set_trace_func|singleton_methods|sleep|split|sprintf|srand|sub|syscall|system|taint|test|throw|to_a|to_s|trace_var|trap|untaint|untrace_var|warn)\\b',
               Name.Builtin),
              (
               '__(FILE|LINE)__\\b', Name.Builtin.Pseudo),
              (
               '(?<!\\w)(<<-?)(["`\\\']?)([a-zA-Z_]\\w*)(\\2)(.*?\\n)', heredoc_callback),
              (
               '(<<-?)("|\\\')()(\\2)(.*?\\n)', heredoc_callback),
              (
               '__END__', Comment.Preproc, 'end-part'),
              (
               '(?:^|(?<=[=<>~!])|(?<=(?:\\s|;)when\\s)|(?<=(?:\\s|;)or\\s)|(?<=(?:\\s|;)and\\s)|(?<=(?:\\s|;|\\.)index\\s)|(?<=(?:\\s|;|\\.)scan\\s)|(?<=(?:\\s|;|\\.)sub\\s)|(?<=(?:\\s|;|\\.)sub!\\s)|(?<=(?:\\s|;|\\.)gsub\\s)|(?<=(?:\\s|;|\\.)gsub!\\s)|(?<=(?:\\s|;|\\.)match\\s)|(?<=(?:\\s|;)if\\s)|(?<=(?:\\s|;)elsif\\s)|(?<=^when\\s)|(?<=^index\\s)|(?<=^scan\\s)|(?<=^sub\\s)|(?<=^gsub\\s)|(?<=^sub!\\s)|(?<=^gsub!\\s)|(?<=^match\\s)|(?<=^if\\s)|(?<=^elsif\\s))(\\s*)(/)',
               bygroups(Text, String.Regex), 'multiline-regex'),
              (
               '(?<=\\(|,)/', String.Regex, 'multiline-regex'),
              (
               '(\\s+)(/[^\\s=])', String.Regex, 'multiline-regex'),
              (
               '(0_?[0-7]+(?:_[0-7]+)*)(\\s*)([/?])?',
               bygroups(Number.Oct, Text, Operator)),
              (
               '(0x[0-9A-Fa-f]+(?:_[0-9A-Fa-f]+)*)(\\s*)([/?])?',
               bygroups(Number.Hex, Text, Operator)),
              (
               '(0b[01]+(?:_[01]+)*)(\\s*)([/?])?',
               bygroups(Number.Bin, Text, Operator)),
              (
               '([\\d]+(?:_\\d+)*)(\\s*)([/?])?',
               bygroups(Number.Integer, Text, Operator)),
              (
               '@@[a-zA-Z_][a-zA-Z0-9_]*', Name.Variable.Class),
              (
               '@[a-zA-Z_][a-zA-Z0-9_]*', Name.Variable.Instance),
              (
               '\\$[a-zA-Z0-9_]+', Name.Variable.Global),
              (
               '\\$[!@&`\\\'+~=/\\\\,;.<>_*$?:"]', Name.Variable.Global),
              (
               '\\$-[0adFiIlpvw]', Name.Variable.Global),
              (
               '::', Operator),
              include('strings'),
              (
               '\\?(\\\\[MC]-)*(\\\\([\\\\abefnrstv#"\\\']|x[a-fA-F0-9]{1,2}|[0-7]{1,3})|\\S)(?!\\w)',
               String.Char),
              (
               '[A-Z][a-zA-Z0-9_]+', Name.Constant),
              (
               '(\\.|::)([a-zA-Z_]\\w*[\\!\\?]?|[*%&^`~+-/\\[<>=])',
               bygroups(Operator, Name)),
              (
               '[a-zA-Z_][\\w_]*[\\!\\?]?', Name),
              (
               '(\\[|\\]|\\*\\*|<<?|>>?|>=|<=|<=>|=~|={3}|!~|&&?|\\|\\||\\.{1,3})',
               Operator),
              (
               '[-+/*%=<>&!^|~]=?', Operator),
              (
               '[(){};,/?:\\\\]', Punctuation),
              (
               '\\s+', Text)], 
       'funcname': [
                  (
                   '\\(', Punctuation, 'defexpr'),
                  (
                   '(?:([a-zA-Z_][a-zA-Z0-9_]*)(\\.))?([a-zA-Z_][\\w_]*[\\!\\?]?|\\*\\*?|[-+]@?|[/%&|^`~]|\\[\\]=?|<<|>>|<=?>|>=?|===?)',
                   bygroups(Name.Class, Operator, Name.Function), '#pop'),
                  (
                   '', Text, '#pop')], 
       'classname': [
                   (
                    '\\(', Punctuation, 'defexpr'),
                   (
                    '<<', Operator, '#pop'),
                   (
                    '[A-Z_][\\w_]*', Name.Class, '#pop'),
                   (
                    '', Text, '#pop')], 
       'defexpr': [
                 (
                  '(\\))(\\.|::)?', bygroups(Punctuation, Operator), '#pop'),
                 (
                  '\\(', Operator, '#push'),
                 include('root')], 
       'in-intp': [
                 (
                  '}', String.Interpol, '#pop'),
                 include('root')], 
       'string-intp': [
                     (
                      '#{', String.Interpol, 'in-intp'),
                     (
                      '#@@?[a-zA-Z_][a-zA-Z0-9_]*', String.Interpol),
                     (
                      '#\\$[a-zA-Z_][a-zA-Z0-9_]*', String.Interpol)], 
       'string-intp-escaped': [
                             include('string-intp'),
                             (
                              '\\\\([\\\\abefnrstv#"\\\']|x[a-fA-F0-9]{1,2}|[0-7]{1,3})', String.Escape)], 
       'interpolated-regex': [
                            include('string-intp'),
                            (
                             '[\\\\#]', String.Regex),
                            (
                             '[^\\\\#]+', String.Regex)], 
       'interpolated-string': [
                             include('string-intp'),
                             (
                              '[\\\\#]', String.Other),
                             (
                              '[^\\\\#]+', String.Other)], 
       'multiline-regex': [
                         include('string-intp'),
                         (
                          '\\\\\\\\', String.Regex),
                         (
                          '\\\\/', String.Regex),
                         (
                          '[\\\\#]', String.Regex),
                         (
                          '[^\\\\/#]+', String.Regex),
                         (
                          '/[mixounse]*', String.Regex, '#pop')], 
       'end-part': [
                  (
                   '.+', Comment.Preproc, '#pop')]}
    tokens.update(gen_rubystrings_rules())

    def analyse_text(text):
        return shebang_matches(text, 'ruby(1\\.\\d)?')


class RubyConsoleLexer(Lexer):
    """
    For Ruby interactive console (**irb**) output like:

    .. sourcecode:: rbcon

        irb(main):001:0> a = 1
        => 1
        irb(main):002:0> puts a
        1
        => nil
    """
    name = 'Ruby irb session'
    aliases = ['rbcon', 'irb']
    mimetypes = ['text/x-ruby-shellsession']
    _prompt_re = re.compile('irb\\([a-zA-Z_][a-zA-Z0-9_]*\\):\\d{3}:\\d+[>*"\'] |>> |\\?> ')

    def get_tokens_unprocessed(self, text):
        rblexer = RubyLexer(**self.options)
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
                    for item in do_insertions(insertions, rblexer.get_tokens_unprocessed(curcode)):
                        yield item

                    curcode = ''
                    insertions = []
                yield (
                 match.start(), Generic.Output, line)

        if curcode:
            for item in do_insertions(insertions, rblexer.get_tokens_unprocessed(curcode)):
                yield item

        return


class PerlLexer(RegexLexer):
    """
    For `Perl <http://www.perl.org>`_ source code.
    """
    name = 'Perl'
    aliases = ['perl', 'pl']
    filenames = ['*.pl', '*.pm']
    mimetypes = ['text/x-perl', 'application/x-perl']
    flags = re.DOTALL | re.MULTILINE
    tokens = {'balanced-regex': [
                        (
                         '/(\\\\\\\\|\\\\/|[^/])*/[egimosx]*', String.Regex, '#pop'),
                        (
                         '!(\\\\\\\\|\\\\!|[^!])*![egimosx]*', String.Regex, '#pop'),
                        (
                         '\\\\(\\\\\\\\|[^\\\\])*\\\\[egimosx]*', String.Regex, '#pop'),
                        (
                         '{(\\\\\\\\|\\\\}|[^}])*}[egimosx]*', String.Regex, '#pop'),
                        (
                         '<(\\\\\\\\|\\\\>|[^>])*>[egimosx]*', String.Regex, '#pop'),
                        (
                         '\\[(\\\\\\\\|\\\\\\]|[^\\]])*\\][egimosx]*', String.Regex, '#pop'),
                        (
                         '\\((\\\\\\\\|\\\\\\)|[^\\)])*\\)[egimosx]*', String.Regex, '#pop'),
                        (
                         '@(\\\\\\\\|\\\\\\@|[^\\@])*@[egimosx]*', String.Regex, '#pop'),
                        (
                         '%(\\\\\\\\|\\\\\\%|[^\\%])*%[egimosx]*', String.Regex, '#pop'),
                        (
                         '\\$(\\\\\\\\|\\\\\\$|[^\\$])*\\$[egimosx]*', String.Regex, '#pop')], 
       'root': [
              (
               '\\#.*?$', Comment.Single),
              (
               '^=[a-zA-Z0-9]+\\s+.*?\\n=cut', Comment.Multiline),
              (
               '(case|continue|do|else|elsif|for|foreach|if|last|my|next|our|redo|reset|then|unless|until|while|use|print|new|BEGIN|CHECK|INIT|END|return)\\b',
               Keyword),
              (
               '(format)(\\s+)([a-zA-Z0-9_]+)(\\s*)(=)(\\s*\\n)',
               bygroups(Keyword, Text, Name, Text, Punctuation, Text), 'format'),
              (
               '(eq|lt|gt|le|ge|ne|not|and|or|cmp)\\b', Operator.Word),
              (
               's/(\\\\\\\\|\\\\/|[^/])*/(\\\\\\\\|\\\\/|[^/])*/[egimosx]*', String.Regex),
              (
               's!(\\\\\\\\|\\\\!|[^!])*!(\\\\\\\\|\\\\!|[^!])*![egimosx]*', String.Regex),
              (
               's\\\\(\\\\\\\\|[^\\\\])*\\\\(\\\\\\\\|[^\\\\])*\\\\[egimosx]*', String.Regex),
              (
               's@(\\\\\\\\|\\\\@|[^@])*@(\\\\\\\\|\\\\@|[^@])*@[egimosx]*', String.Regex),
              (
               's%(\\\\\\\\|\\\\%|[^%])*%(\\\\\\\\|\\\\%|[^%])*%[egimosx]*', String.Regex),
              (
               's{(\\\\\\\\|\\\\}|[^}])*}\\s*', String.Regex, 'balanced-regex'),
              (
               's<(\\\\\\\\|\\\\>|[^>])*>\\s*', String.Regex, 'balanced-regex'),
              (
               's\\[(\\\\\\\\|\\\\\\]|[^\\]])*\\]\\s*', String.Regex, 'balanced-regex'),
              (
               's\\((\\\\\\\\|\\\\\\)|[^\\)])*\\)\\s*', String.Regex, 'balanced-regex'),
              (
               'm?/(\\\\\\\\|\\\\/|[^/\\n])*/[gcimosx]*', String.Regex),
              (
               'm(?=[/!\\\\{<\\[\\(@%\\$])', String.Regex, 'balanced-regex'),
              (
               '((?<==~)|(?<=\\())\\s*/(\\\\\\\\|\\\\/|[^/])*/[gcimosx]*', String.Regex),
              (
               '\\s+', Text),
              (
               '(abs|accept|alarm|atan2|bind|binmode|bless|caller|chdir|chmod|chomp|chop|chown|chr|chroot|close|closedir|connect|continue|cos|crypt|dbmclose|dbmopen|defined|delete|die|dump|each|endgrent|endhostent|endnetent|endprotoent|endpwent|endservent|eof|eval|exec|exists|exit|exp|fcntl|fileno|flock|fork|format|formline|getc|getgrent|getgrgid|getgrnam|gethostbyaddr|gethostbyname|gethostent|getlogin|getnetbyaddr|getnetbyname|getnetent|getpeername|getpgrp|getppid|getpriority|getprotobyname|getprotobynumber|getprotoent|getpwent|getpwnam|getpwuid|getservbyname|getservbyport|getservent|getsockname|getsockopt|glob|gmtime|goto|grep|hex|import|index|int|ioctl|join|keys|kill|last|lc|lcfirst|length|link|listen|local|localtime|log|lstat|map|mkdir|msgctl|msgget|msgrcv|msgsnd|my|next|no|oct|open|opendir|ord|our|pack|package|pipe|pop|pos|printf|prototype|push|quotemeta|rand|read|readdir|readline|readlink|readpipe|recv|redo|ref|rename|require|reverse|rewinddir|rindex|rmdir|scalar|seek|seekdir|select|semctl|semget|semop|send|setgrent|sethostent|setnetent|setpgrp|setpriority|setprotoent|setpwent|setservent|setsockopt|shift|shmctl|shmget|shmread|shmwrite|shutdown|sin|sleep|socket|socketpair|sort|splice|split|sprintf|sqrt|srand|stat|study|substr|symlink|syscall|sysopen|sysread|sysseek|system|syswrite|tell|telldir|tie|tied|time|times|tr|truncate|uc|ucfirst|umask|undef|unlink|unpack|unshift|untie|utime|values|vec|wait|waitpid|wantarray|warn|write)\\b',
               Name.Builtin),
              (
               '((__(DATA|DIE|WARN)__)|(STD(IN|OUT|ERR)))\\b', Name.Builtin.Pseudo),
              (
               '<<([\\\'"]?)([a-zA-Z_][a-zA-Z0-9_]*)\\1;?\\n.*?\\n\\2\\n', String),
              (
               '__END__', Comment.Preproc, 'end-part'),
              (
               '\\$\\^[ADEFHILMOPSTWX]', Name.Variable.Global),
              (
               '\\$[\\\\\\"\\[\\]\'&`+*.,;=%~?@$!<>(^|/-](?!\\w)', Name.Variable.Global),
              (
               '[$@%#]+', Name.Variable, 'varname'),
              (
               '0_?[0-7]+(_[0-7]+)*', Number.Oct),
              (
               '0x[0-9A-Fa-f]+(_[0-9A-Fa-f]+)*', Number.Hex),
              (
               '0b[01]+(_[01]+)*', Number.Bin),
              (
               '(?i)(\\d*(_\\d*)*\\.\\d+(_\\d*)*|\\d+(_\\d*)*\\.\\d+(_\\d*)*)(e[+-]?\\d+)?',
               Number.Float),
              (
               '(?i)\\d+(_\\d*)*e[+-]?\\d+(_\\d*)*', Number.Float),
              (
               '\\d+(_\\d+)*', Number.Integer),
              (
               "'(\\\\\\\\|\\\\'|[^'])*'", String),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '`(\\\\\\\\|\\\\`|[^`])*`', String.Backtick),
              (
               '<([^\\s>]+)>', String.Regex),
              (
               '(q|qq|qw|qr|qx)\\{', String.Other, 'cb-string'),
              (
               '(q|qq|qw|qr|qx)\\(', String.Other, 'rb-string'),
              (
               '(q|qq|qw|qr|qx)\\[', String.Other, 'sb-string'),
              (
               '(q|qq|qw|qr|qx)\\<', String.Other, 'lt-string'),
              (
               '(q|qq|qw|qr|qx)([^a-zA-Z0-9])(.|\\n)*?\\2', String.Other),
              (
               'package\\s+', Keyword, 'modulename'),
              (
               'sub\\s+', Keyword, 'funcname'),
              (
               '(\\[\\]|\\*\\*|::|<<|>>|>=|<=|<=>|={3}|!=|=~|!~|&&?|\\|\\||\\.{1,3})',
               Operator),
              (
               '[-+/*%=<>&^|!\\\\~]=?', Operator),
              (
               '[\\(\\)\\[\\]:;,<>/\\?\\{\\}]', Punctuation),
              (
               '(?=\\w)', Name, 'name')], 
       'format': [
                (
                 '\\.\\n', String.Interpol, '#pop'),
                (
                 '[^\\n]*\\n', String.Interpol)], 
       'varname': [
                 (
                  '\\s+', Text),
                 (
                  '\\{', Punctuation, '#pop'),
                 (
                  '\\)|,', Punctuation, '#pop'),
                 (
                  '[a-zA-Z0-9_]+::', Name.Namespace),
                 (
                  '[a-zA-Z0-9_:]+', Name.Variable, '#pop')], 
       'name': [
              (
               '[a-zA-Z0-9_]+::', Name.Namespace),
              (
               '[a-zA-Z0-9_:]+', Name, '#pop'),
              (
               '[A-Z_]+(?=[^a-zA-Z0-9_])', Name.Constant, '#pop'),
              (
               '(?=[^a-zA-Z0-9_])', Text, '#pop')], 
       'modulename': [
                    (
                     '[a-zA-Z_][\\w_]*', Name.Namespace, '#pop')], 
       'funcname': [
                  (
                   '[a-zA-Z_][\\w_]*[\\!\\?]?', Name.Function),
                  (
                   '\\s+', Text),
                  (
                   '(\\([$@%]*\\))(\\s*)', bygroups(Punctuation, Text)),
                  (
                   '.*?{', Punctuation, '#pop'),
                  (
                   ';', Punctuation, '#pop')], 
       'cb-string': [
                   (
                    '\\\\[\\{\\}\\\\]', String.Other),
                   (
                    '\\\\', String.Other),
                   (
                    '\\{', String.Other, 'cb-string'),
                   (
                    '\\}', String.Other, '#pop'),
                   (
                    '[^\\{\\}\\\\]+', String.Other)], 
       'rb-string': [
                   (
                    '\\\\[\\(\\)\\\\]', String.Other),
                   (
                    '\\\\', String.Other),
                   (
                    '\\(', String.Other, 'rb-string'),
                   (
                    '\\)', String.Other, '#pop'),
                   (
                    '[^\\(\\)]+', String.Other)], 
       'sb-string': [
                   (
                    '\\\\[\\[\\]\\\\]', String.Other),
                   (
                    '\\\\', String.Other),
                   (
                    '\\[', String.Other, 'sb-string'),
                   (
                    '\\]', String.Other, '#pop'),
                   (
                    '[^\\[\\]]+', String.Other)], 
       'lt-string': [
                   (
                    '\\\\[\\<\\>\\\\]', String.Other),
                   (
                    '\\\\', String.Other),
                   (
                    '\\<', String.Other, 'lt-string'),
                   (
                    '\\>', String.Other, '#pop'),
                   (
                    '[^\\<\\>]+', String.Other)], 
       'end-part': [
                  (
                   '.+', Comment.Preproc, '#pop')]}

    def analyse_text(text):
        if shebang_matches(text, 'perl'):
            return True
        if 'my $' in text:
            return 0.9
        return 0.1


class LuaLexer(RegexLexer):
    """
    For `Lua <http://www.lua.org>`_ source code.

    Additional options accepted:

    `func_name_highlighting`
        If given and ``True``, highlight builtin function names
        (default: ``True``).
    `disabled_modules`
        If given, must be a list of module names whose function names
        should not be highlighted. By default all modules are highlighted.

        To get a list of allowed modules have a look into the
        `_luabuiltins` module:

        .. sourcecode:: pycon

            >>> from pygments.lexers._luabuiltins import MODULES
            >>> MODULES.keys()
            ['string', 'coroutine', 'modules', 'io', 'basic', ...]
    """
    name = 'Lua'
    aliases = ['lua']
    filenames = ['*.lua', '*.wlua']
    mimetypes = ['text/x-lua', 'application/x-lua']
    tokens = {'root': [
              (
               '#!(.*?)$', Comment.Preproc),
              (
               '', Text, 'base')], 
       'base': [
              (
               '(?s)--\\[(=*)\\[.*?\\]\\1\\]', Comment.Multiline),
              (
               '--.*$', Comment.Single),
              (
               '(?i)(\\d*\\.\\d+|\\d+\\.\\d*)(e[+-]?\\d+)?', Number.Float),
              (
               '(?i)\\d+e[+-]?\\d+', Number.Float),
              (
               '(?i)0x[0-9a-f]*', Number.Hex),
              (
               '\\d+', Number.Integer),
              (
               '\\n', Text),
              (
               '[^\\S\\n]', Text),
              (
               '(?s)\\[(=*)\\[.*?\\]\\1\\]', String),
              (
               '(==|~=|<=|>=|\\.\\.|\\.\\.\\.|[=+\\-*/%^<>#])', Operator),
              (
               '[\\[\\]\\{\\}\\(\\)\\.,:;]', Punctuation),
              (
               '(and|or|not)\\b', Operator.Word),
              (
               '(break|do|else|elseif|end|for|if|in|repeat|return|then|until|while)\\b',
               Keyword),
              (
               '(local)\\b', Keyword.Declaration),
              (
               '(true|false|nil)\\b', Keyword.Constant),
              (
               '(function)(\\s+)', bygroups(Keyword, Text), 'funcname'),
              (
               '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
              (
               '[A-Za-z_][A-Za-z0-9_]*(\\.[A-Za-z_][A-Za-z0-9_]*)?', Name),
              (
               "'", String.Single, combined('stringescape', 'sqs')),
              (
               '"', String.Double, combined('stringescape', 'dqs'))], 
       'funcname': [
                  (
                   '(?:([A-Za-z_][A-Za-z0-9_]*)(\\.))?([A-Za-z_][A-Za-z0-9_]*)',
                   bygroups(Name.Class, Punctuation, Name.Function), '#pop'),
                  (
                   '\\(', Punctuation, '#pop')], 
       'classname': [
                   (
                    '[A-Za-z_][A-Za-z0-9_]*', Name.Class, '#pop')], 
       'string': [
                (
                 '.', String)], 
       'stringescape': [
                      (
                       '\\\\([abfnrtv\\\\"\']|\\d{1,3})', String.Escape)], 
       'sqs': [
             (
              "'", String, '#pop'),
             include('string')], 
       'dqs': [
             (
              '"', String, '#pop'),
             include('string')]}

    def __init__(self, **options):
        self.func_name_highlighting = get_bool_opt(options, 'func_name_highlighting', True)
        self.disabled_modules = get_list_opt(options, 'disabled_modules', [])
        self._functions = set()
        if self.func_name_highlighting:
            from pygments.lexers._luabuiltins import MODULES
            for (mod, func) in MODULES.iteritems():
                if mod not in self.disabled_modules:
                    self._functions.update(func)

        RegexLexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if value in self._functions:
                    yield (
                     index, Name.Builtin, value)
                    continue
                elif '.' in value:
                    (a, b) = value.split('.')
                    yield (index, Name, a)
                    yield (index + len(a), Punctuation, '.')
                    yield (index + len(a) + 1, Name, b)
                    continue
            yield (
             index, token, value)


class MiniDLexer(RegexLexer):
    """
    For `MiniD <http://www.dsource.org/projects/minid>`_ (a D-like scripting
    language) source.
    """
    name = 'MiniD'
    filenames = ['*.md']
    aliases = ['minid']
    mimetypes = ['text/x-minidsrc']
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
               '/\\+', Comment.Multiline, 'nestedcomment'),
              (
               '(as|assert|break|case|catch|class|continue|coroutine|default|do|else|finally|for|foreach|function|global|namespace|if|import|in|is|local|module|return|super|switch|this|throw|try|vararg|while|with|yield)\\b',
               Keyword),
              (
               '(false|true|null)\\b', Keyword.Constant),
              (
               '([0-9][0-9_]*)?\\.[0-9_]+([eE][+\\-]?[0-9_]+)?', Number.Float),
              (
               '0[Bb][01_]+', Number),
              (
               '0[Cc][0-7_]+', Number.Oct),
              (
               '0[xX][0-9a-fA-F_]+', Number.Hex),
              (
               '(0|[1-9][0-9_]*)', Number.Integer),
              (
               '\'(\\\\[\'"?\\\\abfnrtv]|\\\\x[0-9a-fA-F]{2}|\\\\[0-9]{1,3}|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|.)\'',
               String.Char),
              (
               '@"(""|.)*"', String),
              (
               '`(``|.)*`', String),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '(~=|\\^=|%=|\\*=|==|!=|>>>=|>>>|>>=|>>|>=|<=>|\\?=|-\\>|<<=|<<|<=|\\+\\+|\\+=|--|-=|\\|\\||\\|=|&&|&=|\\.\\.|/=)|[-/.&$@|\\+<>!()\\[\\]{}?,;:=*%^~#\\\\]',
               Punctuation),
              (
               '[a-zA-Z_]\\w*', Name)], 
       'nestedcomment': [
                       (
                        '[^+/]+', Comment.Multiline),
                       (
                        '/\\+', Comment.Multiline, '#push'),
                       (
                        '\\+/', Comment.Multiline, '#pop'),
                       (
                        '[+/]', Comment.Multiline)]}


class IoLexer(RegexLexer):
    """
    For `Io <http://iolanguage.com/>`_ (a small, prototype-based
    programming language) source.

    *New in Pygments 0.10.*
    """
    name = 'Io'
    filenames = ['*.io']
    aliases = ['io']
    mimetypes = ['text/x-iosrc']
    tokens = {'root': [
              (
               '\\n', Text),
              (
               '\\s+', Text),
              (
               '//(.*?)\\n', Comment.Single),
              (
               '#(.*?)\\n', Comment.Single),
              (
               '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
              (
               '/\\+', Comment.Multiline, 'nestedcomment'),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               '::=|:=|=|\\(|\\)|;|,|\\*|-|\\+|>|<|@|!|/|\\||\\^|\\.|%|&|\\[|\\]|\\{|\\}',
               Operator),
              (
               '(clone|do|doFile|doString|method|for|if|else|elseif|then)\\b',
               Keyword),
              (
               '(nil|false|true)\\b', Name.Constant),
              (
               '(Object|list|List|Map|args|Sequence|Coroutine|File)\x08',
               Name.Builtin),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Name),
              (
               '(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
              (
               '\\d+', Number.Integer)], 
       'nestedcomment': [
                       (
                        '[^+/]+', Comment.Multiline),
                       (
                        '/\\+', Comment.Multiline, '#push'),
                       (
                        '\\+/', Comment.Multiline, '#pop'),
                       (
                        '[+/]', Comment.Multiline)]}


class TclLexer(RegexLexer):
    """
    For Tcl source code.

    *New in Pygments 0.10.*
    """
    keyword_cmds_re = '\\b(after|apply|array|break|catch|continue|elseif|else|error|eval|expr|for|foreach|global|if|namespace|proc|rename|return|set|switch|then|trace|unset|update|uplevel|upvar|variable|vwait|while)\\b'
    builtin_cmds_re = '\\b(append|bgerror|binary|cd|chan|clock|close|concat|dde|dict|encoding|eof|exec|exit|fblocked|fconfigure|fcopy|file|fileevent|flush|format|gets|glob|history|http|incr|info|interp|join|lappend|lassign|lindex|linsert|list|llength|load|loadTk|lrange|lrepeat|lreplace|lreverse|lsearch|lset|lsort|mathfunc|mathop|memory|msgcat|open|package|pid|pkg::create|pkg_mkIndex|platform|platform::shell|puts|pwd|re_syntax|read|refchan|regexp|registry|regsub|scan|seek|socket|source|split|string|subst|tell|time|tm|unknown|unload)\\b'
    name = 'Tcl'
    aliases = ['tcl']
    filenames = ['*.tcl']
    mimetypes = ['text/x-tcl', 'text/x-script.tcl', 'application/x-tcl']

    def _gen_command_rules(keyword_cmds_re, builtin_cmds_re, context=''):
        return [
         (
          keyword_cmds_re, Keyword, 'params' + context),
         (
          builtin_cmds_re, Name.Builtin, 'params' + context),
         (
          '([\\w\\.\\-]+)', Name.Variable, 'params' + context),
         (
          '#', Comment, 'comment')]

    tokens = {'root': [
              include('command'),
              include('basic'),
              include('data'),
              (
               '}', Keyword)], 
       'command': _gen_command_rules(keyword_cmds_re, builtin_cmds_re), 
       'command-in-brace': _gen_command_rules(keyword_cmds_re, builtin_cmds_re, '-in-brace'), 
       'command-in-bracket': _gen_command_rules(keyword_cmds_re, builtin_cmds_re, '-in-bracket'), 
       'command-in-paren': _gen_command_rules(keyword_cmds_re, builtin_cmds_re, '-in-paren'), 
       'basic': [
               (
                '\\(', Keyword, 'paren'),
               (
                '\\[', Keyword, 'bracket'),
               (
                '\\{', Keyword, 'brace'),
               (
                '"', String.Double, 'string'),
               (
                '(eq|ne|in|ni)\\b', Operator.Word),
               (
                '!=|==|<<|>>|<=|>=|&&|\\|\\||\\*\\*|[-+~!*/%<>&^|?:]', Operator)], 
       'data': [
              (
               '\\s+', Text),
              (
               '0x[a-fA-F0-9]+', Number.Hex),
              (
               '0[0-7]+', Number.Oct),
              (
               '\\d+\\.\\d+', Number.Float),
              (
               '\\d+', Number.Integer),
              (
               '\\$([\\w\\.\\-\\:]+)', Name.Variable),
              (
               '([\\w\\.\\-\\:]+)', Text)], 
       'params': [
                (
                 ';', Keyword, '#pop'),
                (
                 '\\n', Text, '#pop'),
                (
                 '(else|elseif|then)', Keyword),
                include('basic'),
                include('data')], 
       'params-in-brace': [
                         (
                          '}', Keyword, ('#pop', '#pop')),
                         include('params')], 
       'params-in-paren': [
                         (
                          '\\)', Keyword, ('#pop', '#pop')),
                         include('params')], 
       'params-in-bracket': [
                           (
                            '\\]', Keyword, ('#pop', '#pop')),
                           include('params')], 
       'string': [
                (
                 '\\[', String.Double, 'string-square'),
                (
                 '(?s)(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\])', String.Double),
                (
                 '"', String.Double, '#pop')], 
       'string-square': [
                       (
                        '\\[', String.Double, 'string-square'),
                       (
                        '(?s)(\\\\\\\\|\\\\[0-7]+|\\\\.|\\\\\\n|[^\\]\\\\])', String.Double),
                       (
                        '\\]', String.Double, '#pop')], 
       'brace': [
               (
                '}', Keyword, '#pop'),
               include('command-in-brace'),
               include('basic'),
               include('data')], 
       'paren': [
               (
                '\\)', Keyword, '#pop'),
               include('command-in-paren'),
               include('basic'),
               include('data')], 
       'bracket': [
                 (
                  '\\]', Keyword, '#pop'),
                 include('command-in-bracket'),
                 include('basic'),
                 include('data')], 
       'comment': [
                 (
                  '.*[^\\\\]\\n', Comment, '#pop'),
                 (
                  '.*\\\\\\n', Comment)]}

    def analyse_text(text):
        return shebang_matches(text, '(tcl)')


class ClojureLexer(RegexLexer):
    """
    Lexer for `Clojure <http://clojure.org/>`_ source code.

    *New in Pygments 0.11.*
    """
    name = 'Clojure'
    aliases = ['clojure', 'clj']
    filenames = ['*.clj']
    mimetypes = ['text/x-clojure', 'application/x-clojure']
    keywords = [
     'fn', 'def', 'defn', 'defmacro', 'defmethod', 'defmulti', 'defn-',
     'defstruct',
     'if', 'cond',
     'let', 'for']
    builtins = [
     '.', '..',
     '*', '+', '-', '->', '..', '/', '<', '<=', '=', '==', '>', '>=',
     'accessor', 'agent', 'agent-errors', 'aget', 'alength', 'all-ns',
     'alter', 'and', 'append-child', 'apply', 'array-map', 'aset',
     'aset-boolean', 'aset-byte', 'aset-char', 'aset-double', 'aset-float',
     'aset-int', 'aset-long', 'aset-short', 'assert', 'assoc', 'await',
     'await-for', 'bean', 'binding', 'bit-and', 'bit-not', 'bit-or',
     'bit-shift-left', 'bit-shift-right', 'bit-xor', 'boolean', 'branch?',
     'butlast', 'byte', 'cast', 'char', 'children', 'class',
     'clear-agent-errors', 'comment', 'commute', 'comp', 'comparator',
     'complement', 'concat', 'conj', 'cons', 'constantly',
     'construct-proxy', 'contains?', 'count', 'create-ns', 'create-struct',
     'cycle', 'dec', 'deref', 'difference', 'disj', 'dissoc', 'distinct',
     'doall', 'doc', 'dorun', 'doseq', 'dosync', 'dotimes', 'doto',
     'double', 'down', 'drop', 'drop-while', 'edit', 'end?', 'ensure',
     'eval', 'every?', 'false?', 'ffirst', 'file-seq', 'filter', 'find',
     'find-doc', 'find-ns', 'find-var', 'first', 'float', 'flush',
     'fnseq', 'frest', 'gensym', 'get', 'get-proxy-class',
     'hash-map', 'hash-set', 'identical?', 'identity', 'if-let', 'import',
     'in-ns', 'inc', 'index', 'insert-child', 'insert-left', 'insert-right',
     'inspect-table', 'inspect-tree', 'instance?', 'int', 'interleave',
     'intersection', 'into', 'into-array', 'iterate', 'join', 'key', 'keys',
     'keyword', 'keyword?', 'last', 'lazy-cat', 'lazy-cons', 'left',
     'lefts', 'line-seq', 'list', 'list*', 'load', 'load-file',
     'locking', 'long', 'loop', 'macroexpand', 'macroexpand-1',
     'make-array', 'make-node', 'map', 'map-invert', 'map?', 'mapcat',
     'max', 'max-key', 'memfn', 'merge', 'merge-with', 'meta', 'min',
     'min-key', 'name', 'namespace', 'neg?', 'new', 'newline', 'next',
     'nil?', 'node', 'not', 'not-any?', 'not-every?', 'not=', 'ns-imports',
     'ns-interns', 'ns-map', 'ns-name', 'ns-publics', 'ns-refers',
     'ns-resolve', 'ns-unmap', 'nth', 'nthrest', 'or', 'parse', 'partial',
     'path', 'peek', 'pop', 'pos?', 'pr', 'pr-str', 'print', 'print-str',
     'println', 'println-str', 'prn', 'prn-str', 'project', 'proxy',
     'proxy-mappings', 'quot', 'rand', 'rand-int', 'range', 're-find',
     're-groups', 're-matcher', 're-matches', 're-pattern', 're-seq',
     'read', 'read-line', 'reduce', 'ref', 'ref-set', 'refer', 'rem',
     'remove', 'remove-method', 'remove-ns', 'rename', 'rename-keys',
     'repeat', 'replace', 'replicate', 'resolve', 'rest', 'resultset-seq',
     'reverse', 'rfirst', 'right', 'rights', 'root', 'rrest', 'rseq',
     'second', 'select', 'select-keys', 'send', 'send-off', 'seq',
     'seq-zip', 'seq?', 'set', 'short', 'slurp', 'some', 'sort',
     'sort-by', 'sorted-map', 'sorted-map-by', 'sorted-set',
     'special-symbol?', 'split-at', 'split-with', 'str', 'string?',
     'struct', 'struct-map', 'subs', 'subvec', 'symbol', 'symbol?',
     'sync', 'take', 'take-nth', 'take-while', 'test', 'time', 'to-array',
     'to-array-2d', 'tree-seq', 'true?', 'union', 'up', 'update-proxy',
     'val', 'vals', 'var-get', 'var-set', 'var?', 'vector', 'vector-zip',
     'vector?', 'when', 'when-first', 'when-let', 'when-not',
     'with-local-vars', 'with-meta', 'with-open', 'with-out-str',
     'xml-seq', 'xml-zip', 'zero?', 'zipmap', 'zipper']
    valid_name = '[a-zA-Z0-9!$%&*+,/:<=>?@^_~-]+'
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
               '\\\\([()/\'\\".\'_!Â§$%& ?;=#+-]{1}|[a-zA-Z0-9]+)', String.Char),
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
               '(\\[|\\])', Punctuation),
              (
               '(\\{|\\})', Punctuation),
              (
               '(\\(|\\))', Punctuation)]}


class FactorLexer(RegexLexer):
    """
    Lexer for the `Factor <http://factorcode.org>`_ language.

    *New in Pygments 1.4.*
    """
    name = 'Factor'
    aliases = ['factor']
    filenames = ['*.factor']
    mimetypes = ['text/x-factor']
    flags = re.MULTILINE | re.UNICODE
    builtin_kernel = '(?:or|2bi|2tri|while|wrapper|nip|4dip|wrapper\\\\?|bi\\\\*|callstack>array|both\\\\?|hashcode|die|dupd|callstack|callstack\\\\?|3dup|tri@|pick|curry|build|\\\\?execute|3bi|prepose|>boolean|\\\\?if|clone|eq\\\\?|tri\\\\*|\\\\?|=|swapd|2over|2keep|3keep|clear|2dup|when|not|tuple\\\\?|dup|2bi\\\\*|2tri\\\\*|call|tri-curry|object|bi@|do|unless\\\\*|if\\\\*|loop|bi-curry\\\\*|drop|when\\\\*|assert=|retainstack|assert\\\\?|-rot|execute|2bi@|2tri@|boa|with|either\\\\?|3drop|bi|curry\\\\?|datastack|until|3dip|over|3curry|tri-curry\\\\*|tri-curry@|swap|and|2nip|throw|bi-curry|\\\\(clone\\\\)|hashcode\\\\*|compose|2dip|if|3tri|unless|compose\\\\?|tuple|keep|2curry|equal\\\\?|assert|tri|2drop|most|<wrapper>|boolean\\\\?|identity-hashcode|identity-tuple\\\\?|null|new|dip|bi-curry@|rot|xor|identity-tuple|boolean)\\s'
    builtin_assocs = '(?:\\\\?at|assoc\\\\?|assoc-clone-like|assoc=|delete-at\\\\*|assoc-partition|extract-keys|new-assoc|value\\\\?|assoc-size|map>assoc|push-at|assoc-like|key\\\\?|assoc-intersect|assoc-refine|update|assoc-union|assoc-combine|at\\\\*|assoc-empty\\\\?|at\\\\+|set-at|assoc-all\\\\?|assoc-subset\\\\?|assoc-hashcode|change-at|assoc-each|assoc-diff|zip|values|value-at|rename-at|inc-at|enum\\\\?|at|cache|assoc>map|<enum>|assoc|assoc-map|enum|value-at\\\\*|assoc-map-as|>alist|assoc-filter-as|clear-assoc|assoc-stack|maybe-set-at|substitute|assoc-filter|2cache|delete-at|assoc-find|keys|assoc-any\\\\?|unzip)\\s'
    builtin_combinators = '(?:case|execute-effect|no-cond|no-case\\\\?|3cleave>quot|2cleave|cond>quot|wrong-values\\\\?|no-cond\\\\?|cleave>quot|no-case|case>quot|3cleave|wrong-values|to-fixed-point|alist>quot|case-find|cond|cleave|call-effect|2cleave>quot|recursive-hashcode|linear-case-quot|spread|spread>quot)\\s'
    builtin_math = '(?:number=|if-zero|next-power-of-2|each-integer|\\\\?1\\\\+|fp-special\\\\?|imaginary-part|unless-zero|float>bits|number\\\\?|fp-infinity\\\\?|bignum\\\\?|fp-snan\\\\?|denominator|fp-bitwise=|\\\\*|\\\\+|power-of-2\\\\?|-|u>=|/|>=|bitand|log2-expects-positive|<|log2|>|integer\\\\?|number|bits>double|2/|zero\\\\?|(find-integer)|bits>float|float\\\\?|shift|ratio\\\\?|even\\\\?|ratio|fp-sign|bitnot|>fixnum|complex\\\\?|/i|/f|byte-array>bignum|when-zero|sgn|>bignum|next-float|u<|u>|mod|recip|rational|find-last-integer|>float|(all-integers\\\\?)|2^|times|integer|fixnum\\\\?|neg|fixnum|sq|bignum|(each-integer)|bit\\\\?|fp-qnan\\\\?|find-integer|complex|<fp-nan>|real|double>bits|bitor|rem|fp-nan-payload|all-integers\\\\?|real-part|log2-expects-positive\\\\?|prev-float|align|unordered\\\\?|float|fp-nan\\\\?|abs|bitxor|u<=|odd\\\\?|<=|/mod|rational\\\\?|>integer|real\\\\?|numerator)\\s'
    builtin_sequences = '(?:member-eq\\\\?|append|assert-sequence=|find-last-from|trim-head-slice|clone-like|3sequence|assert-sequence\\\\?|map-as|last-index-from|reversed|index-from|cut\\\\*|pad-tail|remove-eq!|concat-as|but-last|snip|trim-tail|nths|nth|2selector|sequence|slice\\\\?|<slice>|partition|remove-nth|tail-slice|empty\\\\?|tail\\\\*|if-empty|find-from|virtual-sequence\\\\?|member\\\\?|set-length|drop-prefix|unclip|unclip-last-slice|iota|map-sum|bounds-error\\\\?|sequence-hashcode-step|selector-for|accumulate-as|map|start|midpoint@|\\\\(accumulate\\\\)|rest-slice|prepend|fourth|sift|accumulate!|new-sequence|follow|map!|like|first4|1sequence|reverse|slice|unless-empty|padding|virtual@|repetition\\\\?|set-last|index|4sequence|max-length|set-second|immutable-sequence|first2|first3|replicate-as|reduce-index|unclip-slice|supremum|suffix!|insert-nth|trim-tail-slice|tail|3append|short|count|suffix|concat|flip|filter|sum|immutable\\\\?|reverse!|2sequence|map-integers|delete-all|start\\\\*|indices|snip-slice|check-slice|sequence\\\\?|head|map-find|filter!|append-as|reduce|sequence=|halves|collapse-slice|interleave|2map|filter-as|binary-reduce|slice-error\\\\?|product|bounds-check\\\\?|bounds-check|harvest|immutable|virtual-exemplar|find|produce|remove|pad-head|last|replicate|set-fourth|remove-eq|shorten|reversed\\\\?|map-find-last|3map-as|2unclip-slice|shorter\\\\?|3map|find-last|head-slice|pop\\\\*|2map-as|tail-slice\\\\*|but-last-slice|2map-reduce|iota\\\\?|collector-for|accumulate|each|selector|append!|new-resizable|cut-slice|each-index|head-slice\\\\*|2reverse-each|sequence-hashcode|pop|set-nth|\\\\?nth|<flat-slice>|second|join|when-empty|collector|immutable-sequence\\\\?|<reversed>|all\\\\?|3append-as|virtual-sequence|subseq\\\\?|remove-nth!|push-either|new-like|length|last-index|push-if|2all\\\\?|lengthen|assert-sequence|copy|map-reduce|move|third|first|3each|tail\\\\?|set-first|prefix|bounds-error|any\\\\?|<repetition>|trim-slice|exchange|surround|2reduce|cut|change-nth|min-length|set-third|produce-as|push-all|head\\\\?|delete-slice|rest|sum-lengths|2each|head\\\\*|infimum|remove!|glue|slice-error|subseq|trim|replace-slice|push|repetition|map-index|trim-head|unclip-last|mismatch)\\s'
    builtin_namespaces = '(?:global|\\\\+@|change|set-namestack|change-global|init-namespaces|on|off|set-global|namespace|set|with-scope|bind|with-variable|inc|dec|counter|initialize|namestack|get|get-global|make-assoc)\\s'
    builtin_arrays = '(?:<array>|2array|3array|pair|>array|1array|4array|pair\\\\?|array|resize-array|array\\\\?)\\s'
    builtin_io = '(?:\\\\+character\\\\+|bad-seek-type\\\\?|readln|each-morsel|stream-seek|read|print|with-output-stream|contents|write1|stream-write1|stream-copy|stream-element-type|with-input-stream|stream-print|stream-read|stream-contents|stream-tell|tell-output|bl|seek-output|bad-seek-type|nl|stream-nl|write|flush|stream-lines|\\\\+byte\\\\+|stream-flush|read1|seek-absolute\\\\?|stream-read1|lines|stream-readln|stream-read-until|each-line|seek-end|with-output-stream\\\\*|seek-absolute|with-streams|seek-input|seek-relative\\\\?|input-stream|stream-write|read-partial|seek-end\\\\?|seek-relative|error-stream|read-until|with-input-stream\\\\*|with-streams\\\\*|tell-input|each-block|output-stream|stream-read-partial|each-stream-block|each-stream-line)\\s'
    builtin_strings = '(?:resize-string|>string|<string>|1string|string|string\\\\?)\\s'
    builtin_vectors = '(?:vector\\\\?|<vector>|\\\\?push|vector|>vector|1vector)\\s'
    builtin_continuations = '(?:with-return|restarts|return-continuation|with-datastack|recover|rethrow-restarts|<restart>|ifcc|set-catchstack|>continuation<|cleanup|ignore-errors|restart\\\\?|compute-restarts|attempt-all-error|error-thread|continue|<continuation>|attempt-all-error\\\\?|condition\\\\?|<condition>|throw-restarts|error|catchstack|continue-with|thread-error-hook|continuation|rethrow|callcc1|error-continuation|callcc0|attempt-all|condition|continuation\\\\?|restart|return)\\s'
    tokens = {'root': [
              (
               '(\\s*)(:|::|MACRO:|MEMO:)(\\s+)(\\S+)',
               bygroups(Text, Keyword, Text, Name.Function)),
              (
               '(\\s*)(M:)(\\s+)(\\S+)(\\s+)(\\S+)',
               bygroups(Text, Keyword, Text, Name.Class, Text, Name.Function)),
              (
               '(\\s*)(GENERIC:)(\\s+)(\\S+)',
               bygroups(Text, Keyword, Text, Name.Function)),
              (
               '(\\s*)(HOOK:|GENERIC#)(\\s+)(\\S+)(\\s+)(\\S+)',
               bygroups(Text, Keyword, Text, Name.Function, Text, Name.Function)),
              (
               '(\\()(\\s+)', bygroups(Name.Function, Text), 'stackeffect'),
              (
               '\\;\\s', Keyword),
              (
               '(USING:)((?:\\s|\\\\\\s)+)', bygroups(Keyword.Namespace, Text), 'import'),
              (
               '(USE:)(\\s+)(\\S+)', bygroups(Keyword.Namespace, Text, Name.Namespace)),
              (
               '(UNUSE:)(\\s+)(\\S+)', bygroups(Keyword.Namespace, Text, Name.Namespace)),
              (
               '(QUALIFIED:)(\\s+)(\\S+)',
               bygroups(Keyword.Namespace, Text, Name.Namespace)),
              (
               '(QUALIFIED-WITH:)(\\s+)(\\S+)',
               bygroups(Keyword.Namespace, Text, Name.Namespace)),
              (
               '(FROM:|EXCLUDE:)(\\s+)(\\S+)(\\s+)(=>)',
               bygroups(Keyword.Namespace, Text, Name.Namespace, Text, Text)),
              (
               '(IN:)(\\s+)(\\S+)', bygroups(Keyword.Namespace, Text, Name.Namespace)),
              (
               '(?:ALIAS|DEFER|FORGET|POSTPONE):', Keyword.Namespace),
              (
               '(TUPLE:)(\\s+)(\\S+)(\\s+<\\s+)(\\S+)',
               bygroups(Keyword, Text, Name.Class, Text, Name.Class), 'slots'),
              (
               '(TUPLE:)(\\s+)(\\S+)', bygroups(Keyword, Text, Name.Class), 'slots'),
              (
               '(UNION:)(\\s+)(\\S+)', bygroups(Keyword, Text, Name.Class)),
              (
               '(INTERSECTION:)(\\s+)(\\S+)', bygroups(Keyword, Text, Name.Class)),
              (
               '(PREDICATE:)(\\s+)(\\S+)(\\s+<\\s+)(\\S+)',
               bygroups(Keyword, Text, Name.Class, Text, Name.Class)),
              (
               '(C:)(\\s+)(\\S+)(\\s+)(\\S+)',
               bygroups(Keyword, Text, Name.Function, Text, Name.Class)),
              (
               'INSTANCE:', Keyword),
              (
               'SLOT:', Keyword),
              (
               'MIXIN:', Keyword),
              (
               '(?:SINGLETON|SINGLETONS):', Keyword),
              (
               'CONSTANT:', Keyword),
              (
               '(?:SYMBOL|SYMBOLS):', Keyword),
              (
               'ERROR:', Keyword),
              (
               'SYNTAX:', Keyword),
              (
               '(HELP:)(\\s+)(\\S+)', bygroups(Keyword, Text, Name.Function)),
              (
               '(MAIN:)(\\s+)(\\S+)', bygroups(Keyword.Namespace, Text, Name.Function)),
              (
               '(?:ALIEN|TYPEDEF|FUNCTION|STRUCT):', Keyword),
              (
               '(?:<PRIVATE|PRIVATE>)', Keyword.Namespace),
              (
               '"""\\s+(?:.|\\n)*?\\s+"""', String),
              (
               '"(?:\\\\\\\\|\\\\"|[^"])*"', String),
              (
               'CHAR:\\s+(\\\\[\\\\abfnrstv]*|\\S)\\s', String.Char),
              (
               '\\!\\s+.*$', Comment),
              (
               '#\\!\\s+.*$', Comment),
              (
               '(t|f)\\s', Name.Constant),
              (
               '-?\\d+\\.\\d+\\s', Number.Float),
              (
               '-?\\d+\\s', Number.Integer),
              (
               'HEX:\\s+[a-fA-F\\d]+\\s', Number.Hex),
              (
               'BIN:\\s+[01]+\\s', Number.Integer),
              (
               'OCT:\\s+[0-7]+\\s', Number.Oct),
              (
               '[-+/*=<>^]\\s', Operator),
              (
               '(?:deprecated|final|foldable|flushable|inline|recursive)\\s', Keyword),
              (
               builtin_kernel, Name.Builtin),
              (
               builtin_assocs, Name.Builtin),
              (
               builtin_combinators, Name.Builtin),
              (
               builtin_math, Name.Builtin),
              (
               builtin_sequences, Name.Builtin),
              (
               builtin_namespaces, Name.Builtin),
              (
               builtin_arrays, Name.Builtin),
              (
               builtin_io, Name.Builtin),
              (
               builtin_strings, Name.Builtin),
              (
               builtin_vectors, Name.Builtin),
              (
               builtin_continuations, Name.Builtin),
              (
               '\\s+', Text),
              (
               '\\S+', Text)], 
       'stackeffect': [
                     (
                      '\\s*\\(', Name.Function, 'stackeffect'),
                     (
                      '\\)', Name.Function, '#pop'),
                     (
                      '\\-\\-', Name.Function),
                     (
                      '\\s+', Text),
                     (
                      '\\S+', Name.Variable)], 
       'slots': [
               (
                '\\s+', Text),
               (
                ';\\s', Keyword, '#pop'),
               (
                '\\S+', Name.Variable)], 
       'import': [
                (
                 ';', Keyword, '#pop'),
                (
                 '\\S+', Name.Namespace),
                (
                 '\\s+', Text)]}


class IokeLexer(RegexLexer):
    """
    For `Ioke <http://ioke.org/>`_ (a strongly typed, dynamic,
    prototype based programming language) source.

    *New in Pygments 1.4.*
    """
    name = 'Ioke'
    filenames = ['*.ik']
    aliases = ['ioke', 'ik']
    mimetypes = ['text/x-iokesrc']
    tokens = {'interpolatableText': [
                            (
                             '(\\\\b|\\\\e|\\\\t|\\\\n|\\\\f|\\\\r|\\\\"|\\\\\\\\|\\\\#|\\\\\\Z|\\\\u[0-9a-fA-F]{1,4}|\\\\[0-3]?[0-7]?[0-7])',
                             String.Escape),
                            (
                             '#{', Punctuation, 'textInterpolationRoot')], 
       'text': [
              (
               '(?<!\\\\)"', String, '#pop'),
              include('interpolatableText'),
              (
               '[^"]', String)], 
       'documentation': [
                       (
                        '(?<!\\\\)"', String.Doc, '#pop'),
                       include('interpolatableText'),
                       (
                        '[^"]', String.Doc)], 
       'textInterpolationRoot': [
                               (
                                '}', Punctuation, '#pop'),
                               include('root')], 
       'slashRegexp': [
                     (
                      '(?<!\\\\)/[oxpniums]*', String.Regex, '#pop'),
                     include('interpolatableText'),
                     (
                      '\\\\/', String.Regex),
                     (
                      '[^/]', String.Regex)], 
       'squareRegexp': [
                      (
                       '(?<!\\\\)][oxpniums]*', String.Regex, '#pop'),
                      include('interpolatableText'),
                      (
                       '\\\\]', String.Regex),
                      (
                       '[^\\]]', String.Regex)], 
       'squareText': [
                    (
                     '(?<!\\\\)]', String, '#pop'),
                    include('interpolatableText'),
                    (
                     '[^\\]]', String)], 
       'root': [
              (
               '\\n', Text),
              (
               '\\s+', Text),
              (
               ';(.*?)\\n', Comment),
              (
               '\\A#!(.*?)\\n', Comment),
              (
               '#/', String.Regex, 'slashRegexp'),
              (
               '#r\\[', String.Regex, 'squareRegexp'),
              (
               ':[a-zA-Z0-9_!:?]+', String.Symbol),
              (
               '[a-zA-Z0-9_!:?]+:(?![a-zA-Z0-9_!?])', String.Other),
              (
               ':"(\\\\\\\\|\\\\"|[^"])*"', String.Symbol),
              (
               '((?<=fn\\()|(?<=fnx\\()|(?<=method\\()|(?<=macro\\()|(?<=lecro\\()|(?<=syntax\\()|(?<=dmacro\\()|(?<=dlecro\\()|(?<=dlecrox\\()|(?<=dsyntax\\())[\\s\\n\\r]*"',
               String.Doc, 'documentation'),
              (
               '"', String, 'text'),
              (
               '#\\[', String, 'squareText'),
              (
               '[a-zA-Z0-9_][a-zA-Z0-9!?_:]+(?=\\s*=.*mimic\\s)', Name.Entity),
              (
               '[a-zA-Z_][a-zA-Z0-9_!:?]*(?=[\\s]*[+*/-]?=[^=].*($|\\.))', Name.Variable),
              (
               '(break|cond|continue|do|ensure|for|for:dict|for:set|if|let|loop|p:for|p:for:dict|p:for:set|return|unless|until|while|with)(?![a-zA-Z0-9!:_?])',
               Keyword.Reserved),
              (
               '(eval|mimic|print|println)(?![a-zA-Z0-9!:_?])', Keyword),
              (
               '(cell\\?|cellNames|cellOwner\\?|cellOwner|cells|cell|documentation|hash|identity|mimic|removeCell\\!|undefineCell\\!)(?![a-zA-Z0-9!:_?])',
               Keyword),
              (
               '(stackTraceAsText)(?![a-zA-Z0-9!:_?])', Keyword),
              (
               '(dict|list|message|set)(?![a-zA-Z0-9!:_?])', Keyword.Reserved),
              (
               '(case|case:and|case:else|case:nand|case:nor|case:not|case:or|case:otherwise|case:xor)(?![a-zA-Z0-9!:_?])',
               Keyword.Reserved),
              (
               '(asText|become\\!|derive|freeze\\!|frozen\\?|in\\?|is\\?|kind\\?|mimic\\!|mimics|mimics\\?|prependMimic\\!|removeAllMimics\\!|removeMimic\\!|same\\?|send|thaw\\!|uniqueHexId)(?![a-zA-Z0-9!:_?])',
               Keyword),
              (
               '(after|around|before)(?![a-zA-Z0-9!:_?])', Keyword.Reserved),
              (
               '(kind|cellDescriptionDict|cellSummary|genSym|inspect|notice)(?![a-zA-Z0-9!:_?])',
               Keyword),
              (
               '(use|destructuring)', Keyword.Reserved),
              (
               '(cell\\?|cellOwner\\?|cellOwner|cellNames|cells|cell|documentation|identity|removeCell!|undefineCell)(?![a-zA-Z0-9!:_?])',
               Keyword),
              (
               '(internal:compositeRegexp|internal:concatenateText|internal:createDecimal|internal:createNumber|internal:createRegexp|internal:createText)(?![a-zA-Z0-9!:_?])',
               Keyword.Reserved),
              (
               '(availableRestarts|bind|error\\!|findRestart|handle|invokeRestart|rescue|restart|signal\\!|warn\\!)(?![a-zA-Z0-9!:_?])',
               Keyword.Reserved),
              (
               '(nil|false|true)(?![a-zA-Z0-9!:_?])', Name.Constant),
              (
               '(Arity|Base|Call|Condition|DateTime|Aspects|Pointcut|Assignment|BaseBehavior|Boolean|Case|AndCombiner|Else|NAndCombiner|NOrCombiner|NotCombiner|OrCombiner|XOrCombiner|Conditions|Definitions|FlowControl|Internal|Literals|Reflection|DefaultMacro|DefaultMethod|DefaultSyntax|Dict|FileSystem|Ground|Handler|Hook|IO|IokeGround|Struct|LexicalBlock|LexicalMacro|List|Message|Method|Mixins|NativeMethod|Number|Origin|Pair|Range|Reflector|Regexp Match|Regexp|Rescue|Restart|Runtime|Sequence|Set|Symbol|System|Text|Tuple)(?![a-zA-Z0-9!:_?])',
               Name.Builtin),
              (
               '(generateMatchMethod|aliasMethod|λ|ʎ|fnx|fn|method|dmacro|dlecro|syntax|macro|dlecrox|lecrox|lecro|syntax)(?![a-zA-Z0-9!:_?])',
               Name.Function),
              (
               '-?0[xX][0-9a-fA-F]+', Number.Hex),
              (
               '-?(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
              (
               '-?\\d+', Number.Integer),
              (
               '#\\(', Punctuation),
              (
               '(&&>>|\\|\\|>>|\\*\\*>>|:::|::|\\.\\.\\.|===|\\*\\*>|\\*\\*=|&&>|&&=|\\|\\|>|\\|\\|=|\\->>|\\+>>|!>>|<>>>|<>>|&>>|%>>|#>>|@>>|/>>|\\*>>|\\?>>|\\|>>|\\^>>|~>>|\\$>>|=>>|<<=|>>=|<=>|<\\->|=~|!~|=>|\\+\\+|\\-\\-|<=|>=|==|!=|&&|\\.\\.|\\+=|\\-=|\\*=|\\/=|%=|&=|\\^=|\\|=|<\\-|\\+>|!>|<>|&>|%>|#>|\\@>|\\/>|\\*>|\\?>|\\|>|\\^>|~>|\\$>|<\\->|\\->|<<|>>|\\*\\*|\\?\\||\\?&|\\|\\||>|<|\\*|\\/|%|\\+|\\-|&|\\^|\\||=|\\$|!|~|\\?|#|≠|∘|∈|∉)',
               Operator),
              (
               '(and|nand|or|xor|nor|return|import)(?![a-zA-Z0-9_!?])',
               Operator),
              (
               "(\\`\\`|\\`|\\'\\'|\\'|\\.|\\,|@|@@|\\[|\\]|\\(|\\)|{|})", Punctuation),
              (
               '[A-Z][a-zA-Z0-9_!:?]*', Name.Class),
              (
               '[a-z_][a-zA-Z0-9_!:?]*', Name)]}