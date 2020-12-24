# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/ui/components/select/views.py
# Compiled at: 2019-02-26 16:31:22
# Size of source mod 2**32: 2952 bytes
import json
import django.apps as apps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from djangoplus.utils.serialization import dumps_qs_query, loads_qs_query
from djangoplus.utils.metadata import get_metadata

@login_required
@csrf_exempt
def autocomplete--- This code section failed: ---

 L.  16         0  BUILD_LIST_0          0 
                2  STORE_FAST               'results'

 L.  17         4  LOAD_FAST                'request'
                6  LOAD_ATTR                POST
                8  LOAD_METHOD              get
               10  LOAD_STR                 'q'
               12  CALL_METHOD_1         1  '1 positional argument'
               14  STORE_FAST               'q'

 L.  18        16  LOAD_GLOBAL              loads_qs_query
               18  LOAD_FAST                'request'
               20  LOAD_ATTR                POST
               22  LOAD_STR                 'qs[qs]'
               24  BINARY_SUBSCR    
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  STORE_FAST               'qs'

 L.  19        30  LOAD_GLOBAL              get_metadata
               32  LOAD_FAST                'qs'
               34  LOAD_ATTR                model
               36  LOAD_STR                 'search_fields'
               38  BUILD_LIST_0          0 
               40  CALL_FUNCTION_3       3  '3 positional arguments'
               42  STORE_FAST               'search_fields'

 L.  20        44  LOAD_GLOBAL              get_metadata
               46  LOAD_FAST                'qs'
               48  LOAD_ATTR                model
               50  LOAD_STR                 'select_template'
               52  CALL_FUNCTION_2       2  '2 positional arguments'
               54  STORE_FAST               'select_template'

 L.  21        56  LOAD_GLOBAL              get_metadata
               58  LOAD_FAST                'qs'
               60  LOAD_ATTR                model
               62  LOAD_STR                 'select_display'
               64  CALL_FUNCTION_2       2  '2 positional arguments'
               66  STORE_FAST               'select_display'

 L.  22        68  LOAD_CONST               None
               70  STORE_FAST               'queryset'

 L.  23        72  LOAD_FAST                'q'
               74  POP_JUMP_IF_FALSE   180  'to 180'

 L.  24        76  SETUP_LOOP          156  'to 156'
               78  LOAD_GLOBAL              enumerate
               80  LOAD_FAST                'search_fields'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  GET_ITER         
               86  FOR_ITER            154  'to 154'
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'i'
               92  STORE_FAST               'search_field'

 L.  25        94  LOAD_FAST                'i'
               96  LOAD_CONST               0
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   126  'to 126'

 L.  26       102  LOAD_FAST                'qs'
              104  LOAD_ATTR                filter
              106  BUILD_TUPLE_0         0 
              108  LOAD_STR                 '{}__icontains'
              110  LOAD_METHOD              format
              112  LOAD_FAST                'search_field'
              114  CALL_METHOD_1         1  '1 positional argument'
              116  LOAD_FAST                'q'
              118  BUILD_MAP_1           1 
              120  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              122  STORE_FAST               'queryset'
              124  JUMP_BACK            86  'to 86'
            126_0  COME_FROM           100  '100'

 L.  28       126  LOAD_FAST                'queryset'
              128  LOAD_FAST                'qs'
              130  LOAD_ATTR                filter
              132  BUILD_TUPLE_0         0 
              134  LOAD_STR                 '{}__icontains'
              136  LOAD_METHOD              format
              138  LOAD_FAST                'search_field'
              140  CALL_METHOD_1         1  '1 positional argument'
              142  LOAD_FAST                'q'
              144  BUILD_MAP_1           1 
              146  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              148  BINARY_OR        
              150  STORE_FAST               'queryset'
              152  JUMP_BACK            86  'to 86'
              154  POP_BLOCK        
            156_0  COME_FROM_LOOP       76  '76'

 L.  29       156  LOAD_FAST                'queryset'
              158  LOAD_CONST               None
              160  COMPARE_OP               is
              162  POP_JUMP_IF_FALSE   184  'to 184'

 L.  30       164  LOAD_GLOBAL              ValueError
              166  LOAD_STR                 'The class {} does not have any search field.'
              168  LOAD_METHOD              format
              170  LOAD_FAST                'class_name'
              172  CALL_METHOD_1         1  '1 positional argument'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  RAISE_VARARGS_1       1  'exception instance'
              178  JUMP_FORWARD        184  'to 184'
            180_0  COME_FROM            74  '74'

 L.  32       180  LOAD_FAST                'qs'
              182  STORE_FAST               'queryset'
            184_0  COME_FROM           178  '178'
            184_1  COME_FROM           162  '162'

 L.  35       184  SETUP_LOOP          270  'to 270'
              186  LOAD_FAST                'queryset'
              188  LOAD_CONST               0
              190  LOAD_CONST               25
              192  BUILD_SLICE_2         2 
              194  BINARY_SUBSCR    
              196  GET_ITER         
              198  FOR_ITER            268  'to 268'
              200  STORE_FAST               'obj'

 L.  36       202  LOAD_FAST                'select_template'
              204  POP_JUMP_IF_TRUE    210  'to 210'
              206  LOAD_FAST                'select_display'
              208  POP_JUMP_IF_FALSE   232  'to 232'
            210_0  COME_FROM           204  '204'
              210  LOAD_GLOBAL              render_to_string
              212  LOAD_FAST                'select_template'
              214  JUMP_IF_TRUE_OR_POP   218  'to 218'
              216  LOAD_STR                 'select_template.html'
            218_0  COME_FROM           214  '214'
              218  LOAD_GLOBAL              dict
              220  LOAD_FAST                'obj'
              222  LOAD_FAST                'select_display'
              224  LOAD_CONST               ('obj', 'select_display')
              226  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  JUMP_IF_TRUE_OR_POP   238  'to 238'
            232_0  COME_FROM           208  '208'
              232  LOAD_GLOBAL              str
              234  LOAD_FAST                'obj'
              236  CALL_FUNCTION_1       1  '1 positional argument'
            238_0  COME_FROM           230  '230'
              238  STORE_FAST               'html'

 L.  37       240  LOAD_FAST                'results'
              242  LOAD_METHOD              append
              244  LOAD_GLOBAL              dict
              246  LOAD_FAST                'obj'
              248  LOAD_ATTR                id
              250  LOAD_GLOBAL              str
              252  LOAD_FAST                'obj'
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  LOAD_FAST                'html'
              258  LOAD_CONST               ('id', 'text', 'html')
              260  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              262  CALL_METHOD_1         1  '1 positional argument'
              264  POP_TOP          
              266  JUMP_BACK           198  'to 198'
              268  POP_BLOCK        
            270_0  COME_FROM_LOOP      184  '184'

 L.  38       270  LOAD_GLOBAL              json
              272  LOAD_METHOD              dumps
              274  LOAD_GLOBAL              dict
              276  LOAD_FAST                'q'
              278  LOAD_FAST                'results'
              280  LOAD_CONST               ('q', 'results')
              282  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              284  CALL_METHOD_1         1  '1 positional argument'
              286  STORE_FAST               's'

 L.  40       288  LOAD_GLOBAL              HttpResponse
              290  LOAD_FAST                's'
              292  CALL_FUNCTION_1       1  '1 positional argument'
              294  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 232_0


