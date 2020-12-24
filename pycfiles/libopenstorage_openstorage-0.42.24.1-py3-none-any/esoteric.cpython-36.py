# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/esoteric.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 9489 bytes
"""
    pygments.lexers.esoteric
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for esoteric languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
__all__ = [
 'BrainfuckLexer', 'BefungeLexer', 'RedcodeLexer', 'CAmkESLexer',
 'CapDLLexer', 'AheuiLexer']

class BrainfuckLexer(RegexLexer):
    __doc__ = '\n    Lexer for the esoteric `BrainFuck <http://www.muppetlabs.com/~breadbox/bf/>`_\n    language.\n    '
    name = 'Brainfuck'
    aliases = ['brainfuck', 'bf']
    filenames = ['*.bf', '*.b']
    mimetypes = ['application/x-brainfuck']
    tokens = {'common':[
      (
       '[.,]+', Name.Tag),
      (
       '[+-]+', Name.Builtin),
      (
       '[<>]+', Name.Variable),
      (
       '[^.,+\\-<>\\[\\]]+', Comment)], 
     'root':[
      (
       '\\[', Keyword, 'loop'),
      (
       '\\]', Error),
      include('common')], 
     'loop':[
      (
       '\\[', Keyword, '#push'),
      (
       '\\]', Keyword, '#pop'),
      include('common')]}


class BefungeLexer(RegexLexer):
    __doc__ = '\n    Lexer for the esoteric `Befunge <http://en.wikipedia.org/wiki/Befunge>`_\n    language.\n\n    .. versionadded:: 0.7\n    '
    name = 'Befunge'
    aliases = ['befunge']
    filenames = ['*.befunge']
    mimetypes = ['application/x-befunge']
    tokens = {'root': [
              (
               '[0-9a-f]', Number),
              (
               '[+*/%!`-]', Operator),
              (
               '[<>^v?\\[\\]rxjk]', Name.Variable),
              (
               '[:\\\\$.,n]', Name.Builtin),
              (
               '[|_mw]', Keyword),
              (
               '[{}]', Name.Tag),
              (
               '".*?"', String.Double),
              (
               "\\'.", String.Single),
              (
               '[#;]', Comment),
              (
               '[pg&~=@iotsy]', Keyword),
              (
               '[()A-Z]', Comment),
              (
               '\\s+', Text)]}


class CAmkESLexer(RegexLexer):
    __doc__ = '\n    Basic lexer for the input language for the\n    `CAmkES <https://sel4.systems/CAmkES/>`_ component platform.\n\n    .. versionadded:: 2.1\n    '
    name = 'CAmkES'
    aliases = ['camkes', 'idl4']
    filenames = ['*.camkes', '*.idl4']
    tokens = {'root': [
              (
               '^\\s*#.*\\n', Comment.Preproc),
              (
               '\\s+', Text),
              (
               '/\\*(.|\\n)*?\\*/', Comment),
              (
               '//.*\\n', Comment),
              (
               '[\\[(){},.;\\]]', Punctuation),
              (
               '[~!%^&*+=|?:<>/-]', Operator),
              (
               words(('assembly', 'attribute', 'component', 'composition', 'configuration', 'connection',
       'connector', 'consumes', 'control', 'dataport', 'Dataport', 'Dataports', 'emits',
       'event', 'Event', 'Events', 'export', 'from', 'group', 'hardware', 'has',
       'interface', 'Interface', 'maybe', 'procedure', 'Procedure', 'Procedures',
       'provides', 'template', 'thread', 'threads', 'to', 'uses', 'with'),
                 suffix='\\b'), Keyword),
              (
               words(('bool', 'boolean', 'Buf', 'char', 'character', 'double', 'float', 'in', 'inout',
       'int', 'int16_6', 'int32_t', 'int64_t', 'int8_t', 'integer', 'mutex', 'out',
       'real', 'refin', 'semaphore', 'signed', 'string', 'struct', 'uint16_t', 'uint32_t',
       'uint64_t', 'uint8_t', 'uintptr_t', 'unsigned', 'void'),
                 suffix='\\b'), Keyword.Type),
              (
               '[a-zA-Z_]\\w*_(priority|domain|buffer)', Keyword.Reserved),
              (
               words(('dma_pool', 'from_access', 'to_access'), suffix='\\b'),
               Keyword.Reserved),
              (
               'import\\s+(<[^>]*>|"[^"]*");', Comment.Preproc),
              (
               'include\\s+(<[^>]*>|"[^"]*");', Comment.Preproc),
              (
               '0[xX][\\da-fA-F]+', Number.Hex),
              (
               '-?[\\d]+', Number),
              (
               '-?[\\d]+\\.[\\d]+', Number.Float),
              (
               '"[^"]*"', String),
              (
               '[Tt]rue|[Ff]alse', Name.Builtin),
              (
               '[a-zA-Z_]\\w*', Name)]}


class CapDLLexer(RegexLexer):
    __doc__ = '\n    Basic lexer for\n    `CapDL <https://ssrg.nicta.com.au/publications/nictaabstracts/Kuz_KLW_10.abstract.pml>`_.\n\n    The source of the primary tool that reads such specifications is available\n    at https://github.com/seL4/capdl/tree/master/capDL-tool. Note that this\n    lexer only supports a subset of the grammar. For example, identifiers can\n    shadow type names, but these instances are currently incorrectly\n    highlighted as types. Supporting this would need a stateful lexer that is\n    considered unnecessarily complex for now.\n\n    .. versionadded:: 2.2\n    '
    name = 'CapDL'
    aliases = ['capdl']
    filenames = ['*.cdl']
    tokens = {'root': [
              (
               '^\\s*#.*\\n', Comment.Preproc),
              (
               '\\s+', Text),
              (
               '/\\*(.|\\n)*?\\*/', Comment),
              (
               '(//|--).*\\n', Comment),
              (
               '[<>\\[(){},:;=\\]]', Punctuation),
              (
               '\\.\\.', Punctuation),
              (
               words(('arch', 'arm11', 'caps', 'child_of', 'ia32', 'irq', 'maps', 'objects'),
                 suffix='\\b'), Keyword),
              (
               words(('aep', 'asid_pool', 'cnode', 'ep', 'frame', 'io_device', 'io_ports', 'io_pt',
       'notification', 'pd', 'pt', 'tcb', 'ut', 'vcpu'),
                 suffix='\\b'), Keyword.Type),
              (
               words(('asid', 'addr', 'badge', 'cached', 'dom', 'domainID', 'elf', 'fault_ep', 'G',
       'guard', 'guard_size', 'init', 'ip', 'prio', 'sp', 'R', 'RG', 'RX', 'RW',
       'RWG', 'RWX', 'W', 'WG', 'WX', 'level', 'masked', 'master_reply', 'paddr',
       'ports', 'reply', 'uncached'),
                 suffix='\\b'),
               Keyword.Reserved),
              (
               '0[xX][\\da-fA-F]+', Number.Hex),
              (
               '\\d+(\\.\\d+)?(k|M)?', Number),
              (
               words(('bits', ), suffix='\\b'), Number),
              (
               words(('cspace', 'vspace', 'reply_slot', 'caller_slot', 'ipc_buffer_slot'),
                 suffix='\\b'), Number),
              (
               '[a-zA-Z_][-@\\.\\w]*', Name)]}


class RedcodeLexer(RegexLexer):
    __doc__ = "\n    A simple Redcode lexer based on ICWS'94.\n    Contributed by Adam Blinkinsop <blinks@acm.org>.\n\n    .. versionadded:: 0.8\n    "
    name = 'Redcode'
    aliases = ['redcode']
    filenames = ['*.cw']
    opcodes = ('DAT', 'MOV', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'JMP', 'JMZ', 'JMN',
               'DJN', 'CMP', 'SLT', 'SPL', 'ORG', 'EQU', 'END')
    modifiers = ('A', 'B', 'AB', 'BA', 'F', 'X', 'I')
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               ';.*$', Comment.Single),
              (
               '\\b(%s)\\b' % '|'.join(opcodes), Name.Function),
              (
               '\\b(%s)\\b' % '|'.join(modifiers), Name.Decorator),
              (
               '[A-Za-z_]\\w+', Name),
              (
               '[-+*/%]', Operator),
              (
               '[#$@<>]', Operator),
              (
               '[.,]', Punctuation),
              (
               '[-+]?\\d+', Number.Integer)]}


class AheuiLexer(RegexLexer):
    __doc__ = '\n    Aheui_ Lexer.\n\n    Aheui_ is esoteric language based on Korean alphabets.\n\n    .. _Aheui: http://aheui.github.io/\n\n    '
    name = 'Aheui'
    aliases = ['aheui']
    filenames = ['*.aheui']
    tokens = {'root': [
              (
               '[나-낳냐-냫너-넣녀-녛노-놓뇨-눟뉴-닇다-닿댜-댷더-덯뎌-뎧도-돟됴-둫듀-딓따-땋땨-떃떠-떻뗘-뗳또-똫뚀-뚷뜌-띟라-랗랴-럏러-렇려-렿로-롷료-뤃류-릫마-맣먀-먛머-멓며-몋모-뫃묘-뭏뮤-믷바-밯뱌-뱧버-벟벼-볗보-봏뵤-붛뷰-빃빠-빻뺘-뺳뻐-뻫뼈-뼣뽀-뽛뾰-뿧쀼-삏사-샇샤-샿서-섷셔-셯소-솧쇼-숳슈-싛싸-쌓쌰-썋써-쎃쎠-쎻쏘-쏳쑈-쑿쓔-씧자-잫쟈-쟣저-젛져-졓조-좋죠-줗쥬-즿차-챃챠-챻처-첳쳐-쳫초-촣쵸-춯츄-칗카-캏캬-컇커-컿켜-켷코-콯쿄-쿻큐-킣타-탛탸-턓터-텋텨-톃토-톻툐-퉇튜-틯파-팧퍄-퍟퍼-펗펴-폏포-퐇표-풓퓨-픻하-핳햐-햫허-헣혀-혛호-홓효-훟휴-힇]',
               Operator),
              (
               '.', Comment)]}