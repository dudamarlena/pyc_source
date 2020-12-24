# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/pds/generic/read.py
# Compiled at: 2020-05-11 17:05:44
# Size of source mod 2**32: 6486 bytes
from mongoengine import Q
from django_pds.conf import settings
from django_pds.core.controllers import UserReadableDataController, GenericReadController, UserRoleMapsController
from django_pds.core.rest.response import error_response, success_response_with_total_records
from django_pds.core.utils import get_fields, get_document, is_abstract_document
from django_pds.core.utils import print_traceback
from django_pds.serializers import GenericSerializerAlpha
from parser.query import QueryParser
from parser.terms import FILTER, WHERE, SELECT, PAGE_SIZE, PAGE_NUM, ORDER_BY, RAW_WHERE
NOT_SELECTABLE_ENTITIES_BY_PDS = settings.SELECT_NOT_ALLOWED_ENTITIES
SECURITY_ATTRIBUTES = settings.SECURITY_ATTRIBUTES

def basic_data_read--- This code section failed: ---

 L.  20         0  SETUP_FINALLY       244  'to 244'

 L.  22         2  LOAD_GLOBAL              get_document
                4  LOAD_FAST                'document_name'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'document'

 L.  24        10  LOAD_FAST                'document'
               12  POP_JUMP_IF_FALSE    18  'to 18'
               14  LOAD_FAST                'document_name'
               16  POP_JUMP_IF_TRUE     40  'to 40'
             18_0  COME_FROM            12  '12'

 L.  25        18  LOAD_CONST               True
               20  LOAD_GLOBAL              error_response
               22  LOAD_STR                 'document by name `'
               24  LOAD_FAST                'document_name'
               26  FORMAT_VALUE          0  ''
               28  LOAD_STR                 "` does't exists"
               30  BUILD_STRING_3        3 
               32  CALL_FUNCTION_1       1  ''
               34  BUILD_TUPLE_2         2 
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM            16  '16'

 L.  27        40  LOAD_FAST                'fields'
               42  LOAD_STR                 '__all__'
               44  COMPARE_OP               !=
               46  POP_JUMP_IF_FALSE    76  'to 76'
               48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'fields'
               52  LOAD_GLOBAL              list
               54  LOAD_GLOBAL              tuple
               56  BUILD_TUPLE_2         2 
               58  CALL_FUNCTION_2       2  ''
               60  POP_JUMP_IF_TRUE     76  'to 76'

 L.  28        62  LOAD_CONST               True
               64  LOAD_GLOBAL              error_response
               66  LOAD_STR                 'fields must be a list or tuple'
               68  CALL_FUNCTION_1       1  ''
               70  BUILD_TUPLE_2         2 
               72  POP_BLOCK        
               74  RETURN_VALUE     
             76_0  COME_FROM            60  '60'
             76_1  COME_FROM            46  '46'

 L.  30        76  LOAD_GLOBAL              GenericReadController
               78  CALL_FUNCTION_0       0  ''
               80  STORE_FAST               'sql_ctrl'

 L.  31        82  LOAD_FAST                'sql_ctrl'
               84  LOAD_METHOD              read
               86  LOAD_FAST                'document_name'
               88  LOAD_GLOBAL              Q
               90  CALL_FUNCTION_0       0  ''
               92  LOAD_FAST                'page_size'
               94  LOAD_FAST                'page_num'
               96  LOAD_FAST                'order_by'
               98  CALL_METHOD_5         5  ''
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'data'
              104  STORE_FAST               'cnt'

 L.  32       106  LOAD_FAST                'cnt'
              108  LOAD_CONST               0
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   130  'to 130'

 L.  33       114  LOAD_CONST               False
              116  LOAD_GLOBAL              success_response_with_total_records
              118  BUILD_LIST_0          0 
              120  LOAD_FAST                'cnt'
              122  CALL_FUNCTION_2       2  ''
              124  BUILD_TUPLE_2         2 
              126  POP_BLOCK        
              128  RETURN_VALUE     
            130_0  COME_FROM           112  '112'

 L.  34       130  LOAD_GLOBAL              GenericSerializerAlpha
              132  LOAD_FAST                'document_name'
              134  LOAD_CONST               ('document_name',)
              136  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              138  STORE_FAST               'gsa'

 L.  35       140  LOAD_FAST                'fields'
              142  LOAD_STR                 '__all__'
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_TRUE    170  'to 170'

 L.  36       148  LOAD_FAST                'fields'
              150  GET_ITER         
              152  FOR_ITER            168  'to 168'
              154  STORE_FAST               'field'

 L.  37       156  LOAD_FAST                'gsa'
              158  LOAD_METHOD              select
              160  LOAD_FAST                'field'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          
              166  JUMP_BACK           152  'to 152'
              168  JUMP_FORWARD        212  'to 212'
            170_0  COME_FROM           146  '146'

 L.  39       170  LOAD_GLOBAL              get_fields
              172  LOAD_FAST                'document_name'
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'fields'

 L.  40       178  LOAD_FAST                'include_security_fields'
              180  POP_JUMP_IF_TRUE    202  'to 202'

 L.  41       182  LOAD_GLOBAL              tuple
              184  LOAD_GLOBAL              set
              186  LOAD_FAST                'fields'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_GLOBAL              set
              192  LOAD_GLOBAL              SECURITY_ATTRIBUTES
              194  CALL_FUNCTION_1       1  ''
              196  BINARY_SUBTRACT  
              198  CALL_FUNCTION_1       1  ''
              200  STORE_FAST               'fields'
            202_0  COME_FROM           180  '180'

 L.  42       202  LOAD_FAST                'gsa'
              204  LOAD_METHOD              fields
              206  LOAD_FAST                'fields'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
            212_0  COME_FROM           168  '168'

 L.  44       212  LOAD_FAST                'gsa'
              214  LOAD_METHOD              serialize
              216  LOAD_FAST                'data'
              218  CALL_METHOD_1         1  ''
              220  STORE_FAST               'json'

 L.  45       222  LOAD_GLOBAL              success_response_with_total_records
              224  LOAD_FAST                'json'
              226  LOAD_ATTR                data
              228  LOAD_FAST                'cnt'
              230  CALL_FUNCTION_2       2  ''
              232  STORE_FAST               'res'

 L.  46       234  LOAD_CONST               False
              236  LOAD_FAST                'res'
              238  BUILD_TUPLE_2         2 
              240  POP_BLOCK        
              242  RETURN_VALUE     
            244_0  COME_FROM_FINALLY     0  '0'

 L.  47       244  DUP_TOP          
              246  LOAD_GLOBAL              BaseException
              248  COMPARE_OP               exception-match
          250_252  POP_JUMP_IF_FALSE   310  'to 310'
              254  POP_TOP          
              256  STORE_FAST               'e'
              258  POP_TOP          
              260  SETUP_FINALLY       298  'to 298'

 L.  48       262  LOAD_FAST                'error_track'
          264_266  POP_JUMP_IF_FALSE   274  'to 274'

 L.  49       268  LOAD_GLOBAL              print_traceback
              270  CALL_FUNCTION_0       0  ''
              272  POP_TOP          
            274_0  COME_FROM           264  '264'

 L.  50       274  LOAD_CONST               True
              276  LOAD_GLOBAL              error_response
              278  LOAD_GLOBAL              str
              280  LOAD_FAST                'e'
              282  CALL_FUNCTION_1       1  ''
              284  CALL_FUNCTION_1       1  ''
              286  BUILD_TUPLE_2         2 
              288  ROT_FOUR         
              290  POP_BLOCK        
              292  POP_EXCEPT       
              294  CALL_FINALLY        298  'to 298'
              296  RETURN_VALUE     
            298_0  COME_FROM           294  '294'
            298_1  COME_FROM_FINALLY   260  '260'
              298  LOAD_CONST               None
              300  STORE_FAST               'e'
              302  DELETE_FAST              'e'
              304  END_FINALLY      
              306  POP_EXCEPT       
              308  JUMP_FORWARD        312  'to 312'
            310_0  COME_FROM           250  '250'
              310  END_FINALLY      
            312_0  COME_FROM           308  '308'

