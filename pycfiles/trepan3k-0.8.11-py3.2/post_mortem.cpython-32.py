# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/post_mortem.py
# Compiled at: 2017-11-02 15:38:09
import inspect, os, sys, re, traceback
from trepan import debugger as Mdebugger
from trepan.exception import DebuggerQuit, DebuggerRestart

def get_last_or_frame_exception():
    """Intended to be used going into post mortem routines.  If
    sys.last_traceback is set, we will return that and assume that
    this is what post-mortem will want. If sys.last_traceback has not
    been set, then perhaps we *about* to raise an error and are
    fielding an exception. So assume that sys.exc_info()[2]
    is where we want to look."""
    try:
        if inspect.istraceback(sys.last_traceback):
            return (
             sys.last_type, sys.last_value, sys.last_traceback)
    except AttributeError:
        pass

    return sys.exc_info()


def pm(frameno=1, dbg=None):
    """Set up post-mortem debugging using the last traceback.  But if
    there is no traceback, we'll assume that sys.exc_info() contains
    what we want and frameno is the index location of where we want
    to start.

    'dbg', is an optional trepan.Trepan object.
    """
    post_mortem(get_last_or_frame_exception(), frameno, dbg=dbg)


def post_mortem_excepthook(exc_type, exc_value, exc_tb, tb_fn=None):
    if str(exc_type) == str(DebuggerQuit):
        return
    try:
        if str(exc_type) == str(DebuggerRestart):
            if exc_value and exc_value.sys_argv and len(exc_value.sys_argv) > 0:
                print('No restart handler - trying restart via execv(%s)' % repr(exc_value.sys_argv))
                os.execvp(exc_value.sys_argv[0], exc_value.sys_argv)
            else:
                print('No restart handler, no params registered')
                print('Entering post-mortem debugger...')
        else:
            if tb_fn:
                tb_fn(exc_type, exc_value, exc_tb)
            else:
                traceback.print_exception(exc_type, exc_value, exc_tb)
            print('Uncaught exception. Entering post-mortem debugger...')
        post_mortem((exc_type, exc_value, exc_tb))
        print('Post-mortem debugger finished.')
    except:
        pass


