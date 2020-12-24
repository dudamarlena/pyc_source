# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/libraries/admin_lte/model.py
# Compiled at: 2020-04-21 05:34:55
# Size of source mod 2**32: 16484 bytes
import inspect
from typing import Tuple, Type
from django.db import models
from django.db.models import QuerySet
from django.shortcuts import redirect
from avishan import current_request
from avishan.exceptions import ErrorMessageException
from avishan.libraries.admin_lte.classes import *
from avishan.misc.translation import AvishanTranslatable
from avishan.models import AvishanModel, Image, File
from avishan.configure import get_avishan_config

class AvishanModelPanelEnabled:
    panel_view = None
    sidebar_visible = True
    sidebar_visible: bool
    sidebar_fa_icon = 'fa-circle-o'
    sidebar_fa_icon: Optional[str]
    sidebar_parent_view = None
    sidebar_order = -1
    sidebar_order: int

    @classmethod
    def panel_dashboard_items(cls) -> List[DashboardItem]:
        return []

    @classmethod
    def call_panel_model_function--- This code section failed: ---

 L.  30         0  SETUP_FINALLY        20  'to 20'

 L.  31         2  LOAD_GLOBAL              getattr
                4  LOAD_FAST                'cls'
                6  LOAD_STR                 'panel_'
                8  LOAD_FAST                'model_function_name'
               10  BINARY_ADD       
               12  CALL_FUNCTION_2       2  ''
               14  CALL_FUNCTION_0       0  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  32        20  DUP_TOP          
               22  LOAD_GLOBAL              AttributeError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    70  'to 70'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  33        34  LOAD_GLOBAL              ErrorMessageException
               36  LOAD_GLOBAL              AvishanTranslatable

 L.  34        38  LOAD_STR                 'Model '
               40  LOAD_FAST                'cls'
               42  LOAD_METHOD              class_name
               44  CALL_METHOD_0         0  ''
               46  FORMAT_VALUE          0  ''
               48  LOAD_STR                 ' should have a function with name "panel_'
               50  LOAD_FAST                'model_function_name'
               52  FORMAT_VALUE          0  ''
               54  LOAD_STR                 '"'
               56  BUILD_STRING_5        5 

 L.  33        58  LOAD_CONST               ('EN',)
               60  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            26  '26'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'

