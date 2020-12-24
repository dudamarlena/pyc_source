# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/util/cprint.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2993 bytes
"""
Cross-platform color text printing

Based on colorama (see pyqtgraph/util/colorama/README.txt)
"""
import sys, re
from colorama.winterm import WinTerm, WinColor, WinStyle
from colorama.win32 import windll
_WIN = sys.platform.startswith('win')
if windll is not None:
    winterm = WinTerm()
else:
    _WIN = False

def winset(reset=False, fore=None, back=None, style=None, stderr=False):
    if reset:
        winterm.reset_all()
    if fore is not None:
        winterm.fore(fore, stderr)
    if back is not None:
        winterm.back(back, stderr)
    if style is not None:
        winterm.style(style, stderr)


ANSI = {}
WIN = {}
for i, color in enumerate(['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']):
    globals()[color] = i
    globals()['BR_' + color] = i + 8
    globals()['BACK_' + color] = i + 40
    ANSI[i] = '\x1b[%dm' % (30 + i)
    ANSI[i + 8] = '\x1b[2;%dm' % (30 + i)
    ANSI[i + 40] = '\x1b[%dm' % (40 + i)
    color = 'GREY' if color == 'WHITE' else color
    WIN[i] = {'fore':getattr(WinColor, color),  'style':WinStyle.NORMAL}
    WIN[i + 8] = {'fore':getattr(WinColor, color),  'style':WinStyle.BRIGHT}
    WIN[i + 40] = {'back': getattr(WinColor, color)}

RESET = -1
ANSI[RESET] = '\x1b[0m'
WIN[RESET] = {'reset': True}

def cprint--- This code section failed: ---

 L.  64         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'stream'
                4  LOAD_GLOBAL              basestring
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    42  'to 42'

 L.  65        10  LOAD_FAST                'kwds'
               12  LOAD_METHOD              get
               14  LOAD_STR                 'stream'
               16  LOAD_STR                 'stdout'
               18  CALL_METHOD_2         2  '2 positional arguments'
               20  STORE_FAST               'stream'

 L.  66        22  LOAD_FAST                'stream'
               24  LOAD_STR                 'stderr'
               26  COMPARE_OP               ==
               28  STORE_FAST               'err'

 L.  67        30  LOAD_GLOBAL              getattr
               32  LOAD_GLOBAL              sys
               34  LOAD_FAST                'stream'
               36  CALL_FUNCTION_2       2  '2 positional arguments'
               38  STORE_FAST               'stream'
               40  JUMP_FORWARD         54  'to 54'
             42_0  COME_FROM             8  '8'

 L.  69        42  LOAD_FAST                'kwds'
               44  LOAD_METHOD              get
               46  LOAD_STR                 'stderr'
               48  LOAD_CONST               False
               50  CALL_METHOD_2         2  '2 positional arguments'
               52  STORE_FAST               'err'
             54_0  COME_FROM            40  '40'

 L.  71        54  LOAD_GLOBAL              hasattr
               56  LOAD_FAST                'stream'
               58  LOAD_STR                 'isatty'
               60  CALL_FUNCTION_2       2  '2 positional arguments'
               62  POP_JUMP_IF_FALSE   192  'to 192'
               64  LOAD_FAST                'stream'
               66  LOAD_METHOD              isatty
               68  CALL_METHOD_0         0  '0 positional arguments'
               70  POP_JUMP_IF_FALSE   192  'to 192'

 L.  72        72  LOAD_GLOBAL              _WIN
               74  POP_JUMP_IF_FALSE   140  'to 140'

 L.  74        76  SETUP_LOOP          190  'to 190'
               78  LOAD_FAST                'args'
               80  GET_ITER         
               82  FOR_ITER            136  'to 136'
               84  STORE_FAST               'arg'

 L.  75        86  LOAD_GLOBAL              isinstance
               88  LOAD_FAST                'arg'
               90  LOAD_GLOBAL              basestring
               92  CALL_FUNCTION_2       2  '2 positional arguments'
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L.  76        96  LOAD_FAST                'stream'
               98  LOAD_METHOD              write
              100  LOAD_FAST                'arg'
              102  CALL_METHOD_1         1  '1 positional argument'
              104  POP_TOP          
              106  JUMP_BACK            82  'to 82'
            108_0  COME_FROM            94  '94'

 L.  78       108  LOAD_GLOBAL              WIN
              110  LOAD_FAST                'arg'
              112  BINARY_SUBSCR    
              114  STORE_FAST               'kwds'

 L.  79       116  LOAD_GLOBAL              winset
              118  BUILD_TUPLE_0         0 
              120  LOAD_STR                 'stderr'
              122  LOAD_FAST                'err'
              124  BUILD_MAP_1           1 
              126  LOAD_FAST                'kwds'
              128  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              130  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              132  POP_TOP          
              134  JUMP_BACK            82  'to 82'
              136  POP_BLOCK        
              138  JUMP_ABSOLUTE       226  'to 226'
            140_0  COME_FROM            74  '74'

 L.  82       140  SETUP_LOOP          226  'to 226'
              142  LOAD_FAST                'args'
              144  GET_ITER         
              146  FOR_ITER            188  'to 188'
              148  STORE_FAST               'arg'

 L.  83       150  LOAD_GLOBAL              isinstance
              152  LOAD_FAST                'arg'
              154  LOAD_GLOBAL              basestring
              156  CALL_FUNCTION_2       2  '2 positional arguments'
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L.  84       160  LOAD_FAST                'stream'
              162  LOAD_METHOD              write
              164  LOAD_FAST                'arg'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  POP_TOP          
              170  JUMP_BACK           146  'to 146'
            172_0  COME_FROM           158  '158'

 L.  86       172  LOAD_FAST                'stream'
              174  LOAD_METHOD              write
              176  LOAD_GLOBAL              ANSI
              178  LOAD_FAST                'arg'
              180  BINARY_SUBSCR    
              182  CALL_METHOD_1         1  '1 positional argument'
              184  POP_TOP          
              186  JUMP_BACK           146  'to 146'
              188  POP_BLOCK        
            190_0  COME_FROM_LOOP      140  '140'
            190_1  COME_FROM_LOOP       76  '76'
              190  JUMP_FORWARD        226  'to 226'
            192_0  COME_FROM            70  '70'
            192_1  COME_FROM            62  '62'

 L.  89       192  SETUP_LOOP          226  'to 226'
              194  LOAD_FAST                'args'
              196  GET_ITER         
            198_0  COME_FROM           210  '210'
              198  FOR_ITER            224  'to 224'
              200  STORE_FAST               'arg'

 L.  90       202  LOAD_GLOBAL              isinstance
              204  LOAD_FAST                'arg'
              206  LOAD_GLOBAL              basestring
              208  CALL_FUNCTION_2       2  '2 positional arguments'
              210  POP_JUMP_IF_FALSE   198  'to 198'

 L.  91       212  LOAD_FAST                'stream'
              214  LOAD_METHOD              write
              216  LOAD_FAST                'arg'
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_TOP          
              222  JUMP_BACK           198  'to 198'
              224  POP_BLOCK        
            226_0  COME_FROM_LOOP      192  '192'
            226_1  COME_FROM           190  '190'

Parse error at or near `COME_FROM_LOOP' instruction at offset 190_1


def cout(*args):
    """Shorthand for cprint('stdout', ...)"""
    cprint(*('stdout', ), *args)


def cerr(*args):
    """Shorthand for cprint('stderr', ...)"""
    cprint(*('stderr', ), *args)