def post_mortem--- This code section failed: ---

 L.  95         0  LOAD_FAST                'dbg'
                3  LOAD_CONST               None
                6  COMPARE_OP               is
                9  POP_JUMP_IF_FALSE    57  'to 57'

 L.  97        12  LOAD_GLOBAL              Mdebugger
               15  LOAD_ATTR                debugger_obj
               18  LOAD_CONST               None
               21  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE    45  'to 45'

 L.  98        27  LOAD_GLOBAL              Mdebugger
               30  LOAD_ATTR                Trepan
               33  CALL_FUNCTION_0       0  '0 positional, 0 named'
               36  LOAD_GLOBAL              Mdebugger
               39  STORE_ATTR               debugger_obj

 L.  99        42  JUMP_FORWARD         45  'to 45'
             45_0  COME_FROM            42  '42'

 L. 100        45  LOAD_GLOBAL              Mdebugger
               48  LOAD_ATTR                debugger_obj
               51  STORE_FAST               'dbg'

 L. 101        54  JUMP_FORWARD         57  'to 57'
             57_0  COME_FROM            54  '54'

 L. 102        57  LOAD_GLOBAL              re
               60  LOAD_ATTR                compile
               63  LOAD_STR                 '^<.+>$'
               66  CALL_FUNCTION_1       1  '1 positional, 0 named'
               69  STORE_FAST               're_bogus_file'

 L. 104        72  LOAD_FAST                'exc'
               75  LOAD_CONST               0
               78  BINARY_SUBSCR    
               79  LOAD_CONST               None
               82  COMPARE_OP               is
               85  POP_JUMP_IF_FALSE   130  'to 130'

 L. 107        88  LOAD_GLOBAL              get_last_or_frame_exception
               91  CALL_FUNCTION_0       0  '0 positional, 0 named'
               94  STORE_FAST               'exc'

 L. 108        97  LOAD_FAST                'exc'
              100  LOAD_CONST               0
              103  BINARY_SUBSCR    
              104  LOAD_CONST               None
              107  COMPARE_OP               is
              110  POP_JUMP_IF_FALSE   130  'to 130'

 L. 109       113  LOAD_GLOBAL              print
              116  LOAD_STR                 "Can't find traceback for post_mortem in sys.last_traceback or sys.exec_info()"
              119  CALL_FUNCTION_1       1  '1 positional, 0 named'
              122  POP_TOP          

 L. 111       123  LOAD_CONST               None
              126  RETURN_END_IF    

 L. 112       127  JUMP_FORWARD        130  'to 130'
            130_0  COME_FROM           127  '127'

 L. 113       130  LOAD_FAST                'exc'
              133  UNPACK_SEQUENCE_3     3 
              136  STORE_FAST               'exc_type'
              139  STORE_FAST               'exc_value'
              142  STORE_FAST               'exc_tb'

 L. 114       145  LOAD_STR                 'Terminated with unhandled exception %s'

 L. 115       148  LOAD_FAST                'exc_type'
              151  BINARY_MODULO    
              152  LOAD_FAST                'dbg'
              155  LOAD_ATTR                core
              158  STORE_ATTR               execution_status

 L. 120       161  LOAD_FAST                'exc_tb'
              164  LOAD_CONST               None
              167  COMPARE_OP               is-not
              170  POP_JUMP_IF_FALSE   298  'to 298'

 L. 121       173  SETUP_LOOP          277  'to 277'
              176  LOAD_FAST                'exc_tb'
              179  LOAD_ATTR                tb_next
              182  LOAD_CONST               None
              185  COMPARE_OP               is-not
              188  POP_JUMP_IF_FALSE   276  'to 276'

 L. 122       191  LOAD_FAST                'exc_tb'
              194  LOAD_ATTR                tb_frame
              197  LOAD_ATTR                f_code
              200  LOAD_ATTR                co_filename
              203  STORE_FAST               'filename'

 L. 123       206  LOAD_FAST                'dbg'
              209  LOAD_ATTR                mainpyfile
              212  POP_JUMP_IF_FALSE   264  'to 264'
              215  LOAD_CONST               0
              218  LOAD_GLOBAL              len
              221  LOAD_FAST                'dbg'
              224  LOAD_ATTR                mainpyfile
              227  CALL_FUNCTION_1       1  '1 positional, 0 named'
              230  COMPARE_OP               ==
            233_0  COME_FROM           212  '212'
              233  POP_JUMP_IF_FALSE   264  'to 264'

 L. 124       236  LOAD_FAST                're_bogus_file'
              239  LOAD_ATTR                match
              242  LOAD_FAST                'filename'
              245  CALL_FUNCTION_1       1  '1 positional, 0 named'
              248  UNARY_NOT        
            249_0  COME_FROM           233  '233'
              249  POP_JUMP_IF_FALSE   264  'to 264'

 L. 125       252  LOAD_FAST                'filename'
              255  LOAD_FAST                'dbg'
              258  STORE_ATTR               mainpyfile

 L. 126       261  JUMP_FORWARD        264  'to 264'
            264_0  COME_FROM           261  '261'

 L. 127       264  LOAD_FAST                'exc_tb'
              267  LOAD_ATTR                tb_next
              270  STORE_FAST               'exc_tb'

 L. 128       273  JUMP_BACK           176  'to 176'
              276  POP_BLOCK        
            277_0  COME_FROM_LOOP      173  '173'

 L. 129       277  LOAD_FAST                'exc_tb'
              280  LOAD_ATTR                tb_frame
              283  LOAD_FAST                'dbg'
              286  LOAD_ATTR                core
              289  LOAD_ATTR                processor
              292  STORE_ATTR               curframe

 L. 130       295  JUMP_FORWARD        298  'to 298'
            298_0  COME_FROM           295  '295'

 L. 132       298  LOAD_CONST               0
              301  LOAD_GLOBAL              len
              304  LOAD_FAST                'dbg'
              307  LOAD_ATTR                program_sys_argv
              310  CALL_FUNCTION_1       1  '1 positional, 0 named'
              313  COMPARE_OP               ==
              316  POP_JUMP_IF_FALSE   375  'to 375'

 L. 134       319  LOAD_GLOBAL              list
              322  LOAD_GLOBAL              sys
              325  LOAD_ATTR                argv
              328  LOAD_CONST               1
              331  LOAD_CONST               None
              334  BUILD_SLICE_2         2 
              337  BINARY_SUBSCR    
              338  CALL_FUNCTION_1       1  '1 positional, 0 named'
              341  LOAD_FAST                'dbg'
              344  STORE_ATTR               program_sys_argv

 L. 135       347  LOAD_FAST                'dbg'
              350  LOAD_ATTR                mainpyfile
              353  BUILD_LIST_1          1 
              356  LOAD_FAST                'dbg'
              359  LOAD_ATTR                program_sys_argv
              362  LOAD_CONST               None
              365  LOAD_CONST               0
              368  BUILD_SLICE_2         2 
              371  STORE_SUBSCR     
              372  JUMP_FORWARD        375  'to 375'
            375_0  COME_FROM           372  '372'

 L. 142       375  SETUP_EXCEPT        455  'to 455'

 L. 152       378  LOAD_FAST                'exc_tb'
              381  LOAD_ATTR                tb_frame
              384  STORE_FAST               'f'

 L. 153       387  LOAD_FAST                'f'
              390  POP_JUMP_IF_FALSE   423  'to 423'
              393  LOAD_FAST                'f'
              396  LOAD_ATTR                f_lineno
              399  LOAD_FAST                'exc_tb'
              402  LOAD_ATTR                tb_lineno
              405  COMPARE_OP               !=
            408_0  COME_FROM           390  '390'
              408  POP_JUMP_IF_FALSE   423  'to 423'

 L. 153       411  LOAD_FAST                'f'
              414  LOAD_ATTR                f_back
              417  STORE_FAST               'f'
              420  JUMP_FORWARD        423  'to 423'
            423_0  COME_FROM           420  '420'

 L. 154       423  LOAD_FAST                'dbg'
              426  LOAD_ATTR                core
              429  LOAD_ATTR                processor
              432  LOAD_ATTR                event_processor
              435  LOAD_FAST                'f'
              438  LOAD_STR                 'exception'
              441  LOAD_FAST                'exc'
              444  LOAD_STR                 'Trepan3k:pm'
              447  CALL_FUNCTION_4       4  '4 positional, 0 named'
              450  POP_TOP          
              451  POP_BLOCK        
              452  JUMP_FORWARD        612  'to 612'
            455_0  COME_FROM_EXCEPT    375  '375'

 L. 155       455  DUP_TOP          
              456  LOAD_GLOBAL              DebuggerRestart
              459  COMPARE_OP               exception-match
              462  POP_JUMP_IF_FALSE   594  'to 594'
              465  POP_TOP          
              466  POP_TOP          
              467  POP_TOP          

 L. 156       468  SETUP_LOOP          590  'to 590'

 L. 157       471  LOAD_GLOBAL              list
              474  LOAD_FAST                'dbg'
              477  LOAD_ATTR                _program_sys_argv
              480  CALL_FUNCTION_1       1  '1 positional, 0 named'
              483  LOAD_GLOBAL              sys
              486  STORE_ATTR               argv

 L. 158       489  LOAD_FAST                'dbg'
              492  LOAD_ATTR                msg
              495  LOAD_STR                 'Restarting %s with arguments:\n\t%s'

 L. 159       498  LOAD_FAST                'dbg'
              501  LOAD_ATTR                filename
              504  LOAD_FAST                'dbg'
              507  LOAD_ATTR                mainpyfile
              510  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L. 160       513  LOAD_STR                 ' '
              516  LOAD_ATTR                join
              519  LOAD_FAST                'dbg'
              522  LOAD_ATTR                _program_sys_argv
              525  LOAD_CONST               1
              528  LOAD_CONST               None
              531  BUILD_SLICE_2         2 
              534  BINARY_SUBSCR    
              535  CALL_FUNCTION_1       1  '1 positional, 0 named'
              538  BUILD_TUPLE_2         2 
              541  BINARY_MODULO    
              542  CALL_FUNCTION_1       1  '1 positional, 0 named'
              545  POP_TOP          

 L. 161       546  SETUP_EXCEPT        569  'to 569'

 L. 162       549  LOAD_FAST                'dbg'
              552  LOAD_ATTR                run_script
              555  LOAD_FAST                'dbg'
              558  LOAD_ATTR                mainpyfile
              561  CALL_FUNCTION_1       1  '1 positional, 0 named'
              564  POP_TOP          
              565  POP_BLOCK        
              566  JUMP_BACK           471  'to 471'
            569_0  COME_FROM_EXCEPT    546  '546'

 L. 163       569  DUP_TOP          
              570  LOAD_GLOBAL              DebuggerRestart
              573  COMPARE_OP               exception-match
              576  POP_JUMP_IF_FALSE   586  'to 586'
              579  POP_TOP          
              580  POP_TOP          
              581  POP_TOP          

 L. 164       582  POP_EXCEPT       
              583  JUMP_BACK           471  'to 471'
              586  END_FINALLY      

 L. 165       587  CONTINUE            471  'to 471'
            590_0  COME_FROM_LOOP      468  '468'
              590  POP_EXCEPT       
              591  JUMP_FORWARD        612  'to 612'

 L. 166       594  DUP_TOP          
              595  LOAD_GLOBAL              DebuggerQuit
              598  COMPARE_OP               exception-match
              601  POP_JUMP_IF_FALSE   611  'to 611'
              604  POP_TOP          
              605  POP_TOP          
              606  POP_TOP          

 L. 167       607  POP_EXCEPT       
              608  JUMP_FORWARD        612  'to 612'
              611  END_FINALLY      
            612_0  COME_FROM           608  '608'
            612_1  COME_FROM           591  '591'
            612_2  COME_FROM           452  '452'

 L. 168       612  LOAD_CONST               None
              615  RETURN_VALUE     

Parse error at or near `POP_EXCEPT' instruction at offset 590


def uncaught_exception(dbg, tb_fn=None):
    exc = sys.exc_info()
    exc_type, exc_value, exc_tb = exc
    if exc_type == DebuggerQuit:
        return
    else:
        if exc_type == DebuggerRestart:
            print('restart not done yet - entering post mortem debugging')
        else:
            if exc_tb is None:
                print("You don't seem to have an exception traceback, yet.")
                return
            if tb_fn:
                tb_fn(exc_type, exc_value, exc_tb)
            else:
                traceback.print_exception(exc_type, exc_value, exc_tb)
            print('uncaught exception. entering post mortem debugging')
        dbg.core.execution_status = 'Terminated with unhandled exception %s' % exc_type
        dbg.core.processor.event_processorexc_tb.tb_frame'exception'exc'Trepan3k:pm'
        print('Post mortem debugger finished.')
        return


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pm()