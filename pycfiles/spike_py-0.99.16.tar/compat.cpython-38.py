# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/compat.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 1442 bytes
"""Compatibility methods and classes for the progressbar module."""
try:
    next
except NameError:

    def next--- This code section failed: ---

 L.  29         0  SETUP_FINALLY        12  'to 12'

 L.  31         2  LOAD_FAST                'iter'
                4  LOAD_METHOD              __next__
                6  CALL_METHOD_0         0  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  32        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    38  'to 38'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  34        26  LOAD_FAST                'iter'
               28  LOAD_METHOD              next
               30  CALL_METHOD_0         0  ''
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
             38_0  COME_FROM            18  '18'
               38  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22


try:
    any
except NameError:

    def any(iterator):
        for item in iterator:
            if item:
                return True
            return False