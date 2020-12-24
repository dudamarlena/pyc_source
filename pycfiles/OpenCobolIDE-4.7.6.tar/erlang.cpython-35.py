# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/erlang.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 18195 bytes
"""
    pygments.lexers.erlang
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Erlang.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import Lexer, RegexLexer, bygroups, words, do_insertions, include, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic
__all__ = [
 'ErlangLexer', 'ErlangShellLexer', 'ElixirConsoleLexer',
 'ElixirLexer']
line_re = re.compile('.*?\n')

class ErlangLexer(RegexLexer):
    __doc__ = '\n    For the Erlang functional programming language.\n\n    Blame Jeremy Thurgood (http://jerith.za.net/).\n\n    .. versionadded:: 0.9\n    '
    name = 'Erlang'
    aliases = ['erlang']
    filenames = ['*.erl', '*.hrl', '*.es', '*.escript']
    mimetypes = ['text/x-erlang']
    keywords = ('after', 'begin', 'case', 'catch', 'cond', 'end', 'fun', 'if', 'let',
                'of', 'query', 'receive', 'try', 'when')
    builtins = ('abs', 'append_element', 'apply', 'atom_to_list', 'binary_to_list',
                'bitstring_to_list', 'binary_to_term', 'bit_size', 'bump_reductions',
                'byte_size', 'cancel_timer', 'check_process_code', 'delete_module',
                'demonitor', 'disconnect_node', 'display', 'element', 'erase', 'exit',
                'float', 'float_to_list', 'fun_info', 'fun_to_list', 'function_exported',
                'garbage_collect', 'get', 'get_keys', 'group_leader', 'hash', 'hd',
                'integer_to_list', 'iolist_to_binary', 'iolist_size', 'is_atom',
                'is_binary', 'is_bitstring', 'is_boolean', 'is_builtin', 'is_float',
                'is_function', 'is_integer', 'is_list', 'is_number', 'is_pid', 'is_port',
                'is_process_alive', 'is_record', 'is_reference', 'is_tuple', 'length',
                'link', 'list_to_atom', 'list_to_binary', 'list_to_bitstring', 'list_to_existing_atom',
                'list_to_float', 'list_to_integer', 'list_to_pid', 'list_to_tuple',
                'load_module', 'localtime_to_universaltime', 'make_tuple', 'md5',
                'md5_final', 'md5_update', 'memory', 'module_loaded', 'monitor',
                'monitor_node', 'node', 'nodes', 'open_port', 'phash', 'phash2',
                'pid_to_list', 'port_close', 'port_command', 'port_connect', 'port_control',
                'port_call', 'port_info', 'port_to_list', 'process_display', 'process_flag',
                'process_info', 'purge_module', 'put', 'read_timer', 'ref_to_list',
                'register', 'resume_process', 'round', 'send', 'send_after', 'send_nosuspend',
                'set_cookie', 'setelement', 'size', 'spawn', 'spawn_link', 'spawn_monitor',
                'spawn_opt', 'split_binary', 'start_timer', 'statistics', 'suspend_process',
                'system_flag', 'system_info', 'system_monitor', 'system_profile',
                'term_to_binary', 'tl', 'trace', 'trace_delivered', 'trace_info',
                'trace_pattern', 'trunc', 'tuple_size', 'tuple_to_list', 'universaltime_to_localtime',
                'unlink', 'unregister', 'whereis')
    operators = '(\\+\\+?|--?|\\*|/|<|>|/=|=:=|=/=|=<|>=|==?|<-|!|\\?)'
    word_operators = ('and', 'andalso', 'band', 'bnot', 'bor', 'bsl', 'bsr', 'bxor',
                      'div', 'not', 'or', 'orelse', 'rem', 'xor')
    atom_re = "(?:[a-z]\\w*|'[^\\n']*[^\\\\]')"
    variable_re = '(?:[A-Z_]\\w*)'
    escape_re = '(?:\\\\(?:[bdefnrstv\\\'"\\\\/]|[0-7][0-7]?[0-7]?|\\^[a-zA-Z]))'
    macro_re = '(?:' + variable_re + '|' + atom_re + ')'
    base_re = '(?:[2-9]|[12][0-9]|3[0-6])'
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '%.*\\n', Comment),
              (
               words(keywords, suffix='\\b'), Keyword),
              (
               words(builtins, suffix='\\b'), Name.Builtin),
              (
               words(word_operators, suffix='\\b'), Operator.Word),
              (
               '^-', Punctuation, 'directive'),
              (
               operators, Operator),
              (
               '"', String, 'string'),
              (
               '<<', Name.Label),
              (
               '>>', Name.Label),
              (
               '(' + atom_re + ')(:)', bygroups(Name.Namespace, Punctuation)),
              (
               '(?:^|(?<=:))(' + atom_re + ')(\\s*)(\\()',
               bygroups(Name.Function, Text, Punctuation)),
              (
               '[+-]?' + base_re + '#[0-9a-zA-Z]+', Number.Integer),
              (
               '[+-]?\\d+', Number.Integer),
              (
               '[+-]?\\d+.\\d+', Number.Float),
              (
               '[]\\[:_@\\".{}()|;,]', Punctuation),
              (
               variable_re, Name.Variable),
              (
               atom_re, Name),
              (
               '\\?' + macro_re, Name.Constant),
              (
               '\\$(?:' + escape_re + '|\\\\[ %]|[^\\\\])', String.Char),
              (
               '#' + atom_re + '(:?\\.' + atom_re + ')?', Name.Label)], 
     
     'string': [
                (
                 escape_re, String.Escape),
                (
                 '"', String, '#pop'),
                (
                 '~[0-9.*]*[~#+bBcdefginpPswWxX]', String.Interpol),
                (
                 '[^"\\\\~]+', String),
                (
                 '~', String)], 
     
     'directive': [
                   (
                    '(define)(\\s*)(\\()(' + macro_re + ')',
                    bygroups(Name.Entity, Text, Punctuation, Name.Constant), '#pop'),
                   (
                    '(record)(\\s*)(\\()(' + macro_re + ')',
                    bygroups(Name.Entity, Text, Punctuation, Name.Label), '#pop'),
                   (
                    atom_re, Name.Entity, '#pop')]}


class ErlangShellLexer(Lexer):
    __doc__ = '\n    Shell sessions in erl (for Erlang code).\n\n    .. versionadded:: 1.1\n    '
    name = 'Erlang erl session'
    aliases = ['erl']
    filenames = ['*.erl-sh']
    mimetypes = ['text/x-erl-shellsession']
    _prompt_re = re.compile('\\d+>(?=\\s|\\Z)')

    def get_tokens_unprocessed(self, text):
        erlexer = ErlangLexer(**self.options)
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
                    for item in do_insertions(insertions, erlexer.get_tokens_unprocessed(curcode)):
                        yield item

                    curcode = ''
                    insertions = []
                if line.startswith('*'):
                    yield (
                     match.start(), Generic.Traceback, line)
                else:
                    yield (
                     match.start(), Generic.Output, line)

        if curcode:
            for item in do_insertions(insertions, erlexer.get_tokens_unprocessed(curcode)):
                yield item


def gen_elixir_string_rules(name, symbol, token):
    states = {}
    states['string_' + name] = [
     (
      '[^#%s\\\\]+' % (symbol,), token),
     include('escapes'),
     (
      '\\\\.', token),
     (
      '(%s)' % (symbol,), bygroups(token), '#pop'),
     include('interpol')]
    return states


def gen_elixir_sigstr_rules(term, token, interpol=True):
    if interpol:
        return [
         (
          '[^#%s\\\\]+' % (term,), token),
         include('escapes'),
         (
          '\\\\.', token),
         (
          '%s[a-zA-Z]*' % (term,), token, '#pop'),
         include('interpol')]
    else:
        return [('[^%s\\\\]+' % (term,), token),
         (
          '\\\\.', token),
         (
          '%s[a-zA-Z]*' % (term,), token, '#pop')]


class ElixirLexer(RegexLexer):
    __doc__ = '\n    For the `Elixir language <http://elixir-lang.org>`_.\n\n    .. versionadded:: 1.5\n    '
    name = 'Elixir'
    aliases = ['elixir', 'ex', 'exs']
    filenames = ['*.ex', '*.exs']
    mimetypes = ['text/x-elixir']
    KEYWORD = ('fn', 'do', 'end', 'after', 'else', 'rescue', 'catch')
    KEYWORD_OPERATOR = ('not', 'and', 'or', 'when', 'in')
    BUILTIN = ('case', 'cond', 'for', 'if', 'unless', 'try', 'receive', 'raise', 'quote',
               'unquote', 'unquote_splicing', 'throw', 'super')
    BUILTIN_DECLARATION = ('def', 'defp', 'defmodule', 'defprotocol', 'defmacro', 'defmacrop',
                           'defdelegate', 'defexception', 'defstruct', 'defimpl',
                           'defcallback')
    BUILTIN_NAMESPACE = ('import', 'require', 'use', 'alias')
    CONSTANT = ('nil', 'true', 'false')
    PSEUDO_VAR = ('_', '__MODULE__', '__DIR__', '__ENV__', '__CALLER__')
    OPERATORS3 = ('<<<', '>>>', '|||', '&&&', '^^^', '~~~', '===', '!==', '~>>', '<~>',
                  '|~>', '<|>')
    OPERATORS2 = ('==', '!=', '<=', '>=', '&&', '||', '<>', '++', '--', '|>', '=~',
                  '->', '<-', '|', '.', '=', '~>', '<~')
    OPERATORS1 = ('<', '>', '+', '-', '*', '/', '!', '^', '&')
    PUNCTUATION = ('\\\\', '<<', '>>', '=>', '(', ')', ':', ';', ',', '[', ']')

    def get_tokens_unprocessed(self, text):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if value in self.KEYWORD:
                    yield (
                     index, Keyword, value)
                else:
                    if value in self.KEYWORD_OPERATOR:
                        yield (
                         index, Operator.Word, value)
                    else:
                        if value in self.BUILTIN:
                            yield (
                             index, Keyword, value)
                        else:
                            if value in self.BUILTIN_DECLARATION:
                                yield (
                                 index, Keyword.Declaration, value)
                            else:
                                if value in self.BUILTIN_NAMESPACE:
                                    yield (
                                     index, Keyword.Namespace, value)
                                else:
                                    if value in self.CONSTANT:
                                        yield (
                                         index, Name.Constant, value)
                                    else:
                                        if value in self.PSEUDO_VAR:
                                            yield (
                                             index, Name.Builtin.Pseudo, value)
                                        else:
                                            yield (
                                             index, token, value)
            else:
                yield (
                 index, token, value)

    def gen_elixir_sigil_rules():
        terminators = [
         ('\\{', '\\}', 'cb'),
         ('\\[', '\\]', 'sb'),
         ('\\(', '\\)', 'pa'),
         ('<', '>', 'ab'),
         ('/', '/', 'slas'),
         ('\\|', '\\|', 'pipe'),
         ('"', '"', 'quot'),
         ("'", "'", 'apos')]
        triquotes = [
         ('"""', 'triquot'), ("'''", 'triapos')]
        token = String.Other
        states = {'sigils': []}
        for term, name in triquotes:
            states['sigils'] += [
             (
              '(~[a-z])(%s)' % (term,), bygroups(token, String.Heredoc),
              (
               name + '-end', name + '-intp')),
             (
              '(~[A-Z])(%s)' % (term,), bygroups(token, String.Heredoc),
              (
               name + '-end', name + '-no-intp'))]
            states[name + '-end'] = [
             (
              '[a-zA-Z]+', token, '#pop'),
             default('#pop')]
            states[name + '-intp'] = [
             (
              '^\\s*' + term, String.Heredoc, '#pop'),
             include('heredoc_interpol')]
            states[name + '-no-intp'] = [
             (
              '^\\s*' + term, String.Heredoc, '#pop'),
             include('heredoc_no_interpol')]

        for lterm, rterm, name in terminators:
            states['sigils'] += [
             (
              '~[a-z]' + lterm, token, name + '-intp'),
             (
              '~[A-Z]' + lterm, token, name + '-no-intp')]
            states[name + '-intp'] = gen_elixir_sigstr_rules(rterm, token)
            states[name + '-no-intp'] = gen_elixir_sigstr_rules(rterm, token, interpol=False)

        return states

    op3_re = '|'.join(re.escape(s) for s in OPERATORS3)
    op2_re = '|'.join(re.escape(s) for s in OPERATORS2)
    op1_re = '|'.join(re.escape(s) for s in OPERATORS1)
    ops_re = '(?:%s|%s|%s)' % (op3_re, op2_re, op1_re)
    punctuation_re = '|'.join(re.escape(s) for s in PUNCTUATION)
    alnum = '\\w'
    name_re = '(?:\\.\\.\\.|[a-z_]%s*[!?]?)' % alnum
    modname_re = '[A-Z]%(alnum)s*(?:\\.[A-Z]%(alnum)s*)*' % {'alnum': alnum}
    complex_name_re = '(?:%s|%s|%s)' % (name_re, modname_re, ops_re)
    special_atom_re = '(?:\\.\\.\\.|<<>>|%\\{\\}|%|\\{\\})'
    long_hex_char_re = '(\\\\x\\{)([\\da-fA-F]+)(\\})'
    hex_char_re = '(\\\\x[\\da-fA-F]{1,2})'
    escape_char_re = '(\\\\[abdefnrstv])'
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '#.*$', Comment.Single),
              (
               '(\\?)' + long_hex_char_re,
               bygroups(String.Char, String.Escape, Number.Hex, String.Escape)),
              (
               '(\\?)' + hex_char_re,
               bygroups(String.Char, String.Escape)),
              (
               '(\\?)' + escape_char_re,
               bygroups(String.Char, String.Escape)),
              (
               '\\?\\\\?.', String.Char),
              (
               ':::', String.Symbol),
              (
               '::', Operator),
              (
               ':' + special_atom_re, String.Symbol),
              (
               ':' + complex_name_re, String.Symbol),
              (
               ':"', String.Symbol, 'string_double_atom'),
              (
               ":'", String.Symbol, 'string_single_atom'),
              (
               '(%s|%s)(:)(?=\\s|\\n)' % (special_atom_re, complex_name_re),
               bygroups(String.Symbol, Punctuation)),
              (
               '@' + name_re, Name.Attribute),
              (
               name_re, Name),
              (
               '(%%?)(%s)' % (modname_re,), bygroups(Punctuation, Name.Class)),
              (
               op3_re, Operator),
              (
               op2_re, Operator),
              (
               punctuation_re, Punctuation),
              (
               '&\\d', Name.Entity),
              (
               op1_re, Operator),
              (
               '0b[01]+', Number.Bin),
              (
               '0o[0-7]+', Number.Oct),
              (
               '0x[\\da-fA-F]+', Number.Hex),
              (
               '\\d(_?\\d)*\\.\\d(_?\\d)*([eE][-+]?\\d(_?\\d)*)?', Number.Float),
              (
               '\\d(_?\\d)*', Number.Integer),
              (
               '"""\\s*', String.Heredoc, 'heredoc_double'),
              (
               "'''\\s*$", String.Heredoc, 'heredoc_single'),
              (
               '"', String.Double, 'string_double'),
              (
               "'", String.Single, 'string_single'),
              include('sigils'),
              (
               '%\\{', Punctuation, 'map_key'),
              (
               '\\{', Punctuation, 'tuple')], 
     
     'heredoc_double': [
                        (
                         '^\\s*"""', String.Heredoc, '#pop'),
                        include('heredoc_interpol')], 
     
     'heredoc_single': [
                        (
                         "^\\s*'''", String.Heredoc, '#pop'),
                        include('heredoc_interpol')], 
     
     'heredoc_interpol': [
                          (
                           '[^#\\\\\\n]+', String.Heredoc),
                          include('escapes'),
                          (
                           '\\\\.', String.Heredoc),
                          (
                           '\\n+', String.Heredoc),
                          include('interpol')], 
     
     'heredoc_no_interpol': [
                             (
                              '[^\\\\\\n]+', String.Heredoc),
                             (
                              '\\\\.', String.Heredoc),
                             (
                              '\\n+', String.Heredoc)], 
     
     'escapes': [
                 (
                  long_hex_char_re,
                  bygroups(String.Escape, Number.Hex, String.Escape)),
                 (
                  hex_char_re, String.Escape),
                 (
                  escape_char_re, String.Escape)], 
     
     'interpol': [
                  (
                   '#\\{', String.Interpol, 'interpol_string')], 
     
     'interpol_string': [
                         (
                          '\\}', String.Interpol, '#pop'),
                         include('root')], 
     
     'map_key': [
                 include('root'),
                 (
                  ':', Punctuation, 'map_val'),
                 (
                  '=>', Punctuation, 'map_val'),
                 (
                  '\\}', Punctuation, '#pop')], 
     
     'map_val': [
                 include('root'),
                 (
                  ',', Punctuation, '#pop'),
                 (
                  '(?=\\})', Punctuation, '#pop')], 
     
     'tuple': [
               include('root'),
               (
                '\\}', Punctuation, '#pop')]}
    tokens.update(gen_elixir_string_rules('double', '"', String.Double))
    tokens.update(gen_elixir_string_rules('single', "'", String.Single))
    tokens.update(gen_elixir_string_rules('double_atom', '"', String.Symbol))
    tokens.update(gen_elixir_string_rules('single_atom', "'", String.Symbol))
    tokens.update(gen_elixir_sigil_rules())