@login_required
@csrf_exempt
def reload_options--- This code section failed: ---

 L.  46         0  BUILD_LIST_0          0 
                2  STORE_FAST               'l'

 L.  47         4  BUILD_LIST_0          0 
                6  STORE_FAST               'pks'

 L.  48         8  LOAD_FAST                'current_value'
               10  LOAD_STR                 '0'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_TRUE     50  'to 50'

 L.  49        16  SETUP_LOOP           50  'to 50'
               18  LOAD_FAST                'current_value'
               20  LOAD_METHOD              split
               22  LOAD_STR                 '_'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  GET_ITER         
               28  FOR_ITER             48  'to 48'
               30  STORE_FAST               'pk'

 L.  50        32  LOAD_FAST                'pks'
               34  LOAD_METHOD              append
               36  LOAD_GLOBAL              int
               38  LOAD_FAST                'pk'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  POP_TOP          
               46  JUMP_BACK            28  'to 28'
               48  POP_BLOCK        
             50_0  COME_FROM_LOOP       16  '16'
             50_1  COME_FROM            14  '14'

 L.  51        50  LOAD_GLOBAL              int
               52  LOAD_FAST                'selected_value'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  STORE_FAST               'selected_value'

 L.  52        58  LOAD_GLOBAL              int
               60  LOAD_FAST                'lazy'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  STORE_FAST               'lazy'

 L.  53        66  LOAD_GLOBAL              apps
               68  LOAD_METHOD              get_model
               70  LOAD_FAST                'app_name'
               72  LOAD_FAST                'class_name'
               74  CALL_METHOD_2         2  '2 positional arguments'
               76  STORE_FAST               'cls'

 L.  54        78  LOAD_GLOBAL              get_metadata
               80  LOAD_FAST                'cls'
               82  LOAD_STR                 'select_template'
               84  CALL_FUNCTION_2       2  '2 positional arguments'
               86  STORE_FAST               'select_template'

 L.  55        88  LOAD_GLOBAL              get_metadata
               90  LOAD_FAST                'cls'
               92  LOAD_STR                 'select_display'
               94  CALL_FUNCTION_2       2  '2 positional arguments'
               96  STORE_FAST               'select_display'

 L.  56        98  LOAD_FAST                'cls'
              100  LOAD_ATTR                objects
              102  LOAD_ATTR                filter
              104  BUILD_TUPLE_0         0 
              106  LOAD_FAST                'lookup'
              108  LOAD_FAST                'selected_value'
              110  BUILD_MAP_1           1 
              112  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              114  STORE_FAST               'queryset'

 L.  58       116  LOAD_GLOBAL              dict
              118  LOAD_FAST                'selected_value'
              120  BUILD_LIST_0          0 
              122  LOAD_FAST                'lazy'
              124  POP_JUMP_IF_FALSE   134  'to 134'
              126  LOAD_GLOBAL              dumps_qs_query
              128  LOAD_FAST                'queryset'
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  JUMP_IF_TRUE_OR_POP   136  'to 136'
            134_0  COME_FROM           124  '124'
              134  LOAD_CONST               None
            136_0  COME_FROM           132  '132'
              136  LOAD_CONST               ('selected_value', 'results', 'qs')
              138  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              140  STORE_FAST               'data'

 L.  59       142  LOAD_FAST                'lazy'
              144  POP_JUMP_IF_FALSE   244  'to 244'

 L.  60       146  LOAD_FAST                'pks'
              148  POP_JUMP_IF_FALSE   242  'to 242'

 L.  61       150  SETUP_LOOP          334  'to 334'
              152  LOAD_FAST                'cls'
              154  LOAD_ATTR                objects
              156  LOAD_ATTR                filter
              158  LOAD_FAST                'pks'
              160  LOAD_CONST               ('pk__in',)
              162  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              164  GET_ITER         
              166  FOR_ITER            240  'to 240'
              168  STORE_FAST               'obj'

 L.  62       170  LOAD_FAST                'select_template'
              172  POP_JUMP_IF_TRUE    178  'to 178'
              174  LOAD_FAST                'select_display'
              176  POP_JUMP_IF_FALSE   200  'to 200'
            178_0  COME_FROM           172  '172'
              178  LOAD_GLOBAL              render_to_string
              180  LOAD_FAST                'select_template'
              182  JUMP_IF_TRUE_OR_POP   186  'to 186'
              184  LOAD_STR                 'select_template.html'
            186_0  COME_FROM           182  '182'
              186  LOAD_GLOBAL              dict
              188  LOAD_FAST                'obj'
              190  LOAD_FAST                'select_display'
              192  LOAD_CONST               ('obj', 'select_display')
              194  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              196  CALL_FUNCTION_2       2  '2 positional arguments'
              198  JUMP_IF_TRUE_OR_POP   206  'to 206'
            200_0  COME_FROM           176  '176'
              200  LOAD_GLOBAL              str
              202  LOAD_FAST                'obj'
              204  CALL_FUNCTION_1       1  '1 positional argument'
            206_0  COME_FROM           198  '198'
              206  STORE_FAST               'html'

 L.  63       208  LOAD_FAST                'data'
              210  LOAD_STR                 'results'
              212  BINARY_SUBSCR    
              214  LOAD_METHOD              append
              216  LOAD_GLOBAL              dict
              218  LOAD_FAST                'obj'
              220  LOAD_ATTR                id
              222  LOAD_GLOBAL              str
              224  LOAD_FAST                'obj'
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  LOAD_FAST                'html'
              230  LOAD_CONST               ('id', 'text', 'html')
              232  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              234  CALL_METHOD_1         1  '1 positional argument'
              236  POP_TOP          
              238  JUMP_BACK           166  'to 166'
              240  POP_BLOCK        
            242_0  COME_FROM           148  '148'
              242  JUMP_FORWARD        334  'to 334'
            244_0  COME_FROM           144  '144'

 L.  65       244  SETUP_LOOP          334  'to 334'
              246  LOAD_FAST                'queryset'
              248  GET_ITER         
              250  FOR_ITER            332  'to 332'
              252  STORE_FAST               'obj'

 L.  66       254  LOAD_FAST                'select_template'
          256_258  POP_JUMP_IF_TRUE    266  'to 266'
              260  LOAD_FAST                'select_display'
          262_264  POP_JUMP_IF_FALSE   292  'to 292'
            266_0  COME_FROM           256  '256'
              266  LOAD_GLOBAL              render_to_string
              268  LOAD_FAST                'select_template'
          270_272  JUMP_IF_TRUE_OR_POP   276  'to 276'
              274  LOAD_STR                 'select_template.html'
            276_0  COME_FROM           270  '270'
              276  LOAD_GLOBAL              dict
              278  LOAD_FAST                'obj'
              280  LOAD_FAST                'select_display'
              282  LOAD_CONST               ('obj', 'select_display')
              284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              286  CALL_FUNCTION_2       2  '2 positional arguments'
          288_290  JUMP_IF_TRUE_OR_POP   298  'to 298'
            292_0  COME_FROM           262  '262'
              292  LOAD_GLOBAL              str
              294  LOAD_FAST                'obj'
              296  CALL_FUNCTION_1       1  '1 positional argument'
            298_0  COME_FROM           288  '288'
              298  STORE_FAST               'html'

 L.  67       300  LOAD_FAST                'data'
              302  LOAD_STR                 'results'
              304  BINARY_SUBSCR    
              306  LOAD_METHOD              append
              308  LOAD_GLOBAL              dict
              310  LOAD_FAST                'obj'
              312  LOAD_ATTR                id
              314  LOAD_GLOBAL              str
              316  LOAD_FAST                'obj'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  LOAD_FAST                'html'
              322  LOAD_CONST               ('id', 'text', 'html')
              324  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              326  CALL_METHOD_1         1  '1 positional argument'
              328  POP_TOP          
              330  JUMP_BACK           250  'to 250'
              332  POP_BLOCK        
            334_0  COME_FROM_LOOP      244  '244'
            334_1  COME_FROM           242  '242'
            334_2  COME_FROM_LOOP      150  '150'

 L.  68       334  LOAD_GLOBAL              json
              336  LOAD_METHOD              dumps
              338  LOAD_FAST                'data'
              340  CALL_METHOD_1         1  '1 positional argument'
              342  STORE_FAST               's'

 L.  70       344  LOAD_GLOBAL              HttpResponse
              346  LOAD_FAST                's'
              348  CALL_FUNCTION_1       1  '1 positional argument'
              350  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 200_0