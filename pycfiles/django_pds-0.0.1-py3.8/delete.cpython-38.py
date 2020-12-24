# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/pds/generic/delete.py
# Compiled at: 2020-05-11 09:14:32
# Size of source mod 2**32: 988 bytes
from django_pds.core.controllers import DefaultPermissionSettingsController, GenericDeleteCommandController

def data_delete--- This code section failed: ---

 L.   5         0  SETUP_FINALLY       110  'to 110'

 L.   7         2  LOAD_GLOBAL              GenericDeleteCommandController
                4  CALL_FUNCTION_0       0  ''
                6  STORE_FAST               'delete_ctrl'

 L.   9         8  LOAD_FAST                'ignore_permissions'
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L.  10        12  LOAD_FAST                'delete_ctrl'
               14  LOAD_METHOD              delete
               16  LOAD_FAST                'document_name'
               18  LOAD_FAST                'document_id'
               20  CALL_METHOD_2         2  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM            10  '10'

 L.  12        26  LOAD_GLOBAL              DefaultPermissionSettingsController
               28  CALL_FUNCTION_0       0  ''
               30  STORE_FAST               'entity_permission'

 L.  13        32  LOAD_CONST               False
               34  STORE_FAST               'role_can_delete'

 L.  14        36  LOAD_FAST                'user_id'
               38  POP_JUMP_IF_FALSE    52  'to 52'

 L.  15        40  LOAD_FAST                'entity_permission'
               42  LOAD_METHOD              can_delete
               44  LOAD_FAST                'document_name'
               46  LOAD_FAST                'user_id'
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'role_can_delete'
             52_0  COME_FROM            38  '38'

 L.  16        52  LOAD_CONST               False
               54  STORE_FAST               'id_can_delete'

 L.  17        56  LOAD_FAST                'role_can_delete'
               58  POP_JUMP_IF_TRUE     78  'to 78'
               60  LOAD_FAST                'user_id'
               62  POP_JUMP_IF_TRUE     78  'to 78'

 L.  18        64  LOAD_FAST                'delete_ctrl'
               66  LOAD_METHOD              has_permission
               68  LOAD_FAST                'document_name'
               70  LOAD_FAST                'user_id'
               72  LOAD_FAST                'document_id'
               74  CALL_METHOD_3         3  ''
               76  STORE_FAST               'id_can_delete'
             78_0  COME_FROM            62  '62'
             78_1  COME_FROM            58  '58'

 L.  19        78  LOAD_FAST                'role_can_delete'
               80  POP_JUMP_IF_TRUE     86  'to 86'
               82  LOAD_FAST                'id_can_delete'
               84  POP_JUMP_IF_FALSE   100  'to 100'
             86_0  COME_FROM            80  '80'

 L.  20        86  LOAD_FAST                'delete_ctrl'
               88  LOAD_METHOD              delete
               90  LOAD_FAST                'document_name'
               92  LOAD_FAST                'document_id'
               94  CALL_METHOD_2         2  ''
               96  POP_BLOCK        
               98  RETURN_VALUE     
            100_0  COME_FROM            84  '84'

 L.  22       100  POP_BLOCK        
              102  LOAD_CONST               (True, "you don't have sufficient permission to delete")
              104  RETURN_VALUE     
              106  POP_BLOCK        
              108  JUMP_FORWARD        160  'to 160'
            110_0  COME_FROM_FINALLY     0  '0'

 L.  23       110  DUP_TOP          
              112  LOAD_GLOBAL              BaseException
              114  COMPARE_OP               exception-match
              116  POP_JUMP_IF_FALSE   158  'to 158'
              118  POP_TOP          
              120  STORE_FAST               'e'
              122  POP_TOP          
              124  SETUP_FINALLY       146  'to 146'

 L.  24       126  LOAD_CONST               True
              128  LOAD_GLOBAL              str
              130  LOAD_FAST                'e'
              132  CALL_FUNCTION_1       1  ''
              134  BUILD_TUPLE_2         2 
              136  ROT_FOUR         
              138  POP_BLOCK        
              140  POP_EXCEPT       
              142  CALL_FINALLY        146  'to 146'
              144  RETURN_VALUE     
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM_FINALLY   124  '124'
              146  LOAD_CONST               None
              148  STORE_FAST               'e'
              150  DELETE_FAST              'e'
              152  END_FINALLY      
              154  POP_EXCEPT       
              156  JUMP_FORWARD        160  'to 160'
            158_0  COME_FROM           116  '116'
              158  END_FINALLY      
            160_0  COME_FROM           156  '156'
            160_1  COME_FROM           108  '108'

Parse error at or near `RETURN_VALUE' instruction at offset 104