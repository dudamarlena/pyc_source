# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/wimsapi/utils.py
# Compiled at: 2020-05-04 16:09:45
# Size of source mod 2**32: 413 bytes
import datetime

def one_year_later():
    """Give the date one year later from now in the format yyyymmdd."""
    d = datetime.date.today()
    return d.replace(year=(d.year + 1)).strftime('%Y%m%d')


def default--- This code section failed: ---

 L.  14         0  SETUP_FINALLY        16  'to 16'

 L.  15         2  LOAD_FAST                'd'
                4  LOAD_FAST                'k'
                6  BINARY_SUBSCR    
                8  LOAD_FAST                'i'
               10  BINARY_SUBSCR    
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  16        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  LOAD_GLOBAL              IndexError
               22  BUILD_TUPLE_2         2 
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    42  'to 42'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  17        34  LOAD_FAST                'default'
               36  ROT_FOUR         
               38  POP_EXCEPT       
               40  RETURN_VALUE     
             42_0  COME_FROM            26  '26'
               42  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 30