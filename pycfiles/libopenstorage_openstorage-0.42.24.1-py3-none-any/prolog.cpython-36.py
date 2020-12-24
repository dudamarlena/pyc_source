# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/prolog.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 12405 bytes
"""
    pygments.lexers.prolog
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Prolog and Prolog-like languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'PrologLexer', 'LogtalkLexer']

class PrologLexer(RegexLexer):
    __doc__ = '\n    Lexer for Prolog files.\n    '
    name = 'Prolog'
    aliases = ['prolog']
    filenames = ['*.ecl', '*.prolog', '*.pro', '*.pl']
    mimetypes = ['text/x-prolog']
    flags = re.UNICODE | re.MULTILINE
    tokens = {'root':[
      (
       '/\\*', Comment.Multiline, 'nested-comment'),
      (
       '%.*', Comment.Single),
      (
       "0\\'.", String.Char),
      (
       '0b[01]+', Number.Bin),
      (
       '0o[0-7]+', Number.Oct),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       "\\d\\d?\\'[a-zA-Z0-9]+", Number.Integer),
      (
       '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
      (
       '\\d+', Number.Integer),
      (
       '[\\[\\](){}|.,;!]', Punctuation),
      (
       ':-|-->', Punctuation),
      (
       '"(?:\\\\x[0-9a-fA-F]+\\\\|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|\\\\[0-7]+\\\\|\\\\["\\nabcefnrstv]|[^\\\\"])*"',
       String.Double),
      (
       "'(?:''|[^'])*'", String.Atom),
      (
       'is\\b', Operator),
      (
       '(<|>|=<|>=|==|=:=|=|/|//|\\*|\\+|-)(?=\\s|[a-zA-Z0-9\\[])',
       Operator),
      (
       '(mod|div|not)\\b', Operator),
      (
       '_', Keyword),
      (
       '([a-z]+)(:)', bygroups(Name.Namespace, Punctuation)),
      (
       '([a-zÀ-\u1fff\u3040-\ud7ff\ue000-\uffef][\\w$À-\u1fff\u3040-\ud7ff\ue000-\uffef]*)(\\s*)(:-|-->)',
       bygroups(Name.Function, Text, Operator)),
      (
       '([a-zÀ-\u1fff\u3040-\ud7ff\ue000-\uffef][\\w$À-\u1fff\u3040-\ud7ff\ue000-\uffef]*)(\\s*)(\\()',
       bygroups(Name.Function, Text, Punctuation)),
      (
       '[a-zÀ-\u1fff\u3040-\ud7ff\ue000-\uffef][\\w$À-\u1fff\u3040-\ud7ff\ue000-\uffef]*',
       String.Atom),
      (
       '[#&*+\\-./:<=>?@\\\\^~¡-¿‐-〿]+',
       String.Atom),
      (
       '[A-Z_]\\w*', Name.Variable),
      (
       '\\s+|[\u2000-\u200f\ufff0-\ufffe\uffef]', Text)], 
     'nested-comment':[
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


class LogtalkLexer(RegexLexer):
    __doc__ = '\n    For `Logtalk <http://logtalk.org/>`_ source code.\n\n    .. versionadded:: 0.10\n    '
    name = 'Logtalk'
    aliases = ['logtalk']
    filenames = ['*.lgt', '*.logtalk']
    mimetypes = ['text/x-logtalk']
    tokens = {'root':[
      (
       '^\\s*:-\\s', Punctuation, 'directive'),
      (
       '%.*?\\n', Comment),
      (
       '/\\*(.|\\n)*?\\*/', Comment),
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       "0'[\\\\]?.", Number),
      (
       '0b[01]+', Number.Bin),
      (
       '0o[0-7]+', Number.Oct),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '\\d+\\.?\\d*((e|E)(\\+|-)?\\d+)?', Number),
      (
       '([A-Z_][a-zA-Z0-9_]*)', Name.Variable),
      (
       '(after|before)(?=[(])', Keyword),
      (
       'forward(?=[(])', Keyword),
      (
       '(context|parameter|this|se(lf|nder))(?=[(])', Keyword),
      (
       '(current_predicate|predicate_property)(?=[(])', Keyword),
      (
       '(expand_(goal|term)|(goal|term)_expansion|phrase)(?=[(])', Keyword),
      (
       '(abolish|c(reate|urrent))_(object|protocol|category)(?=[(])', Keyword),
      (
       '(object|protocol|category)_property(?=[(])', Keyword),
      (
       'co(mplements_object|nforms_to_protocol)(?=[(])', Keyword),
      (
       'extends_(object|protocol|category)(?=[(])', Keyword),
      (
       'imp(lements_protocol|orts_category)(?=[(])', Keyword),
      (
       '(instantiat|specializ)es_class(?=[(])', Keyword),
      (
       '(current_event|(abolish|define)_events)(?=[(])', Keyword),
      (
       '(create|current|set)_logtalk_flag(?=[(])', Keyword),
      (
       'logtalk_(compile|l(ibrary_path|oad|oad_context)|make(_target_action)?)(?=[(])', Keyword),
      (
       '\\blogtalk_make\\b', Keyword),
      (
       '(clause|retract(all)?)(?=[(])', Keyword),
      (
       'a(bolish|ssert(a|z))(?=[(])', Keyword),
      (
       '(ca(ll|tch)|throw)(?=[(])', Keyword),
      (
       '(fa(il|lse)|true|(instantiation|system)_error)\\b', Keyword),
      (
       '(type|domain|existence|permission|representation|evaluation|resource|syntax)_error(?=[(])', Keyword),
      (
       '((bag|set)of|f(ind|or)all)(?=[(])', Keyword),
      (
       'threaded(_(ca(ll|ncel)|once|ignore|exit|peek|wait|notify))?(?=[(])', Keyword),
      (
       'threaded_engine(_(create|destroy|self|next|next_reified|yield|post|fetch))?(?=[(])', Keyword),
      (
       '(subsumes_term|unify_with_occurs_check)(?=[(])', Keyword),
      (
       '(functor|arg|copy_term|numbervars|term_variables)(?=[(])', Keyword),
      (
       '(div|rem|m(ax|in|od)|abs|sign)(?=[(])', Keyword),
      (
       'float(_(integer|fractional)_part)?(?=[(])', Keyword),
      (
       '(floor|t(an|runcate)|round|ceiling)(?=[(])', Keyword),
      (
       '(cos|a(cos|sin|tan|tan2)|exp|log|s(in|qrt)|xor)(?=[(])', Keyword),
      (
       '(var|atom(ic)?|integer|float|c(allable|ompound)|n(onvar|umber)|ground|acyclic_term)(?=[(])', Keyword),
      (
       'compare(?=[(])', Keyword),
      (
       '(curren|se)t_(in|out)put(?=[(])', Keyword),
      (
       '(open|close)(?=[(])', Keyword),
      (
       'flush_output(?=[(])', Keyword),
      (
       '(at_end_of_stream|flush_output)\\b', Keyword),
      (
       '(stream_property|at_end_of_stream|set_stream_position)(?=[(])', Keyword),
      (
       '(nl|(get|peek|put)_(byte|c(har|ode)))(?=[(])', Keyword),
      (
       '\\bnl\\b', Keyword),
      (
       'read(_term)?(?=[(])', Keyword),
      (
       'write(q|_(canonical|term))?(?=[(])', Keyword),
      (
       '(current_)?op(?=[(])', Keyword),
      (
       '(current_)?char_conversion(?=[(])', Keyword),
      (
       'atom_(length|c(hars|o(ncat|des)))(?=[(])', Keyword),
      (
       '(char_code|sub_atom)(?=[(])', Keyword),
      (
       'number_c(har|ode)s(?=[(])', Keyword),
      (
       '(se|curren)t_prolog_flag(?=[(])', Keyword),
      (
       '\\bhalt\\b', Keyword),
      (
       'halt(?=[(])', Keyword),
      (
       '(::|:|\\^\\^)', Operator),
      (
       '[{}]', Keyword),
      (
       '(ignore|once)(?=[(])', Keyword),
      (
       '\\brepeat\\b', Keyword),
      (
       '(key)?sort(?=[(])', Keyword),
      (
       '(>>|<<|/\\\\|\\\\\\\\|\\\\)', Operator),
      (
       '\\bas\\b', Operator),
      (
       '\\bis\\b', Keyword),
      (
       '(=:=|=\\\\=|<|=<|>=|>)', Operator),
      (
       '=\\.\\.', Operator),
      (
       '(=|\\\\=)', Operator),
      (
       '(==|\\\\==|@=<|@<|@>=|@>)', Operator),
      (
       '(//|[-+*/])', Operator),
      (
       '\\b(e|pi|div|mod|rem)\\b', Operator),
      (
       '\\b\\*\\*\\b', Operator),
      (
       '-->', Operator),
      (
       '([!;]|->)', Operator),
      (
       '\\\\+', Operator),
      (
       '[?@]', Operator),
      (
       '\\^', Operator),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       '[()\\[\\],.|]', Text),
      (
       '[a-z][a-zA-Z0-9_]*', Text),
      (
       "'", String, 'quoted_atom')], 
     'quoted_atom':[
      (
       "''", String),
      (
       "'", String, '#pop'),
      (
       '\\\\([\\\\abfnrtv"\\\']|(x[a-fA-F0-9]+|[0-7]+)\\\\)', String.Escape),
      (
       "[^\\\\'\\n]+", String),
      (
       '\\\\', String)], 
     'directive':[
      (
       '(el)?if(?=[(])', Keyword, 'root'),
      (
       '(e(lse|ndif))(?=[.])', Keyword, 'root'),
      (
       '(category|object|protocol)(?=[(])', Keyword, 'entityrelations'),
      (
       '(end_(category|object|protocol))(?=[.])', Keyword, 'root'),
      (
       '(public|protected|private)(?=[(])', Keyword, 'root'),
      (
       'e(n(coding|sure_loaded)|xport)(?=[(])', Keyword, 'root'),
      (
       'in(clude|itialization|fo)(?=[(])', Keyword, 'root'),
      (
       '(built_in|dynamic|synchronized|threaded)(?=[.])', Keyword, 'root'),
      (
       '(alias|d(ynamic|iscontiguous)|m(eta_(non_terminal|predicate)|ode|ultifile)|s(et_(logtalk|prolog)_flag|ynchronized))(?=[(])', Keyword, 'root'),
      (
       'op(?=[(])', Keyword, 'root'),
      (
       '(c(alls|oinductive)|module|reexport|use(s|_module))(?=[(])', Keyword, 'root'),
      (
       '[a-z][a-zA-Z0-9_]*(?=[(])', Text, 'root'),
      (
       '[a-z][a-zA-Z0-9_]*(?=[.])', Text, 'root')], 
     'entityrelations':[
      (
       '(complements|extends|i(nstantiates|mp(lements|orts))|specializes)(?=[(])', Keyword),
      (
       "0'[\\\\]?.", Number),
      (
       '0b[01]+', Number.Bin),
      (
       '0o[0-7]+', Number.Oct),
      (
       '0x[0-9a-fA-F]+', Number.Hex),
      (
       '\\d+\\.?\\d*((e|E)(\\+|-)?\\d+)?', Number),
      (
       '([A-Z_][a-zA-Z0-9_]*)', Name.Variable),
      (
       '[a-z][a-zA-Z0-9_]*', Text),
      (
       "'", String, 'quoted_atom'),
      (
       '"(\\\\\\\\|\\\\"|[^"])*"', String),
      (
       '([)]\\.)', Text, 'root'),
      (
       '(::)', Operator),
      (
       '[()\\[\\],.|]', Text),
      (
       '%.*?\\n', Comment),
      (
       '/\\*(.|\\n)*?\\*/', Comment),
      (
       '\\n', Text),
      (
       '\\s+', Text)]}

    def analyse_text(text):
        if ':- object(' in text:
            return 1.0
        else:
            if ':- protocol(' in text:
                return 1.0
            else:
                if ':- category(' in text:
                    return 1.0
                if re.search('^:-\\s[a-z]', text, re.M):
                    return 0.9
            return 0.0