class ElixirConsoleLexer(Lexer):
    __doc__ = '\n    For Elixir interactive console (iex) output like:\n\n    .. sourcecode:: iex\n\n        iex> [head | tail] = [1,2,3]\n        [1,2,3]\n        iex> head\n        1\n        iex> tail\n        [2,3]\n        iex> [head | tail]\n        [1,2,3]\n        iex> length [head | tail]\n        3\n\n    .. versionadded:: 1.5\n    '
    name = 'Elixir iex session'
    aliases = ['iex']
    mimetypes = ['text/x-elixir-shellsession']
    _prompt_re = re.compile('(iex|\\.{3})(\\(\\d+\\))?> ')

    def get_tokens_unprocessed(self, text):
        exlexer = ElixirLexer(**self.options)
        curcode = ''
        in_error = False
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            if line.startswith('** '):
                in_error = True
                insertions.append((len(curcode),
                 [
                  (
                   0, Generic.Error, line[:-1])]))
                curcode += line[-1:]
            else:
                m = self._prompt_re.match(line)
                if m is not None:
                    in_error = False
                    end = m.end()
                    insertions.append((len(curcode),
                     [
                      (
                       0, Generic.Prompt, line[:end])]))
                    curcode += line[end:]
                else:
                    if curcode:
                        for item in do_insertions(insertions, exlexer.get_tokens_unprocessed(curcode)):
                            yield item

                        curcode = ''
                        insertions = []
                    token = Generic.Error if in_error else Generic.Output
                    yield (match.start(), token, line)

        if curcode:
            for item in do_insertions(insertions, exlexer.get_tokens_unprocessed(curcode)):
                yield item