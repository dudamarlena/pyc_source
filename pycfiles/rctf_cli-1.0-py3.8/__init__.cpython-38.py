# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rctf-cli/rctf/__init__.py
# Compiled at: 2020-03-23 01:46:29
# Size of source mod 2**32: 3268 bytes
from . import logger
import os, sys
logging = logger.logging
colored = logger.colored
colored_command = logger.colored_command
colors = logger.colors
log_levels = logger.log_levels

def verify_privileges(euid=0):
    return os.geteuid() == euid


def check_file(fn):
    return os.path.isfile(fn)


def get_editor():
    editor = os.environ.get('EDITOR')
    try_editors = ['/usr/bin/vim', '/usr/bin/nano']
    for test_editor in try_editors:
        if editor:
            break
        if check_file(test_editor):
            editor = test_editor
    else:
        if not editor:
            raise RuntimeError('No $EDITOR configured and no editors discovered.')
        return editor


def execute--- This code section failed: ---

 L.  56         0  LOAD_GLOBAL              logging
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'Executing '
                6  LOAD_GLOBAL              colored_command
                8  LOAD_FAST                'command'
               10  CALL_FUNCTION_1       1  ''
               12  LOAD_STR                 '...'
               14  CALL_METHOD_3         3  ''
               16  POP_TOP          

 L.  58        18  LOAD_FAST                'environ'
               20  POP_JUMP_IF_TRUE     32  'to 32'

 L.  59        22  LOAD_GLOBAL              os
               24  LOAD_ATTR                environ
               26  LOAD_METHOD              copy
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'environ'
             32_0  COME_FROM            20  '20'

 L.  62        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'command'
               36  LOAD_GLOBAL              str
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L.  63        42  LOAD_STR                 '/bin/sh'
               44  LOAD_STR                 '-c'
               46  LOAD_FAST                'command'
               48  BUILD_LIST_3          3 
               50  STORE_FAST               'command'
             52_0  COME_FROM            40  '40'

 L.  65        52  LOAD_GLOBAL              subprocess
               54  LOAD_ATTR                Popen
               56  LOAD_FAST                'command'
               58  LOAD_CONST               False
               60  LOAD_GLOBAL              subprocess
               62  LOAD_ATTR                PIPE
               64  LOAD_GLOBAL              subprocess
               66  LOAD_ATTR                PIPE
               68  LOAD_GLOBAL              subprocess
               70  LOAD_ATTR                PIPE
               72  LOAD_FAST                'environ'
               74  LOAD_CONST               ('shell', 'stdin', 'stdout', 'stderr', 'env')
               76  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               78  STORE_FAST               'p'

 L.  67        80  LOAD_GLOBAL              selectors
               82  LOAD_METHOD              DefaultSelector
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'sel'

 L.  68        88  LOAD_FAST                'sel'
               90  LOAD_METHOD              register
               92  LOAD_FAST                'p'
               94  LOAD_ATTR                stdout
               96  LOAD_GLOBAL              selectors
               98  LOAD_ATTR                EVENT_READ
              100  CALL_METHOD_2         2  ''
              102  POP_TOP          

 L.  69       104  LOAD_FAST                'sel'
              106  LOAD_METHOD              register
              108  LOAD_FAST                'p'
              110  LOAD_ATTR                stderr
              112  LOAD_GLOBAL              selectors
              114  LOAD_ATTR                EVENT_READ
              116  CALL_METHOD_2         2  ''
              118  POP_TOP          

 L.  71       120  LOAD_CONST               False
              122  STORE_FAST               'should_exit'

 L.  72       124  LOAD_CONST               False
              126  STORE_FAST               'should_print_bars'

 L.  76       128  LOAD_FAST                'should_exit'
              130  POP_JUMP_IF_FALSE   136  'to 136'

 L.  77   132_134  BREAK_LOOP          298  'to 298'
            136_0  COME_FROM           130  '130'

 L.  79       136  LOAD_FAST                'sel'
              138  LOAD_METHOD              select
              140  CALL_METHOD_0         0  ''
              142  GET_ITER         
              144  FOR_ITER            296  'to 296'
              146  UNPACK_SEQUENCE_2     2 
              148  STORE_FAST               'key'
              150  STORE_FAST               '_'

 L.  80       152  LOAD_FAST                'key'
              154  LOAD_ATTR                fileobj
              156  LOAD_METHOD              read1
              158  CALL_METHOD_0         0  ''
              160  LOAD_METHOD              decode
              162  CALL_METHOD_0         0  ''
              164  STORE_FAST               'data'

 L.  82       166  LOAD_FAST                'data'
              168  POP_JUMP_IF_TRUE    178  'to 178'

 L.  83       170  LOAD_CONST               True
              172  STORE_FAST               'should_exit'

 L.  84       174  POP_TOP          
              176  JUMP_BACK           128  'to 128'
            178_0  COME_FROM           168  '168'

 L.  86       178  LOAD_GLOBAL              strip_ansi
              180  LOAD_FAST                'data'
              182  LOAD_METHOD              strip
              184  CALL_METHOD_0         0  ''
              186  CALL_FUNCTION_1       1  ''
              188  STORE_FAST               'data'

 L.  88       190  LOAD_STR                 ' *  '
              192  STORE_FAST               'prompt'

 L.  89       194  LOAD_FAST                'data'
              196  LOAD_METHOD              replace
              198  LOAD_STR                 '\n'
              200  LOAD_STR                 '\n'
              202  LOAD_FAST                'prompt'
              204  BINARY_ADD       
              206  CALL_METHOD_2         2  ''
              208  STORE_FAST               'data'

 L.  91       210  LOAD_FAST                'should_print_bars'
              212  POP_JUMP_IF_TRUE    232  'to 232'

 L.  92       214  LOAD_GLOBAL              logging
              216  LOAD_ATTR                debug
              218  LOAD_STR                 '--------------------------------------------------------------------------------'
              220  LOAD_STR                 ' *--'
              222  LOAD_CONST               ('prompt',)
              224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              226  POP_TOP          

 L.  93       228  LOAD_CONST               True
              230  STORE_FAST               'should_print_bars'
            232_0  COME_FROM           212  '212'

 L.  95       232  LOAD_FAST                'key'
              234  LOAD_ATTR                fileobj
              236  LOAD_FAST                'p'
              238  LOAD_ATTR                stdout
              240  COMPARE_OP               is
          242_244  POP_JUMP_IF_FALSE   270  'to 270'

 L.  97       246  LOAD_GLOBAL              logging
              248  LOAD_ATTR                debug
              250  LOAD_GLOBAL              colored
              252  LOAD_FAST                'data'
              254  LOAD_STR                 'italics'
              256  BUILD_LIST_1          1 
              258  CALL_FUNCTION_2       2  ''
              260  LOAD_FAST                'prompt'
              262  LOAD_CONST               ('prompt',)
              264  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              266  POP_TOP          
              268  JUMP_BACK           144  'to 144'
            270_0  COME_FROM           242  '242'

 L. 100       270  LOAD_GLOBAL              logging
              272  LOAD_ATTR                debug
              274  LOAD_GLOBAL              colored
              276  LOAD_FAST                'data'
              278  LOAD_STR                 'italics'
              280  LOAD_STR                 'bold'
              282  BUILD_LIST_2          2 
              284  CALL_FUNCTION_2       2  ''
              286  LOAD_FAST                'prompt'
              288  LOAD_CONST               ('prompt',)
              290  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              292  POP_TOP          
              294  JUMP_BACK           144  'to 144'
              296  JUMP_BACK           128  'to 128'

 L. 102       298  LOAD_FAST                'p'
              300  LOAD_METHOD              communicate
              302  CALL_METHOD_0         0  ''
              304  POP_TOP          

 L. 103       306  LOAD_FAST                'p'
              308  LOAD_ATTR                returncode
              310  STORE_FAST               'status_code'

 L. 106       312  LOAD_FAST                'should_print_bars'
          314_316  POP_JUMP_IF_FALSE   332  'to 332'

 L. 107       318  LOAD_GLOBAL              logging
              320  LOAD_ATTR                debug
              322  LOAD_STR                 '--------------------------------------------------------------------------------'
              324  LOAD_STR                 ' *--'
              326  LOAD_CONST               ('prompt',)
              328  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              330  POP_TOP          
            332_0  COME_FROM           314  '314'

 L. 109       332  LOAD_FAST                'status_code'
          334_336  POP_JUMP_IF_FALSE   356  'to 356'

 L. 110       338  LOAD_GLOBAL              logging
              340  LOAD_METHOD              error
              342  LOAD_STR                 'Command failed to execute; exited with status code '
              344  LOAD_GLOBAL              colored_command
              346  LOAD_FAST                'status_code'
              348  CALL_FUNCTION_1       1  ''
              350  LOAD_STR                 '.'
              352  CALL_METHOD_3         3  ''
              354  POP_TOP          
            356_0  COME_FROM           334  '334'

 L. 113       356  LOAD_FAST                'status_code'
              358  LOAD_CONST               1
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   408  'to 408'
              366  LOAD_GLOBAL              verify_privileges
              368  CALL_FUNCTION_0       0  ''
          370_372  POP_JUMP_IF_TRUE    408  'to 408'

 L. 114       374  LOAD_GLOBAL              logging
              376  LOAD_METHOD              warning
              378  LOAD_STR                 'Possible permission denied error? Try running as root.\n\n    %s\n'
              380  LOAD_GLOBAL              colored_command
              382  LOAD_STR                 ' '
              384  LOAD_METHOD              join
              386  LOAD_GLOBAL              sys
              388  LOAD_ATTR                argv
              390  CALL_METHOD_1         1  ''
              392  CALL_FUNCTION_1       1  ''
              394  BINARY_MODULO    
              396  CALL_METHOD_1         1  ''
              398  POP_TOP          

 L. 115       400  LOAD_GLOBAL              PermissionError
              402  LOAD_STR                 'Permission denied. Try running as root.'
              404  CALL_FUNCTION_1       1  ''
              406  RAISE_VARARGS_1       1  'exception instance'
            408_0  COME_FROM           370  '370'
            408_1  COME_FROM           362  '362'

 L. 118       408  LOAD_FAST                'status_code'
              410  LOAD_CONST               0
              412  COMPARE_OP               ==
              414  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 176


from . import rctf, config