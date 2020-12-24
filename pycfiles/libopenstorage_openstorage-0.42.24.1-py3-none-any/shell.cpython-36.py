# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/shell.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 33870 bytes
"""
    pygments.lexers.shell
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for various shells.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, do_insertions, bygroups, include, default, this, using, words
from pygments.token import Punctuation, Text, Comment, Operator, Keyword, Name, String, Number, Generic
from pygments.util import shebang_matches
__all__ = [
 'BashLexer', 'BashSessionLexer', 'TcshLexer', 'BatchLexer',
 'SlurmBashLexer', 'MSDOSSessionLexer', 'PowerShellLexer',
 'PowerShellSessionLexer', 'TcshSessionLexer', 'FishShellLexer']
line_re = re.compile('.*?\n')

class BashLexer(RegexLexer):
    __doc__ = '\n    Lexer for (ba|k|z|)sh shell scripts.\n\n    .. versionadded:: 0.6\n    '
    name = 'Bash'
    aliases = ['bash', 'sh', 'ksh', 'zsh', 'shell']
    filenames = ['*.sh', '*.ksh', '*.bash', '*.ebuild', '*.eclass',
     '*.exheres-0', '*.exlib', '*.zsh',
     '.bashrc', 'bashrc', '.bash_*', 'bash_*', 'zshrc', '.zshrc',
     'PKGBUILD']
    mimetypes = ['application/x-sh', 'application/x-shellscript', 'text/x-shellscript']
    tokens = {'root':[
      include('basic'),
      (
       '`', String.Backtick, 'backticks'),
      include('data'),
      include('interp')], 
     'interp':[
      (
       '\\$\\(\\(', Keyword, 'math'),
      (
       '\\$\\(', Keyword, 'paren'),
      (
       '\\$\\{#?', String.Interpol, 'curly'),
      (
       '\\$[a-zA-Z_]\\w*', Name.Variable),
      (
       '\\$(?:\\d+|[#$?!_*@-])', Name.Variable),
      (
       '\\$', Text)], 
     'basic':[
      (
       '\\b(if|fi|else|while|do|done|for|then|return|function|case|select|continue|until|esac|elif)(\\s*)\\b',
       bygroups(Keyword, Text)),
      (
       '\\b(alias|bg|bind|break|builtin|caller|cd|command|compgen|complete|declare|dirs|disown|echo|enable|eval|exec|exit|export|false|fc|fg|getopts|hash|help|history|jobs|kill|let|local|logout|popd|printf|pushd|pwd|read|readonly|set|shift|shopt|source|suspend|test|time|times|trap|true|type|typeset|ulimit|umask|unalias|unset|wait)(?=[\\s)`])',
       Name.Builtin),
      (
       '\\A#!.+\\n', Comment.Hashbang),
      (
       '#.*\\n', Comment.Single),
      (
       '\\\\[\\w\\W]', String.Escape),
      (
       '(\\b\\w+)(\\s*)(\\+?=)', bygroups(Name.Variable, Text, Operator)),
      (
       '[\\[\\]{}()=]', Operator),
      (
       '<<<', Operator),
      (
       "<<-?\\s*(\\'?)\\\\?(\\w+)[\\w\\W]+?\\2", String),
      (
       '&&|\\|\\|', Operator)], 
     'data':[
      (
       '(?s)\\$?"(\\\\.|[^"\\\\$])*"', String.Double),
      (
       '"', String.Double, 'string'),
      (
       "(?s)\\$'(\\\\\\\\|\\\\[0-7]+|\\\\.|[^'\\\\])*'", String.Single),
      (
       "(?s)'.*?'", String.Single),
      (
       ';', Punctuation),
      (
       '&', Punctuation),
      (
       '\\|', Punctuation),
      (
       '\\s+', Text),
      (
       '\\d+\\b', Number),
      (
       '[^=\\s\\[\\]{}()$"\\\'`\\\\<&|;]+', Text),
      (
       '<', Text)], 
     'string':[
      (
       '"', String.Double, '#pop'),
      (
       '(?s)(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\$])+', String.Double),
      include('interp')], 
     'curly':[
      (
       '\\}', String.Interpol, '#pop'),
      (
       ':-', Keyword),
      (
       '\\w+', Name.Variable),
      (
       '[^}:"\\\'`$\\\\]+', Punctuation),
      (
       ':', Punctuation),
      include('root')], 
     'paren':[
      (
       '\\)', Keyword, '#pop'),
      include('root')], 
     'math':[
      (
       '\\)\\)', Keyword, '#pop'),
      (
       '[-+*/%^|&]|\\*\\*|\\|\\|', Operator),
      (
       '\\d+#\\d+', Number),
      (
       '\\d+#(?! )', Number),
      (
       '\\d+', Number),
      include('root')], 
     'backticks':[
      (
       '`', String.Backtick, '#pop'),
      include('root')]}

    def analyse_text(text):
        if shebang_matches(text, '(ba|z|)sh'):
            return 1
        if text.startswith('$ '):
            return 0.2


class SlurmBashLexer(BashLexer):
    __doc__ = '\n    Lexer for (ba|k|z|)sh Slurm scripts.\n\n    .. versionadded:: 2.4\n    '
    name = 'Slurm'
    aliases = ['slurm', 'sbatch']
    filenames = ['*.sl']
    mimetypes = []
    EXTRA_KEYWORDS = {'srun'}

    def get_tokens_unprocessed(self, text):
        for index, token, value in BashLexer.get_tokens_unprocessed(self, text):
            if token is Text and value in self.EXTRA_KEYWORDS:
                yield (
                 index, Name.Builtin, value)
            elif token is Comment.Single and 'SBATCH' in value:
                yield (
                 index, Keyword.Pseudo, value)
            else:
                yield (
                 index, token, value)


class ShellSessionBaseLexer(Lexer):
    __doc__ = '\n    Base lexer for simplistic shell sessions.\n\n    .. versionadded:: 2.1\n    '
    _venv = re.compile('^(\\([^)]*\\))(\\s*)')

    def get_tokens_unprocessed(self, text):
        innerlexer = (self._innerLexerCls)(**self.options)
        pos = 0
        curcode = ''
        insertions = []
        backslash_continuation = False
        for match in line_re.finditer(text):
            line = match.group()
            if backslash_continuation:
                curcode += line
                backslash_continuation = curcode.endswith('\\\n')
                continue
            venv_match = self._venv.match(line)
            if venv_match:
                venv = venv_match.group(1)
                venv_whitespace = venv_match.group(2)
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt.VirtualEnv, venv)]))
                if venv_whitespace:
                    insertions.append((len(curcode),
                     [
                      (
                       0, Text, venv_whitespace)]))
                line = line[venv_match.end():]
            m = self._ps1rgx.match(line)
            if m:
                if not insertions:
                    pos = match.start()
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, m.group(1))]))
                curcode += m.group(2)
                backslash_continuation = curcode.endswith('\\\n')
            elif line.startswith(self._ps2):
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Prompt, line[:len(self._ps2)])]))
                curcode += line[len(self._ps2):]
                backslash_continuation = curcode.endswith('\\\n')
            else:
                if insertions:
                    toks = innerlexer.get_tokens_unprocessed(curcode)
                    for i, t, v in do_insertions(insertions, toks):
                        yield (
                         pos + i, t, v)

                yield (
                 match.start(), Generic.Output, line)
                insertions = []
                curcode = ''

        if insertions:
            for i, t, v in do_insertions(insertions, innerlexer.get_tokens_unprocessed(curcode)):
                yield (
                 pos + i, t, v)


class BashSessionLexer(ShellSessionBaseLexer):
    __doc__ = '\n    Lexer for simplistic shell sessions.\n\n    .. versionadded:: 1.1\n    '
    name = 'Bash Session'
    aliases = ['console', 'shell-session']
    filenames = ['*.sh-session', '*.shell-session']
    mimetypes = ['application/x-shell-session', 'application/x-sh-session']
    _innerLexerCls = BashLexer
    _ps1rgx = re.compile('^((?:(?:\\[.*?\\])|(?:\\(\\S+\\))?(?:| |sh\\S*?|\\w+\\S+[@:]\\S+(?:\\s+\\S+)?|\\[\\S+[@:][^\\n]+\\].+))\\s*[$#%])(.*\\n?)')
    _ps2 = '>'


class BatchLexer(RegexLexer):
    __doc__ = '\n    Lexer for the DOS/Windows Batch file format.\n\n    .. versionadded:: 0.7\n    '
    name = 'Batchfile'
    aliases = ['bat', 'batch', 'dosbatch', 'winbatch']
    filenames = ['*.bat', '*.cmd']
    mimetypes = ['application/x-dos-batch']
    flags = re.MULTILINE | re.IGNORECASE
    _nl = '\\n\\x1a'
    _punct = '&<>|'
    _ws = '\\t\\v\\f\\r ,;=\\xa0'
    _space = '(?:(?:(?:\\^[%s])?[%s])+)' % (_nl, _ws)
    _keyword_terminator = '(?=(?:\\^[%s]?)?[%s+./:[\\\\\\]]|[%s%s(])' % (
     _nl, _ws, _nl, _punct)
    _token_terminator = '(?=\\^?[%s]|[%s%s])' % (_ws, _punct, _nl)
    _start_label = '((?:(?<=^[^:])|^[^:]?)[%s]*)(:)' % _ws
    _label = '(?:(?:[^%s%s%s+:^]|\\^[%s]?[\\w\\W])*)' % (_nl, _punct, _ws, _nl)
    _label_compound = '(?:(?:[^%s%s%s+:^)]|\\^[%s]?[^)])*)' % (
     _nl, _punct, _ws, _nl)
    _number = '(?:-?(?:0[0-7]+|0x[\\da-f]+|\\d+)%s)' % _token_terminator
    _opword = '(?:equ|geq|gtr|leq|lss|neq)'
    _string = '(?:"[^%s"]*(?:"|(?=[%s])))' % (_nl, _nl)
    _variable = '(?:(?:%%(?:\\*|(?:~[a-z]*(?:\\$[^:]+:)?)?\\d|[^%%:%s]+(?::(?:~(?:-?\\d+)?(?:,(?:-?\\d+)?)?|(?:[^%%%s^]|\\^[^%%%s])[^=%s]*=(?:[^%%%s^]|\\^[^%%%s])*)?)?%%))|(?:\\^?![^!:%s]+(?::(?:~(?:-?\\d+)?(?:,(?:-?\\d+)?)?|(?:[^!%s^]|\\^[^!%s])[^=%s]*=(?:[^!%s^]|\\^[^!%s])*)?)?\\^?!))' % (
     _nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl)
    _core_token = '(?:(?:(?:\\^[%s]?)?[^"%s%s%s])+)' % (_nl, _nl, _punct, _ws)
    _core_token_compound = '(?:(?:(?:\\^[%s]?)?[^"%s%s%s)])+)' % (_nl, _nl,
     _punct, _ws)
    _token = '(?:[%s]+|%s)' % (_punct, _core_token)
    _token_compound = '(?:[%s]+|%s)' % (_punct, _core_token_compound)
    _stoken = '(?:[%s]+|(?:%s|%s|%s)+)' % (
     _punct, _string, _variable, _core_token)

    def _make_begin_state(compound, _core_token=_core_token, _core_token_compound=_core_token_compound, _keyword_terminator=_keyword_terminator, _nl=_nl, _punct=_punct, _string=_string, _space=_space, _start_label=_start_label, _stoken=_stoken, _token_terminator=_token_terminator, _variable=_variable, _ws=_ws):
        rest = '(?:%s|%s|[^"%%%s%s%s])*' % (_string, _variable, _nl, _punct,
         ')' if compound else '')
        rest_of_line = '(?:(?:[^%s^]|\\^[%s]?[\\w\\W])*)' % (_nl, _nl)
        rest_of_line_compound = '(?:(?:[^%s^)]|\\^[%s]?[^)])*)' % (_nl, _nl)
        set_space = '((?:(?:\\^[%s]?)?[^\\S\\n])*)' % _nl
        suffix = ''
        if compound:
            _keyword_terminator = '(?:(?=\\))|%s)' % _keyword_terminator
            _token_terminator = '(?:(?=\\))|%s)' % _token_terminator
            suffix = '/compound'
        return [
         ('\\)', Punctuation, '#pop') if compound else (
          '\\)((?=\\()|%s)%s' % (_token_terminator, rest_of_line),
          Comment.Single),
         (
          '(?=%s)' % _start_label, Text, 'follow%s' % suffix),
         (
          _space, using(this, state='text')),
         include('redirect%s' % suffix),
         (
          '[%s]+' % _nl, Text),
         (
          '\\(', Punctuation, 'root/compound'),
         (
          '@+', Punctuation),
         (
          '((?:for|if|rem)(?:(?=(?:\\^[%s]?)?/)|(?:(?!\\^)|(?<=m))(?:(?=\\()|%s)))(%s?%s?(?:\\^[%s]?)?/(?:\\^[%s]?)?\\?)' % (
           _nl, _token_terminator, _space,
           _core_token_compound if compound else _core_token, _nl, _nl),
          bygroups(Keyword, using(this, state='text')),
          'follow%s' % suffix),
         (
          '(goto%s)(%s(?:\\^[%s]?)?/(?:\\^[%s]?)?\\?%s)' % (
           _keyword_terminator, rest, _nl, _nl, rest),
          bygroups(Keyword, using(this, state='text')),
          'follow%s' % suffix),
         (
          words(('assoc', 'break', 'cd', 'chdir', 'cls', 'color', 'copy', 'date', 'del', 'dir',
       'dpath', 'echo', 'endlocal', 'erase', 'exit', 'ftype', 'keys', 'md', 'mkdir',
       'mklink', 'move', 'path', 'pause', 'popd', 'prompt', 'pushd', 'rd', 'ren',
       'rename', 'rmdir', 'setlocal', 'shift', 'start', 'time', 'title', 'type',
       'ver', 'verify', 'vol'),
            suffix=_keyword_terminator), Keyword, 'follow%s' % suffix),
         (
          '(call)(%s?)(:)' % _space,
          bygroups(Keyword, using(this, state='text'), Punctuation),
          'call%s' % suffix),
         (
          'call%s' % _keyword_terminator, Keyword),
         (
          '(for%s(?!\\^))(%s)(/f%s)' % (
           _token_terminator, _space, _token_terminator),
          bygroups(Keyword, using(this, state='text'), Keyword),
          ('for/f', 'for')),
         (
          '(for%s(?!\\^))(%s)(/l%s)' % (
           _token_terminator, _space, _token_terminator),
          bygroups(Keyword, using(this, state='text'), Keyword),
          ('for/l', 'for')),
         (
          'for%s(?!\\^)' % _token_terminator, Keyword, ('for2', 'for')),
         (
          '(goto%s)(%s?)(:?)' % (_keyword_terminator, _space),
          bygroups(Keyword, using(this, state='text'), Punctuation),
          'label%s' % suffix),
         (
          '(if(?:(?=\\()|%s)(?!\\^))(%s?)((?:/i%s)?)(%s?)((?:not%s)?)(%s?)' % (
           _token_terminator, _space, _token_terminator, _space,
           _token_terminator, _space),
          bygroups(Keyword, using(this, state='text'), Keyword, using(this, state='text'), Keyword, using(this, state='text')), ('(?', 'if')),
         (
          'rem(((?=\\()|%s)%s?%s?.*|%s%s)' % (
           _token_terminator, _space, _stoken, _keyword_terminator,
           rest_of_line_compound if compound else rest_of_line),
          Comment.Single, 'follow%s' % suffix),
         (
          '(set%s)%s(/a)' % (_keyword_terminator, set_space),
          bygroups(Keyword, using(this, state='text'), Keyword),
          'arithmetic%s' % suffix),
         (
          '(set%s)%s((?:/p)?)%s((?:(?:(?:\\^[%s]?)?[^"%s%s^=%s]|\\^[%s]?[^"=])+)?)((?:(?:\\^[%s]?)?=)?)' % (
           _keyword_terminator, set_space, set_space, _nl, _nl, _punct,
           ')' if compound else '', _nl, _nl),
          bygroups(Keyword, using(this, state='text'), Keyword, using(this, state='text'), using(this, state='variable'), Punctuation),
          'follow%s' % suffix),
         default('follow%s' % suffix)]

    def _make_follow_state(compound, _label=_label, _label_compound=_label_compound, _nl=_nl, _space=_space, _start_label=_start_label, _token=_token, _token_compound=_token_compound, _ws=_ws):
        suffix = '/compound' if compound else ''
        state = []
        if compound:
            state.append(('(?=\\))', Text, '#pop'))
        state += [
         (
          '%s([%s]*)(%s)(.*)' % (
           _start_label, _ws, _label_compound if compound else _label),
          bygroups(Text, Punctuation, Text, Name.Label, Comment.Single)),
         include('redirect%s' % suffix),
         (
          '(?=[%s])' % _nl, Text, '#pop'),
         (
          '\\|\\|?|&&?', Punctuation, '#pop'),
         include('text')]
        return state

    def _make_arithmetic_state(compound, _nl=_nl, _punct=_punct, _string=_string, _variable=_variable, _ws=_ws):
        op = '=+\\-*/!~'
        state = []
        if compound:
            state.append(('(?=\\))', Text, '#pop'))
        state += [
         (
          '0[0-7]+', Number.Oct),
         (
          '0x[\\da-f]+', Number.Hex),
         (
          '\\d+', Number.Integer),
         (
          '[(),]+', Punctuation),
         (
          '([%s]|%%|\\^\\^)+' % op, Operator),
         (
          '(%s|%s|(\\^[%s]?)?[^()%s%%^"%s%s%s]|\\^[%s%s]?%s)+' % (
           _string, _variable, _nl, op, _nl, _punct, _ws, _nl, _ws,
           '[^)]' if compound else '[\\w\\W]'),
          using(this, state='variable')),
         (
          '(?=[\\x00|&])', Text, '#pop'),
         include('follow')]
        return state

    def _make_call_state(compound, _label=_label, _label_compound=_label_compound):
        state = []
        if compound:
            state.append(('(?=\\))', Text, '#pop'))
        state.append(('(:?)(%s)' % (_label_compound if compound else _label),
         bygroups(Punctuation, Name.Label), '#pop'))
        return state

    def _make_label_state(compound, _label=_label, _label_compound=_label_compound, _nl=_nl, _punct=_punct, _string=_string, _variable=_variable):
        state = []
        if compound:
            state.append(('(?=\\))', Text, '#pop'))
        state.append((
         '(%s?)((?:%s|%s|\\^[%s]?%s|[^"%%^%s%s%s])*)' % (
          _label_compound if compound else _label, _string,
          _variable, _nl, '[^)]' if compound else '[\\w\\W]', _nl,
          _punct, ')' if compound else ''),
         bygroups(Name.Label, Comment.Single), '#pop'))
        return state

    def _make_redirect_state(compound, _core_token_compound=_core_token_compound, _nl=_nl, _punct=_punct, _stoken=_stoken, _string=_string, _space=_space, _variable=_variable, _ws=_ws):
        stoken_compound = '(?:[%s]+|(?:%s|%s|%s)+)' % (
         _punct, _string, _variable, _core_token_compound)
        return [
         (
          '((?:(?<=[%s%s])\\d)?)(>>?&|<&)([%s%s]*)(\\d)' % (
           _nl, _ws, _nl, _ws),
          bygroups(Number.Integer, Punctuation, Text, Number.Integer)),
         (
          '((?:(?<=[%s%s])(?<!\\^[%s])\\d)?)(>>?|<)(%s?%s)' % (
           _nl, _ws, _nl, _space, stoken_compound if compound else _stoken),
          bygroups(Number.Integer, Punctuation, using(this, state='text')))]

    tokens = {'root':_make_begin_state(False), 
     'follow':_make_follow_state(False), 
     'arithmetic':_make_arithmetic_state(False), 
     'call':_make_call_state(False), 
     'label':_make_label_state(False), 
     'redirect':_make_redirect_state(False), 
     'root/compound':_make_begin_state(True), 
     'follow/compound':_make_follow_state(True), 
     'arithmetic/compound':_make_arithmetic_state(True), 
     'call/compound':_make_call_state(True), 
     'label/compound':_make_label_state(True), 
     'redirect/compound':_make_redirect_state(True), 
     'variable-or-escape':[
      (
       _variable, Name.Variable),
      (
       '%%%%|\\^[%s]?(\\^!|[\\w\\W])' % _nl, String.Escape)], 
     'string':[
      (
       '"', String.Double, '#pop'),
      (
       _variable, Name.Variable),
      (
       '\\^!|%%', String.Escape),
      (
       '[^"%%^%s]+|[%%^]' % _nl, String.Double),
      default('#pop')], 
     'sqstring':[
      include('variable-or-escape'),
      (
       '[^%]+|%', String.Single)], 
     'bqstring':[
      include('variable-or-escape'),
      (
       '[^%]+|%', String.Backtick)], 
     'text':[
      (
       '"', String.Double, 'string'),
      include('variable-or-escape'),
      (
       '[^"%%^%s%s%s\\d)]+|.' % (_nl, _punct, _ws), Text)], 
     'variable':[
      (
       '"', String.Double, 'string'),
      include('variable-or-escape'),
      (
       '[^"%%^%s]+|.' % _nl, Name.Variable)], 
     'for':[
      (
       '(%s)(in)(%s)(\\()' % (_space, _space),
       bygroups(using(this, state='text'), Keyword, using(this, state='text'), Punctuation), '#pop'),
      include('follow')], 
     'for2':[
      (
       '\\)', Punctuation),
      (
       '(%s)(do%s)' % (_space, _token_terminator),
       bygroups(using(this, state='text'), Keyword), '#pop'),
      (
       '[%s]+' % _nl, Text),
      include('follow')], 
     'for/f':[
      (
       '(")((?:%s|[^"])*?")([%s%s]*)(\\))' % (_variable, _nl, _ws),
       bygroups(String.Double, using(this, state='string'), Text, Punctuation)),
      (
       '"', String.Double, ('#pop', 'for2', 'string')),
      (
       "('(?:%%%%|%s|[\\w\\W])*?')([%s%s]*)(\\))" % (_variable, _nl, _ws),
       bygroups(using(this, state='sqstring'), Text, Punctuation)),
      (
       '(`(?:%%%%|%s|[\\w\\W])*?`)([%s%s]*)(\\))' % (_variable, _nl, _ws),
       bygroups(using(this, state='bqstring'), Text, Punctuation)),
      include('for2')], 
     'for/l':[
      (
       '-?\\d+', Number.Integer),
      include('for2')], 
     'if':[
      (
       '((?:cmdextversion|errorlevel)%s)(%s)(\\d+)' % (
        _token_terminator, _space),
       bygroups(Keyword, using(this, state='text'), Number.Integer), '#pop'),
      (
       '(defined%s)(%s)(%s)' % (_token_terminator, _space, _stoken),
       bygroups(Keyword, using(this, state='text'), using(this, state='variable')), '#pop'),
      (
       '(exist%s)(%s%s)' % (_token_terminator, _space, _stoken),
       bygroups(Keyword, using(this, state='text')), '#pop'),
      (
       '(%s%s)(%s)(%s%s)' % (_number, _space, _opword, _space, _number),
       bygroups(using(this, state='arithmetic'), Operator.Word, using(this, state='arithmetic')), '#pop'),
      (
       _stoken, using(this, state='text'), ('#pop', 'if2'))], 
     'if2':[
      (
       '(%s?)(==)(%s?%s)' % (_space, _space, _stoken),
       bygroups(using(this, state='text'), Operator, using(this, state='text')), '#pop'),
      (
       '(%s)(%s)(%s%s)' % (_space, _opword, _space, _stoken),
       bygroups(using(this, state='text'), Operator.Word, using(this, state='text')), '#pop')], 
     '(?':[
      (
       _space, using(this, state='text')),
      (
       '\\(', Punctuation, ('#pop', 'else?', 'root/compound')),
      default('#pop')], 
     'else?':[
      (
       _space, using(this, state='text')),
      (
       'else%s' % _token_terminator, Keyword, '#pop'),
      default('#pop')]}


class MSDOSSessionLexer(ShellSessionBaseLexer):
    __doc__ = '\n    Lexer for simplistic MSDOS sessions.\n\n    .. versionadded:: 2.1\n    '
    name = 'MSDOS Session'
    aliases = ['doscon']
    filenames = []
    mimetypes = []
    _innerLexerCls = BatchLexer
    _ps1rgx = re.compile('^([^>]*>)(.*\\n?)')
    _ps2 = 'More? '


class TcshLexer(RegexLexer):
    __doc__ = '\n    Lexer for tcsh scripts.\n\n    .. versionadded:: 0.10\n    '
    name = 'Tcsh'
    aliases = ['tcsh', 'csh']
    filenames = ['*.tcsh', '*.csh']
    mimetypes = ['application/x-csh']
    tokens = {'root':[
      include('basic'),
      (
       '\\$\\(', Keyword, 'paren'),
      (
       '\\$\\{#?', Keyword, 'curly'),
      (
       '`', String.Backtick, 'backticks'),
      include('data')], 
     'basic':[
      (
       '\\b(if|endif|else|while|then|foreach|case|default|continue|goto|breaksw|end|switch|endsw)\\s*\\b',
       Keyword),
      (
       '\\b(alias|alloc|bg|bindkey|break|builtins|bye|caller|cd|chdir|complete|dirs|echo|echotc|eval|exec|exit|fg|filetest|getxvers|glob|getspath|hashstat|history|hup|inlib|jobs|kill|limit|log|login|logout|ls-F|migrate|newgrp|nice|nohup|notify|onintr|popd|printenv|pushd|rehash|repeat|rootnode|popd|pushd|set|shift|sched|setenv|setpath|settc|setty|setxvers|shift|source|stop|suspend|source|suspend|telltc|time|umask|unalias|uncomplete|unhash|universe|unlimit|unset|unsetenv|ver|wait|warp|watchlog|where|which)\\s*\\b',
       Name.Builtin),
      (
       '#.*', Comment),
      (
       '\\\\[\\w\\W]', String.Escape),
      (
       '(\\b\\w+)(\\s*)(=)', bygroups(Name.Variable, Text, Operator)),
      (
       '[\\[\\]{}()=]+', Operator),
      (
       "<<\\s*(\\'?)\\\\?(\\w+)[\\w\\W]+?\\2", String),
      (
       ';', Punctuation)], 
     'data':[
      (
       '(?s)"(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\])*"', String.Double),
      (
       "(?s)'(\\\\\\\\|\\\\[0-7]+|\\\\.|[^'\\\\])*'", String.Single),
      (
       '\\s+', Text),
      (
       '[^=\\s\\[\\]{}()$"\\\'`\\\\;#]+', Text),
      (
       '\\d+(?= |\\Z)', Number),
      (
       '\\$#?(\\w+|.)', Name.Variable)], 
     'curly':[
      (
       '\\}', Keyword, '#pop'),
      (
       ':-', Keyword),
      (
       '\\w+', Name.Variable),
      (
       '[^}:"\\\'`$]+', Punctuation),
      (
       ':', Punctuation),
      include('root')], 
     'paren':[
      (
       '\\)', Keyword, '#pop'),
      include('root')], 
     'backticks':[
      (
       '`', String.Backtick, '#pop'),
      include('root')]}


class TcshSessionLexer(ShellSessionBaseLexer):
    __doc__ = '\n    Lexer for Tcsh sessions.\n\n    .. versionadded:: 2.1\n    '
    name = 'Tcsh Session'
    aliases = ['tcshcon']
    filenames = []
    mimetypes = []
    _innerLexerCls = TcshLexer
    _ps1rgx = re.compile('^([^>]+>)(.*\\n?)')
    _ps2 = '? '


class PowerShellLexer(RegexLexer):
    __doc__ = '\n    For Windows PowerShell code.\n\n    .. versionadded:: 1.5\n    '
    name = 'PowerShell'
    aliases = ['powershell', 'posh', 'ps1', 'psm1']
    filenames = ['*.ps1', '*.psm1']
    mimetypes = ['text/x-powershell']
    flags = re.DOTALL | re.IGNORECASE | re.MULTILINE
    keywords = 'while validateset validaterange validatepattern validatelength validatecount until trap switch return ref process param parameter in if global: function foreach for finally filter end elseif else dynamicparam do default continue cmdletbinding break begin alias \\? % #script #private #local #global mandatory parametersetname position valuefrompipeline valuefrompipelinebypropertyname valuefromremainingarguments helpmessage try catch throw'.split()
    operators = 'and as band bnot bor bxor casesensitive ccontains ceq cge cgt cle clike clt cmatch cne cnotcontains cnotlike cnotmatch contains creplace eq exact f file ge gt icontains ieq ige igt ile ilike ilt imatch ine inotcontains inotlike inotmatch ireplace is isnot le like lt match ne not notcontains notlike notmatch or regex replace wildcard'.split()
    verbs = 'write where watch wait use update unregister unpublish unprotect unlock uninstall undo unblock trace test tee take sync switch suspend submit stop step start split sort skip show set send select search scroll save revoke resume restore restart resolve resize reset request repair rename remove register redo receive read push publish protect pop ping out optimize open new move mount merge measure lock limit join invoke install initialize import hide group grant get format foreach find export expand exit enter enable edit dismount disconnect disable deny debug cxnew copy convertto convertfrom convert connect confirm compress complete compare close clear checkpoint block backup assert approve aggregate add'.split()
    aliases_ = 'ac asnp cat cd cfs chdir clc clear clhy cli clp cls clv cnsn compare copy cp cpi cpp curl cvpa dbp del diff dir dnsn ebp echo epal epcsv epsn erase etsn exsn fc fhx fl foreach ft fw gal gbp gc gci gcm gcs gdr ghy gi gjb gl gm gmo gp gps gpv group gsn gsnp gsv gu gv gwmi h history icm iex ihy ii ipal ipcsv ipmo ipsn irm ise iwmi iwr kill lp ls man md measure mi mount move mp mv nal ndr ni nmo npssc nsn nv ogv oh popd ps pushd pwd r rbp rcjb rcsn rd rdr ren ri rjb rm rmdir rmo rni rnp rp rsn rsnp rujb rv rvpa rwmi sajb sal saps sasv sbp sc select set shcm si sl sleep sls sort sp spjb spps spsv start sujb sv swmi tee trcm type wget where wjb write'.split()
    commenthelp = 'component description example externalhelp forwardhelpcategory forwardhelptargetname functionality inputs link notes outputs parameter remotehelprunspace role synopsis'.split()
    tokens = {'root':[
      (
       '\\(', Punctuation, 'child'),
      (
       '\\s+', Text),
      (
       '^(\\s*#[#\\s]*)(\\.(?:%s))([^\\n]*$)' % '|'.join(commenthelp),
       bygroups(Comment, String.Doc, Comment)),
      (
       '#[^\\n]*?$', Comment),
      (
       '(&lt;|<)#', Comment.Multiline, 'multline'),
      (
       '@"\\n', String.Heredoc, 'heredoc-double'),
      (
       "@'\\n.*?\\n'@", String.Heredoc),
      (
       '`[\\\'"$@-]', Punctuation),
      (
       '"', String.Double, 'string'),
      (
       "'([^']|'')*'", String.Single),
      (
       '(\\$|@@|@)((global|script|private|env):)?\\w+',
       Name.Variable),
      (
       '(%s)\\b' % '|'.join(keywords), Keyword),
      (
       '-(%s)\\b' % '|'.join(operators), Operator),
      (
       '(%s)-[a-z_]\\w*\\b' % '|'.join(verbs), Name.Builtin),
      (
       '(%s)\\s' % '|'.join(aliases_), Name.Builtin),
      (
       '\\[[a-z_\\[][\\w. `,\\[\\]]*\\]', Name.Constant),
      (
       '-[a-z_]\\w*', Name),
      (
       '\\w+', Name),
      (
       '[.,;@{}\\[\\]$()=+*/\\\\&%!~?^`|<>-]|::', Punctuation)], 
     'child':[
      (
       '\\)', Punctuation, '#pop'),
      include('root')], 
     'multline':[
      (
       '[^#&.]+', Comment.Multiline),
      (
       '#(>|&gt;)', Comment.Multiline, '#pop'),
      (
       '\\.(%s)' % '|'.join(commenthelp), String.Doc),
      (
       '[#&.]', Comment.Multiline)], 
     'string':[
      (
       '`[0abfnrtv\'\\"$`]', String.Escape),
      (
       '[^$`"]+', String.Double),
      (
       '\\$\\(', Punctuation, 'child'),
      (
       '""', String.Double),
      (
       '[`$]', String.Double),
      (
       '"', String.Double, '#pop')], 
     'heredoc-double':[
      (
       '\\n"@', String.Heredoc, '#pop'),
      (
       '\\$\\(', Punctuation, 'child'),
      (
       '[^@\\n]+"]', String.Heredoc),
      (
       '.', String.Heredoc)]}


class PowerShellSessionLexer(ShellSessionBaseLexer):
    __doc__ = '\n    Lexer for simplistic Windows PowerShell sessions.\n\n    .. versionadded:: 2.1\n    '
    name = 'PowerShell Session'
    aliases = ['ps1con']
    filenames = []
    mimetypes = []
    _innerLexerCls = PowerShellLexer
    _ps1rgx = re.compile('^(PS [^>]+> )(.*\\n?)')
    _ps2 = '>> '


class FishShellLexer(RegexLexer):
    __doc__ = '\n    Lexer for Fish shell scripts.\n\n    .. versionadded:: 2.1\n    '
    name = 'Fish'
    aliases = ['fish', 'fishshell']
    filenames = ['*.fish', '*.load']
    mimetypes = ['application/x-fish']
    tokens = {'root':[
      include('basic'),
      include('data'),
      include('interp')], 
     'interp':[
      (
       '\\$\\(\\(', Keyword, 'math'),
      (
       '\\(', Keyword, 'paren'),
      (
       '\\$#?(\\w+|.)', Name.Variable)], 
     'basic':[
      (
       '\\b(begin|end|if|else|while|break|for|in|return|function|block|case|continue|switch|not|and|or|set|echo|exit|pwd|true|false|cd|count|test)(\\s*)\\b',
       bygroups(Keyword, Text)),
      (
       '\\b(alias|bg|bind|breakpoint|builtin|command|commandline|complete|contains|dirh|dirs|emit|eval|exec|fg|fish|fish_config|fish_indent|fish_pager|fish_prompt|fish_right_prompt|fish_update_completions|fishd|funced|funcsave|functions|help|history|isatty|jobs|math|mimedb|nextd|open|popd|prevd|psub|pushd|random|read|set_color|source|status|trap|type|ulimit|umask|vared|fc|getopts|hash|kill|printf|time|wait)\\s*\\b(?!\\.)',
       Name.Builtin),
      (
       '#.*\\n', Comment),
      (
       '\\\\[\\w\\W]', String.Escape),
      (
       '(\\b\\w+)(\\s*)(=)', bygroups(Name.Variable, Text, Operator)),
      (
       '[\\[\\]()=]', Operator),
      (
       "<<-?\\s*(\\'?)\\\\?(\\w+)[\\w\\W]+?\\2", String)], 
     'data':[
      (
       '(?s)\\$?"(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\$])*"', String.Double),
      (
       '"', String.Double, 'string'),
      (
       "(?s)\\$'(\\\\\\\\|\\\\[0-7]+|\\\\.|[^'\\\\])*'", String.Single),
      (
       "(?s)'.*?'", String.Single),
      (
       ';', Punctuation),
      (
       '&|\\||\\^|<|>', Operator),
      (
       '\\s+', Text),
      (
       '\\d+(?= |\\Z)', Number),
      (
       '[^=\\s\\[\\]{}()$"\\\'`\\\\<&|;]+', Text)], 
     'string':[
      (
       '"', String.Double, '#pop'),
      (
       '(?s)(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\$])+', String.Double),
      include('interp')], 
     'paren':[
      (
       '\\)', Keyword, '#pop'),
      include('root')], 
     'math':[
      (
       '\\)\\)', Keyword, '#pop'),
      (
       '[-+*/%^|&]|\\*\\*|\\|\\|', Operator),
      (
       '\\d+#\\d+', Number),
      (
       '\\d+#(?! )', Number),
      (
       '\\d+', Number),
      include('root')]}