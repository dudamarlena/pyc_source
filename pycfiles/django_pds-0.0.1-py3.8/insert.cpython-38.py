# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/controllers/insert.py
# Compiled at: 2020-05-11 10:47:12
# Size of source mod 2**32: 2664 bytes
import json
from django_pds.conf import settings
from django_pds.core.controllers.base import BaseController
OWNER = 'owner'

class GenericInsertCommandController(BaseController):

    def __modify_ids(self, _GenericInsertCommandController__defaults, user_id):
        items = []
        for _id in _GenericInsertCommandController__defaults:
            if _id == OWNER:
                items.append(user_id)
            else:
                items.append(_id)
        else:
            return items

    def json_load--- This code section failed: ---

 L.  21         0  SETUP_FINALLY        18  'to 18'

 L.  22         2  LOAD_CONST               False
                4  LOAD_GLOBAL              json
                6  LOAD_METHOD              loads
                8  LOAD_FAST                'json_string'
               10  CALL_METHOD_1         1  ''
               12  BUILD_TUPLE_2         2 
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.  23        18  DUP_TOP          
               20  LOAD_GLOBAL              BaseException
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    66  'to 66'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        54  'to 54'

 L.  24        34  LOAD_CONST               True
               36  LOAD_GLOBAL              str
               38  LOAD_FAST                'e'
               40  CALL_FUNCTION_1       1  ''
               42  BUILD_TUPLE_2         2 
               44  ROT_FOUR         
               46  POP_BLOCK        
               48  POP_EXCEPT       
               50  CALL_FINALLY         54  'to 54'
               52  RETURN_VALUE     
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM_FINALLY    32  '32'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            24  '24'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'

