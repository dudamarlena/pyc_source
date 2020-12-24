# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/asm.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.asm
    ~~~~~~~~~~~~~~~~~~~

    Lexers for assembly languages.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, using, DelegatingLexer
from pygments.lexers.compiled import DLexer, CppLexer, CLexer
from pygments.token import *
__all__ = [
 'GasLexer', 'ObjdumpLexer', 'DObjdumpLexer', 'CppObjdumpLexer',
 'CObjdumpLexer', 'LlvmLexer', 'NasmLexer']

class GasLexer(RegexLexer):
    """
    For Gas (AT&T) assembly code.
    """
    name = 'GAS'
    aliases = ['gas']
    filenames = ['*.s', '*.S']
    mimetypes = ['text/x-gas']
    string = '"(\\\\"|[^"])*"'
    char = '[a-zA-Z$._0-9@]'
    identifier = '(?:[a-zA-Z$_]' + char + '*|\\.' + char + '+)'
    number = '(?:0[xX][a-zA-Z0-9]+|\\d+)'
    tokens = {'root': [
              include('whitespace'),
              (
               identifier + ':', Name.Label),
              (
               '\\.' + identifier, Name.Attribute, 'directive-args'),
              (
               'lock|rep(n?z)?|data\\d+', Name.Attribute),
              (
               identifier, Name.Function, 'instruction-args'),
              (
               '[\\r\\n]+', Text)], 
       'directive-args': [
                        (
                         identifier, Name.Constant),
                        (
                         string, String),
                        (
                         '@' + identifier, Name.Attribute),
                        (
                         number, Number.Integer),
                        (
                         '[\\r\\n]+', Text, '#pop'),
                        (
                         '#.*?$', Comment, '#pop'),
                        include('punctuation'),
                        include('whitespace')], 
       'instruction-args': [
                          (
                           '([a-z0-9]+)( )(<)(' + identifier + ')(>)',
                           bygroups(Number.Hex, Text, Punctuation, Name.Constant, Punctuation)),
                          (
                           '([a-z0-9]+)( )(<)(' + identifier + ')([-+])(' + number + ')(>)',
                           bygroups(Number.Hex, Text, Punctuation, Name.Constant, Punctuation, Number.Integer, Punctuation)),
                          (
                           identifier, Name.Constant),
                          (
                           number, Number.Integer),
                          (
                           '%' + identifier, Name.Variable),
                          (
                           '$' + number, Number.Integer),
                          (
                           '[\\r\\n]+', Text, '#pop'),
                          (
                           '#.*?$', Comment, '#pop'),
                          include('punctuation'),
                          include('whitespace')], 
       'whitespace': [
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     '#.*?\\n', Comment)], 
       'punctuation': [
                     (
                      '[-*,.():]+', Punctuation)]}

    def analyse_text(text):
        return re.match('^\\.\\w+', text, re.M)


class ObjdumpLexer(RegexLexer):
    """
    For the output of 'objdump -dr'
    """
    name = 'objdump'
    aliases = ['objdump']
    filenames = ['*.objdump']
    mimetypes = ['text/x-objdump']
    hex = '[0-9A-Za-z]'
    tokens = {'root': [
              (
               '(.*?)(:)( +file format )(.*?)$',
               bygroups(Name.Label, Punctuation, Text, String)),
              (
               '(Disassembly of section )(.*?)(:)$',
               bygroups(Text, Name.Label, Punctuation)),
              (
               '(' + hex + '+)( )(<)(.*?)([-+])(0[xX][A-Za-z0-9]+)(>:)$',
               bygroups(Number.Hex, Text, Punctuation, Name.Function, Punctuation, Number.Hex, Punctuation)),
              (
               '(' + hex + '+)( )(<)(.*?)(>:)$',
               bygroups(Number.Hex, Text, Punctuation, Name.Function, Punctuation)),
              (
               '( *)(' + hex + '+:)(\\t)((?:' + hex + hex + ' )+)( *\t)([a-zA-Z].*?)$',
               bygroups(Text, Name.Label, Text, Number.Hex, Text, using(GasLexer))),
              (
               '( *)(' + hex + '+:)(\\t)((?:' + hex + hex + ' )+)( *)(.*?)$',
               bygroups(Text, Name.Label, Text, Number.Hex, Text, String)),
              (
               '( *)(' + hex + '+:)(\\t)((?:' + hex + hex + ' )+)$',
               bygroups(Text, Name.Label, Text, Number.Hex)),
              (
               '\t\\.\\.\\.$', Text),
              (
               '(\t\t\t)(' + hex + '+:)( )([^\t]+)(\t)(.*?)([-+])(0x' + hex + '+)$',
               bygroups(Text, Name.Label, Text, Name.Property, Text, Name.Constant, Punctuation, Number.Hex)),
              (
               '(\t\t\t)(' + hex + '+:)( )([^\t]+)(\t)(.*?)$',
               bygroups(Text, Name.Label, Text, Name.Property, Text, Name.Constant)),
              (
               '[^\n]+\n', Other)]}


