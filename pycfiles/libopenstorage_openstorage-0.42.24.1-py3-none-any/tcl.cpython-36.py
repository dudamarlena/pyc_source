# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/tcl.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 5398 bytes
"""
    pygments.lexers.tcl
    ~~~~~~~~~~~~~~~~~~~

    Lexers for Tcl and related languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number
from pygments.util import shebang_matches
__all__ = [
 'TclLexer']

class TclLexer(RegexLexer):
    __doc__ = '\n    For Tcl source code.\n\n    .. versionadded:: 0.10\n    '
    keyword_cmds_re = words(('after', 'apply', 'array', 'break', 'catch', 'continue',
                             'elseif', 'else', 'error', 'eval', 'expr', 'for', 'foreach',
                             'global', 'if', 'namespace', 'proc', 'rename', 'return',
                             'set', 'switch', 'then', 'trace', 'unset', 'update',
                             'uplevel', 'upvar', 'variable', 'vwait', 'while'),
      prefix='\\b', suffix='\\b')
    builtin_cmds_re = words(('append', 'bgerror', 'binary', 'cd', 'chan', 'clock',
                             'close', 'concat', 'dde', 'dict', 'encoding', 'eof',
                             'exec', 'exit', 'fblocked', 'fconfigure', 'fcopy', 'file',
                             'fileevent', 'flush', 'format', 'gets', 'glob', 'history',
                             'http', 'incr', 'info', 'interp', 'join', 'lappend',
                             'lassign', 'lindex', 'linsert', 'list', 'llength', 'load',
                             'loadTk', 'lrange', 'lrepeat', 'lreplace', 'lreverse',
                             'lsearch', 'lset', 'lsort', 'mathfunc', 'mathop', 'memory',
                             'msgcat', 'open', 'package', 'pid', 'pkg::create', 'pkg_mkIndex',
                             'platform', 'platform::shell', 'puts', 'pwd', 're_syntax',
                             'read', 'refchan', 'regexp', 'registry', 'regsub', 'scan',
                             'seek', 'socket', 'source', 'split', 'string', 'subst',
                             'tell', 'time', 'tm', 'unknown', 'unload'),
      prefix='\\b', suffix='\\b')
    name = 'Tcl'
    aliases = ['tcl']
    filenames = ['*.tcl', '*.rvt']
    mimetypes = ['text/x-tcl', 'text/x-script.tcl', 'application/x-tcl']

    def _gen_command_rules(keyword_cmds_re, builtin_cmds_re, context=''):
        return [
         (
          keyword_cmds_re, Keyword, 'params' + context),
         (
          builtin_cmds_re, Name.Builtin, 'params' + context),
         (
          '([\\w.-]+)', Name.Variable, 'params' + context),
         (
          '#', Comment, 'comment')]

    tokens = {'root':[
      include('command'),
      include('basic'),
      include('data'),
      (
       '\\}', Keyword)], 
     'command':_gen_command_rules(keyword_cmds_re, builtin_cmds_re), 
     'command-in-brace':_gen_command_rules(keyword_cmds_re, builtin_cmds_re, '-in-brace'), 
     'command-in-bracket':_gen_command_rules(keyword_cmds_re, builtin_cmds_re, '-in-bracket'), 
     'command-in-paren':_gen_command_rules(keyword_cmds_re, builtin_cmds_re, '-in-paren'), 
     'basic':[
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
     'data':[
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
       '\\$([\\w.:-]+)', Name.Variable),
      (
       '([\\w.:-]+)', Text)], 
     'params':[
      (
       ';', Keyword, '#pop'),
      (
       '\\n', Text, '#pop'),
      (
       '(else|elseif|then)\\b', Keyword),
      include('basic'),
      include('data')], 
     'params-in-brace':[
      (
       '\\}', Keyword, ('#pop', '#pop')),
      include('params')], 
     'params-in-paren':[
      (
       '\\)', Keyword, ('#pop', '#pop')),
      include('params')], 
     'params-in-bracket':[
      (
       '\\]', Keyword, ('#pop', '#pop')),
      include('params')], 
     'string':[
      (
       '\\[', String.Double, 'string-square'),
      (
       '(?s)(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\])', String.Double),
      (
       '"', String.Double, '#pop')], 
     'string-square':[
      (
       '\\[', String.Double, 'string-square'),
      (
       '(?s)(\\\\\\\\|\\\\[0-7]+|\\\\.|\\\\\\n|[^\\]\\\\])', String.Double),
      (
       '\\]', String.Double, '#pop')], 
     'brace':[
      (
       '\\}', Keyword, '#pop'),
      include('command-in-brace'),
      include('basic'),
      include('data')], 
     'paren':[
      (
       '\\)', Keyword, '#pop'),
      include('command-in-paren'),
      include('basic'),
      include('data')], 
     'bracket':[
      (
       '\\]', Keyword, '#pop'),
      include('command-in-bracket'),
      include('basic'),
      include('data')], 
     'comment':[
      (
       '.*[^\\\\]\\n', Comment, '#pop'),
      (
       '.*\\\\\\n', Comment)]}

    def analyse_text(text):
        return shebang_matches(text, '(tcl)')