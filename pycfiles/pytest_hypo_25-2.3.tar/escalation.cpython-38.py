# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\escalation.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 3384 bytes
import os, sys, traceback
from inspect import getframeinfo
from pathlib import Path
from typing import Dict
import hypothesis
from hypothesis.errors import DeadlineExceeded, HypothesisException, MultipleFailures, StopTest, UnsatisfiedAssumption

def belongs_to(package):
    if not hasattr(package, '__file__'):
        return lambda filepath: False
    root = Path(package.__file__).resolve().parent
    cache = {str: {}, bytes: {}}

    def accept--- This code section failed: ---

 L.  41         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'filepath'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'ftype'

 L.  42         8  SETUP_FINALLY        24  'to 24'

 L.  43        10  LOAD_DEREF               'cache'
               12  LOAD_FAST                'ftype'
               14  BINARY_SUBSCR    
               16  LOAD_FAST                'filepath'
               18  BINARY_SUBSCR    
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     8  '8'

 L.  44        24  DUP_TOP          
               26  LOAD_GLOBAL              KeyError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    42  'to 42'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  45        38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
             42_0  COME_FROM            30  '30'
               42  END_FINALLY      
             44_0  COME_FROM            40  '40'

 L.  46        44  LOAD_GLOBAL              Path
               46  LOAD_FAST                'filepath'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_METHOD              resolve
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'abspath'

 L.  47        56  SETUP_FINALLY        76  'to 76'

 L.  48        58  LOAD_FAST                'abspath'
               60  LOAD_METHOD              relative_to
               62  LOAD_DEREF               'root'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L.  49        68  LOAD_CONST               True
               70  STORE_FAST               'result'
               72  POP_BLOCK        
               74  JUMP_FORWARD        100  'to 100'
             76_0  COME_FROM_FINALLY    56  '56'

 L.  50        76  DUP_TOP          
               78  LOAD_GLOBAL              ValueError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE    98  'to 98'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L.  51        90  LOAD_CONST               False
               92  STORE_FAST               'result'
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            82  '82'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            74  '74'

 L.  52       100  LOAD_FAST                'result'
              102  LOAD_DEREF               'cache'
              104  LOAD_FAST                'ftype'
              106  BINARY_SUBSCR    
              108  LOAD_FAST                'filepath'
              110  STORE_SUBSCR     

 L.  53       112  LOAD_FAST                'result'
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 34

    accept.__name__ = 'is_%s_file' % (package.__name__,)
    return accept


PREVENT_ESCALATION = os.getenv('HYPOTHESIS_DO_NOT_ESCALATE') == 'true'
FILE_CACHE = {}
is_hypothesis_file = belongs_to(hypothesis)
HYPOTHESIS_CONTROL_EXCEPTIONS = (
 DeadlineExceeded, StopTest, UnsatisfiedAssumption)

def mark_for_escalation(e):
    if not isinstance(e, HYPOTHESIS_CONTROL_EXCEPTIONS):
        e.hypothesis_internal_always_escalate = True


def escalate_hypothesis_internal_error():
    if PREVENT_ESCALATION:
        return
    else:
        error_type, e, tb = sys.exc_info()
        if getattr(e, 'hypothesis_internal_never_escalate', False):
            return
        if getattr(e, 'hypothesis_internal_always_escalate', False):
            raise
        filepath = traceback.extract_tb(tb)[(-1)][0]
        if is_hypothesis_file(filepath) and not isinstance(e, (HypothesisException,) + HYPOTHESIS_CONTROL_EXCEPTIONS):
            raise


def get_trimmed_traceback():
    """Return the current traceback, minus any frames added by Hypothesis."""
    error_type, _, tb = sys.exc_info()
    if not hypothesis.settings.default.verbosity >= hypothesis.Verbosity.debug:
        if is_hypothesis_file(traceback.extract_tb(tb)[(-1)][0]):
            return isinstance(error_type, MultipleFailures) or tb
    else:
        while tb is not None:
            if is_hypothesis_file(getframeinfo(tb.tb_frame)[0]) or tb.tb_frame.f_globals.get('__hypothesistracebackhide__') is True:
                tb = tb.tb_next

    return tb