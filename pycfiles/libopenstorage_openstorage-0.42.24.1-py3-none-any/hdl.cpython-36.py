# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/hdl.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 18179 bytes
"""
    pygments.lexers.hdl
    ~~~~~~~~~~~~~~~~~~~

    Lexers for hardware descriptor languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, include, using, this, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
__all__ = [
 'VerilogLexer', 'SystemVerilogLexer', 'VhdlLexer']

class VerilogLexer(RegexLexer):
    __doc__ = '\n    For verilog source code with preprocessor directives.\n\n    .. versionadded:: 1.4\n    '
    name = 'verilog'
    aliases = ['verilog', 'v']
    filenames = ['*.v']
    mimetypes = ['text/x-verilog']
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'root':[
      (
       '^\\s*`define', Comment.Preproc, 'macro'),
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
       '[{}#@]', Punctuation),
      (
       'L?"', String, 'string'),
      (
       "L?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[lL]?', Number.Float),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
      (
       "([0-9]+)|(\\'h)[0-9a-fA-F]+", Number.Hex),
      (
       "([0-9]+)|(\\'b)[01]+", Number.Bin),
      (
       "([0-9]+)|(\\'d)[0-9]+", Number.Integer),
      (
       "([0-9]+)|(\\'o)[0-7]+", Number.Oct),
      (
       "\\'[01xz]", Number),
      (
       '\\d+[Ll]?', Number.Integer),
      (
       '\\*/', Error),
      (
       '[~!%^&*+=|?:<>/-]', Operator),
      (
       "[()\\[\\],.;\\']", Punctuation),
      (
       '`[a-zA-Z_]\\w*', Name.Constant),
      (
       '^(\\s*)(package)(\\s+)', bygroups(Text, Keyword.Namespace, Text)),
      (
       '^(\\s*)(import)(\\s+)', bygroups(Text, Keyword.Namespace, Text),
       'import'),
      (
       words(('always', 'always_comb', 'always_ff', 'always_latch', 'and', 'assign', 'automatic',
       'begin', 'break', 'buf', 'bufif0', 'bufif1', 'case', 'casex', 'casez', 'cmos',
       'const', 'continue', 'deassign', 'default', 'defparam', 'disable', 'do', 'edge',
       'else', 'end', 'endcase', 'endfunction', 'endgenerate', 'endmodule', 'endpackage',
       'endprimitive', 'endspecify', 'endtable', 'endtask', 'enum', 'event', 'final',
       'for', 'force', 'forever', 'fork', 'function', 'generate', 'genvar', 'highz0',
       'highz1', 'if', 'initial', 'inout', 'input', 'integer', 'join', 'large', 'localparam',
       'macromodule', 'medium', 'module', 'nand', 'negedge', 'nmos', 'nor', 'not',
       'notif0', 'notif1', 'or', 'output', 'packed', 'parameter', 'pmos', 'posedge',
       'primitive', 'pull0', 'pull1', 'pulldown', 'pullup', 'rcmos', 'ref', 'release',
       'repeat', 'return', 'rnmos', 'rpmos', 'rtran', 'rtranif0', 'rtranif1', 'scalared',
       'signed', 'small', 'specify', 'specparam', 'strength', 'string', 'strong0',
       'strong1', 'struct', 'table', 'task', 'tran', 'tranif0', 'tranif1', 'type',
       'typedef', 'unsigned', 'var', 'vectored', 'void', 'wait', 'weak0', 'weak1',
       'while', 'xnor', 'xor'),
         suffix='\\b'),
       Keyword),
      (
       words(('accelerate', 'autoexpand_vectornets', 'celldefine', 'default_nettype', 'else',
       'elsif', 'endcelldefine', 'endif', 'endprotect', 'endprotected', 'expand_vectornets',
       'ifdef', 'ifndef', 'include', 'noaccelerate', 'noexpand_vectornets', 'noremove_gatenames',
       'noremove_netnames', 'nounconnected_drive', 'protect', 'protected', 'remove_gatenames',
       'remove_netnames', 'resetall', 'timescale', 'unconnected_drive', 'undef'),
         prefix='`', suffix='\\b'),
       Comment.Preproc),
      (
       words(('bits', 'bitstoreal', 'bitstoshortreal', 'countdrivers', 'display', 'fclose',
       'fdisplay', 'finish', 'floor', 'fmonitor', 'fopen', 'fstrobe', 'fwrite', 'getpattern',
       'history', 'incsave', 'input', 'itor', 'key', 'list', 'log', 'monitor', 'monitoroff',
       'monitoron', 'nokey', 'nolog', 'printtimescale', 'random', 'readmemb', 'readmemh',
       'realtime', 'realtobits', 'reset', 'reset_count', 'reset_value', 'restart',
       'rtoi', 'save', 'scale', 'scope', 'shortrealtobits', 'showscopes', 'showvariables',
       'showvars', 'sreadmemb', 'sreadmemh', 'stime', 'stop', 'strobe', 'time', 'timeformat',
       'write'),
         prefix='\\$',
         suffix='\\b'),
       Name.Builtin),
      (
       words(('byte', 'shortint', 'int', 'longint', 'integer', 'time', 'bit', 'logic', 'reg',
       'supply0', 'supply1', 'tri', 'triand', 'trior', 'tri0', 'tri1', 'trireg',
       'uwire', 'wire', 'wand', 'woshortreal', 'real', 'realtime'),
         suffix='\\b'),
       Keyword.Type),
      (
       '[a-zA-Z_]\\w*:(?!:)', Name.Label),
      (
       '\\$?[a-zA-Z_]\\w*', Name)], 
     'string':[
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
     'macro':[
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
     'import':[
      (
       '[\\w:]+\\*?', Name.Namespace, '#pop')]}


class SystemVerilogLexer(RegexLexer):
    __doc__ = '\n    Extends verilog lexer to recognise all SystemVerilog keywords from IEEE\n    1800-2009 standard.\n\n    .. versionadded:: 1.5\n    '
    name = 'systemverilog'
    aliases = ['systemverilog', 'sv']
    filenames = ['*.sv', '*.svh']
    mimetypes = ['text/x-systemverilog']
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'root':[
      (
       '^\\s*`define', Comment.Preproc, 'macro'),
      (
       '^(\\s*)(package)(\\s+)', bygroups(Text, Keyword.Namespace, Text)),
      (
       '^(\\s*)(import)(\\s+)', bygroups(Text, Keyword.Namespace, Text), 'import'),
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
       '[{}#@]', Punctuation),
      (
       'L?"', String, 'string'),
      (
       "L?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[lL]?', Number.Float),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
      (
       "([0-9]+)|(\\'h)[0-9a-fA-F]+", Number.Hex),
      (
       "([0-9]+)|(\\'b)[01]+", Number.Bin),
      (
       "([0-9]+)|(\\'d)[0-9]+", Number.Integer),
      (
       "([0-9]+)|(\\'o)[0-7]+", Number.Oct),
      (
       "\\'[01xz]", Number),
      (
       '\\d+[Ll]?', Number.Integer),
      (
       '\\*/', Error),
      (
       '[~!%^&*+=|?:<>/-]', Operator),
      (
       "[()\\[\\],.;\\']", Punctuation),
      (
       '`[a-zA-Z_]\\w*', Name.Constant),
      (
       words(('accept_on', 'alias', 'always', 'always_comb', 'always_ff', 'always_latch',
       'and', 'assert', 'assign', 'assume', 'automatic', 'before', 'begin', 'bind',
       'bins', 'binsof', 'bit', 'break', 'buf', 'bufif0', 'bufif1', 'byte', 'case',
       'casex', 'casez', 'cell', 'chandle', 'checker', 'class', 'clocking', 'cmos',
       'config', 'const', 'constraint', 'context', 'continue', 'cover', 'covergroup',
       'coverpoint', 'cross', 'deassign', 'default', 'defparam', 'design', 'disable',
       'dist', 'do', 'edge', 'else', 'end', 'endcase', 'endchecker', 'endclass',
       'endclocking', 'endconfig', 'endfunction', 'endgenerate', 'endgroup', 'endinterface',
       'endmodule', 'endpackage', 'endprimitive', 'endprogram', 'endproperty', 'endsequence',
       'endspecify', 'endtable', 'endtask', 'enum', 'event', 'eventually', 'expect',
       'export', 'extends', 'extern', 'final', 'first_match', 'for', 'force', 'foreach',
       'forever', 'fork', 'forkjoin', 'function', 'generate', 'genvar', 'global',
       'highz0', 'highz1', 'if', 'iff', 'ifnone', 'ignore_bins', 'illegal_bins',
       'implies', 'import', 'incdir', 'include', 'initial', 'inout', 'input', 'inside',
       'instance', 'int', 'integer', 'interface', 'intersect', 'join', 'join_any',
       'join_none', 'large', 'let', 'liblist', 'library', 'local', 'localparam',
       'logic', 'longint', 'macromodule', 'matches', 'medium', 'modport', 'module',
       'nand', 'negedge', 'new', 'nexttime', 'nmos', 'nor', 'noshowcancelled', 'not',
       'notif0', 'notif1', 'null', 'or', 'output', 'package', 'packed', 'parameter',
       'pmos', 'posedge', 'primitive', 'priority', 'program', 'property', 'protected',
       'pull0', 'pull1', 'pulldown', 'pullup', 'pulsestyle_ondetect', 'pulsestyle_onevent',
       'pure', 'rand', 'randc', 'randcase', 'randsequence', 'rcmos', 'real', 'realtime',
       'ref', 'reg', 'reject_on', 'release', 'repeat', 'restrict', 'return', 'rnmos',
       'rpmos', 'rtran', 'rtranif0', 'rtranif1', 's_always', 's_eventually', 's_nexttime',
       's_until', 's_until_with', 'scalared', 'sequence', 'shortint', 'shortreal',
       'showcancelled', 'signed', 'small', 'solve', 'specify', 'specparam', 'static',
       'string', 'strong', 'strong0', 'strong1', 'struct', 'super', 'supply0', 'supply1',
       'sync_accept_on', 'sync_reject_on', 'table', 'tagged', 'task', 'this', 'throughout',
       'time', 'timeprecision', 'timeunit', 'tran', 'tranif0', 'tranif1', 'tri',
       'tri0', 'tri1', 'triand', 'trior', 'trireg', 'type', 'typedef', 'union', 'unique',
       'unique0', 'unsigned', 'until', 'until_with', 'untyped', 'use', 'uwire', 'var',
       'vectored', 'virtual', 'void', 'wait', 'wait_order', 'wand', 'weak', 'weak0',
       'weak1', 'while', 'wildcard', 'wire', 'with', 'within', 'wor', 'xnor', 'xor'),
         suffix='\\b'),
       Keyword),
      (
       words(('`__FILE__', '`__LINE__', '`begin_keywords', '`celldefine', '`default_nettype',
       '`define', '`else', '`elsif', '`end_keywords', '`endcelldefine', '`endif',
       '`ifdef', '`ifndef', '`include', '`line', '`nounconnected_drive', '`pragma',
       '`resetall', '`timescale', '`unconnected_drive', '`undef', '`undefineall'),
         suffix='\\b'),
       Comment.Preproc),
      (
       words(('$display', '$displayb', '$displayh', '$displayo', '$dumpall', '$dumpfile',
       '$dumpflush', '$dumplimit', '$dumpoff', '$dumpon', '$dumpports', '$dumpportsall',
       '$dumpportsflush', '$dumpportslimit', '$dumpportsoff', '$dumpportson', '$dumpvars',
       '$fclose', '$fdisplay', '$fdisplayb', '$fdisplayh', '$fdisplayo', '$feof',
       '$ferror', '$fflush', '$fgetc', '$fgets', '$finish', '$fmonitor', '$fmonitorb',
       '$fmonitorh', '$fmonitoro', '$fopen', '$fread', '$fscanf', '$fseek', '$fstrobe',
       '$fstrobeb', '$fstrobeh', '$fstrobeo', '$ftell', '$fwrite', '$fwriteb', '$fwriteh',
       '$fwriteo', '$monitor', '$monitorb', '$monitorh', '$monitoro', '$monitoroff',
       '$monitoron', '$plusargs', '$random', '$readmemb', '$readmemh', '$rewind',
       '$sformat', '$sformatf', '$sscanf', '$strobe', '$strobeb', '$strobeh', '$strobeo',
       '$swrite', '$swriteb', '$swriteh', '$swriteo', '$test', '$ungetc', '$value$plusargs',
       '$write', '$writeb', '$writeh', '$writememb', '$writememh', '$writeo'),
         suffix='\\b'),
       Name.Builtin),
      (
       '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
      (
       words(('byte', 'shortint', 'int', 'longint', 'integer', 'time', 'bit', 'logic', 'reg',
       'supply0', 'supply1', 'tri', 'triand', 'trior', 'tri0', 'tri1', 'trireg',
       'uwire', 'wire', 'wand', 'woshortreal', 'real', 'realtime'),
         suffix='\\b'),
       Keyword.Type),
      (
       '[a-zA-Z_]\\w*:(?!:)', Name.Label),
      (
       '\\$?[a-zA-Z_]\\w*', Name)], 
     'classname':[
      (
       '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     'string':[
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
     'macro':[
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
     'import':[
      (
       '[\\w:]+\\*?', Name.Namespace, '#pop')]}


class VhdlLexer(RegexLexer):
    __doc__ = '\n    For VHDL source code.\n\n    .. versionadded:: 1.5\n    '
    name = 'vhdl'
    aliases = ['vhdl']
    filenames = ['*.vhdl', '*.vhd']
    mimetypes = ['text/x-vhdl']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root':[
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       '\\\\\\n', Text),
      (
       '--.*?$', Comment.Single),
      (
       "'(U|X|0|1|Z|W|L|H|-)'", String.Char),
      (
       '[~!%^&*+=|?:<>/-]', Operator),
      (
       "'[a-z_]\\w*", Name.Attribute),
      (
       "[()\\[\\],.;\\']", Punctuation),
      (
       '"[^\\n\\\\"]*"', String),
      (
       '(library)(\\s+)([a-z_]\\w*)',
       bygroups(Keyword, Text, Name.Namespace)),
      (
       '(use)(\\s+)(entity)', bygroups(Keyword, Text, Keyword)),
      (
       '(use)(\\s+)([a-z_][\\w.]*\\.)(all)',
       bygroups(Keyword, Text, Name.Namespace, Keyword)),
      (
       '(use)(\\s+)([a-z_][\\w.]*)',
       bygroups(Keyword, Text, Name.Namespace)),
      (
       '(std|ieee)(\\.[a-z_]\\w*)',
       bygroups(Name.Namespace, Name.Namespace)),
      (
       words(('std', 'ieee', 'work'), suffix='\\b'),
       Name.Namespace),
      (
       '(entity|component)(\\s+)([a-z_]\\w*)',
       bygroups(Keyword, Text, Name.Class)),
      (
       '(architecture|configuration)(\\s+)([a-z_]\\w*)(\\s+)(of)(\\s+)([a-z_]\\w*)(\\s+)(is)',
       bygroups(Keyword, Text, Name.Class, Text, Keyword, Text, Name.Class, Text, Keyword)),
      (
       '([a-z_]\\w*)(:)(\\s+)(process|for)',
       bygroups(Name.Class, Operator, Text, Keyword)),
      (
       '(end)(\\s+)', bygroups(using(this), Text), 'endblock'),
      include('types'),
      include('keywords'),
      include('numbers'),
      (
       '[a-z_]\\w*', Name)], 
     'endblock':[
      include('keywords'),
      (
       '[a-z_]\\w*', Name.Class),
      (
       '(\\s+)', Text),
      (
       ';', Punctuation, '#pop')], 
     'types':[
      (
       words(('boolean', 'bit', 'character', 'severity_level', 'integer', 'time', 'delay_length',
       'natural', 'positive', 'string', 'bit_vector', 'file_open_kind', 'file_open_status',
       'std_ulogic', 'std_ulogic_vector', 'std_logic', 'std_logic_vector', 'signed',
       'unsigned'),
         suffix='\\b'),
       Keyword.Type)], 
     'keywords':[
      (
       words(('abs', 'access', 'after', 'alias', 'all', 'and', 'architecture', 'array', 'assert',
       'attribute', 'begin', 'block', 'body', 'buffer', 'bus', 'case', 'component',
       'configuration', 'constant', 'disconnect', 'downto', 'else', 'elsif', 'end',
       'entity', 'exit', 'file', 'for', 'function', 'generate', 'generic', 'group',
       'guarded', 'if', 'impure', 'in', 'inertial', 'inout', 'is', 'label', 'library',
       'linkage', 'literal', 'loop', 'map', 'mod', 'nand', 'new', 'next', 'nor',
       'not', 'null', 'of', 'on', 'open', 'or', 'others', 'out', 'package', 'port',
       'postponed', 'procedure', 'process', 'pure', 'range', 'record', 'register',
       'reject', 'rem', 'return', 'rol', 'ror', 'select', 'severity', 'signal', 'shared',
       'sla', 'sll', 'sra', 'srl', 'subtype', 'then', 'to', 'transport', 'type',
       'units', 'until', 'use', 'variable', 'wait', 'when', 'while', 'with', 'xnor',
       'xor'),
         suffix='\\b'),
       Keyword)], 
     'numbers':[
      (
       '\\d{1,2}#[0-9a-f_]+#?', Number.Integer),
      (
       '\\d+', Number.Integer),
      (
       '(\\d+\\.\\d*|\\.\\d+|\\d+)E[+-]?\\d+', Number.Float),
      (
       'X"[0-9a-f_]+"', Number.Hex),
      (
       'O"[0-7_]+"', Number.Oct),
      (
       'B"[01_]+"', Number.Bin)]}