# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/console/ansi.py
# Compiled at: 2020-03-19 23:19:03
# Size of source mod 2**32: 3357 bytes
import os, sys
_USE_ANSI = False

def init(enabled=os.isatty(sys.stdout.fileno())):
    global _USE_ANSI
    if not (enabled):
        if not 'OS' in os.environ or os.environ['OS'] == 'Windows_NT':
            raise ValueError('ANSI not suported on dumb terminals or Windows')
        else:
            _USE_ANSI = enabled


class FgPalette:
    GREY, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = [*range(30, 38)]
    RESET = 39


class BgPalette:
    GREY, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = [*range(40, 48)]
    RESET = 49


class StylePalette:
    RESET_ALL, BRIGHT, DIM, ITALICS, UNDERLINE, BLINK_SLOW, BLINK_FAST, INVERSE = [*range(0, 8)]
    STRIKE_THRU = 9
    RESET_BRIGHT, RESET_ITALICS, RESET_UNDERLINE, RESET_BLINK_SLOW, RESET_BLINK_FAST, RESET_INVERSE = [*range(22, 28)]
    RESET_STRIKE_THRU = 29
    RESET_DIM = RESET_BRIGHT


class AnsiCodes(object):
    _CSI = '\x1b['

    def __init__--- This code section failed: ---

 L.  67         0  LOAD_CODE                <code_object code_to_chars>
                2  LOAD_STR                 'AnsiCodes.__init__.<locals>.code_to_chars'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'code_to_chars'

 L.  70         8  LOAD_GLOBAL              dir
               10  LOAD_FAST                'codes'
               12  CALL_FUNCTION_1       1  ''
               14  GET_ITER         
             16_0  COME_FROM            30  '30'
               16  FOR_ITER            134  'to 134'
               18  STORE_FAST               'name'

 L.  71        20  LOAD_FAST                'name'
               22  LOAD_FAST                'name'
               24  LOAD_METHOD              upper
               26  CALL_METHOD_0         0  ''
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    16  'to 16'

 L.  72        32  LOAD_GLOBAL              getattr
               34  LOAD_FAST                'codes'
               36  LOAD_FAST                'name'
               38  CALL_FUNCTION_2       2  ''
               40  STORE_FAST               'value'

 L.  73        42  LOAD_GLOBAL              setattr
               44  LOAD_FAST                'self'
               46  LOAD_FAST                'name'
               48  LOAD_FAST                'code_to_chars'
               50  LOAD_FAST                'value'
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_3       3  ''
               56  POP_TOP          

 L.  76        58  LOAD_STR                 'RESET_%s'
               60  LOAD_FAST                'name'
               62  BINARY_MODULO    
               64  LOAD_STR                 'RESET'
               66  BUILD_TUPLE_2         2 
               68  GET_ITER         
             70_0  COME_FROM            82  '82'
               70  FOR_ITER            132  'to 132'
               72  STORE_FAST               'reset_name'

 L.  77        74  LOAD_GLOBAL              hasattr
               76  LOAD_FAST                'codes'
               78  LOAD_FAST                'reset_name'
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_FALSE    70  'to 70'

 L.  78        84  LOAD_GLOBAL              getattr
               86  LOAD_FAST                'codes'
               88  LOAD_FAST                'reset_name'
               90  CALL_FUNCTION_2       2  ''
               92  STORE_FAST               'reset_value'

 L.  79        94  LOAD_GLOBAL              setattr
               96  LOAD_FAST                'self'
               98  LOAD_FAST                'name'
              100  LOAD_METHOD              lower
              102  CALL_METHOD_0         0  ''

 L.  80       104  LOAD_GLOBAL              AnsiCodes
              106  LOAD_METHOD              _mkfunc
              108  LOAD_FAST                'code_to_chars'
              110  LOAD_FAST                'value'
              112  CALL_FUNCTION_1       1  ''

 L.  81       114  LOAD_FAST                'code_to_chars'
              116  LOAD_FAST                'reset_value'
              118  CALL_FUNCTION_1       1  ''

 L.  80       120  CALL_METHOD_2         2  ''

 L.  79       122  CALL_FUNCTION_3       3  ''
              124  POP_TOP          

 L.  82       126  POP_TOP          
              128  CONTINUE             16  'to 16'
              130  JUMP_BACK            70  'to 70'
              132  JUMP_BACK            16  'to 16'

Parse error at or near `CONTINUE' instruction at offset 128

    @staticmethod
    def _mkfunc(color, reset):

        def _cwrap(text, *styles):
            if not _USE_ANSI:
                return text
            s = ''
            for st in styles:
                s += st
            else:
                s += color + text + reset
                if styles:
                    s += Style.RESET_ALL
                return s

        return _cwrap

    def __getattribute__(self, name):
        attr = super(AnsiCodes, self).__getattribute__(name)
        if not _USE_ANSI:
            if hasattr(attr, 'startswith'):
                if attr.startswith(AnsiCodes._CSI):
                    return ''
        return attr

    def __getitem__(self, name):
        return getattr(self, name.upper())


Fg = AnsiCodes(FgPalette)
Bg = AnsiCodes(BgPalette)
Style = AnsiCodes(StylePalette)
__all__ = [
 'Fg', 'Bg', 'Style']