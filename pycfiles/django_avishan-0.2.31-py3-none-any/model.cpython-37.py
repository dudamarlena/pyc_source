# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/parkners_new/avishan/libraries/admin_lte/model.py
# Compiled at: 2020-03-23 05:56:12
# Size of source mod 2**32: 15893 bytes
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
    def call_panel_model_function(cls: AvishanModel, model_function_name: str):
        try:
            return getattr(cls, 'panel_' + model_function_name)()
        except AttributeError:
            raise ErrorMessageException(AvishanTranslatable(EN=f'Model {cls.class_name()} should have a function with name "panel_{model_function_name}"'))

    def call_panel_item_function(self: AvishanModel, model_function_name: str):
        try:
            return getattr(self, 'panel_' + model_function_name)()
        except AttributeError:
            raise ErrorMessageException(AvishanTranslatable(EN=f'Model {self.class_name()} should have a function with name "panel_{model_function_name}"'))

    @classmethod
    def panel_list(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')]):
        from avishan.views.panel_views import AvishanPanelModelPage
        cls
        cls.panel_view.page_header_text = cls.panel_plural_name()
        cls.panel_view.contents.append(Row().add_item(Col(12).add_item(Card(header=CardHeader(buttons=(cls.panel_list_header_buttons())),
          body=Table(heads=[TableHead(name=(item[0]), title=(item[1])) for item in cls.panel_list_title_items()],
          link_head_key='id',
          link_prepend=f"/{get_avishan_config().PANEL_ROOT}/{cls.class_plural_snake_case_name()}/",
          link_append='/detail').add_items(items=(cls.panel_list_items())),
          body_added_classes='table-responsive p-0'))))

    @classmethod
    def panel_create--- This code section failed: ---

 L.  74         0  LOAD_CONST               0
                2  LOAD_CONST               ('AvishanPanelModelPage',)
                4  IMPORT_NAME_ATTR         avishan.views.panel_views
                6  IMPORT_FROM              AvishanPanelModelPage
                8  STORE_FAST               'AvishanPanelModelPage'
               10  POP_TOP          

 L.  75        12  LOAD_FAST                'cls'
               14  POP_TOP          

 L.  76        16  LOAD_FAST                'edit_mode'
               18  POP_JUMP_IF_FALSE    24  'to 24'
               20  LOAD_STR                 'ویرایش'
               22  JUMP_FORWARD         26  'to 26'
             24_0  COME_FROM            18  '18'
               24  LOAD_STR                 'ایجاد'
             26_0  COME_FROM            22  '22'
               26  LOAD_STR                 ' '
               28  LOAD_FAST                'cls'
               30  LOAD_METHOD              panel_name
               32  CALL_METHOD_0         0  '0 positional arguments'
               34  FORMAT_VALUE          0  ''
               36  BUILD_STRING_2        2 
               38  BINARY_ADD       
               40  LOAD_FAST                'cls'
               42  LOAD_ATTR                panel_view
               44  STORE_ATTR               page_header_text

 L.  77        46  LOAD_FAST                'cls'
               48  LOAD_ATTR                panel_view
               50  LOAD_ATTR                item
               52  STORE_FAST               'created'

 L.  78        54  LOAD_STR                 '/'
               56  LOAD_GLOBAL              get_avishan_config
               58  CALL_FUNCTION_0       0  '0 positional arguments'
               60  LOAD_ATTR                PANEL_ROOT
               62  FORMAT_VALUE          0  ''
               64  LOAD_STR                 '/'
               66  LOAD_FAST                'cls'
               68  LOAD_METHOD              class_plural_snake_case_name
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  FORMAT_VALUE          0  ''
               74  LOAD_STR                 '/'
               76  BUILD_STRING_5        5 
               78  STORE_FAST               'action_url'

 L.  79        80  LOAD_FAST                'edit_mode'
               82  POP_JUMP_IF_FALSE   102  'to 102'

 L.  80        84  LOAD_FAST                'action_url'
               86  LOAD_FAST                'created'
               88  LOAD_ATTR                id
               90  FORMAT_VALUE          0  ''
               92  LOAD_STR                 '/edit'
               94  BUILD_STRING_2        2 
               96  INPLACE_ADD      
               98  STORE_FAST               'action_url'
              100  JUMP_FORWARD        110  'to 110'
            102_0  COME_FROM            82  '82'

 L.  82       102  LOAD_FAST                'action_url'
              104  LOAD_STR                 'create'
              106  INPLACE_ADD      
              108  STORE_FAST               'action_url'
            110_0  COME_FROM           100  '100'

 L.  83       110  LOAD_GLOBAL              Form

 L.  84       112  LOAD_FAST                'action_url'

 L.  85       114  LOAD_STR                 'create'

 L.  86       116  LOAD_GLOBAL              Button
              118  LOAD_FAST                'edit_mode'
              120  POP_JUMP_IF_FALSE   126  'to 126'
              122  LOAD_STR                 'ویرایش'
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           120  '120'
              126  LOAD_STR                 'ایجاد'
            128_0  COME_FROM           124  '124'
              128  LOAD_CONST               ('text',)
              130  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L.  87       132  LOAD_FAST                'edit_mode'
              134  POP_JUMP_IF_TRUE    144  'to 144'
              136  LOAD_FAST                'created'
              138  POP_JUMP_IF_FALSE   144  'to 144'
              140  LOAD_CONST               True
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM           138  '138'
            144_1  COME_FROM           134  '134'
              144  LOAD_CONST               False
            146_0  COME_FROM           142  '142'
              146  LOAD_CONST               ('action_url', 'name', 'button', 'disabled')
              148  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              150  LOAD_METHOD              add_items

 L.  88       152  LOAD_FAST                'cls'
              154  LOAD_ATTR                panel_create_form_items
              156  LOAD_FAST                'created'
              158  LOAD_CONST               ('item',)
              160  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              162  CALL_METHOD_1         1  '1 positional argument'
              164  LOAD_FAST                'cls'
              166  LOAD_ATTR                panel_view
              168  STORE_ATTR               form

 L.  90       170  BUILD_LIST_0          0 
              172  STORE_FAST               'related_forms'

 L.  91   174_176  SETUP_LOOP          470  'to 470'
              178  LOAD_FAST                'cls'
              180  LOAD_METHOD              panel_create_related_models
              182  CALL_METHOD_0         0  '0 positional arguments'
              184  GET_ITER         
          186_188  FOR_ITER            468  'to 468'
              190  UNPACK_SEQUENCE_2     2 
              192  STORE_DEREF              'model'
              194  STORE_FAST               'related_field_name'

 L.  92       196  LOAD_CONST               0
              198  STORE_FAST               'created_id'

 L.  93       200  LOAD_FAST                'created'
              202  POP_JUMP_IF_FALSE   210  'to 210'

 L.  94       204  LOAD_FAST                'created'
              206  LOAD_ATTR                id
              208  STORE_FAST               'created_id'
            210_0  COME_FROM           202  '202'

 L.  96       210  LOAD_STR                 '/'
              212  LOAD_GLOBAL              get_avishan_config
              214  CALL_FUNCTION_0       0  '0 positional arguments'
              216  LOAD_ATTR                PANEL_ROOT
              218  FORMAT_VALUE          0  ''
              220  LOAD_STR                 '/'
              222  LOAD_FAST                'cls'
              224  LOAD_METHOD              class_plural_snake_case_name
              226  CALL_METHOD_0         0  '0 positional arguments'
              228  FORMAT_VALUE          0  ''
              230  LOAD_STR                 '/'
              232  LOAD_FAST                'created_id'
              234  FORMAT_VALUE          0  ''
              236  LOAD_STR                 '/'
              238  BUILD_STRING_7        7 
              240  STORE_FAST               'action_url'

 L.  98       242  LOAD_FAST                'edit_mode'
          244_246  POP_JUMP_IF_FALSE   258  'to 258'

 L.  99       248  LOAD_FAST                'action_url'
              250  LOAD_STR                 'edit'
              252  INPLACE_ADD      
              254  STORE_FAST               'action_url'
              256  JUMP_FORWARD        266  'to 266'
            258_0  COME_FROM           244  '244'

 L. 101       258  LOAD_FAST                'action_url'
              260  LOAD_STR                 'create'
              262  INPLACE_ADD      
              264  STORE_FAST               'action_url'
            266_0  COME_FROM           256  '256'

 L. 102       266  LOAD_FAST                'action_url'
              268  LOAD_STR                 '?on='
              270  LOAD_DEREF               'model'
              272  LOAD_METHOD              class_name
              274  CALL_METHOD_0         0  '0 positional arguments'
              276  FORMAT_VALUE          0  ''
              278  BUILD_STRING_2        2 
              280  INPLACE_ADD      
              282  STORE_FAST               'action_url'

 L. 104       284  LOAD_FAST                'related_forms'
              286  LOAD_METHOD              append
              288  LOAD_GLOBAL              Row
              290  CALL_FUNCTION_0       0  '0 positional arguments'
              292  LOAD_METHOD              add_item

 L. 105       294  LOAD_GLOBAL              Col
              296  LOAD_CONST               6
              298  CALL_FUNCTION_1       1  '1 positional argument'
              300  LOAD_METHOD              add_item

 L. 106       302  LOAD_GLOBAL              Card

 L. 107       304  LOAD_GLOBAL              CardHeader

 L. 108       306  LOAD_DEREF               'model'
              308  LOAD_METHOD              panel_plural_name
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  LOAD_CONST               ('title',)
              314  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 110       316  LOAD_GLOBAL              Row
              318  CALL_FUNCTION_0       0  '0 positional arguments'
              320  LOAD_METHOD              add_item

 L. 113       322  LOAD_GLOBAL              Col
              324  LOAD_CONST               12
              326  CALL_FUNCTION_1       1  '1 positional argument'
              328  LOAD_METHOD              add_item

 L. 114       330  LOAD_GLOBAL              UnorderedList
              332  CALL_FUNCTION_0       0  '0 positional arguments'
              334  LOAD_METHOD              add_items

 L. 115       336  LOAD_CLOSURE             'model'
              338  BUILD_TUPLE_1         1 
              340  LOAD_LISTCOMP            '<code_object <listcomp>>'
              342  LOAD_STR                 'AvishanModelPanelEnabled.panel_create.<locals>.<listcomp>'
              344  MAKE_FUNCTION_8          'closure'

 L. 119       346  LOAD_DEREF               'model'
              348  LOAD_ATTR                objects
              350  LOAD_ATTR                filter
              352  BUILD_TUPLE_0         0 

 L. 120       354  LOAD_FAST                'related_field_name'
              356  LOAD_FAST                'created'
              358  BUILD_MAP_1           1 
              360  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              362  GET_ITER         
              364  CALL_FUNCTION_1       1  '1 positional argument'
              366  CALL_METHOD_1         1  '1 positional argument'
              368  CALL_METHOD_1         1  '1 positional argument'
              370  CALL_METHOD_1         1  '1 positional argument'
              372  LOAD_METHOD              add_item

 L. 125       374  LOAD_GLOBAL              Col
              376  LOAD_CONST               12
              378  CALL_FUNCTION_1       1  '1 positional argument'
              380  LOAD_METHOD              add_item

 L. 126       382  LOAD_GLOBAL              Form

 L. 127       384  LOAD_FAST                'action_url'

 L. 128       386  LOAD_DEREF               'model'
              388  LOAD_METHOD              class_snake_case_name
              390  CALL_METHOD_0         0  '0 positional arguments'
              392  FORMAT_VALUE          0  ''
              394  LOAD_STR                 '_create'
              396  BUILD_STRING_2        2 

 L. 129       398  LOAD_GLOBAL              Button
              400  LOAD_STR                 'افزودن'
              402  LOAD_CONST               ('text',)
              404  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 130       406  LOAD_FAST                'created'
          408_410  POP_JUMP_IF_FALSE   416  'to 416'
              412  LOAD_CONST               False
              414  JUMP_FORWARD        418  'to 418'
            416_0  COME_FROM           408  '408'
              416  LOAD_CONST               True
            418_0  COME_FROM           414  '414'
              418  LOAD_CONST               ('action_url', 'name', 'button', 'disabled')
              420  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              422  LOAD_METHOD              add_items

 L. 131       424  LOAD_DEREF               'model'
              426  LOAD_ATTR                panel_create_form_items

 L. 132       428  LOAD_FAST                'related_field_name'
              430  LOAD_GLOBAL              str
              432  LOAD_FAST                'created'
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  BUILD_TUPLE_2         2 
              438  BUILD_LIST_1          1 

 L. 133       440  LOAD_FAST                'related_field_name'
              442  BUILD_LIST_1          1 
              444  LOAD_CONST               ('values_list', 'disabled_list')
              446  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              448  CALL_METHOD_1         1  '1 positional argument'
              450  CALL_METHOD_1         1  '1 positional argument'
              452  CALL_METHOD_1         1  '1 positional argument'
              454  LOAD_CONST               ('header', 'body')
              456  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              458  CALL_METHOD_1         1  '1 positional argument'
              460  CALL_METHOD_1         1  '1 positional argument'
              462  CALL_METHOD_1         1  '1 positional argument'
              464  POP_TOP          
              466  JUMP_BACK           186  'to 186'
              468  POP_BLOCK        
            470_0  COME_FROM_LOOP      174  '174'

 L. 140       470  LOAD_GLOBAL              current_request
              472  LOAD_STR                 'request'
              474  BINARY_SUBSCR    
              476  LOAD_ATTR                method
              478  LOAD_STR                 'POST'
              480  COMPARE_OP               ==
          482_484  POP_JUMP_IF_FALSE   940  'to 940'

 L. 141       486  LOAD_GLOBAL              current_request
              488  LOAD_STR                 'request'
              490  BINARY_SUBSCR    
              492  LOAD_ATTR                GET
              494  LOAD_METHOD              get
              496  LOAD_STR                 'on'
              498  CALL_METHOD_1         1  '1 positional argument'
          500_502  POP_JUMP_IF_TRUE    644  'to 644'

 L. 142       504  BUILD_MAP_0           0 
              506  STORE_FAST               'data'

 L. 143       508  SETUP_LOOP          590  'to 590'
              510  LOAD_GLOBAL              current_request
              512  LOAD_STR                 'request'
              514  BINARY_SUBSCR    
              516  LOAD_ATTR                data
              518  LOAD_METHOD              items
              520  CALL_METHOD_0         0  '0 positional arguments'
              522  GET_ITER         
            524_0  COME_FROM           550  '550'
              524  FOR_ITER            588  'to 588'
              526  UNPACK_SEQUENCE_2     2 
              528  STORE_FAST               'key'
              530  STORE_FAST               'value'

 L. 144       532  LOAD_FAST                'key'
              534  LOAD_METHOD              startswith
              536  LOAD_FAST                'cls'
              538  LOAD_ATTR                panel_view
              540  LOAD_ATTR                form
              542  LOAD_ATTR                name
              544  LOAD_STR                 '__'
              546  BINARY_ADD       
              548  CALL_METHOD_1         1  '1 positional argument'
          550_552  POP_JUMP_IF_FALSE   524  'to 524'

 L. 145       554  LOAD_FAST                'value'
              556  LOAD_FAST                'data'
              558  LOAD_FAST                'key'
              560  LOAD_GLOBAL              len
              562  LOAD_FAST                'cls'
              564  LOAD_ATTR                panel_view
              566  LOAD_ATTR                form
              568  LOAD_ATTR                name
              570  CALL_FUNCTION_1       1  '1 positional argument'
              572  LOAD_CONST               2
              574  BINARY_ADD       
              576  LOAD_CONST               None
              578  BUILD_SLICE_2         2 
              580  BINARY_SUBSCR    
              582  STORE_SUBSCR     
          584_586  JUMP_BACK           524  'to 524'
              588  POP_BLOCK        
            590_0  COME_FROM_LOOP      508  '508'

 L. 147       590  LOAD_FAST                'edit_mode'
          592_594  POP_JUMP_IF_FALSE   620  'to 620'

 L. 148       596  LOAD_FAST                'created'
              598  LOAD_ATTR                panel_edit_method
              600  BUILD_TUPLE_0         0 

 L. 149       602  LOAD_FAST                'cls'
              604  LOAD_ATTR                panel_view
              606  LOAD_ATTR                form
              608  LOAD_METHOD              parse
              610  LOAD_FAST                'data'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              616  STORE_FAST               'created'
              618  JUMP_FORWARD        642  'to 642'
            620_0  COME_FROM           592  '592'

 L. 152       620  LOAD_FAST                'cls'
              622  LOAD_ATTR                panel_create_method
              624  BUILD_TUPLE_0         0 

 L. 153       626  LOAD_FAST                'cls'
              628  LOAD_ATTR                panel_view
              630  LOAD_ATTR                form
              632  LOAD_METHOD              parse
              634  LOAD_FAST                'data'
              636  CALL_METHOD_1         1  '1 positional argument'
              638  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              640  STORE_FAST               'created'
            642_0  COME_FROM           618  '618'
              642  JUMP_FORWARD        834  'to 834'
            644_0  COME_FROM           500  '500'

 L. 156       644  LOAD_FAST                'cls'
              646  LOAD_METHOD              panel_create_related_model_find

 L. 157       648  LOAD_GLOBAL              current_request
              650  LOAD_STR                 'request'
              652  BINARY_SUBSCR    
              654  LOAD_ATTR                GET
              656  LOAD_METHOD              get
              658  LOAD_STR                 'on'
              660  CALL_METHOD_1         1  '1 positional argument'
              662  CALL_METHOD_1         1  '1 positional argument'
              664  UNPACK_SEQUENCE_2     2 
              666  STORE_FAST               'related_model'
              668  STORE_FAST               'related_field'

 L. 159       670  LOAD_FAST                'related_field'
              672  LOAD_FAST                'created'
              674  BUILD_MAP_1           1 
              676  STORE_FAST               'data'

 L. 161       678  LOAD_FAST                'related_model'
              680  LOAD_METHOD              class_snake_case_name
              682  CALL_METHOD_0         0  '0 positional arguments'
              684  LOAD_STR                 '_create__'
              686  BINARY_ADD       
              688  STORE_FAST               'start'

 L. 162       690  SETUP_LOOP          752  'to 752'
              692  LOAD_GLOBAL              current_request
              694  LOAD_STR                 'request'
              696  BINARY_SUBSCR    
              698  LOAD_ATTR                data
              700  LOAD_METHOD              items
              702  CALL_METHOD_0         0  '0 positional arguments'
              704  GET_ITER         
            706_0  COME_FROM           722  '722'
              706  FOR_ITER            750  'to 750'
              708  UNPACK_SEQUENCE_2     2 
              710  STORE_FAST               'key'
              712  STORE_FAST               'value'

 L. 163       714  LOAD_FAST                'key'
              716  LOAD_METHOD              startswith
              718  LOAD_FAST                'start'
              720  CALL_METHOD_1         1  '1 positional argument'
          722_724  POP_JUMP_IF_FALSE   706  'to 706'

 L. 164       726  LOAD_FAST                'value'
              728  LOAD_FAST                'data'
              730  LOAD_FAST                'key'
              732  LOAD_GLOBAL              len
              734  LOAD_FAST                'start'
              736  CALL_FUNCTION_1       1  '1 positional argument'
              738  LOAD_CONST               None
              740  BUILD_SLICE_2         2 
              742  BINARY_SUBSCR    
              744  STORE_SUBSCR     
          746_748  JUMP_BACK           706  'to 706'
              750  POP_BLOCK        
            752_0  COME_FROM_LOOP      690  '690'

 L. 165       752  SETUP_LOOP          822  'to 822'
              754  LOAD_GLOBAL              current_request
              756  LOAD_STR                 'request'
              758  BINARY_SUBSCR    
              760  LOAD_ATTR                FILES
              762  LOAD_METHOD              items
              764  CALL_METHOD_0         0  '0 positional arguments'
              766  GET_ITER         
            768_0  COME_FROM           784  '784'
              768  FOR_ITER            820  'to 820'
              770  UNPACK_SEQUENCE_2     2 
              772  STORE_FAST               'key'
              774  STORE_FAST               'value'

 L. 166       776  LOAD_FAST                'key'
              778  LOAD_METHOD              startswith
              780  LOAD_FAST                'start'
              782  CALL_METHOD_1         1  '1 positional argument'
          784_786  POP_JUMP_IF_FALSE   768  'to 768'

 L. 167       788  LOAD_GLOBAL              Image
              790  LOAD_ATTR                image_from_in_memory_upload
              792  LOAD_FAST                'value'
              794  LOAD_CONST               ('file',)
              796  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              798  LOAD_FAST                'data'
              800  LOAD_FAST                'key'
              802  LOAD_GLOBAL              len
              804  LOAD_FAST                'start'
              806  CALL_FUNCTION_1       1  '1 positional argument'
              808  LOAD_CONST               None
              810  BUILD_SLICE_2         2 
              812  BINARY_SUBSCR    
              814  STORE_SUBSCR     
          816_818  JUMP_BACK           768  'to 768'
              820  POP_BLOCK        
            822_0  COME_FROM_LOOP      752  '752'

 L. 168       822  LOAD_FAST                'related_model'
              824  LOAD_ATTR                create
              826  BUILD_TUPLE_0         0 
              828  LOAD_FAST                'data'
              830  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              832  STORE_FAST               'related_created'
            834_0  COME_FROM           642  '642'

 L. 170       834  LOAD_STR                 '/'
              836  LOAD_GLOBAL              get_avishan_config
              838  CALL_FUNCTION_0       0  '0 positional arguments'
              840  LOAD_ATTR                PANEL_ROOT
              842  FORMAT_VALUE          0  ''
              844  LOAD_STR                 '/'
              846  LOAD_FAST                'cls'
              848  LOAD_METHOD              class_plural_snake_case_name
              850  CALL_METHOD_0         0  '0 positional arguments'
              852  FORMAT_VALUE          0  ''
              854  LOAD_STR                 '/'
              856  BUILD_STRING_5        5 
              858  STORE_FAST               'redirect_link'

 L. 171       860  LOAD_GLOBAL              len
              862  LOAD_FAST                'related_forms'
              864  CALL_FUNCTION_1       1  '1 positional argument'
              866  LOAD_CONST               0
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   892  'to 892'

 L. 172       874  LOAD_FAST                'redirect_link'
              876  LOAD_FAST                'created'
              878  LOAD_ATTR                id
              880  FORMAT_VALUE          0  ''
              882  LOAD_STR                 '/detail'
              884  BUILD_STRING_2        2 
              886  INPLACE_ADD      
              888  STORE_FAST               'redirect_link'
              890  JUMP_FORWARD        932  'to 932'
            892_0  COME_FROM           870  '870'

 L. 174       892  LOAD_FAST                'edit_mode'
          894_896  POP_JUMP_IF_FALSE   916  'to 916'

 L. 175       898  LOAD_FAST                'redirect_link'
              900  LOAD_FAST                'created'
              902  LOAD_ATTR                id
              904  FORMAT_VALUE          0  ''
              906  LOAD_STR                 '/edit'
              908  BUILD_STRING_2        2 
              910  INPLACE_ADD      
              912  STORE_FAST               'redirect_link'
              914  JUMP_FORWARD        932  'to 932'
            916_0  COME_FROM           894  '894'

 L. 177       916  LOAD_FAST                'redirect_link'
              918  LOAD_FAST                'created'
              920  LOAD_ATTR                id
              922  FORMAT_VALUE          0  ''
              924  LOAD_STR                 '/create'
              926  BUILD_STRING_2        2 
              928  INPLACE_ADD      
              930  STORE_FAST               'redirect_link'
            932_0  COME_FROM           914  '914'
            932_1  COME_FROM           890  '890'

 L. 178       932  LOAD_GLOBAL              redirect
              934  LOAD_FAST                'redirect_link'
              936  CALL_FUNCTION_1       1  '1 positional argument'
              938  RETURN_VALUE     
            940_0  COME_FROM           482  '482'

 L. 179       940  LOAD_GLOBAL              current_request
              942  LOAD_STR                 'request'
              944  BINARY_SUBSCR    
              946  LOAD_ATTR                method
              948  LOAD_STR                 'GET'
              950  COMPARE_OP               ==
          952_954  POP_JUMP_IF_FALSE  1044  'to 1044'

 L. 180       956  LOAD_FAST                'cls'
              958  LOAD_ATTR                panel_view
              960  LOAD_ATTR                contents
              962  LOAD_METHOD              append

 L. 181       964  LOAD_GLOBAL              Row
              966  CALL_FUNCTION_0       0  '0 positional arguments'
              968  LOAD_METHOD              add_item

 L. 182       970  LOAD_GLOBAL              Col
              972  LOAD_CONST               6
              974  CALL_FUNCTION_1       1  '1 positional argument'
              976  LOAD_METHOD              add_item

 L. 183       978  LOAD_GLOBAL              Card

 L. 184       980  LOAD_GLOBAL              CardHeader

 L. 186       982  LOAD_FAST                'edit_mode'
          984_986  POP_JUMP_IF_FALSE   996  'to 996'
              988  LOAD_FAST                'created'
              990  LOAD_METHOD              panel_edit_form_buttons
              992  CALL_METHOD_0         0  '0 positional arguments'
              994  JUMP_FORWARD       1002  'to 1002'
            996_0  COME_FROM           984  '984'

 L. 187       996  LOAD_FAST                'cls'
              998  LOAD_METHOD              panel_create_form_buttons
             1000  CALL_METHOD_0         0  '0 positional arguments'
           1002_0  COME_FROM           994  '994'

 L. 188      1002  LOAD_FAST                'cls'
             1004  LOAD_METHOD              panel_name
             1006  CALL_METHOD_0         0  '0 positional arguments'
             1008  LOAD_CONST               ('buttons', 'title')
             1010  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 190      1012  LOAD_FAST                'cls'
             1014  LOAD_ATTR                panel_view
             1016  LOAD_ATTR                form
             1018  LOAD_CONST               ('header', 'body')
             1020  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1022  CALL_METHOD_1         1  '1 positional argument'
             1024  CALL_METHOD_1         1  '1 positional argument'
             1026  CALL_METHOD_1         1  '1 positional argument'
             1028  POP_TOP          

 L. 195      1030  LOAD_FAST                'cls'
             1032  LOAD_ATTR                panel_view
             1034  LOAD_ATTR                contents
             1036  LOAD_METHOD              extend
             1038  LOAD_FAST                'related_forms'
             1040  CALL_METHOD_1         1  '1 positional argument'
             1042  POP_TOP          
           1044_0  COME_FROM           952  '952'

Parse error at or near `COME_FROM' instruction at offset 144_1

    def panel_detail(self: Union[(AvishanModel, 'AvishanModelPanelEnabled')]):
        from avishan.views.panel_views import AvishanPanelModelPage
        self
        self.panel_view.page_header_text = f"جزئیات {self.panel_name()}"
        self.panel_view.contents.append(Row().add_item(Col(6).add_item(Card(header=CardHeader(buttons=(self.panel_detail_buttons())),
          body=(DataList().add_items(self.panel_detail_items()))))))

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
        return [(item, cls.panel_translator(item)) for item in cls.panel_list_title_keys()]

    @classmethod
    def panel_list_title_keys(cls) -> List[str]:
        return ['id']

    @classmethod
    def panel_list_items(cls) -> List[TableItem]:
        items = []
        for item in cls.panel_list_items_filter():
            items.append(TableItem(data_dict=(item.__dict__)))

        return items

    @classmethod
    def panel_list_items_filter(cls: AvishanModel) -> QuerySet:
        return cls.objects.all()

    @classmethod
    def panel_list_header_buttons(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')]) -> List[Button]:
        buttons = []
        if cls.panel_model_create_enable():
            buttons.append(Button(text='ایجاد',
              link=f"/{get_avishan_config().PANEL_ROOT}/{cls.class_plural_snake_case_name()}/create"))
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
           link=f"/{get_avishan_config().PANEL_ROOT}/{cls.class_plural_snake_case_name()}",
           added_classes='btn-default')]

    @classmethod
    def panel_create_form_fields(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')]) -> List[models.Field]:
        fields = []
        for field in cls.get_fields():
            if cls.is_field_readonly(field):
                continue
            fields.append(field)

        return fields

    @classmethod
    def panel_create_form_items(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')], item: Union[(AvishanModel, 'AvishanModelPanelEnabled')]=None, values_list: List[Tuple[(str, str)]]=(), disabled_list: List[str]=()) -> List[FormElement]:
        items = []
        for field in cls.panel_create_form_fields():
            element_value = item.__getattribute__(field.name) if item else ''
            for name, value in values_list:
                if field.name == name:
                    element_value = value

            if isinstance(field, models.ForeignKey) and field.related_model in [Image, File]:
                form_element = FileChooseFormElement(name=(field.name),
                  label=(cls.panel_translator(field.name)),
                  disabled=(True if field.name in disabled_list else False))
            else:
                form_element = InputFormElement(name=(field.name),
                  label=(cls.panel_translator(field.name)),
                  value=element_value,
                  disabled=(True if field.name in disabled_list else False))
            items.append(form_element)

        return items

    @classmethod
    def panel_create_related_models(cls) -> List[Tuple[(Union[(Type[AvishanModel], 'AvishanModelPanelEnabled')], str)]]:
        return []

    @classmethod
    def panel_create_related_model_find(cls, model_name: str) -> Optional[Tuple[(Type[AvishanModel], str)]]:
        for model, related_field in cls.panel_create_related_models():
            if model.class_name() == model_name:
                return (
                 model, related_field)

    @classmethod
    def panel_translator(cls, text: str) -> str:
        try:
            return cls.panel_translator_dict()[text.lower()]
        except KeyError:
            return text

    @classmethod
    def panel_translator_dict(cls) -> dict:
        return {**{'id':'شناسه', 
         'title':'عنوان', 
         'order':'ترتیب', 
         'image':'عکس', 
         'text':'متن', 
         'parking':'پارکینگ'}, **(get_avishan_config().PANEL_TRANSLATION_DICT)}

    def panel_detail_buttons(self: Union[(AvishanModel, 'AvishanModelPanelEnabled')]) -> List[Button]:
        buttons = []
        if self.panel_edit_model_enable():
            buttons.append(Button(text='ویرایش',
              link=f"/{get_avishan_config().PANEL_ROOT}/{self.class_plural_snake_case_name()}/{self.id}/edit",
              added_classes='btn-success'))
        buttons.append(Button(text='بازگشت',
          link=f"/{get_avishan_config().PANEL_ROOT}/{self.class_plural_snake_case_name()}",
          added_classes='btn-default'))
        return buttons

    def panel_detail_items(self):
        items = []
        for name in self.panel_detail_keys():
            if inspect.ismethod(self.__getattribute__(name)):
                value = self.__getattribute__(name)()
            else:
                value = self.__getattribute__(name)
            items.append((self.panel_translator(name), value))

        return items

    @classmethod
    def panel_detail_related_models(cls) -> List[Tuple[(Union[(Type[AvishanModel], 'AvishanModelPanelEnabled')], str)]]:
        return []

    @classmethod
    def panel_detail_keys(cls: Union[(AvishanModel, 'AvishanModelPanelEnabled')]):
        return [field.name for field in cls.get_fields()]

    @classmethod
    def panel_edit_model_enable(cls) -> bool:
        return True

    def panel_edit_method(self: Union[(AvishanModel, 'AvishanModelPanelEnabled')], **kwargs):
        return (self.update)(**kwargs)

    def panel_edit_form_buttons(self: Union[(AvishanModel, 'AvishanModelPanelEnabled')]) -> List[Button]:
        return [
         Button(text='بازگشت',
           link=f"/{get_avishan_config().PANEL_ROOT}/{self.class_plural_snake_case_name()}/{self.id}/detail",
           added_classes='btn-default')]