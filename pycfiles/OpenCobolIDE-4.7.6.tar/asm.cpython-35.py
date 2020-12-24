# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/asm.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 14627 bytes
"""
    pygments.lexers.asm
    ~~~~~~~~~~~~~~~~~~~

    Lexers for assembly languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, using, DelegatingLexer
from pygments.lexers.c_cpp import CppLexer, CLexer
from pygments.lexers.d import DLexer
from pygments.token import Text, Name, Number, String, Comment, Punctuation, Other, Keyword, Operator
__all__ = [
 'GasLexer', 'ObjdumpLexer', 'DObjdumpLexer', 'CppObjdumpLexer',
 'CObjdumpLexer', 'LlvmLexer', 'NasmLexer', 'NasmObjdumpLexer',
 'Ca65Lexer']

class GasLexer(RegexLexer):
    __doc__ = '\n    For Gas (AT&T) assembly code.\n    '
    name = 'GAS'
    aliases = ['gas', 'asm']
    filenames = ['*.s', '*.S']
    mimetypes = ['text/x-gas']
    string = '"(\\\\"|[^"])*"'
    char = '[\\w$.@-]'
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
                           "$'(.|\\\\')'", String.Char),
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
                      '[-*,.()\\[\\]!:]+', Punctuation)]}

    def analyse_text(text):
        if re.match('^\\.(text|data|section)', text, re.M):
            return True
        if re.match('^\\.\\w+', text, re.M):
            return 0.1


def _objdump_lexer_tokens(asm_lexer):
    """
    Common objdump lexer tokens to wrap an ASM lexer.
    """
    hex_re = '[0-9A-Za-z]'
    return {'root': [
              (
               '(.*?)(:)( +file format )(.*?)$',
               bygroups(Name.Label, Punctuation, Text, String)),
              (
               '(Disassembly of section )(.*?)(:)$',
               bygroups(Text, Name.Label, Punctuation)),
              (
               '(' + hex_re + '+)( )(<)(.*?)([-+])(0[xX][A-Za-z0-9]+)(>:)$',
               bygroups(Number.Hex, Text, Punctuation, Name.Function, Punctuation, Number.Hex, Punctuation)),
              (
               '(' + hex_re + '+)( )(<)(.*?)(>:)$',
               bygroups(Number.Hex, Text, Punctuation, Name.Function, Punctuation)),
              (
               '( *)(' + hex_re + '+:)(\\t)((?:' + hex_re + hex_re + ' )+)( *\t)([a-zA-Z].*?)$',
               bygroups(Text, Name.Label, Text, Number.Hex, Text, using(asm_lexer))),
              (
               '( *)(' + hex_re + '+:)(\\t)((?:' + hex_re + hex_re + ' )+)( *)(.*?)$',
               bygroups(Text, Name.Label, Text, Number.Hex, Text, String)),
              (
               '( *)(' + hex_re + '+:)(\\t)((?:' + hex_re + hex_re + ' )+)$',
               bygroups(Text, Name.Label, Text, Number.Hex)),
              (
               '\\t\\.\\.\\.$', Text),
              (
               '(\\t\\t\\t)(' + hex_re + '+:)( )([^\\t]+)(\\t)(.*?)([-+])(0x' + hex_re + '+)$',
               bygroups(Text, Name.Label, Text, Name.Property, Text, Name.Constant, Punctuation, Number.Hex)),
              (
               '(\\t\\t\\t)(' + hex_re + '+:)( )([^\\t]+)(\\t)(.*?)$',
               bygroups(Text, Name.Label, Text, Name.Property, Text, Name.Constant)),
              (
               '[^\\n]+\\n', Other)]}


class ObjdumpLexer(RegexLexer):
    __doc__ = "\n    For the output of 'objdump -dr'\n    "
    name = 'objdump'
    aliases = ['objdump']
    filenames = ['*.objdump']
    mimetypes = ['text/x-objdump']
    tokens = _objdump_lexer_tokens(GasLexer)


class DObjdumpLexer(DelegatingLexer):
    __doc__ = "\n    For the output of 'objdump -Sr on compiled D files'\n    "
    name = 'd-objdump'
    aliases = ['d-objdump']
    filenames = ['*.d-objdump']
    mimetypes = ['text/x-d-objdump']

    def __init__(self, **options):
        super(DObjdumpLexer, self).__init__(DLexer, ObjdumpLexer, **options)


class CppObjdumpLexer(DelegatingLexer):
    __doc__ = "\n    For the output of 'objdump -Sr on compiled C++ files'\n    "
    name = 'cpp-objdump'
    aliases = ['cpp-objdump', 'c++-objdumb', 'cxx-objdump']
    filenames = ['*.cpp-objdump', '*.c++-objdump', '*.cxx-objdump']
    mimetypes = ['text/x-cpp-objdump']

    def __init__(self, **options):
        super(CppObjdumpLexer, self).__init__(CppLexer, ObjdumpLexer, **options)


class CObjdumpLexer(DelegatingLexer):
    __doc__ = "\n    For the output of 'objdump -Sr on compiled C files'\n    "
    name = 'c-objdump'
    aliases = ['c-objdump']
    filenames = ['*.c-objdump']
    mimetypes = ['text/x-c-objdump']

    def __init__(self, **options):
        super(CObjdumpLexer, self).__init__(CLexer, ObjdumpLexer, **options)


class LlvmLexer(RegexLexer):
    __doc__ = '\n    For LLVM assembly code.\n    '
    name = 'LLVM'
    aliases = ['llvm']
    filenames = ['*.ll']
    mimetypes = ['text/x-llvm']
    string = '"[^"]*?"'
    identifier = '([-a-zA-Z$._][\\w\\-$.]*|' + string + ')'
    tokens = {'root': [
              include('whitespace'),
              (
               identifier + '\\s*:', Name.Label),
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
               '#\\d+', Name.Variable.Global),
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
                  '(begin|end|true|false|declare|define|global|constant|private|linker_private|internal|available_externally|linkonce|linkonce_odr|weak|weak_odr|appending|dllimport|dllexport|common|default|hidden|protected|extern_weak|external|thread_local|zeroinitializer|undef|null|to|tail|target|triple|datalayout|volatile|nuw|nsw|nnan|ninf|nsz|arcp|fast|exact|inbounds|align|addrspace|section|alias|module|asm|sideeffect|gc|dbg|linker_private_weak|attributes|blockaddress|initialexec|localdynamic|localexec|prefix|unnamed_addr|ccc|fastcc|coldcc|x86_stdcallcc|x86_fastcallcc|arm_apcscc|arm_aapcscc|arm_aapcs_vfpcc|ptx_device|ptx_kernel|intel_ocl_bicc|msp430_intrcc|spir_func|spir_kernel|x86_64_sysvcc|x86_64_win64cc|x86_thiscallcc|cc|c|signext|zeroext|inreg|sret|nounwind|noreturn|noalias|nocapture|byval|nest|readnone|readonly|inlinehint|noinline|alwaysinline|optsize|ssp|sspreq|noredzone|noimplicitfloat|naked|builtin|cold|nobuiltin|noduplicate|nonlazybind|optnone|returns_twice|sanitize_address|sanitize_memory|sanitize_thread|sspstrong|uwtable|returned|type|opaque|eq|ne|slt|sgt|sle|sge|ult|ugt|ule|uge|oeq|one|olt|ogt|ole|oge|ord|uno|ueq|une|x|acq_rel|acquire|alignstack|atomic|catch|cleanup|filter|inteldialect|max|min|monotonic|nand|personality|release|seq_cst|singlethread|umax|umin|unordered|xchg|add|fadd|sub|fsub|mul|fmul|udiv|sdiv|fdiv|urem|srem|frem|shl|lshr|ashr|and|or|xor|icmp|fcmp|phi|call|trunc|zext|sext|fptrunc|fpext|uitofp|sitofp|fptoui|fptosi|inttoptr|ptrtoint|bitcast|addrspacecast|select|va_arg|ret|br|switch|invoke|unwind|unreachable|indirectbr|landingpad|resume|malloc|alloca|free|load|store|getelementptr|extractelement|insertelement|shufflevector|getresult|extractvalue|insertvalue|atomicrmw|cmpxchg|fence)\\b',
                  Keyword),
                 (
                  'void|half|float|double|x86_fp80|fp128|ppc_fp128|label|metadata',
                  Keyword.Type),
                 (
                  'i[1-9]\\d*', Keyword)]}


class NasmLexer(RegexLexer):
    __doc__ = '\n    For Nasm (Intel) assembly code.\n    '
    name = 'NASM'
    aliases = ['nasm']
    filenames = ['*.asm', '*.ASM']
    mimetypes = ['text/x-nasm']
    identifier = '[a-z$._?][\\w$.?#@~]*'
    hexn = '(?:0x[0-9a-f]+|$0[0-9a-f]*|[0-9]+[0-9a-f]*h)'
    octn = '[0-7]+q'
    binn = '[01]+b'
    decn = '[0-9]+'
    floatn = decn + '\\.e?' + decn
    string = '"(\\\\"|[^"\\n])*"|' + "'(\\\\'|[^'\\n])*'|" + '`(\\\\`|[^`\\n])*`'
    declkw = '(?:res|d)[bwdqt]|times'
    register = 'r[0-9][0-5]?[bwd]|[a-d][lh]|[er]?[a-d]x|[er]?[sb]p|[er]?[sd]i|[c-gs]s|st[0-7]|mm[0-7]|cr[0-4]|dr[0-367]|tr[3-7]'
    wordop = 'seg|wrt|strict'
    type = 'byte|[dq]?word'
    directives = 'BITS|USE16|USE32|SECTION|SEGMENT|ABSOLUTE|EXTERN|GLOBAL|ORG|ALIGN|STRUC|ENDSTRUC|COMMON|CPU|GROUP|UPPERCASE|IMPORT|EXPORT|LIBRARY|MODULE'
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root': [
              (
               '^\\s*%', Comment.Preproc, 'preproc'),
              include('whitespace'),
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
                           binn, Number.Bin),
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


class NasmObjdumpLexer(ObjdumpLexer):
    __doc__ = "\n    For the output of 'objdump -d -M intel'.\n\n    .. versionadded:: 2.0\n    "
    name = 'objdump-nasm'
    aliases = ['objdump-nasm']
    filenames = ['*.objdump-intel']
    mimetypes = ['text/x-nasm-objdump']
    tokens = _objdump_lexer_tokens(NasmLexer)


class Ca65Lexer(RegexLexer):
    __doc__ = '\n    For ca65 assembler sources.\n\n    .. versionadded:: 1.6\n    '
    name = 'ca65 assembler'
    aliases = ['ca65']
    filenames = ['*.s']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               ';.*', Comment.Single),
              (
               '\\s+', Text),
              (
               '[a-z_.@$][\\w.@$]*:', Name.Label),
              (
               '((ld|st)[axy]|(in|de)[cxy]|asl|lsr|ro[lr]|adc|sbc|cmp|cp[xy]|cl[cvdi]|se[cdi]|jmp|jsr|bne|beq|bpl|bmi|bvc|bvs|bcc|bcs|p[lh][ap]|rt[is]|brk|nop|ta[xy]|t[xy]a|txs|tsx|and|ora|eor|bit)\\b',
               Keyword),
              (
               '\\.\\w+', Keyword.Pseudo),
              (
               '[-+~*/^&|!<>=]', Operator),
              (
               '"[^"\\n]*.', String),
              (
               "'[^'\\n]*.", String.Char),
              (
               '\\$[0-9a-f]+|[0-9a-f]+h\\b', Number.Hex),
              (
               '\\d+', Number.Integer),
              (
               '%[01]+', Number.Bin),
              (
               '[#,.:()=\\[\\]]', Punctuation),
              (
               '[a-z_.@$][\\w.@$]*', Name)]}

    def analyse_text(self, text):
        if re.match('^\\s*;', text, re.MULTILINE):
            return 0.9