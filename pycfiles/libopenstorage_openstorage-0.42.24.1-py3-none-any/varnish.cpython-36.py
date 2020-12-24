# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/varnish.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 7265 bytes
"""
    pygments.lexers.varnish
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Varnish configuration

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, bygroups, using, this, inherit, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Literal
__all__ = [
 'VCLLexer', 'VCLSnippetLexer']

class VCLLexer(RegexLexer):
    __doc__ = '\n    For Varnish Configuration Language (VCL).\n\n    .. versionadded:: 2.2\n    '
    name = 'VCL'
    aliases = ['vcl']
    filenames = ['*.vcl']
    mimetypes = ['text/x-vclsrc']

    def analyse_text(text):
        if text.startswith('vcl 4.0;'):
            return 1.0
        if '\nvcl 4.0;' in text[:1000]:
            return 0.9

    tokens = {'probe':[
      include('whitespace'),
      include('comments'),
      (
       '(\\.\\w+)(\\s*=\\s*)([^;]*)(;)',
       bygroups(Name.Attribute, Operator, using(this), Punctuation)),
      (
       '\\}', Punctuation, '#pop')], 
     'acl':[
      include('whitespace'),
      include('comments'),
      (
       '[!/]+', Operator),
      (
       ';', Punctuation),
      (
       '\\d+', Number),
      (
       '\\}', Punctuation, '#pop')], 
     'backend':[
      include('whitespace'),
      (
       '(\\.probe)(\\s*=\\s*)(\\w+)(;)',
       bygroups(Name.Attribute, Operator, Name.Variable.Global, Punctuation)),
      (
       '(\\.probe)(\\s*=\\s*)(\\{)',
       bygroups(Name.Attribute, Operator, Punctuation), 'probe'),
      (
       '(\\.\\w+\\b)(\\s*=\\s*)([^;]*)(\\s*;)',
       bygroups(Name.Attribute, Operator, using(this), Punctuation)),
      (
       '\\{', Punctuation, '#push'),
      (
       '\\}', Punctuation, '#pop')], 
     'statements':[
      (
       '(\\d\\.)?\\d+[sdwhmy]', Literal.Date),
      (
       '(\\d\\.)?\\d+ms', Literal.Date),
      (
       '(vcl_pass|vcl_hash|vcl_hit|vcl_init|vcl_backend_fetch|vcl_pipe|vcl_backend_response|vcl_synth|vcl_deliver|vcl_backend_error|vcl_fini|vcl_recv|vcl_purge|vcl_miss)\\b',
       Name.Function),
      (
       '(pipe|retry|hash|synth|deliver|purge|abandon|lookup|pass|fail|ok|miss|fetch|restart)\\b',
       Name.Constant),
      (
       '(beresp|obj|resp|req|req_top|bereq)\\.http\\.[a-zA-Z_-]+\\b', Name.Variable),
      (
       words(('obj.status', 'req.hash_always_miss', 'beresp.backend', 'req.esi_level', 'req.can_gzip',
       'beresp.ttl', 'obj.uncacheable', 'req.ttl', 'obj.hits', 'client.identity',
       'req.hash_ignore_busy', 'obj.reason', 'req.xid', 'req_top.proto', 'beresp.age',
       'obj.proto', 'obj.age', 'local.ip', 'beresp.uncacheable', 'req.method', 'beresp.backend.ip',
       'now', 'obj.grace', 'req.restarts', 'beresp.keep', 'req.proto', 'resp.proto',
       'bereq.xid', 'bereq.between_bytes_timeout', 'req.esi', 'bereq.first_byte_timeout',
       'bereq.method', 'bereq.connect_timeout', 'beresp.do_gzip', 'resp.status',
       'beresp.do_gunzip', 'beresp.storage_hint', 'resp.is_streaming', 'beresp.do_stream',
       'req_top.method', 'bereq.backend', 'beresp.backend.name', 'beresp.status',
       'req.url', 'obj.keep', 'obj.ttl', 'beresp.reason', 'bereq.retries', 'resp.reason',
       'bereq.url', 'beresp.do_esi', 'beresp.proto', 'client.ip', 'bereq.proto',
       'server.hostname', 'remote.ip', 'req.backend_hint', 'server.identity', 'req_top.url',
       'beresp.grace', 'beresp.was_304', 'server.ip', 'bereq.uncacheable'),
         suffix='\\b'),
       Name.Variable),
      (
       '[!%&+*\\-,/<.}{>=|~]+', Operator),
      (
       '[();]', Punctuation),
      (
       '[,]+', Punctuation),
      (
       words(('hash_data', 'regsub', 'regsuball', 'if', 'else', 'elsif', 'elif', 'synth',
       'synthetic', 'ban', 'return', 'set', 'unset', 'import', 'include', 'new',
       'rollback', 'call'),
         suffix='\\b'),
       Keyword),
      (
       'storage\\.\\w+\\.\\w+\\b', Name.Variable),
      (
       words(('true', 'false')), Name.Builtin),
      (
       '\\d+\\b', Number),
      (
       '(backend)(\\s+\\w+)(\\s*\\{)',
       bygroups(Keyword, Name.Variable.Global, Punctuation), 'backend'),
      (
       '(probe\\s)(\\s*\\w+\\s)(\\{)',
       bygroups(Keyword, Name.Variable.Global, Punctuation), 'probe'),
      (
       '(acl\\s)(\\s*\\w+\\s)(\\{)',
       bygroups(Keyword, Name.Variable.Global, Punctuation), 'acl'),
      (
       '(vcl )(4.0)(;)$',
       bygroups(Keyword.Reserved, Name.Constant, Punctuation)),
      (
       '(sub\\s+)([a-zA-Z]\\w*)(\\s*\\{)',
       bygroups(Keyword, Name.Function, Punctuation)),
      (
       '([a-zA-Z_]\\w*)(\\.)([a-zA-Z_]\\w*)(\\s*\\(.*\\))',
       bygroups(Name.Function, Punctuation, Name.Function, using(this))),
      (
       '[a-zA-Z_]\\w*', Name)], 
     'comment':[
      (
       '[^*/]+', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)], 
     'comments':[
      (
       '#.*$', Comment),
      (
       '/\\*', Comment.Multiline, 'comment'),
      (
       '//.*$', Comment)], 
     'string':[
      (
       '"', String, '#pop'),
      (
       '[^"\\n]+', String)], 
     'multistring':[
      (
       '[^"}]', String),
      (
       '"\\}', String, '#pop'),
      (
       '["}]', String)], 
     'whitespace':[
      (
       'L?"', String, 'string'),
      (
       '\\{"', String, 'multistring'),
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       '\\\\\\n', Text)], 
     'root':[
      include('whitespace'),
      include('comments'),
      include('statements'),
      (
       '\\s+', Text)]}


class VCLSnippetLexer(VCLLexer):
    __doc__ = '\n    For Varnish Configuration Language snippets.\n\n    .. versionadded:: 2.2\n    '
    name = 'VCLSnippets'
    aliases = ['vclsnippets', 'vclsnippet']
    mimetypes = ['text/x-vclsnippet']
    filenames = []

    def analyse_text(text):
        return 0

    tokens = {'snippetspre':[
      (
       '\\.\\.\\.+', Comment),
      (
       '(bereq|req|req_top|resp|beresp|obj|client|server|local|remote|storage)($|\\.\\*)',
       Name.Variable)], 
     'snippetspost':[
      (
       '(backend)\\b', Keyword.Reserved)], 
     'root':[
      include('snippetspre'),
      inherit,
      include('snippetspost')]}