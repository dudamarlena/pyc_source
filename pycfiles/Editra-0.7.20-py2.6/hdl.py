# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/hdl.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.hdl
    ~~~~~~~~~~~~~~~~~~~

    Lexers for hardware descriptor languages.

    :copyright: Copyright 2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
__all__ = [
 'VerilogLexer']

class VerilogLexer(RegexLexer):
    """
    For verilog source code with preprocessor directives.

    *New in Pygments 1.4.*
    """
    name = 'verilog'
    aliases = ['v']
    filenames = ['*.v', '*.sv']
    mimetypes = ['text/x-verilog']
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'root': [
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
               "([0-9]+)|(\\'b)[0-1]+", Number.Hex),
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
               '`[a-zA-Z_][a-zA-Z0-9_]*', Name.Constant),
              (
               '^\\s*(package)(\\s+)', bygroups(Keyword.Namespace, Text)),
              (
               '^\\s*(import)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'),
              (
               '(always|always_comb|always_ff|always_latch|and|assign|automatic|begin|break|buf|bufif0|bufif1|case|casex|casez|cmos|const|continue|deassign|default|defparam|disable|do|edge|else|end|endcase|endfunction|endgenerate|endmodule|endpackage|endprimitive|endspecify|endtable|endtask|enum|event|final|for|force|forever|fork|function|generate|genvar|highz0|highz1|if|initial|inout|input|integer|join|large|localparam|macromodule|medium|module|nand|negedge|nmos|nor|not|notif0|notif1|or|output|packed|parameter|pmos|posedge|primitive|pull0|pull1|pulldown|pullup|rcmos|ref|release|repeat|return|rnmos|rpmos|rtran|rtranif0|rtranif1|scalared|signed|small|specify|specparam|strength|string|strong0|strong1|struct|table|task|tran|tranif0|tranif1|type|typedef|unsigned|var|vectored|void|wait|weak0|weak1|while|xnor|xor)\\b',
               Keyword),
              (
               '(`accelerate|`autoexpand_vectornets|`celldefine|`default_nettype|`else|`elsif|`endcelldefine|`endif|`endprotect|`endprotected|`expand_vectornets|`ifdef|`ifndef|`include|`noaccelerate|`noexpand_vectornets|`noremove_gatenames|`noremove_netnames|`nounconnected_drive|`protect|`protected|`remove_gatenames|`remove_netnames|`resetall|`timescale|`unconnected_drive|`undef)\\b',
               Comment.Preproc),
              (
               '(\\$bits|\\$bitstoreal|\\$bitstoshortreal|\\$countdrivers|\\$display|\\$fclose|\\$fdisplay|\\$finish|\\$floor|\\$fmonitor|\\$fopen|\\$fstrobe|\\$fwrite|\\$getpattern|\\$history|\\$incsave|\\$input|\\$itor|\\$key|\\$list|\\$log|\\$monitor|\\$monitoroff|\\$monitoron|\\$nokey|\\$nolog|\\$printtimescale|\\$random|\\$readmemb|\\$readmemh|\\$realtime|\\$realtobits|\\$reset|\\$reset_count|\\$reset_value|\\$restart|\\$rtoi|\\$save|\\$scale|\\$scope|\\$shortrealtobits|\\$showscopes|\\$showvariables|\\$showvars|\\$sreadmemb|\\$sreadmemh|\\$stime|\\$stop|\\$strobe|\\$time|\\$timeformat|\\$write)\\b',
               Name.Builtin),
              (
               '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
              (
               '(byte|shortint|int|longint|interger|time|bit|logic|reg|supply0|supply1|tri|triand|trior|tri0|tri1|trireg|uwire|wire|wand|worshortreal|real|realtime)\\b',
               Keyword.Type),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*:(?!:)', Name.Label),
              (
               '[a-zA-Z_][a-zA-Z0-9_]*', Name)], 
       'classname': [
                   (
                    '[a-zA-Z_][a-zA-Z0-9_]*', Name.Class, '#pop')], 
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
       'import': [
                (
                 '[a-zA-Z0-9_:]+\\*?', Name.Namespace, '#pop')]}

    def get_tokens_unprocessed(self, text):
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if value.isupper():
                    token = Name.Constant
            yield (
             index, token, value)