class DObjdumpLexer(DelegatingLexer):
    """
    For the output of 'objdump -Sr on compiled D files'
    """
    name = 'd-objdump'
    aliases = ['d-objdump']
    filenames = ['*.d-objdump']
    mimetypes = ['text/x-d-objdump']

    def __init__(self, **options):
        super(DObjdumpLexer, self).__init__(DLexer, ObjdumpLexer, **options)


class CppObjdumpLexer(DelegatingLexer):
    """
    For the output of 'objdump -Sr on compiled C++ files'
    """
    name = 'cpp-objdump'
    aliases = ['cpp-objdump', 'c++-objdumb', 'cxx-objdump']
    filenames = ['*.cpp-objdump', '*.c++-objdump', '*.cxx-objdump']
    mimetypes = ['text/x-cpp-objdump']

    def __init__(self, **options):
        super(CppObjdumpLexer, self).__init__(CppLexer, ObjdumpLexer, **options)


class CObjdumpLexer(DelegatingLexer):
    """
    For the output of 'objdump -Sr on compiled C files'
    """
    name = 'c-objdump'
    aliases = ['c-objdump']
    filenames = ['*.c-objdump']
    mimetypes = ['text/x-c-objdump']

    def __init__(self, **options):
        super(CObjdumpLexer, self).__init__(CLexer, ObjdumpLexer, **options)


class LlvmLexer(RegexLexer):
    """
    For LLVM assembly code.
    """
    name = 'LLVM'
    aliases = ['llvm']
    filenames = ['*.ll']
    mimetypes = ['text/x-llvm']
    string = '"[^"]*?"'
    identifier = '([-a-zA-Z$._][-a-zA-Z$._0-9]*|' + string + ')'
    tokens = {'root': [
              include('whitespace'),
              (
               '^\\s*' + identifier + '\\s*:', Name.Label),
              include('keyword'),
              (
               '%' + identifier, Name.Variable),
              (
               '@' + identifier, Name.Variable.Global),
              (
               '%\\d+', Name.Variable.Anonymous),
              (
               '@\\d+', Name.Variable.Global),
              (
               '!' + identifier, Name.Variable),
              (
               '!\\d+', Name.Variable.Anonymous),
              (
               'c?' + string, String),
              (
               '0[xX][a-fA-F0-9]+', Number),
              (
               '-?\\d+(?:[.]\\d+)?(?:[eE][-+]?\\d+(?:[.]\\d+)?)?', Number),
              (
               '[=<>{}\\[\\]()*.,!]|x\\b', Punctuation)], 
       'whitespace': [
                    (
                     '(\\n|\\s)+', Text),
                    (
                     ';.*?\\n', Comment)], 
       'keyword': [
                 (
                  '(begin|end|true|false|declare|define|global|constant|private|linker_private|internal|available_externally|linkonce|linkonce_odr|weak|weak_odr|appending|dllimport|dllexport|common|default|hidden|protected|extern_weak|external|thread_local|zeroinitializer|undef|null|to|tail|target|triple|deplibs|datalayout|volatile|nuw|nsw|exact|inbounds|align|addrspace|section|alias|module|asm|sideeffect|gc|dbg|ccc|fastcc|coldcc|x86_stdcallcc|x86_fastcallcc|arm_apcscc|arm_aapcscc|arm_aapcs_vfpcc|cc|c|signext|zeroext|inreg|sret|nounwind|noreturn|noalias|nocapture|byval|nest|readnone|readonly|inlinehint|noinline|alwaysinline|optsize|ssp|sspreq|noredzone|noimplicitfloat|naked|type|opaque|eq|ne|slt|sgt|sle|sge|ult|ugt|ule|uge|oeq|one|olt|ogt|ole|oge|ord|uno|ueq|une|x|add|fadd|sub|fsub|mul|fmul|udiv|sdiv|fdiv|urem|srem|frem|shl|lshr|ashr|and|or|xor|icmp|fcmp|phi|call|trunc|zext|sext|fptrunc|fpext|uitofp|sitofp|fptouifptosi|inttoptr|ptrtoint|bitcast|select|va_arg|ret|br|switch|invoke|unwind|unreachable|malloc|alloca|free|load|store|getelementptr|extractelement|insertelement|shufflevector|getresult|extractvalue|insertvalue)\\b',
                  Keyword),
                 (
                  'void|float|double|x86_fp80|fp128|ppc_fp128|label|metadata',
                  Keyword.Type),
                 (
                  'i[1-9]\\d*', Keyword)]}


