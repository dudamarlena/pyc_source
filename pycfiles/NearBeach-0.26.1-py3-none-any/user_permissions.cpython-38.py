# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled/NearBeach/user_permissions.py
# Compiled at: 2020-05-03 01:13:24
# Size of source mod 2**32: 6738 bytes
"""
This python script will return the user's permission level for ANY given permission
"""
import json
from .models import *
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.urls import reverse

def return_user_permission_level--- This code section failed: ---

 L.  58         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'permission_field'
                4  LOAD_GLOBAL              list
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     16  'to 16'

 L.  59        10  LOAD_FAST                'permission_field'
               12  BUILD_LIST_1          1 
               14  STORE_FAST               'permission_field'
             16_0  COME_FROM             8  '8'

 L.  62        16  BUILD_MAP_0           0 
               18  STORE_FAST               'user_permission_level'

 L.  68        20  LOAD_FAST                'request'
               22  LOAD_ATTR                user
               24  LOAD_ATTR                is_superuser
               26  LOAD_CONST               True
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    70  'to 70'

 L.  70        32  LOAD_FAST                'permission_field'
               34  GET_ITER         
               36  FOR_ITER             50  'to 50'
               38  STORE_FAST               'row'

 L.  71        40  LOAD_CONST               4
               42  LOAD_FAST                'user_permission_level'
               44  LOAD_FAST                'row'
               46  STORE_SUBSCR     
               48  JUMP_BACK            36  'to 36'

 L.  73        50  LOAD_CONST               4
               52  LOAD_FAST                'user_permission_level'
               54  LOAD_STR                 'new_item'
               56  STORE_SUBSCR     

 L.  74        58  LOAD_CONST               4
               60  LOAD_FAST                'user_permission_level'
               62  LOAD_STR                 'administration'
               64  STORE_SUBSCR     

 L.  75        66  LOAD_FAST                'user_permission_level'
               68  RETURN_VALUE     
             70_0  COME_FROM            30  '30'

 L.  84        70  LOAD_FAST                'permission_field'
               72  GET_ITER         
            74_76  FOR_ITER            336  'to 336'
               78  STORE_FAST               'row'

 L.  89        80  LOAD_FAST                'row'
               82  LOAD_STR                 ''
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE    94  'to 94'

 L.  90        88  POP_TOP          
            90_92  JUMP_ABSOLUTE       336  'to 336'
             94_0  COME_FROM            86  '86'

 L.  94        94  LOAD_FAST                'group_list'
               96  LOAD_CONST               None
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   158  'to 158'

 L.  96       102  LOAD_GLOBAL              user_group
              104  LOAD_ATTR                objects
              106  LOAD_ATTR                filter

 L.  97       108  LOAD_STR                 'FALSE'

 L.  98       110  LOAD_FAST                'request'
              112  LOAD_ATTR                user

 L.  99       114  LOAD_STR                 'FALSE'

 L.  96       116  LOAD_CONST               ('is_deleted', 'username', 'permission_set__is_deleted')
              118  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              120  LOAD_METHOD              aggregate

 L. 100       122  LOAD_GLOBAL              Max
              124  LOAD_STR                 'permission_set__'
              126  LOAD_FAST                'row'
              128  BINARY_ADD       
              130  CALL_FUNCTION_1       1  ''

 L.  96       132  CALL_METHOD_1         1  ''
              134  STORE_FAST               'user_groups_results'

 L. 101       136  LOAD_FAST                'user_groups_results'
              138  LOAD_STR                 'permission_set__'
              140  LOAD_FAST                'row'
              142  BINARY_ADD       
              144  LOAD_STR                 '__max'
              146  BINARY_ADD       
              148  BINARY_SUBSCR    
              150  LOAD_FAST                'user_permission_level'
              152  LOAD_FAST                'row'
              154  STORE_SUBSCR     
              156  JUMP_BACK            74  'to 74'
            158_0  COME_FROM           100  '100'

 L. 105       158  LOAD_CONST               0
              160  STORE_FAST               'group_permission'

 L. 106       162  LOAD_FAST                'group_list'
              164  GET_ITER         
            166_0  COME_FROM           306  '306'
            166_1  COME_FROM           286  '286'
              166  FOR_ITER            326  'to 326'
              168  STORE_FAST               'group_id'

 L. 108       170  SETUP_FINALLY       216  'to 216'

 L. 109       172  LOAD_GLOBAL              user_group
              174  LOAD_ATTR                objects
              176  LOAD_ATTR                filter

 L. 110       178  LOAD_STR                 'FALSE'

 L. 111       180  LOAD_FAST                'request'
              182  LOAD_ATTR                user

 L. 112       184  LOAD_STR                 'FALSE'

 L. 113       186  LOAD_FAST                'group_id'
              188  LOAD_STR                 'group_id'
              190  BINARY_SUBSCR    

 L. 109       192  LOAD_CONST               ('is_deleted', 'username', 'permission_set__is_deleted', 'group_id')
              194  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              196  LOAD_METHOD              aggregate

 L. 114       198  LOAD_GLOBAL              Max
              200  LOAD_STR                 'permission_set__'
              202  LOAD_FAST                'row'
              204  BINARY_ADD       
              206  CALL_FUNCTION_1       1  ''

 L. 109       208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'user_groups_results'
              212  POP_BLOCK        
              214  JUMP_FORWARD        268  'to 268'
            216_0  COME_FROM_FINALLY   170  '170'

 L. 115       216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 116       222  LOAD_GLOBAL              user_group
              224  LOAD_ATTR                objects
              226  LOAD_ATTR                filter

 L. 117       228  LOAD_STR                 'FALSE'

 L. 118       230  LOAD_FAST                'request'
              232  LOAD_ATTR                user

 L. 119       234  LOAD_STR                 'FALSE'

 L. 120       236  LOAD_FAST                'group_id'
              238  LOAD_STR                 'group_id_id'
              240  BINARY_SUBSCR    

 L. 116       242  LOAD_CONST               ('is_deleted', 'username', 'permission_set__is_deleted', 'group_id')
              244  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              246  LOAD_METHOD              aggregate

 L. 121       248  LOAD_GLOBAL              Max
              250  LOAD_STR                 'permission_set__'
              252  LOAD_FAST                'row'
              254  BINARY_ADD       
              256  CALL_FUNCTION_1       1  ''

 L. 116       258  CALL_METHOD_1         1  ''
              260  STORE_FAST               'user_groups_results'
              262  POP_EXCEPT       
              264  JUMP_FORWARD        268  'to 268'
              266  END_FINALLY      
            268_0  COME_FROM           264  '264'
            268_1  COME_FROM           214  '214'

 L. 124       268  LOAD_FAST                'user_groups_results'
              270  LOAD_STR                 'permission_set__'
              272  LOAD_FAST                'row'
              274  BINARY_ADD       
              276  LOAD_STR                 '__max'
              278  BINARY_ADD       
              280  BINARY_SUBSCR    
              282  LOAD_CONST               None
              284  COMPARE_OP               ==
              286  POP_JUMP_IF_TRUE    166  'to 166'

 L. 125       288  LOAD_FAST                'group_permission'
              290  LOAD_FAST                'user_groups_results'
              292  LOAD_STR                 'permission_set__'
              294  LOAD_FAST                'row'
              296  BINARY_ADD       
              298  LOAD_STR                 '__max'
              300  BINARY_ADD       
              302  BINARY_SUBSCR    
              304  COMPARE_OP               <
              306  POP_JUMP_IF_FALSE   166  'to 166'

 L. 126       308  LOAD_FAST                'user_groups_results'
              310  LOAD_STR                 'permission_set__'
              312  LOAD_FAST                'row'
              314  BINARY_ADD       
              316  LOAD_STR                 '__max'
              318  BINARY_ADD       
              320  BINARY_SUBSCR    
              322  STORE_FAST               'group_permission'
              324  JUMP_BACK           166  'to 166'

 L. 128       326  LOAD_FAST                'group_permission'
              328  LOAD_FAST                'user_permission_level'
              330  LOAD_FAST                'row'
              332  STORE_SUBSCR     
              334  JUMP_BACK            74  'to 74'

 L. 135       336  LOAD_GLOBAL              user_group
              338  LOAD_ATTR                objects
              340  LOAD_ATTR                filter

 L. 136       342  LOAD_STR                 'FALSE'

 L. 137       344  LOAD_FAST                'request'
              346  LOAD_ATTR                user

 L. 138       348  LOAD_STR                 'FALSE'

 L. 135       350  LOAD_CONST               ('is_deleted', 'username', 'permission_set__is_deleted')
              352  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              354  LOAD_METHOD              aggregate

 L. 140       356  LOAD_GLOBAL              Max
              358  LOAD_STR                 'permission_set__project'
              360  CALL_FUNCTION_1       1  ''

 L. 141       362  LOAD_GLOBAL              Max
              364  LOAD_STR                 'permission_set__task'
              366  CALL_FUNCTION_1       1  ''

 L. 142       368  LOAD_GLOBAL              Max
              370  LOAD_STR                 'permission_set__requirement'
              372  CALL_FUNCTION_1       1  ''

 L. 143       374  LOAD_GLOBAL              Max
              376  LOAD_STR                 'permission_set__request_for_change'
              378  CALL_FUNCTION_1       1  ''

 L. 144       380  LOAD_GLOBAL              Max
              382  LOAD_STR                 'permission_set__organisation'
              384  CALL_FUNCTION_1       1  ''

 L. 145       386  LOAD_GLOBAL              Max
              388  LOAD_STR                 'permission_set__customer'
              390  CALL_FUNCTION_1       1  ''

 L. 146       392  LOAD_GLOBAL              Max
              394  LOAD_STR                 'permission_set__administration_assign_user_to_group'
              396  CALL_FUNCTION_1       1  ''

 L. 147       398  LOAD_GLOBAL              Max
              400  LOAD_STR                 'permission_set__administration_create_group'
              402  CALL_FUNCTION_1       1  ''

 L. 148       404  LOAD_GLOBAL              Max
              406  LOAD_STR                 'permission_set__administration_create_permission_set'
              408  CALL_FUNCTION_1       1  ''

 L. 149       410  LOAD_GLOBAL              Max
              412  LOAD_STR                 'permission_set__administration_create_user'
              414  CALL_FUNCTION_1       1  ''

 L. 135       416  CALL_METHOD_10       10  ''
              418  STORE_FAST               'permission_results'

 L. 152       420  LOAD_GLOBAL              max

 L. 153       422  LOAD_FAST                'permission_results'
              424  LOAD_STR                 'permission_set__project__max'
              426  BINARY_SUBSCR    

 L. 154       428  LOAD_FAST                'permission_results'
              430  LOAD_STR                 'permission_set__task__max'
              432  BINARY_SUBSCR    

 L. 155       434  LOAD_FAST                'permission_results'
              436  LOAD_STR                 'permission_set__requirement__max'
              438  BINARY_SUBSCR    

 L. 156       440  LOAD_FAST                'permission_results'
              442  LOAD_STR                 'permission_set__organisation__max'
              444  BINARY_SUBSCR    

 L. 157       446  LOAD_FAST                'permission_results'
              448  LOAD_STR                 'permission_set__customer__max'
              450  BINARY_SUBSCR    

 L. 152       452  CALL_FUNCTION_5       5  ''
              454  LOAD_FAST                'user_permission_level'
              456  LOAD_STR                 'new_item'
              458  STORE_SUBSCR     

 L. 159       460  LOAD_GLOBAL              max

 L. 160       462  LOAD_FAST                'permission_results'
              464  LOAD_STR                 'permission_set__administration_assign_user_to_group__max'
              466  BINARY_SUBSCR    

 L. 161       468  LOAD_FAST                'permission_results'
              470  LOAD_STR                 'permission_set__administration_create_group__max'
              472  BINARY_SUBSCR    

 L. 162       474  LOAD_FAST                'permission_results'
              476  LOAD_STR                 'permission_set__administration_create_permission_set__max'
              478  BINARY_SUBSCR    

 L. 163       480  LOAD_FAST                'permission_results'
              482  LOAD_STR                 'permission_set__administration_create_user__max'
              484  BINARY_SUBSCR    

 L. 159       486  CALL_FUNCTION_4       4  ''
              488  LOAD_FAST                'user_permission_level'
              490  LOAD_STR                 'administration'
              492  STORE_SUBSCR     

 L. 167       494  LOAD_FAST                'user_permission_level'
              496  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 94_0