Parse error at or near `POP_BLOCK' instruction at offset 46

    def already_exists--- This code section failed: ---

 L.  27         0  SETUP_FINALLY        34  'to 34'

 L.  28         2  LOAD_FAST                'self'
                4  LOAD_METHOD              get_document
                6  LOAD_FAST                'document_name'
                8  CALL_METHOD_1         1  ''
               10  LOAD_ATTR                objects
               12  LOAD_FAST                'document_id'
               14  LOAD_CONST               ('ItemId',)
               16  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               18  STORE_FAST               'data'

 L.  29        20  LOAD_FAST                'data'
               22  LOAD_METHOD              count
               24  CALL_METHOD_0         0  ''
               26  LOAD_CONST               0
               28  COMPARE_OP               >
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY     0  '0'

 L.  30        34  DUP_TOP          
               36  LOAD_GLOBAL              BaseException
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    72  'to 72'
               42  POP_TOP          
               44  STORE_FAST               'e'
               46  POP_TOP          
               48  SETUP_FINALLY        60  'to 60'

 L.  31        50  POP_BLOCK        
               52  POP_EXCEPT       
               54  CALL_FINALLY         60  'to 60'
               56  LOAD_CONST               False
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'
             60_1  COME_FROM_FINALLY    48  '48'
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  END_FINALLY      
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
             72_0  COME_FROM            40  '40'
               72  END_FINALLY      
             74_0  COME_FROM            70  '70'

Parse error at or near `POP_EXCEPT' instruction at offset 52

    def insert_one--- This code section failed: ---

 L.  34         0  SETUP_FINALLY       208  'to 208'

 L.  36         2  LOAD_FAST                'self'
                4  LOAD_METHOD              is_base_instance
                6  LOAD_FAST                'document_name'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'base_instance'

 L.  37        12  LOAD_FAST                'self'
               14  LOAD_METHOD              is_simple_base_doc_instance
               16  LOAD_FAST                'document_name'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'simple_base_instance'

 L.  39        22  LOAD_FAST                'base_instance'
               24  POP_JUMP_IF_FALSE    30  'to 30'
               26  LOAD_FAST                'simple_base_instance'
               28  POP_JUMP_IF_TRUE     36  'to 36'
             30_0  COME_FROM            24  '24'

 L.  40        30  POP_BLOCK        
               32  LOAD_CONST               (True, 'Document type must be `BaseDocument` or `SimpleBaseDocument` from django_pds.core.base Module')
               34  RETURN_VALUE     
             36_0  COME_FROM            28  '28'

 L.  44        36  LOAD_FAST                'self'
               38  LOAD_METHOD              get_document
               40  LOAD_FAST                'document_name'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'Model'

 L.  45        46  LOAD_FAST                'Model'
               48  BUILD_TUPLE_0         0 
               50  LOAD_FAST                'data'
               52  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               54  STORE_FAST               'mod'

 L.  47        56  LOAD_FAST                'base_instance'
               58  POP_JUMP_IF_FALSE   188  'to 188'

 L.  49        60  LOAD_FAST                'user_id'
               62  POP_JUMP_IF_FALSE   124  'to 124'

 L.  50        64  LOAD_FAST                'user_id'
               66  LOAD_FAST                'mod'
               68  STORE_ATTR               CreatedBy

 L.  51        70  LOAD_FAST                'user_id'
               72  LOAD_FAST                'mod'
               74  STORE_ATTR               LastUpdateBy

 L.  52        76  LOAD_GLOBAL              settings
               78  LOAD_ATTR                SECURITY_IDS_ATTRIBUTES
               80  GET_ITER         
               82  FOR_ITER            124  'to 124'
               84  STORE_FAST               'item'

 L.  53        86  LOAD_FAST                'default_permission'
               88  LOAD_METHOD              get
               90  LOAD_FAST                'item'
               92  BUILD_LIST_0          0 
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'ids'

 L.  54        98  LOAD_FAST                'self'
              100  LOAD_METHOD              _GenericInsertCommandController__modify_ids
              102  LOAD_FAST                'ids'
              104  LOAD_FAST                'user_id'
              106  CALL_METHOD_2         2  ''
              108  STORE_FAST               'ids'

 L.  55       110  LOAD_GLOBAL              setattr
              112  LOAD_FAST                'mod'
              114  LOAD_FAST                'item'
              116  LOAD_FAST                'ids'
              118  CALL_FUNCTION_3       3  ''
              120  POP_TOP          
              122  JUMP_BACK            82  'to 82'
            124_0  COME_FROM            62  '62'

 L.  57       124  LOAD_FAST                'default_permission'
              126  POP_JUMP_IF_FALSE   188  'to 188'

 L.  58       128  LOAD_GLOBAL              settings
              130  LOAD_ATTR                SECURITY_ROLES_ATTRIBUTES
              132  GET_ITER         
              134  FOR_ITER            164  'to 164'
              136  STORE_FAST               'item'

 L.  59       138  LOAD_FAST                'default_permission'
              140  LOAD_METHOD              get
              142  LOAD_FAST                'item'
              144  BUILD_LIST_0          0 
              146  CALL_METHOD_2         2  ''
              148  STORE_FAST               'roles'

 L.  60       150  LOAD_GLOBAL              setattr
              152  LOAD_FAST                'mod'
              154  LOAD_FAST                'item'
              156  LOAD_FAST                'roles'
              158  CALL_FUNCTION_3       3  ''
              160  POP_TOP          
              162  JUMP_BACK           134  'to 134'

 L.  61       164  LOAD_GLOBAL              setattr
              166  LOAD_FAST                'mod'
              168  LOAD_STR                 'RolesAllowedToWrite'
              170  BUILD_LIST_0          0 
              172  CALL_FUNCTION_3       3  ''
              174  POP_TOP          

 L.  62       176  LOAD_GLOBAL              setattr
              178  LOAD_FAST                'mod'
              180  LOAD_STR                 'IdsAllowedToWrite'
              182  BUILD_LIST_0          0 
              184  CALL_FUNCTION_3       3  ''
              186  POP_TOP          
            188_0  COME_FROM           126  '126'
            188_1  COME_FROM            58  '58'

 L.  64       188  LOAD_FAST                'mod'
              190  LOAD_METHOD              save
              192  CALL_METHOD_0         0  ''
              194  POP_TOP          

 L.  65       196  LOAD_CONST               False
              198  LOAD_FAST                'mod'
              200  LOAD_ATTR                ItemId
              202  BUILD_TUPLE_2         2 
              204  POP_BLOCK        
              206  RETURN_VALUE     
            208_0  COME_FROM_FINALLY     0  '0'

 L.  67       208  DUP_TOP          
              210  LOAD_GLOBAL              BaseException
              212  COMPARE_OP               exception-match
          214_216  POP_JUMP_IF_FALSE   254  'to 254'
              218  POP_TOP          
              220  STORE_FAST               'e'
              222  POP_TOP          
              224  SETUP_FINALLY       242  'to 242'

 L.  68       226  LOAD_CONST               True
              228  LOAD_FAST                'e'
              230  BUILD_TUPLE_2         2 
              232  ROT_FOUR         
              234  POP_BLOCK        
              236  POP_EXCEPT       
              238  CALL_FINALLY        242  'to 242'
              240  RETURN_VALUE     
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM_FINALLY   224  '224'
              242  LOAD_CONST               None
              244  STORE_FAST               'e'
              246  DELETE_FAST              'e'
              248  END_FINALLY      
              250  POP_EXCEPT       
              252  JUMP_FORWARD        256  'to 256'
            254_0  COME_FROM           214  '214'
              254  END_FINALLY      
            256_0  COME_FROM           252  '252'

Parse error at or near `LOAD_CONST' instruction at offset 32

    def insert_many(self, document_name, data_array, user_id=None, default_permission=None):
        results = []
        for data in data_array:
            err, item_id = self.insert_one(document_name, data, user_id, default_permission)
            if err:
                results.append(None)
            else:
                results.append(item_id)
        else:
            return results