class NasmLexer(RegexLexer):
    """
    For Nasm (Intel) assembly code.
    """
    name = 'NASM'
    aliases = ['nasm']
    filenames = ['*.asm', '*.ASM']
    mimetypes = ['text/x-nasm']
    identifier = '[a-zA-Z$._?][a-zA-Z0-9$._?#@~]*'
    hexn = '(?:0[xX][0-9a-fA-F]+|$0[0-9a-fA-F]*|[0-9]+[0-9a-fA-F]*h)'
    octn = '[0-7]+q'
    binn = '[01]+b'
    decn = '[0-9]+'
    floatn = decn + '\\.e?' + decn
    string = '"(\\\\"|[^"])*"|' + "'(\\\\'|[^'])*'"
    declkw = '(?:res|d)[bwdqt]|times'
    register = '[a-d][lh]|e?[a-d]x|e?[sb]p|e?[sd]i|[c-gs]s|st[0-7]|mm[0-7]|cr[0-4]|dr[0-367]|tr[3-7]'
    wordop = 'seg|wrt|strict'
    type = 'byte|[dq]?word'
    directives = 'BITS|USE16|USE32|SECTION|SEGMENT|ABSOLUTE|EXTERN|GLOBAL|ORG|ALIGN|STRUC|ENDSTRUC|COMMON|CPU|GROUP|UPPERCASE|IMPORT|EXPORT|LIBRARY|MODULE'
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root': [
              include('whitespace'),
              (
               '^\\s*%', Comment.Preproc, 'preproc'),
              (
               identifier + ':', Name.Label),
              (
               '(%s)(\\s+)(equ)' % identifier,
               bygroups(Name.Constant, Keyword.Declaration, Keyword.Declaration),
               'instruction-args'),
              (
               directives, Keyword, 'instruction-args'),
              (
               declkw, Keyword.Declaration, 'instruction-args'),
              (
               identifier, Name.Function, 'instruction-args'),
              (
               '[\\r\\n]+', Text)], 
       'instruction-args': [
                          (
                           string, String),
                          (
                           hexn, Number.Hex),
                          (
                           octn, Number.Oct),
                          (
                           binn, Number),
                          (
                           floatn, Number.Float),
                          (
                           decn, Number.Integer),
                          include('punctuation'),
                          (
                           register, Name.Builtin),
                          (
                           identifier, Name.Variable),
                          (
                           '[\\r\\n]+', Text, '#pop'),
                          include('whitespace')], 
       'preproc': [
                 (
                  '[^;\\n]+', Comment.Preproc),
                 (
                  ';.*?\\n', Comment.Single, '#pop'),
                 (
                  '\\n', Comment.Preproc, '#pop')], 
       'whitespace': [
                    (
                     '\\n', Text),
                    (
                     '[ \\t]+', Text),
                    (
                     ';.*', Comment.Single)], 
       'punctuation': [
                     (
                      '[,():\\[\\]]+', Punctuation),
                     (
                      '[&|^<>+*/%~-]+', Operator),
                     (
                      '[$]+', Keyword.Constant),
                     (
                      wordop, Operator.Word),
                     (
                      type, Keyword.Type)]}