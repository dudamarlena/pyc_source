# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/helper/xstr.py
# Compiled at: 2020-05-11 16:58:46
# Size of source mod 2**32: 1231 bytes
import json
from json.decoder import JSONDecodeError

class xstr(str):
    __doc__ = '\n    xstr is a subclass of string (str)\n    converts string to any other types\n    '

    def isbool(self):
        return self == 'True' or self == 'true' or self == 'False' or self == 'false'

    def convert_to_bool(self):
        if self == 'True' or self == 'true':
            return True
        return False

    def isint--- This code section failed: ---

 L.  20         0  SETUP_FINALLY        16  'to 16'

 L.  21         2  LOAD_GLOBAL              int
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'item'

 L.  22        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  23        16  DUP_TOP          
               18  LOAD_GLOBAL              ValueError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  24        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14

    def isfloat--- This code section failed: ---

 L.  27         0  SETUP_FINALLY        16  'to 16'

 L.  28         2  LOAD_GLOBAL              float
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'item'

 L.  29        10  POP_BLOCK        
               12  LOAD_CONST               True
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  30        16  DUP_TOP          
               18  LOAD_GLOBAL              ValueError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  31        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
             36_0  COME_FROM            22  '22'
               36  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 14

    def is_dict--- This code section failed: ---

 L.  34         0  SETUP_FINALLY        18  'to 18'

 L.  35         2  LOAD_GLOBAL              json
                4  LOAD_METHOD              loads
                6  LOAD_FAST                'self'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'item'

 L.  36        12  POP_BLOCK        
               14  LOAD_CONST               True
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.  37        18  DUP_TOP          
               20  LOAD_GLOBAL              JSONDecodeError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    38  'to 38'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  38        32  POP_EXCEPT       
               34  LOAD_CONST               False
               36  RETURN_VALUE     
             38_0  COME_FROM            24  '24'
               38  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 16

    def get(self):
        if self.isbool():
            return self.convert_to_bool()
        else:
            if self.isint():
                return int(self)
            if self.isfloat():
                return float(self)
            if self.is_dict():
                return json.loadsself
            if self.startswith"'" and self.endswith"'":
                return self[1:len(self) - 1]
        return self.strip()