Parse error at or near `POP_TOP' instruction at offset 30

    def call_panel_item_function--- This code section failed: ---

 L.  38         0  SETUP_FINALLY        20  'to 20'

 L.  39         2  LOAD_GLOBAL              getattr
                4  LOAD_FAST                'self'
                6  LOAD_STR                 'panel_'
                8  LOAD_FAST                'model_function_name'
               10  BINARY_ADD       
               12  CALL_FUNCTION_2       2  ''
               14  CALL_FUNCTION_0       0  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  40        20  DUP_TOP          
               22  LOAD_GLOBAL              AttributeError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    70  'to 70'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  41        34  LOAD_GLOBAL              ErrorMessageException
               36  LOAD_GLOBAL              AvishanTranslatable

 L.  42        38  LOAD_STR                 'Model '
               40  LOAD_FAST                'self'
               42  LOAD_METHOD              class_name
               44  CALL_METHOD_0         0  ''
               46  FORMAT_VALUE          0  ''
               48  LOAD_STR                 ' should have a function with name "panel_'
               50  LOAD_FAST                'model_function_name'
               52  FORMAT_VALUE          0  ''
               54  LOAD_STR                 '"'
               56  BUILD_STRING_5        5 

 L.  41        58  LOAD_CONST               ('EN',)
               60  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            26  '26'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'

Parse error at or near `POP_TOP' instruction at offset 30

    @classmethod
    def panel_list(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')]):
        from avishan.views.panel_views import AvishanPanelModelPage
        cls
        cls.panel_view.page_header_text = cls.panel_plural_name
        cls.panel_view.contents.append(Row.add_item(Col(12).add_item(Card(header=CardHeader(buttons=(cls.panel_list_header_buttons)),
          body=Table(heads=[TableHead(name=(item[0]), title=(item[1])) for item in cls.panel_list_title_items],
          link_head_key='id',
          link_prepend=f"/{get_avishan_config.PANEL_ROOT}/{cls.class_plural_snake_case_name}/",
          link_append='/detail').add_items(items=(cls.panel_list_items)),
          body_added_classes='table-responsive p-0'))))

    @classmethod
    def panel_create--- This code section failed: ---

 L.  78         0  LOAD_CONST               0
                2  LOAD_CONST               ('AvishanPanelModelPage',)
                4  IMPORT_NAME_ATTR         avishan.views.panel_views
                6  IMPORT_FROM              AvishanPanelModelPage
                8  STORE_FAST               'AvishanPanelModelPage'
               10  POP_TOP          

 L.  79        12  LOAD_FAST                'cls'
               14  POP_TOP          

 L.  80        16  LOAD_FAST                'edit_mode'
               18  POP_JUMP_IF_FALSE    24  'to 24'
               20  LOAD_STR                 'ویرایش'
               22  JUMP_FORWARD         26  'to 26'
             24_0  COME_FROM            18  '18'
               24  LOAD_STR                 'ایجاد'
             26_0  COME_FROM            22  '22'
               26  LOAD_STR                 ' '
               28  LOAD_FAST                'cls'
               30  LOAD_METHOD              panel_name
               32  CALL_METHOD_0         0  ''
               34  FORMAT_VALUE          0  ''
               36  BUILD_STRING_2        2 
               38  BINARY_ADD       
               40  LOAD_FAST                'cls'
               42  LOAD_ATTR                panel_view
               44  STORE_ATTR               page_header_text

 L.  81        46  LOAD_FAST                'cls'
               48  LOAD_ATTR                panel_view
               50  LOAD_ATTR                item
               52  STORE_FAST               'created'

 L.  82        54  LOAD_STR                 '/'
               56  LOAD_GLOBAL              get_avishan_config
               58  CALL_FUNCTION_0       0  ''
               60  LOAD_ATTR                PANEL_ROOT
               62  FORMAT_VALUE          0  ''
               64  LOAD_STR                 '/'
               66  LOAD_FAST                'cls'
               68  LOAD_METHOD              class_plural_snake_case_name
               70  CALL_METHOD_0         0  ''
               72  FORMAT_VALUE          0  ''
               74  LOAD_STR                 '/'
               76  BUILD_STRING_5        5 
               78  STORE_FAST               'action_url'

 L.  83        80  LOAD_FAST                'edit_mode'
               82  POP_JUMP_IF_FALSE   102  'to 102'

 L.  84        84  LOAD_FAST                'action_url'
               86  LOAD_FAST                'created'
               88  LOAD_ATTR                id
               90  FORMAT_VALUE          0  ''
               92  LOAD_STR                 '/edit'
               94  BUILD_STRING_2        2 
               96  INPLACE_ADD      
               98  STORE_FAST               'action_url'
              100  JUMP_FORWARD        110  'to 110'
            102_0  COME_FROM            82  '82'

 L.  86       102  LOAD_FAST                'action_url'
              104  LOAD_STR                 'create'
              106  INPLACE_ADD      
              108  STORE_FAST               'action_url'
            110_0  COME_FROM           100  '100'

 L.  87       110  LOAD_GLOBAL              Form

 L.  88       112  LOAD_FAST                'action_url'

 L.  89       114  LOAD_STR                 'create'

 L.  90       116  LOAD_GLOBAL              Button
              118  LOAD_FAST                'edit_mode'
              120  POP_JUMP_IF_FALSE   126  'to 126'
              122  LOAD_STR                 'ویرایش'
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           120  '120'
              126  LOAD_STR                 'ایجاد'
            128_0  COME_FROM           124  '124'
              128  LOAD_CONST               ('text',)
              130  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.  91       132  LOAD_FAST                'edit_mode'
              134  POP_JUMP_IF_TRUE    144  'to 144'
              136  LOAD_FAST                'created'
              138  POP_JUMP_IF_FALSE   144  'to 144'
              140  LOAD_CONST               True
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM           138  '138'
            144_1  COME_FROM           134  '134'
              144  LOAD_CONST               False
            146_0  COME_FROM           142  '142'

 L.  87       146  LOAD_CONST               ('action_url', 'name', 'button', 'disabled')
              148  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              150  LOAD_METHOD              add_items

 L.  92       152  LOAD_FAST                'cls'
              154  LOAD_ATTR                panel_create_form_items
              156  LOAD_FAST                'created'
              158  LOAD_CONST               ('item',)
              160  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.  87       162  CALL_METHOD_1         1  ''
              164  LOAD_FAST                'cls'
              166  LOAD_ATTR                panel_view
              168  STORE_ATTR               form

 L.  94       170  BUILD_LIST_0          0 
              172  STORE_FAST               'related_forms'

 L.  95       174  LOAD_FAST                'cls'
              176  LOAD_METHOD              panel_create_related_models
              178  CALL_METHOD_0         0  ''
              180  GET_ITER         
          182_184  FOR_ITER            462  'to 462'
              186  UNPACK_SEQUENCE_2     2 
              188  STORE_DEREF              'model'
              190  STORE_FAST               'related_field_name'

 L.  96       192  LOAD_CONST               0
              194  STORE_FAST               'created_id'

 L.  97       196  LOAD_FAST                'created'
              198  POP_JUMP_IF_FALSE   206  'to 206'

 L.  98       200  LOAD_FAST                'created'
              202  LOAD_ATTR                id
              204  STORE_FAST               'created_id'
            206_0  COME_FROM           198  '198'

 L. 100       206  LOAD_STR                 '/'
              208  LOAD_GLOBAL              get_avishan_config
              210  CALL_FUNCTION_0       0  ''
              212  LOAD_ATTR                PANEL_ROOT
              214  FORMAT_VALUE          0  ''
              216  LOAD_STR                 '/'
              218  LOAD_FAST                'cls'
              220  LOAD_METHOD              class_plural_snake_case_name
              222  CALL_METHOD_0         0  ''
              224  FORMAT_VALUE          0  ''
              226  LOAD_STR                 '/'
              228  LOAD_FAST                'created_id'
              230  FORMAT_VALUE          0  ''
              232  LOAD_STR                 '/'
              234  BUILD_STRING_7        7 
              236  STORE_FAST               'action_url'

 L. 102       238  LOAD_FAST                'edit_mode'
              240  POP_JUMP_IF_FALSE   252  'to 252'

 L. 103       242  LOAD_FAST                'action_url'
              244  LOAD_STR                 'edit'
              246  INPLACE_ADD      
              248  STORE_FAST               'action_url'
              250  JUMP_FORWARD        260  'to 260'
            252_0  COME_FROM           240  '240'

 L. 105       252  LOAD_FAST                'action_url'
              254  LOAD_STR                 'create'
              256  INPLACE_ADD      
              258  STORE_FAST               'action_url'
            260_0  COME_FROM           250  '250'

 L. 106       260  LOAD_FAST                'action_url'
              262  LOAD_STR                 '?on='
              264  LOAD_DEREF               'model'
              266  LOAD_METHOD              class_name
              268  CALL_METHOD_0         0  ''
              270  FORMAT_VALUE          0  ''
              272  BUILD_STRING_2        2 
              274  INPLACE_ADD      
              276  STORE_FAST               'action_url'

 L. 108       278  LOAD_FAST                'related_forms'
              280  LOAD_METHOD              append
              282  LOAD_GLOBAL              Row
              284  CALL_FUNCTION_0       0  ''
              286  LOAD_METHOD              add_item

 L. 109       288  LOAD_GLOBAL              Col
              290  LOAD_CONST               6
              292  CALL_FUNCTION_1       1  ''
              294  LOAD_METHOD              add_item

 L. 110       296  LOAD_GLOBAL              Card

 L. 111       298  LOAD_GLOBAL              CardHeader

 L. 112       300  LOAD_DEREF               'model'
              302  LOAD_METHOD              panel_plural_name
              304  CALL_METHOD_0         0  ''

 L. 111       306  LOAD_CONST               ('title',)
              308  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 114       310  LOAD_GLOBAL              Row
              312  CALL_FUNCTION_0       0  ''
              314  LOAD_METHOD              add_item

 L. 117       316  LOAD_GLOBAL              Col
              318  LOAD_CONST               12
              320  CALL_FUNCTION_1       1  ''
              322  LOAD_METHOD              add_item

 L. 118       324  LOAD_GLOBAL              UnorderedList
              326  CALL_FUNCTION_0       0  ''
              328  LOAD_METHOD              add_items

 L. 119       330  LOAD_CLOSURE             'model'
              332  BUILD_TUPLE_1         1 
              334  LOAD_LISTCOMP            '<code_object <listcomp>>'
              336  LOAD_STR                 'AvishanModelPanelEnabled.panel_create.<locals>.<listcomp>'
              338  MAKE_FUNCTION_8          'closure'

 L. 123       340  LOAD_DEREF               'model'
              342  LOAD_ATTR                objects
              344  LOAD_ATTR                filter
              346  BUILD_TUPLE_0         0 

 L. 124       348  LOAD_FAST                'related_field_name'
              350  LOAD_FAST                'created'
              352  BUILD_MAP_1           1 

 L. 123       354  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 119       356  GET_ITER         
              358  CALL_FUNCTION_1       1  ''

 L. 118       360  CALL_METHOD_1         1  ''

 L. 117       362  CALL_METHOD_1         1  ''

 L. 114       364  CALL_METHOD_1         1  ''
              366  LOAD_METHOD              add_item

 L. 129       368  LOAD_GLOBAL              Col
              370  LOAD_CONST               12
              372  CALL_FUNCTION_1       1  ''
              374  LOAD_METHOD              add_item

 L. 130       376  LOAD_GLOBAL              Form

 L. 131       378  LOAD_FAST                'action_url'

 L. 132       380  LOAD_DEREF               'model'
              382  LOAD_METHOD              class_snake_case_name
              384  CALL_METHOD_0         0  ''
              386  FORMAT_VALUE          0  ''
              388  LOAD_STR                 '_create'
              390  BUILD_STRING_2        2 

 L. 133       392  LOAD_GLOBAL              Button
              394  LOAD_STR                 'افزودن'
              396  LOAD_CONST               ('text',)
              398  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 134       400  LOAD_FAST                'created'
          402_404  POP_JUMP_IF_FALSE   410  'to 410'
              406  LOAD_CONST               False
              408  JUMP_FORWARD        412  'to 412'
            410_0  COME_FROM           402  '402'
              410  LOAD_CONST               True
            412_0  COME_FROM           408  '408'

 L. 130       412  LOAD_CONST               ('action_url', 'name', 'button', 'disabled')
              414  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              416  LOAD_METHOD              add_items

 L. 135       418  LOAD_DEREF               'model'
              420  LOAD_ATTR                panel_create_form_items

 L. 136       422  LOAD_FAST                'related_field_name'
              424  LOAD_GLOBAL              str
              426  LOAD_FAST                'created'
              428  CALL_FUNCTION_1       1  ''
              430  BUILD_TUPLE_2         2 
              432  BUILD_LIST_1          1 

 L. 137       434  LOAD_FAST                'related_field_name'
              436  BUILD_LIST_1          1 

 L. 135       438  LOAD_CONST               ('values_list', 'disabled_list')
              440  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 130       442  CALL_METHOD_1         1  ''

 L. 129       444  CALL_METHOD_1         1  ''

 L. 114       446  CALL_METHOD_1         1  ''

 L. 110       448  LOAD_CONST               ('header', 'body')
              450  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 109       452  CALL_METHOD_1         1  ''

 L. 108       454  CALL_METHOD_1         1  ''
              456  CALL_METHOD_1         1  ''
              458  POP_TOP          
              460  JUMP_BACK           182  'to 182'

 L. 144       462  LOAD_GLOBAL              current_request
              464  LOAD_STR                 'request'
              466  BINARY_SUBSCR    
              468  LOAD_ATTR                method
              470  LOAD_STR                 'POST'
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   920  'to 920'

 L. 145       478  LOAD_GLOBAL              current_request
              480  LOAD_STR                 'request'
              482  BINARY_SUBSCR    
              484  LOAD_ATTR                GET
              486  LOAD_METHOD              get
              488  LOAD_STR                 'on'
              490  CALL_METHOD_1         1  ''
          492_494  POP_JUMP_IF_TRUE    632  'to 632'

 L. 146       496  BUILD_MAP_0           0 
              498  STORE_FAST               'data'

 L. 147       500  LOAD_GLOBAL              current_request
              502  LOAD_STR                 'request'
              504  BINARY_SUBSCR    
              506  LOAD_ATTR                data
              508  LOAD_METHOD              items
              510  CALL_METHOD_0         0  ''
              512  GET_ITER         
            514_0  COME_FROM           540  '540'
              514  FOR_ITER            578  'to 578'
              516  UNPACK_SEQUENCE_2     2 
              518  STORE_FAST               'key'
              520  STORE_FAST               'value'

 L. 148       522  LOAD_FAST                'key'
              524  LOAD_METHOD              startswith
              526  LOAD_FAST                'cls'
              528  LOAD_ATTR                panel_view
              530  LOAD_ATTR                form
              532  LOAD_ATTR                name
              534  LOAD_STR                 '__'
              536  BINARY_ADD       
              538  CALL_METHOD_1         1  ''
          540_542  POP_JUMP_IF_FALSE   514  'to 514'

 L. 149       544  LOAD_FAST                'value'
              546  LOAD_FAST                'data'
              548  LOAD_FAST                'key'
              550  LOAD_GLOBAL              len
              552  LOAD_FAST                'cls'
              554  LOAD_ATTR                panel_view
              556  LOAD_ATTR                form
              558  LOAD_ATTR                name
              560  CALL_FUNCTION_1       1  ''
              562  LOAD_CONST               2
              564  BINARY_ADD       
              566  LOAD_CONST               None
              568  BUILD_SLICE_2         2 
              570  BINARY_SUBSCR    
              572  STORE_SUBSCR     
          574_576  JUMP_BACK           514  'to 514'

 L. 151       578  LOAD_FAST                'edit_mode'
          580_582  POP_JUMP_IF_FALSE   608  'to 608'

 L. 152       584  LOAD_FAST                'created'
              586  LOAD_ATTR                panel_edit_method
              588  BUILD_TUPLE_0         0 

 L. 153       590  LOAD_FAST                'cls'
              592  LOAD_ATTR                panel_view
              594  LOAD_ATTR                form
              596  LOAD_METHOD              parse
              598  LOAD_FAST                'data'
              600  CALL_METHOD_1         1  ''

 L. 152       602  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              604  STORE_FAST               'created'
              606  JUMP_FORWARD        630  'to 630'
            608_0  COME_FROM           580  '580'

 L. 156       608  LOAD_FAST                'cls'
              610  LOAD_ATTR                panel_create_method
              612  BUILD_TUPLE_0         0 

 L. 157       614  LOAD_FAST                'cls'
              616  LOAD_ATTR                panel_view
              618  LOAD_ATTR                form
              620  LOAD_METHOD              parse
              622  LOAD_FAST                'data'
              624  CALL_METHOD_1         1  ''

 L. 156       626  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              628  STORE_FAST               'created'
            630_0  COME_FROM           606  '606'
              630  JUMP_FORWARD        814  'to 814'
            632_0  COME_FROM           492  '492'

 L. 160       632  LOAD_FAST                'cls'
              634  LOAD_METHOD              panel_create_related_model_find

 L. 161       636  LOAD_GLOBAL              current_request
              638  LOAD_STR                 'request'
              640  BINARY_SUBSCR    
              642  LOAD_ATTR                GET
              644  LOAD_METHOD              get
              646  LOAD_STR                 'on'
              648  CALL_METHOD_1         1  ''

 L. 160       650  CALL_METHOD_1         1  ''
              652  UNPACK_SEQUENCE_2     2 
              654  STORE_FAST               'related_model'
              656  STORE_FAST               'related_field'

 L. 163       658  LOAD_FAST                'related_field'

 L. 163       660  LOAD_FAST                'created'

 L. 162       662  BUILD_MAP_1           1 
              664  STORE_FAST               'data'

 L. 165       666  LOAD_FAST                'related_model'
              668  LOAD_METHOD              class_snake_case_name
              670  CALL_METHOD_0         0  ''
              672  LOAD_STR                 '_create__'
              674  BINARY_ADD       
              676  STORE_FAST               'start'

 L. 166       678  LOAD_GLOBAL              current_request
              680  LOAD_STR                 'request'
              682  BINARY_SUBSCR    
              684  LOAD_ATTR                data
              686  LOAD_METHOD              items
              688  CALL_METHOD_0         0  ''
              690  GET_ITER         
            692_0  COME_FROM           708  '708'
              692  FOR_ITER            736  'to 736'
              694  UNPACK_SEQUENCE_2     2 
              696  STORE_FAST               'key'
              698  STORE_FAST               'value'

 L. 167       700  LOAD_FAST                'key'
              702  LOAD_METHOD              startswith
              704  LOAD_FAST                'start'
              706  CALL_METHOD_1         1  ''
          708_710  POP_JUMP_IF_FALSE   692  'to 692'

 L. 168       712  LOAD_FAST                'value'
              714  LOAD_FAST                'data'
              716  LOAD_FAST                'key'
              718  LOAD_GLOBAL              len
              720  LOAD_FAST                'start'
              722  CALL_FUNCTION_1       1  ''
              724  LOAD_CONST               None
              726  BUILD_SLICE_2         2 
              728  BINARY_SUBSCR    
              730  STORE_SUBSCR     
          732_734  JUMP_BACK           692  'to 692'

 L. 169       736  LOAD_GLOBAL              current_request
              738  LOAD_STR                 'request'
              740  BINARY_SUBSCR    
              742  LOAD_ATTR                FILES
              744  LOAD_METHOD              items
              746  CALL_METHOD_0         0  ''
              748  GET_ITER         
            750_0  COME_FROM           766  '766'
              750  FOR_ITER            802  'to 802'
              752  UNPACK_SEQUENCE_2     2 
              754  STORE_FAST               'key'
              756  STORE_FAST               'value'

 L. 170       758  LOAD_FAST                'key'
              760  LOAD_METHOD              startswith
              762  LOAD_FAST                'start'
              764  CALL_METHOD_1         1  ''
          766_768  POP_JUMP_IF_FALSE   750  'to 750'

 L. 171       770  LOAD_GLOBAL              Image
              772  LOAD_ATTR                image_from_in_memory_upload
              774  LOAD_FAST                'value'
              776  LOAD_CONST               ('file',)
              778  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              780  LOAD_FAST                'data'
              782  LOAD_FAST                'key'
              784  LOAD_GLOBAL              len
              786  LOAD_FAST                'start'
              788  CALL_FUNCTION_1       1  ''
              790  LOAD_CONST               None
              792  BUILD_SLICE_2         2 
              794  BINARY_SUBSCR    
              796  STORE_SUBSCR     
          798_800  JUMP_BACK           750  'to 750'

 L. 172       802  LOAD_FAST                'related_model'
              804  LOAD_ATTR                create
              806  BUILD_TUPLE_0         0 
              808  LOAD_FAST                'data'
              810  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              812  STORE_FAST               'related_created'
            814_0  COME_FROM           630  '630'

 L. 174       814  LOAD_STR                 '/'
              816  LOAD_GLOBAL              get_avishan_config
              818  CALL_FUNCTION_0       0  ''
              820  LOAD_ATTR                PANEL_ROOT
              822  FORMAT_VALUE          0  ''
              824  LOAD_STR                 '/'
              826  LOAD_FAST                'cls'
              828  LOAD_METHOD              class_plural_snake_case_name
              830  CALL_METHOD_0         0  ''
              832  FORMAT_VALUE          0  ''
              834  LOAD_STR                 '/'
              836  BUILD_STRING_5        5 
              838  STORE_FAST               'redirect_link'

 L. 175       840  LOAD_GLOBAL              len
              842  LOAD_FAST                'related_forms'
              844  CALL_FUNCTION_1       1  ''
              846  LOAD_CONST               0
              848  COMPARE_OP               ==
          850_852  POP_JUMP_IF_FALSE   872  'to 872'

 L. 176       854  LOAD_FAST                'redirect_link'
              856  LOAD_FAST                'created'
              858  LOAD_ATTR                id
              860  FORMAT_VALUE          0  ''
              862  LOAD_STR                 '/detail'
              864  BUILD_STRING_2        2 
              866  INPLACE_ADD      
              868  STORE_FAST               'redirect_link'
              870  JUMP_FORWARD        912  'to 912'
            872_0  COME_FROM           850  '850'

 L. 178       872  LOAD_FAST                'edit_mode'
          874_876  POP_JUMP_IF_FALSE   896  'to 896'

 L. 179       878  LOAD_FAST                'redirect_link'
              880  LOAD_FAST                'created'
              882  LOAD_ATTR                id
              884  FORMAT_VALUE          0  ''
              886  LOAD_STR                 '/edit'
              888  BUILD_STRING_2        2 
              890  INPLACE_ADD      
              892  STORE_FAST               'redirect_link'
              894  JUMP_FORWARD        912  'to 912'
            896_0  COME_FROM           874  '874'

 L. 181       896  LOAD_FAST                'redirect_link'
              898  LOAD_FAST                'created'
              900  LOAD_ATTR                id
              902  FORMAT_VALUE          0  ''
              904  LOAD_STR                 '/create'
              906  BUILD_STRING_2        2 
              908  INPLACE_ADD      
              910  STORE_FAST               'redirect_link'
            912_0  COME_FROM           894  '894'
            912_1  COME_FROM           870  '870'

 L. 182       912  LOAD_GLOBAL              redirect
              914  LOAD_FAST                'redirect_link'
              916  CALL_FUNCTION_1       1  ''
              918  RETURN_VALUE     
            920_0  COME_FROM           474  '474'

 L. 183       920  LOAD_GLOBAL              current_request
              922  LOAD_STR                 'request'
              924  BINARY_SUBSCR    
              926  LOAD_ATTR                method
              928  LOAD_STR                 'GET'
              930  COMPARE_OP               ==
          932_934  POP_JUMP_IF_FALSE  1030  'to 1030'

 L. 184       936  LOAD_FAST                'cls'
              938  LOAD_ATTR                panel_view
              940  LOAD_ATTR                contents
              942  LOAD_METHOD              append

 L. 185       944  LOAD_GLOBAL              Row
              946  CALL_FUNCTION_0       0  ''
              948  LOAD_METHOD              add_item

 L. 186       950  LOAD_GLOBAL              Col
              952  LOAD_CONST               6
              954  LOAD_CONST               6
              956  LOAD_CONST               12
              958  LOAD_CONST               ('large', 'extra_large', 'medium')
              960  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              962  LOAD_METHOD              add_item

 L. 187       964  LOAD_GLOBAL              Card

 L. 188       966  LOAD_GLOBAL              CardHeader

 L. 190       968  LOAD_FAST                'edit_mode'

 L. 189   970_972  POP_JUMP_IF_FALSE   982  'to 982'
              974  LOAD_FAST                'created'
              976  LOAD_METHOD              panel_edit_form_buttons
              978  CALL_METHOD_0         0  ''
              980  JUMP_FORWARD        988  'to 988'
            982_0  COME_FROM           970  '970'

 L. 191       982  LOAD_FAST                'cls'
              984  LOAD_METHOD              panel_create_form_buttons
              986  CALL_METHOD_0         0  ''
            988_0  COME_FROM           980  '980'

 L. 192       988  LOAD_FAST                'cls'
              990  LOAD_METHOD              panel_name
              992  CALL_METHOD_0         0  ''

 L. 188       994  LOAD_CONST               ('buttons', 'title')
              996  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 194       998  LOAD_FAST                'cls'
             1000  LOAD_ATTR                panel_view
             1002  LOAD_ATTR                form

 L. 187      1004  LOAD_CONST               ('header', 'body')
             1006  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 186      1008  CALL_METHOD_1         1  ''

 L. 185      1010  CALL_METHOD_1         1  ''

 L. 184      1012  CALL_METHOD_1         1  ''
             1014  POP_TOP          

 L. 199      1016  LOAD_FAST                'cls'
             1018  LOAD_ATTR                panel_view
             1020  LOAD_ATTR                contents
             1022  LOAD_METHOD              extend
             1024  LOAD_FAST                'related_forms'
             1026  CALL_METHOD_1         1  ''
             1028  POP_TOP          
           1030_0  COME_FROM           932  '932'

Parse error at or near `COME_FROM' instruction at offset 144_1

    def panel_detail(self: Union[(AvishanModel, 'AvishanModelPanelEnabled')]):
        from avishan.views.panel_views import AvishanPanelModelPage
        self
        self.panel_view.page_header_text = f"جزئیات {self.panel_name}"
        self.panel_view.contents.append(Row.add_item(Col(extra_large=6, large=6, medium=12).add_item(self.panel_detail_main_card)))

    def panel_edit(self):
        return self.panel_create(edit_mode=True)

    def panel_delete(self):
        pass

    @classmethod
    def panel_name(cls):
        raise NotImplementedError

    @classmethod
    def panel_plural_name(cls):
        raise NotImplementedError

    @classmethod
    def panel_list_title_items(cls) -> List[Tuple[(str, str)]]:
        return [(
         item,
         cls.panel_translator(item)) for item in cls.panel_list_title_keys]

    @classmethod
    def panel_list_title_keys(cls) -> List[str]:
        return ['id']

    @classmethod
    def panel_list_items(cls) -> List[TableItem]:
        items = []
        for item in cls.panel_list_items_filter:
            items.append(TableItem(data_dict=(item.panel_item_data_dict)))
        else:
            return items

    def panel_item_data_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def panel_list_items_filter(cls: AvishanModel) -> QuerySet:
        return cls.objects.all

    @classmethod
    def panel_list_header_buttons(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')]) -> List[Button]:
        buttons = []
        if cls.panel_model_create_enable:
            buttons.append(Button(text='ایجاد',
              link=f"/{get_avishan_config.PANEL_ROOT}/{cls.class_plural_snake_case_name}/create"))
        return buttons

    @classmethod
    def panel_model_create_enable(cls) -> bool:
        return True

    @classmethod
    def panel_create_method(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')], **kwargs):
        return (cls.create)(**kwargs)

    @classmethod
    def panel_create_form_buttons(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')]) -> List[Button]:
        return [
         Button(text='بازگشت',
           link=f"/{get_avishan_config.PANEL_ROOT}/{cls.class_plural_snake_case_name}",
           added_classes='btn-default')]

    @classmethod
    def panel_create_form_fields(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')]) -> List[models.Field]:
        fields = []
        for field in cls.get_fields:
            if cls.is_field_readonly(field):
                pass
            else:
                fields.append(field)
        else:
            return fields

    @classmethod
    def panel_create_form_items(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')], item: Union[(AvishanModel, 'AvishanModelPanelEnabled')]=None, values_list: List[Tuple[(str, str)]]=(), disabled_list: List[str]=()) -> List[FormElement]:
        items = []
        for field in cls.panel_create_form_fields:
            element_value = item.__getattribute__(field.name) if item else ''
            for name, value in values_list:
                if field.name == name:
                    element_value = value
                if isinstance(field, models.ForeignKey) and field.related_model in (Image, File):
                    form_element = FileChooseFormElement(name=(field.name),
                      label=(cls.panel_translator(field.name)),
                      disabled=(True if field.name in disabled_list else False))
                else:
                    form_element = InputFormElement(name=(field.name),
                      label=(cls.panel_translator(field.name)),
                      value=element_value,
                      disabled=(True if field.name in disabled_list else False))
                items.append(form_element)
            else:
                return items

    @classmethod
    def panel_create_related_models(cls) -> List[Tuple[(Union[(Type[AvishanModel], 'AvishanModelPanelEnabled')], str)]]:
        return []

    @classmethod
    def panel_create_related_model_find(cls, model_name: str) -> Optional[Tuple[(Type[AvishanModel], str)]]:
        for model, related_field in cls.panel_create_related_models:
            if model.class_name == model_name:
                return (
                 model, related_field)

    @classmethod
    def panel_translator--- This code section failed: ---

 L. 327         0  SETUP_FINALLY        20  'to 20'

 L. 328         2  LOAD_FAST                'cls'
                4  LOAD_METHOD              panel_translator_dict
                6  CALL_METHOD_0         0  ''
                8  LOAD_FAST                'text'
               10  LOAD_METHOD              lower
               12  CALL_METHOD_0         0  ''
               14  BINARY_SUBSCR    
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L. 329        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    42  'to 42'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 330        34  LOAD_FAST                'text'
               36  ROT_FOUR         
               38  POP_EXCEPT       
               40  RETURN_VALUE     
             42_0  COME_FROM            26  '26'
               42  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 30

    @classmethod
    def panel_translator_dict(cls) -> dict:
        return {**{'id':'شناسه', 
         'title':'عنوان', 
         'order':'ترتیب', 
         'image':'عکس', 
         'text':'متن', 
         'parking':'پارکینگ'}, **(get_avishan_config.PANEL_TRANSLATION_DICT)}

    def panel_detail_buttons(self: Union[(AvishanModel, 'AvishanModelPanelEnabled')]) -> List[Button]:
        buttons = []
        if self.panel_edit_model_enable:
            buttons.append(Button(text='ویرایش',
              link=f"/{get_avishan_config.PANEL_ROOT}/{self.class_plural_snake_case_name}/{self.id}/edit",
              added_classes='btn-success'))
        buttons.append(Button(text='بازگشت',
          link=f"/{get_avishan_config.PANEL_ROOT}/{self.class_plural_snake_case_name}",
          added_classes='btn-default'))
        return buttons

    def panel_detail_items(self):
        items = []
        for name in self.panel_detail_keys:
            if inspect.ismethod(self.__getattribute__(name)):
                value = self.__getattribute__(name)
            else:
                value = self.__getattribute__(name)
            items.append((self.panel_translator(name), value))
        else:
            return items

    @classmethod
    def panel_detail_related_models(cls) -> List[Tuple[(Union[(Type[AvishanModel], 'AvishanModelPanelEnabled')], str)]]:
        return []

    @classmethod
    def panel_detail_keys(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')]):
        return [field.name for field in cls.get_fields]

    def panel_detail_main_card(self) -> Card:
        card = Card(header=CardHeader(buttons=(self.panel_detail_buttons)))
        if len(self.panel_detail_main_card_items) == 1:
            card.body = self.panel_detail_main_card_items[0]
        else:
            for tab in self.panel_detail_main_card_items:
                card.add_tab(tab)
            else:
                return card

    def panel_detail_main_card_items(self) -> Union[List[DivComponent]]:
        return [DataList.add_items(self.panel_detail_items)]

    @classmethod
    def panel_edit_model_enable(cls) -> bool:
        return True

    def panel_edit_method(self: Union[(AvishanModel, 'AvishanModelPanelEnabled')], **kwargs):
        return (self.update)(**kwargs)

    def panel_edit_form_buttons(self: Union[(AvishanModel, 'AvishanModelPanelEnabled')]) -> List[Button]:
        return [
         Button(text='بازگشت',
           link=f"/{get_avishan_config.PANEL_ROOT}/{self.class_plural_snake_case_name}/{self.id}/detail",
           added_classes='btn-default')]