Parse error at or near `POP_BLOCK' instruction at offset 290


def data_read--- This code section failed: ---

 L.  74         0  LOAD_GLOBAL              get_document
                2  LOAD_FAST                'document_name'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'document'

 L.  79         8  LOAD_FAST                'document'
               10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  80        12  LOAD_CONST               False
               14  LOAD_GLOBAL              error_response
               16  LOAD_STR                 'document model not found'
               18  CALL_FUNCTION_1       1  ''
               20  BUILD_TUPLE_2         2 
               22  RETURN_VALUE     
             24_0  COME_FROM            10  '10'

 L.  82        24  LOAD_GLOBAL              is_abstract_document
               26  LOAD_FAST                'document_name'
               28  CALL_FUNCTION_1       1  ''
               30  POP_JUMP_IF_FALSE    44  'to 44'

 L.  83        32  LOAD_CONST               False
               34  LOAD_GLOBAL              error_response
               36  LOAD_STR                 'document model not found'
               38  CALL_FUNCTION_1       1  ''
               40  BUILD_TUPLE_2         2 
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'

 L.  85        44  LOAD_FAST                'selectable'
               46  POP_JUMP_IF_FALSE    68  'to 68'
               48  LOAD_FAST                'document_name'
               50  LOAD_GLOBAL              NOT_SELECTABLE_ENTITIES_BY_PDS
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE    68  'to 68'

 L.  86        56  LOAD_CONST               False
               58  LOAD_GLOBAL              error_response
               60  LOAD_STR                 'document model is not selectable'
               62  CALL_FUNCTION_1       1  ''
               64  BUILD_TUPLE_2         2 
               66  RETURN_VALUE     
             68_0  COME_FROM            54  '54'
             68_1  COME_FROM            46  '46'

 L.  88     68_70  SETUP_FINALLY       728  'to 728'

 L.  89        72  LOAD_GLOBAL              QueryParser
               74  LOAD_FAST                'sql_text'
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'parser'

 L.  90        80  LOAD_FAST                'parser'
               82  LOAD_METHOD              parse
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'dictionary'

 L.  93        88  BUILD_LIST_0          0 
               90  STORE_FAST               '_filters'

 L.  94        92  LOAD_FAST                'dictionary'
               94  LOAD_METHOD              get
               96  LOAD_GLOBAL              FILTER
               98  LOAD_CONST               None
              100  CALL_METHOD_2         2  ''
              102  POP_JUMP_IF_FALSE   112  'to 112'

 L.  95       104  LOAD_FAST                'dictionary'
              106  LOAD_GLOBAL              FILTER
              108  BINARY_SUBSCR    
              110  STORE_FAST               '_filters'
            112_0  COME_FROM           102  '102'

 L.  97       112  LOAD_GLOBAL              set
              114  LOAD_FAST                '_filters'
              116  CALL_FUNCTION_1       1  ''
              118  STORE_FAST               'filter_fields'

 L.  98       120  LOAD_GLOBAL              set
              122  LOAD_GLOBAL              get_fields
              124  LOAD_FAST                'document_name'
              126  CALL_FUNCTION_1       1  ''
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'document_fields'

 L. 100       132  LOAD_GLOBAL              len
              134  LOAD_FAST                'filter_fields'
              136  LOAD_FAST                'document_fields'
              138  BINARY_SUBTRACT  
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_CONST               0
              144  COMPARE_OP               >
              146  POP_JUMP_IF_FALSE   162  'to 162'

 L. 101       148  LOAD_CONST               True
              150  LOAD_GLOBAL              error_response
              152  LOAD_STR                 'Where clause contains unknown attribute to this Document'
              154  CALL_FUNCTION_1       1  ''
              156  BUILD_TUPLE_2         2 
              158  POP_BLOCK        
              160  RETURN_VALUE     
            162_0  COME_FROM           146  '146'

 L. 103       162  LOAD_FAST                'security_attributes'
              164  POP_JUMP_IF_FALSE   210  'to 210'

 L. 104       166  LOAD_GLOBAL              set
              168  LOAD_GLOBAL              SECURITY_ATTRIBUTES
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               'security_attr'

 L. 105       174  LOAD_FAST                'filter_fields'
              176  LOAD_METHOD              intersection
              178  LOAD_FAST                'security_attr'
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'contains_security_attributes'

 L. 106       184  LOAD_GLOBAL              len
              186  LOAD_FAST                'contains_security_attributes'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_CONST               0
              192  COMPARE_OP               >
              194  POP_JUMP_IF_FALSE   210  'to 210'

 L. 107       196  LOAD_CONST               True
              198  LOAD_GLOBAL              error_response
              200  LOAD_STR                 'Security attributes found in where clause'
              202  CALL_FUNCTION_1       1  ''
              204  BUILD_TUPLE_2         2 
              206  POP_BLOCK        
              208  RETURN_VALUE     
            210_0  COME_FROM           194  '194'
            210_1  COME_FROM           164  '164'

 L. 111       210  LOAD_STR                 'ItemId'
              212  BUILD_LIST_1          1 
              214  STORE_FAST               'fields'

 L. 112       216  LOAD_FAST                'dictionary'
              218  LOAD_METHOD              get
              220  LOAD_GLOBAL              SELECT
              222  LOAD_CONST               None
              224  CALL_METHOD_2         2  ''
              226  POP_JUMP_IF_FALSE   236  'to 236'

 L. 113       228  LOAD_FAST                'dictionary'
              230  LOAD_GLOBAL              SELECT
              232  BINARY_SUBSCR    
              234  STORE_FAST               'fields'
            236_0  COME_FROM           226  '226'

 L. 114       236  LOAD_FAST                'read_all'
              238  POP_JUMP_IF_FALSE   244  'to 244'

 L. 115       240  LOAD_FAST                'document_fields'
              242  STORE_FAST               'fields'
            244_0  COME_FROM           238  '238'

 L. 117       244  LOAD_GLOBAL              UserRoleMapsController
              246  CALL_FUNCTION_0       0  ''
              248  STORE_FAST               'urm_ctrl'

 L. 119       250  LOAD_FAST                'readable'
          252_254  POP_JUMP_IF_FALSE   378  'to 378'

 L. 120       256  LOAD_GLOBAL              UserReadableDataController
              258  CALL_FUNCTION_0       0  ''
              260  STORE_FAST               'urds_ctrl'

 L. 121       262  LOAD_CONST               None
              264  STORE_FAST               '__roles'

 L. 122       266  LOAD_FAST                'user_id'
          268_270  POP_JUMP_IF_FALSE   288  'to 288'
              272  LOAD_FAST                'roles'
          274_276  POP_JUMP_IF_TRUE    288  'to 288'

 L. 123       278  LOAD_FAST                'urm_ctrl'
              280  LOAD_METHOD              get_user_roles
              282  LOAD_FAST                'user_id'
              284  CALL_METHOD_1         1  ''
              286  STORE_FAST               '__roles'
            288_0  COME_FROM           274  '274'
            288_1  COME_FROM           268  '268'

 L. 124       288  LOAD_FAST                'urds_ctrl'
              290  LOAD_METHOD              get_user_readable_data_fields
              292  LOAD_FAST                'document_name'
              294  LOAD_FAST                '__roles'
              296  LOAD_FAST                'exclude_default'
              298  CALL_METHOD_3         3  ''
              300  UNPACK_SEQUENCE_2     2 
              302  STORE_FAST               'err'
              304  STORE_FAST               '_fields'

 L. 125       306  LOAD_FAST                'err'
          308_310  POP_JUMP_IF_FALSE   338  'to 338'

 L. 126       312  LOAD_STR                 "Entity '"
              314  LOAD_FAST                'document_name'
              316  FORMAT_VALUE          0  ''
              318  LOAD_STR                 "' is missing from user readable data's"
              320  BUILD_STRING_3        3 
              322  STORE_FAST               'msg'

 L. 127       324  LOAD_CONST               True
              326  LOAD_GLOBAL              error_response
              328  LOAD_FAST                'msg'
              330  CALL_FUNCTION_1       1  ''
              332  BUILD_TUPLE_2         2 
              334  POP_BLOCK        
              336  RETURN_VALUE     
            338_0  COME_FROM           308  '308'

 L. 129       338  LOAD_GLOBAL              set
              340  LOAD_FAST                'fields'
              342  CALL_FUNCTION_1       1  ''
              344  LOAD_FAST                '_fields'
              346  BINARY_SUBTRACT  
              348  STORE_FAST               'diff'

 L. 130       350  LOAD_GLOBAL              len
              352  LOAD_FAST                'diff'
              354  CALL_FUNCTION_1       1  ''
              356  LOAD_CONST               0
              358  COMPARE_OP               >
          360_362  POP_JUMP_IF_FALSE   378  'to 378'

 L. 131       364  LOAD_CONST               True
              366  LOAD_GLOBAL              error_response
              368  LOAD_STR                 'Select clause contains non readable attributes'
              370  CALL_FUNCTION_1       1  ''
              372  BUILD_TUPLE_2         2 
              374  POP_BLOCK        
              376  RETURN_VALUE     
            378_0  COME_FROM           360  '360'
            378_1  COME_FROM           252  '252'

 L. 133       378  LOAD_GLOBAL              GenericReadController
              380  CALL_FUNCTION_0       0  ''
              382  STORE_FAST               'sql_ctrl'

 L. 134       384  LOAD_FAST                'dictionary'
              386  LOAD_METHOD              get
              388  LOAD_GLOBAL              RAW_WHERE
              390  BUILD_MAP_0           0 
              392  CALL_METHOD_2         2  ''
              394  STORE_FAST               '__raw__where'

 L. 136       396  LOAD_FAST                'dictionary'
              398  LOAD_METHOD              get
              400  LOAD_GLOBAL              PAGE_NUM
              402  LOAD_FAST                'page_number'
              404  CALL_METHOD_2         2  ''
              406  STORE_FAST               'page_num'

 L. 137       408  LOAD_FAST                'dictionary'
              410  LOAD_METHOD              get
              412  LOAD_GLOBAL              PAGE_SIZE
              414  LOAD_FAST                '_size'
              416  CALL_METHOD_2         2  ''
              418  STORE_FAST               'page_size'

 L. 139       420  LOAD_GLOBAL              Q
              422  CALL_FUNCTION_0       0  ''
              424  STORE_FAST               'q'

 L. 140       426  LOAD_FAST                'dictionary'
              428  LOAD_METHOD              get
              430  LOAD_GLOBAL              WHERE
              432  LOAD_CONST               None
              434  CALL_METHOD_2         2  ''
          436_438  POP_JUMP_IF_FALSE   448  'to 448'

 L. 141       440  LOAD_FAST                'dictionary'
              442  LOAD_GLOBAL              WHERE
              444  BINARY_SUBSCR    
              446  STORE_FAST               'q'
            448_0  COME_FROM           436  '436'

 L. 145       448  LOAD_GLOBAL              Q
              450  CALL_FUNCTION_0       0  ''
              452  STORE_FAST               'q2'

 L. 147       454  LOAD_FAST                'user_id'
          456_458  POP_JUMP_IF_FALSE   470  'to 470'

 L. 148       460  LOAD_GLOBAL              Q
              462  LOAD_FAST                'user_id'
              464  LOAD_CONST               ('IdsAllowedToRead',)
              466  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              468  STORE_FAST               'q2'
            470_0  COME_FROM           456  '456'

 L. 150       470  LOAD_FAST                'checking_roles'
          472_474  POP_JUMP_IF_FALSE   562  'to 562'

 L. 151       476  LOAD_FAST                'roles'
          478_480  POP_JUMP_IF_TRUE    498  'to 498'
              482  LOAD_FAST                'user_id'
          484_486  POP_JUMP_IF_FALSE   498  'to 498'

 L. 152       488  LOAD_FAST                'urm_ctrl'
              490  LOAD_METHOD              get_user_roles
              492  LOAD_FAST                'user_id'
              494  CALL_METHOD_1         1  ''
              496  STORE_FAST               'roles'
            498_0  COME_FROM           484  '484'
            498_1  COME_FROM           478  '478'

 L. 153       498  LOAD_FAST                'roles'
          500_502  POP_JUMP_IF_FALSE   534  'to 534'
              504  LOAD_GLOBAL              isinstance
              506  LOAD_FAST                'roles'
              508  LOAD_GLOBAL              list
              510  LOAD_GLOBAL              tuple
              512  BUILD_TUPLE_2         2 
              514  CALL_FUNCTION_2       2  ''
          516_518  POP_JUMP_IF_TRUE    534  'to 534'

 L. 154       520  LOAD_CONST               True
              522  LOAD_GLOBAL              error_response
              524  LOAD_STR                 'roles must be a list or a tuple.'
              526  CALL_FUNCTION_1       1  ''
              528  BUILD_TUPLE_2         2 
              530  POP_BLOCK        
              532  RETURN_VALUE     
            534_0  COME_FROM           516  '516'
            534_1  COME_FROM           500  '500'

 L. 155       534  LOAD_FAST                'roles'
              536  GET_ITER         
              538  FOR_ITER            562  'to 562'
              540  STORE_FAST               'role'

 L. 156       542  LOAD_FAST                'q2'
              544  LOAD_METHOD              __or__
              546  LOAD_GLOBAL              Q
              548  LOAD_FAST                'role'
              550  LOAD_CONST               ('RolesAllowedToRead',)
              552  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              554  CALL_METHOD_1         1  ''
              556  STORE_FAST               'q2'
          558_560  JUMP_BACK           538  'to 538'
            562_0  COME_FROM           472  '472'

 L. 158       562  LOAD_FAST                'user_id'
          564_566  POP_JUMP_IF_TRUE    580  'to 580'
              568  LOAD_FAST                'checking_roles'
          570_572  POP_JUMP_IF_FALSE   590  'to 590'
              574  LOAD_FAST                'roles'
          576_578  POP_JUMP_IF_FALSE   590  'to 590'
            580_0  COME_FROM           564  '564'

 L. 159       580  LOAD_FAST                'q'
              582  LOAD_METHOD              __and__
              584  LOAD_FAST                'q2'
              586  CALL_METHOD_1         1  ''
              588  STORE_FAST               'q'
            590_0  COME_FROM           576  '576'
            590_1  COME_FROM           570  '570'

 L. 163       590  BUILD_LIST_0          0 
              592  STORE_FAST               'order_by'

 L. 164       594  LOAD_FAST                'dictionary'
              596  LOAD_METHOD              get
              598  LOAD_GLOBAL              ORDER_BY
              600  LOAD_CONST               None
              602  CALL_METHOD_2         2  ''
          604_606  POP_JUMP_IF_FALSE   616  'to 616'

 L. 165       608  LOAD_FAST                'dictionary'
              610  LOAD_GLOBAL              ORDER_BY
              612  BINARY_SUBSCR    
              614  STORE_FAST               'order_by'
            616_0  COME_FROM           604  '604'

 L. 167       616  LOAD_FAST                'sql_ctrl'
              618  LOAD_METHOD              read
              620  LOAD_FAST                'document_name'
              622  LOAD_FAST                'q'
              624  LOAD_FAST                'page_size'
              626  LOAD_FAST                'page_num'
              628  LOAD_FAST                'order_by'
              630  CALL_METHOD_5         5  ''
              632  UNPACK_SEQUENCE_2     2 
              634  STORE_FAST               'data'
              636  STORE_FAST               'cnt'

 L. 168       638  LOAD_FAST                'cnt'
              640  LOAD_CONST               0
              642  COMPARE_OP               ==
          644_646  POP_JUMP_IF_FALSE   664  'to 664'

 L. 169       648  LOAD_CONST               False
              650  LOAD_GLOBAL              success_response_with_total_records
              652  BUILD_LIST_0          0 
              654  LOAD_FAST                'cnt'
              656  CALL_FUNCTION_2       2  ''
              658  BUILD_TUPLE_2         2 
              660  POP_BLOCK        
              662  RETURN_VALUE     
            664_0  COME_FROM           644  '644'

 L. 170       664  LOAD_GLOBAL              GenericSerializerAlpha
              666  LOAD_FAST                'document_name'
              668  LOAD_CONST               ('document_name',)
              670  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              672  STORE_FAST               'gsa'

 L. 171       674  LOAD_FAST                'fields'
              676  GET_ITER         
              678  FOR_ITER            696  'to 696'
              680  STORE_FAST               'field'

 L. 172       682  LOAD_FAST                'gsa'
              684  LOAD_METHOD              select
              686  LOAD_FAST                'field'
              688  CALL_METHOD_1         1  ''
              690  POP_TOP          
          692_694  JUMP_BACK           678  'to 678'

 L. 173       696  LOAD_FAST                'gsa'
              698  LOAD_METHOD              serialize
              700  LOAD_FAST                'data'
              702  CALL_METHOD_1         1  ''
              704  STORE_FAST               'json'

 L. 174       706  LOAD_GLOBAL              success_response_with_total_records
              708  LOAD_FAST                'json'
              710  LOAD_ATTR                data
              712  LOAD_FAST                'cnt'
              714  CALL_FUNCTION_2       2  ''
              716  STORE_FAST               'res'

 L. 175       718  LOAD_CONST               False
              720  LOAD_FAST                'res'
              722  BUILD_TUPLE_2         2 
              724  POP_BLOCK        
              726  RETURN_VALUE     
            728_0  COME_FROM_FINALLY    68  '68'

 L. 176       728  DUP_TOP          
              730  LOAD_GLOBAL              BaseException
              732  COMPARE_OP               exception-match
          734_736  POP_JUMP_IF_FALSE   794  'to 794'
              738  POP_TOP          
              740  STORE_FAST               'e'
              742  POP_TOP          
              744  SETUP_FINALLY       782  'to 782'

 L. 177       746  LOAD_FAST                'error_track'
          748_750  POP_JUMP_IF_FALSE   758  'to 758'

 L. 178       752  LOAD_GLOBAL              print_traceback
              754  CALL_FUNCTION_0       0  ''
              756  POP_TOP          
            758_0  COME_FROM           748  '748'

 L. 179       758  LOAD_CONST               True
              760  LOAD_GLOBAL              error_response
              762  LOAD_GLOBAL              str
              764  LOAD_FAST                'e'
              766  CALL_FUNCTION_1       1  ''
              768  CALL_FUNCTION_1       1  ''
              770  BUILD_TUPLE_2         2 
              772  ROT_FOUR         
              774  POP_BLOCK        
              776  POP_EXCEPT       
              778  CALL_FINALLY        782  'to 782'
              780  RETURN_VALUE     
            782_0  COME_FROM           778  '778'
            782_1  COME_FROM_FINALLY   744  '744'
              782  LOAD_CONST               None
              784  STORE_FAST               'e'
              786  DELETE_FAST              'e'
              788  END_FINALLY      
              790  POP_EXCEPT       
              792  JUMP_FORWARD        796  'to 796'
            794_0  COME_FROM           734  '734'
              794  END_FINALLY      
            796_0  COME_FROM           792  '792'

Parse error at or near `POP_BLOCK' instruction at offset 774