# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breezekay/GDrive/Codes/ez/bree/bree/pagelets/script.py
# Compiled at: 2015-01-24 09:45:18
from __future__ import unicode_literals
from tornado.web import UIModule

class Script(UIModule):

    def render--- This code section failed: ---

 L.   8         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'handler'
                6  LOAD_ATTR             1  'js_debug'
                9  STORE_FAST            5  'debug'

 L.  10        12  BUILD_LIST_0          0 
               15  STORE_FAST            6  'to_show'

 L.  12        18  LOAD_CONST               ''
               21  STORE_FAST            7  'buff'

 L.  13        24  LOAD_FAST             5  'debug'
               27  POP_JUMP_IF_TRUE     45  'to 45'
               30  LOAD_FAST             2  'compress'
               33  LOAD_CONST               None
               36  COMPARE_OP            8  is
               39  POP_JUMP_IF_TRUE     45  'to 45'
               42  JUMP_FORWARD         36  'to 81'

 L.  14        45  LOAD_GLOBAL           2  'isinstance'
               48  LOAD_FAST             1  'origin'
               51  LOAD_GLOBAL           3  'str'
               54  CALL_FUNCTION_2       2  None
               57  POP_JUMP_IF_FALSE    72  'to 72'

 L.  15        60  LOAD_FAST             1  'origin'
               63  BUILD_LIST_1          1 
               66  STORE_FAST            6  'to_show'
               69  JUMP_FORWARD          6  'to 78'

 L.  17        72  LOAD_FAST             1  'origin'
               75  STORE_FAST            6  'to_show'
             78_0  COME_FROM            69  '69'
               78  JUMP_FORWARD         33  'to 114'
             81_0  COME_FROM            42  '42'

 L.  19        81  LOAD_GLOBAL           2  'isinstance'
               84  LOAD_FAST             2  'compress'
               87  LOAD_GLOBAL           3  'str'
               90  CALL_FUNCTION_2       2  None
               93  POP_JUMP_IF_FALSE   108  'to 108'

 L.  20        96  LOAD_FAST             2  'compress'
               99  BUILD_LIST_1          1 
              102  STORE_FAST            6  'to_show'
              105  JUMP_FORWARD          6  'to 114'

 L.  22       108  LOAD_FAST             2  'compress'
              111  STORE_FAST            6  'to_show'
            114_0  COME_FROM           105  '105'
            114_1  COME_FROM            78  '78'

 L.  24       114  SETUP_LOOP           45  'to 162'
              117  LOAD_FAST             6  'to_show'
              120  GET_ITER         
              121  FOR_ITER             37  'to 161'
              124  STORE_FAST            8  'v'

 L.  25       127  LOAD_FAST             7  'buff'
              130  LOAD_CONST               '<script src="{}"></script>'
              133  LOOKUP_METHOD         4  'format'
              136  LOAD_FAST             0  'self'
              139  LOAD_ATTR             0  'handler'
              142  LOOKUP_METHOD         5  'static_url'
              145  LOAD_FAST             8  'v'
              148  CALL_METHOD_1         1  None
              151  CALL_METHOD_1         1  None
              154  INPLACE_ADD      
              155  STORE_FAST            7  'buff'
              158  JUMP_BACK           121  'to 121'
              161  POP_BLOCK        
            162_0  COME_FROM           114  '114'

 L.  28       162  LOAD_FAST             7  'buff'
              165  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 78