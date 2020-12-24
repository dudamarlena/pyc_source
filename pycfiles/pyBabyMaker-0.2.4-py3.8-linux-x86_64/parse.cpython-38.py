# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyBabyMaker/parse.py
# Compiled at: 2020-05-01 05:18:06
# Size of source mod 2**32: 1056 bytes
"""
This module provides limited functionality to extract variables from certain
type of C++ expressions.

Currently, supported C++ expressions includes arithmetic and boolean calculation
and nested function calls.
"""
import re

def is_numeral--- This code section failed: ---

 L.  21         0  SETUP_FINALLY        16  'to 16'

 L.  22         2  LOAD_GLOBAL              float
                4  LOAD_FAST                'n'
                6  CALL_FUNCTION_1       1  ''
                8  POP_TOP          

 L.  23        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  24        16  DUP_TOP          
               18  LOAD_GLOBAL              ValueError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  25        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14


def find_all_args(s, tokens=[
 '[\\w\\d_]*\\(', '\\)', ',',
 '\\+', '-', '\\*', '/', '%',
 '&&', '\\|\\|',
 '!', '>', '<', '=']):
    """
    Find all arguments inside a C++ expression ``s``.
    """
    for t in tokens:
        s = re.sub(t, ' ', s)
    else:
        return s.split()


def find_all_vars(s, **kwargs):
    """
    Find all arguments, minus numerals, inside a C++ expression ``s``.
    """
    args = find_all_args(s, **kwargs)
    return [v for v in args if not is_numeral(v)]