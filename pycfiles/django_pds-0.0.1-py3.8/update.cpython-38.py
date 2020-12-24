# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/pds/generic/update.py
# Compiled at: 2020-05-11 10:56:23
# Size of source mod 2**32: 1531 bytes
from django_pds.conf import settings
from django_pds.core.controllers import GenericUpdateCommandController
SECURITY_ATTRIBUTES = settings.SECURITY_ATTRIBUTES
READ_ONLY_FIELDS = settings.READ_ONLY_FIELDS

def data_update--- This code section failed: ---

 L.   9         0  SETUP_FINALLY       242  'to 242'

 L.  11         2  LOAD_GLOBAL              GenericUpdateCommandController
                4  CALL_FUNCTION_0       0  ''
                6  STORE_FAST               'update_ctrl'

 L.  12         8  LOAD_FAST                'update_ctrl'
               10  LOAD_METHOD              json_load
               12  LOAD_FAST                'data_json'
               14  CALL_METHOD_1         1  ''
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'err'
               20  STORE_FAST               'data'

 L.  14        22  LOAD_FAST                'err'
               24  POP_JUMP_IF_FALSE    40  'to 40'

 L.  15        26  LOAD_CONST               True
               28  LOAD_GLOBAL              str
               30  LOAD_FAST                'err'
               32  CALL_FUNCTION_1       1  ''
               34  BUILD_TUPLE_2         2 
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM            24  '24'

 L.  17        40  LOAD_FAST                'ignore_security'
               42  POP_JUMP_IF_FALSE    58  'to 58'

 L.  18        44  LOAD_FAST                'update_ctrl'
               46  LOAD_METHOD              update_one
               48  LOAD_FAST                'document_name'
               50  LOAD_FAST                'data'
               52  CALL_METHOD_2         2  ''
               54  POP_BLOCK        
               56  RETURN_VALUE     
             58_0  COME_FROM            42  '42'

 L.  20        58  LOAD_GLOBAL              set
               60  LOAD_FAST                'data'
               62  LOAD_METHOD              keys
               64  CALL_METHOD_0         0  ''
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'data_fields'

 L.  21        70  LOAD_GLOBAL              set
               72  LOAD_GLOBAL              SECURITY_ATTRIBUTES
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'security_attributes'

 L.  22        78  LOAD_FAST                'update_ctrl'
               80  LOAD_METHOD              common_fields
               82  LOAD_FAST                'data_fields'
               84  LOAD_FAST                'security_attributes'
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'common_fields'

 L.  24        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'common_fields'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_CONST               0
               98  COMPARE_OP               >
              100  POP_JUMP_IF_FALSE   130  'to 130'

 L.  25       102  LOAD_STR                 ','
              104  LOAD_METHOD              join
              106  LOAD_FAST                'common_fields'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'fields'

 L.  26       112  LOAD_CONST               True
              114  LOAD_STR                 'the following security attributes '
              116  LOAD_FAST                'fields'
              118  FORMAT_VALUE          0  ''
              120  LOAD_STR                 ' found in the json data'
              122  BUILD_STRING_3        3 
              124  BUILD_TUPLE_2         2 
              126  POP_BLOCK        
              128  RETURN_VALUE     
            130_0  COME_FROM           100  '100'

 L.  28       130  LOAD_GLOBAL              set
              132  LOAD_GLOBAL              READ_ONLY_FIELDS
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'read_only_fields'

 L.  29       138  LOAD_FAST                'update_ctrl'
              140  LOAD_METHOD              common_fields
              142  LOAD_FAST                'data_fields'
              144  LOAD_FAST                'read_only_fields'
              146  CALL_METHOD_2         2  ''
              148  STORE_FAST               'rof'

 L.  30       150  LOAD_GLOBAL              len
              152  LOAD_FAST                'rof'
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_CONST               0
              158  COMPARE_OP               >
              160  POP_JUMP_IF_FALSE   190  'to 190'

 L.  31       162  LOAD_STR                 ','
              164  LOAD_METHOD              join
              166  LOAD_FAST                'rof'
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'fields'

 L.  32       172  LOAD_CONST               True
              174  LOAD_STR                 'the following read only attributes '
              176  LOAD_FAST                'fields'
              178  FORMAT_VALUE          0  ''
              180  LOAD_STR                 ' found in the json data'
              182  BUILD_STRING_3        3 
              184  BUILD_TUPLE_2         2 
              186  POP_BLOCK        
              188  RETURN_VALUE     
            190_0  COME_FROM           160  '160'

 L.  34       190  LOAD_FAST                'update_ctrl'
              192  LOAD_METHOD              can_update
              194  LOAD_FAST                'document_name'
              196  LOAD_FAST                'data'
              198  LOAD_METHOD              get
              200  LOAD_STR                 'ItemId'
              202  LOAD_CONST               None
              204  CALL_METHOD_2         2  ''
              206  LOAD_FAST                'user_id'
              208  CALL_METHOD_3         3  ''
              210  STORE_FAST               'can_update'

 L.  36       212  LOAD_FAST                'can_update'
              214  POP_JUMP_IF_FALSE   232  'to 232'

 L.  37       216  LOAD_FAST                'update_ctrl'
              218  LOAD_METHOD              update_one
              220  LOAD_FAST                'document_name'
              222  LOAD_FAST                'data'
              224  LOAD_FAST                'user_id'
              226  CALL_METHOD_3         3  ''
              228  POP_BLOCK        
              230  RETURN_VALUE     
            232_0  COME_FROM           214  '214'

 L.  39       232  POP_BLOCK        
              234  LOAD_CONST               (True, "access denied, you don't have sufficient permission to update")
              236  RETURN_VALUE     
              238  POP_BLOCK        
              240  JUMP_FORWARD        294  'to 294'
            242_0  COME_FROM_FINALLY     0  '0'

 L.  40       242  DUP_TOP          
              244  LOAD_GLOBAL              BaseException
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   292  'to 292'
              252  POP_TOP          
              254  STORE_FAST               'e'
              256  POP_TOP          
              258  SETUP_FINALLY       280  'to 280'

 L.  41       260  LOAD_CONST               True
              262  LOAD_GLOBAL              str
              264  LOAD_FAST                'e'
              266  CALL_FUNCTION_1       1  ''
              268  BUILD_TUPLE_2         2 
              270  ROT_FOUR         
              272  POP_BLOCK        
              274  POP_EXCEPT       
              276  CALL_FINALLY        280  'to 280'
              278  RETURN_VALUE     
            280_0  COME_FROM           276  '276'
            280_1  COME_FROM_FINALLY   258  '258'
              280  LOAD_CONST               None
              282  STORE_FAST               'e'
              284  DELETE_FAST              'e'
              286  END_FINALLY      
              288  POP_EXCEPT       
              290  JUMP_FORWARD        294  'to 294'
            292_0  COME_FROM           248  '248'
              292  END_FINALLY      
            294_0  COME_FROM           290  '290'
            294_1  COME_FROM           240  '240'

Parse error at or near `RETURN_VALUE' instruction at offset 236