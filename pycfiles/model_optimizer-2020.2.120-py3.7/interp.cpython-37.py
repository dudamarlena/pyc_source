# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/interp.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 7228 bytes
"""
 Copyright (C) 2017-2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import inspect, logging as log
from extensions.ops.resize_factor_utils import factor_update
from mo.front.common.layout import get_batch_dim, get_features_dim, get_height_dim, get_width_dim, shape_for_layout
from mo.graph.graph import Node, Graph
from mo.ops.op import Op
from mo.utils.utils import refer_to_faq_msg

class InterpOp(Op):
    op = 'Interp'
    enabled = False

    def __init__(self, graph, attrs):
        mandatory_props = {'type':__class__.op, 
         'op':__class__.op, 
         'factor':None, 
         'align_corners':1, 
         'parse_2nd_input':'value', 
         'in_ports_count':2, 
         'out_ports_count':1, 
         'infer':None}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return [
         'height',
         'width',
         'zoom_factor',
         'shrink_factor',
         'factor',
         'pad_beg',
         'pad_end',
         'align_corners']

    @staticmethod
    def interp_infer--- This code section failed: ---

 L.  58         0  LOAD_FAST                'node'
                2  LOAD_ATTR                graph
                4  LOAD_ATTR                graph
                6  LOAD_STR                 'layout'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'layout'

 L.  59        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'layout'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  LOAD_CONST               4
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  LOAD_ASSERT              AssertionError
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'

 L.  60        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'node'
               32  LOAD_METHOD              in_nodes
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  LOAD_CONST               2
               40  COMPARE_OP               ==
            42_44  POP_JUMP_IF_FALSE   396  'to 396'

 L.  61        46  LOAD_FAST                'node'
               48  LOAD_METHOD              in_node
               50  LOAD_CONST               0
               52  CALL_METHOD_1         1  '1 positional argument'
               54  LOAD_ATTR                shape
               56  STORE_FAST               'src_shape'

 L.  62        58  LOAD_FAST                'node'
               60  LOAD_METHOD              in_node
               62  LOAD_CONST               1
               64  CALL_METHOD_1         1  '1 positional argument'
               66  LOAD_ATTR                shape
               68  STORE_FAST               'dst_shape'

 L.  65        70  LOAD_FAST                'node'
               72  LOAD_ATTR                parse_2nd_input
               74  LOAD_STR                 'shape'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   110  'to 110'

 L.  66        80  LOAD_FAST                'dst_shape'
               82  LOAD_GLOBAL              get_height_dim
               84  LOAD_FAST                'layout'
               86  LOAD_CONST               4
               88  CALL_FUNCTION_2       2  '2 positional arguments'
               90  BINARY_SUBSCR    
               92  LOAD_FAST                'dst_shape'
               94  LOAD_GLOBAL              get_width_dim
               96  LOAD_FAST                'layout'
               98  LOAD_CONST               4
              100  CALL_FUNCTION_2       2  '2 positional arguments'
              102  BINARY_SUBSCR    
              104  BUILD_LIST_2          2 
              106  STORE_FAST               'dst_shape'
              108  JUMP_FORWARD        122  'to 122'
            110_0  COME_FROM            78  '78'

 L.  69       110  LOAD_FAST                'node'
              112  LOAD_METHOD              in_node
              114  LOAD_CONST               1
              116  CALL_METHOD_1         1  '1 positional argument'
              118  LOAD_ATTR                value
              120  STORE_FAST               'dst_shape'
            122_0  COME_FROM           108  '108'

 L.  71       122  LOAD_FAST                'src_shape'
              124  LOAD_CONST               None
              126  COMPARE_OP               is
              128  POP_JUMP_IF_TRUE    162  'to 162'
              130  LOAD_FAST                'dst_shape'
              132  LOAD_CONST               None
              134  COMPARE_OP               is
              136  POP_JUMP_IF_TRUE    162  'to 162'
              138  LOAD_GLOBAL              len
              140  LOAD_FAST                'src_shape'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  LOAD_CONST               4
              146  COMPARE_OP               !=
              148  POP_JUMP_IF_TRUE    162  'to 162'
              150  LOAD_GLOBAL              len
              152  LOAD_FAST                'dst_shape'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  LOAD_CONST               2
              158  COMPARE_OP               !=
              160  POP_JUMP_IF_FALSE   198  'to 198'
            162_0  COME_FROM           148  '148'
            162_1  COME_FROM           136  '136'
            162_2  COME_FROM           128  '128'

 L.  72       162  LOAD_GLOBAL              log
              164  LOAD_METHOD              error

 L.  73       166  LOAD_STR                 'Node {} with op {} cannot be converted to Resample layer because there is no enough info about src/dst shapes: src_shape = {}, dst_shape = {}'
              168  LOAD_METHOD              format

 L.  74       170  LOAD_FAST                'node'
              172  LOAD_ATTR                name
              174  LOAD_FAST                'node'
              176  LOAD_ATTR                op
              178  LOAD_FAST                'src_shape'
              180  LOAD_FAST                'dst_shape'
              182  CALL_METHOD_4         4  '4 positional arguments'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  POP_TOP          

 L.  75       188  LOAD_CONST               None
              190  LOAD_FAST                'node'
              192  STORE_ATTR               type

 L.  76       194  LOAD_CONST               None
              196  RETURN_VALUE     
            198_0  COME_FROM           160  '160'

 L.  77       198  LOAD_FAST                'src_shape'
              200  LOAD_GLOBAL              get_height_dim
              202  LOAD_FAST                'layout'
              204  LOAD_CONST               4
              206  CALL_FUNCTION_2       2  '2 positional arguments'
              208  BINARY_SUBSCR    
              210  STORE_FAST               'in_height'

 L.  78       212  LOAD_FAST                'src_shape'
              214  LOAD_GLOBAL              get_width_dim
              216  LOAD_FAST                'layout'
              218  LOAD_CONST               4
              220  CALL_FUNCTION_2       2  '2 positional arguments'
              222  BINARY_SUBSCR    
              224  STORE_FAST               'in_width'

 L.  79       226  LOAD_FAST                'dst_shape'
              228  LOAD_CONST               0
              230  BINARY_SUBSCR    
              232  STORE_FAST               'out_height'

 L.  80       234  LOAD_FAST                'dst_shape'
              236  LOAD_CONST               1
              238  BINARY_SUBSCR    
              240  STORE_FAST               'out_width'

 L.  82       242  LOAD_GLOBAL              factor_update

 L.  83       244  LOAD_FAST                'node'
              246  LOAD_ATTR                factor

 L.  84       248  LOAD_GLOBAL              float
              250  LOAD_FAST                'out_height'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  LOAD_FAST                'in_height'
              256  BINARY_TRUE_DIVIDE
              258  LOAD_GLOBAL              float
              260  LOAD_FAST                'out_width'
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  LOAD_FAST                'in_width'
              266  BINARY_TRUE_DIVIDE
              268  BUILD_LIST_2          2 

 L.  85       270  LOAD_FAST                'in_height'
              272  LOAD_FAST                'in_width'
              274  BUILD_LIST_2          2 

 L.  86       276  LOAD_FAST                'out_height'
              278  LOAD_FAST                'out_width'
              280  BUILD_LIST_2          2 

 L.  87       282  LOAD_FAST                'node'
              284  LOAD_METHOD              soft_get
              286  LOAD_STR                 'name'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  CALL_FUNCTION_5       5  '5 positional arguments'
              292  LOAD_FAST                'node'
              294  STORE_ATTR               factor

 L.  90       296  LOAD_FAST                'node'
              298  LOAD_ATTR                factor
              300  LOAD_CONST               None
              302  COMPARE_OP               is
          304_306  POP_JUMP_IF_FALSE   324  'to 324'

 L.  91       308  LOAD_FAST                'out_width'
              310  LOAD_FAST                'node'
              312  LOAD_STR                 'width'
              314  STORE_SUBSCR     

 L.  92       316  LOAD_FAST                'out_height'
              318  LOAD_FAST                'node'
              320  LOAD_STR                 'height'
              322  STORE_SUBSCR     
            324_0  COME_FROM           304  '304'

 L.  94       324  LOAD_GLOBAL              shape_for_layout
              326  LOAD_FAST                'layout'

 L.  95       328  LOAD_FAST                'src_shape'
              330  LOAD_GLOBAL              get_batch_dim
              332  LOAD_FAST                'layout'
              334  LOAD_CONST               4
              336  CALL_FUNCTION_2       2  '2 positional arguments'
              338  BINARY_SUBSCR    

 L.  96       340  LOAD_FAST                'src_shape'
              342  LOAD_GLOBAL              get_features_dim
              344  LOAD_FAST                'layout'
              346  LOAD_CONST               4
              348  CALL_FUNCTION_2       2  '2 positional arguments'
              350  BINARY_SUBSCR    

 L.  97       352  LOAD_FAST                'out_height'

 L.  98       354  LOAD_FAST                'out_width'
              356  LOAD_CONST               ('batch', 'features', 'height', 'width')
              358  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              360  LOAD_FAST                'node'
              362  LOAD_METHOD              out_node
              364  CALL_METHOD_0         0  '0 positional arguments'
              366  STORE_ATTR               shape

 L.  99       368  LOAD_FAST                'node'
              370  LOAD_ATTR                graph
              372  LOAD_METHOD              remove_edge
              374  LOAD_FAST                'node'
              376  LOAD_METHOD              in_node
              378  LOAD_CONST               1
              380  CALL_METHOD_1         1  '1 positional argument'
              382  LOAD_ATTR                id
              384  LOAD_FAST                'node'
              386  LOAD_ATTR                id
              388  CALL_METHOD_2         2  '2 positional arguments'
              390  POP_TOP          
          392_394  JUMP_FORWARD        948  'to 948'
            396_0  COME_FROM            42  '42'

 L. 101       396  LOAD_FAST                'node'
              398  LOAD_METHOD              out_node
              400  LOAD_CONST               0
              402  CALL_METHOD_1         1  '1 positional argument'
              404  STORE_FAST               'outn'

 L. 103       406  LOAD_FAST                'node'
              408  LOAD_METHOD              in_node
              410  LOAD_CONST               0
              412  CALL_METHOD_1         1  '1 positional argument'
              414  STORE_FAST               'in_shape'

 L. 104       416  LOAD_FAST                'in_shape'
              418  LOAD_ATTR                shape
              420  LOAD_GLOBAL              get_batch_dim
              422  LOAD_FAST                'layout'
              424  LOAD_CONST               4
              426  CALL_FUNCTION_2       2  '2 positional arguments'
              428  BINARY_SUBSCR    
              430  STORE_FAST               'num_'

 L. 105       432  LOAD_FAST                'in_shape'
              434  LOAD_ATTR                shape
              436  LOAD_GLOBAL              get_features_dim
              438  LOAD_FAST                'layout'
              440  LOAD_CONST               4
              442  CALL_FUNCTION_2       2  '2 positional arguments'
              444  BINARY_SUBSCR    
              446  STORE_FAST               'channels_'

 L. 106       448  LOAD_FAST                'in_shape'
              450  LOAD_ATTR                shape
              452  LOAD_GLOBAL              get_height_dim
              454  LOAD_FAST                'layout'
              456  LOAD_CONST               4
              458  CALL_FUNCTION_2       2  '2 positional arguments'
              460  BINARY_SUBSCR    
              462  STORE_FAST               'height_in_'

 L. 107       464  LOAD_FAST                'in_shape'
              466  LOAD_ATTR                shape
              468  LOAD_GLOBAL              get_width_dim
              470  LOAD_FAST                'layout'
              472  LOAD_CONST               4
              474  CALL_FUNCTION_2       2  '2 positional arguments'
              476  BINARY_SUBSCR    
              478  STORE_FAST               'width_in_'

 L. 109       480  LOAD_FAST                'height_in_'
              482  LOAD_FAST                'node'
              484  LOAD_ATTR                pad_beg
              486  BINARY_ADD       
              488  LOAD_FAST                'node'
              490  LOAD_ATTR                pad_end
              492  BINARY_ADD       
              494  STORE_FAST               'height_out_'

 L. 110       496  LOAD_FAST                'width_in_'
              498  LOAD_FAST                'node'
              500  LOAD_ATTR                pad_beg
              502  BINARY_ADD       
              504  LOAD_FAST                'node'
              506  LOAD_ATTR                pad_end
              508  BINARY_ADD       
              510  STORE_FAST               'width_out_'

 L. 112       512  LOAD_FAST                'node'
              514  LOAD_ATTR                shrink_factor
              516  LOAD_CONST               1
              518  COMPARE_OP               !=
          520_522  POP_JUMP_IF_FALSE   610  'to 610'
              524  LOAD_FAST                'node'
              526  LOAD_ATTR                zoom_factor
              528  LOAD_CONST               1
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_FALSE   610  'to 610'

 L. 113       536  LOAD_FAST                'node'
              538  LOAD_ATTR                shrink_factor
              540  STORE_FAST               'shrink_factor'

 L. 114       542  LOAD_FAST                'shrink_factor'
              544  LOAD_CONST               1
              546  COMPARE_OP               <
          548_550  POP_JUMP_IF_FALSE   574  'to 574'

 L. 115       552  LOAD_GLOBAL              log
              554  LOAD_METHOD              error
              556  LOAD_STR                 'Shrink factor should be positive in node {}'
              558  LOAD_METHOD              format
              560  LOAD_FAST                'node'
              562  LOAD_ATTR                id
              564  CALL_METHOD_1         1  '1 positional argument'
              566  CALL_METHOD_1         1  '1 positional argument'
              568  POP_TOP          

 L. 116       570  LOAD_CONST               None
              572  RETURN_VALUE     
            574_0  COME_FROM           548  '548'

 L. 117       574  LOAD_FAST                'height_out_'
              576  LOAD_CONST               1
              578  BINARY_SUBTRACT  
              580  LOAD_FAST                'shrink_factor'
              582  BINARY_TRUE_DIVIDE
              584  LOAD_CONST               1
              586  BINARY_ADD       
              588  STORE_FAST               'height_out_'

 L. 118       590  LOAD_FAST                'width_out_'
              592  LOAD_CONST               1
              594  BINARY_SUBTRACT  
              596  LOAD_FAST                'shrink_factor'
              598  BINARY_TRUE_DIVIDE
              600  LOAD_CONST               1
              602  BINARY_ADD       
              604  STORE_FAST               'width_out_'
          606_608  JUMP_FORWARD        928  'to 928'
            610_0  COME_FROM           532  '532'
            610_1  COME_FROM           520  '520'

 L. 119       610  LOAD_FAST                'node'
              612  LOAD_ATTR                shrink_factor
              614  LOAD_CONST               1
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_FALSE   718  'to 718'
              622  LOAD_FAST                'node'
              624  LOAD_ATTR                zoom_factor
              626  LOAD_CONST               1
              628  COMPARE_OP               !=
          630_632  POP_JUMP_IF_FALSE   718  'to 718'

 L. 120       634  LOAD_FAST                'node'
              636  LOAD_ATTR                zoom_factor
              638  STORE_FAST               'zoom_factor'

 L. 121       640  LOAD_FAST                'zoom_factor'
              642  LOAD_CONST               1
              644  COMPARE_OP               <
          646_648  POP_JUMP_IF_FALSE   672  'to 672'

 L. 122       650  LOAD_GLOBAL              log
              652  LOAD_METHOD              error
              654  LOAD_STR                 'Zoom factor should be positive in node {}'
              656  LOAD_METHOD              format
              658  LOAD_FAST                'node'
              660  LOAD_ATTR                id
              662  CALL_METHOD_1         1  '1 positional argument'
              664  CALL_METHOD_1         1  '1 positional argument'
              666  POP_TOP          

 L. 123       668  LOAD_CONST               None
              670  RETURN_VALUE     
            672_0  COME_FROM           646  '646'

 L. 125       672  LOAD_STR                 'Interp layer shape inference function may be wrong, please, try to update layer shape inference function in the file (extensions/ops/interp.op at the line {}).'
              674  LOAD_METHOD              format

 L. 127       676  LOAD_GLOBAL              inspect
              678  LOAD_METHOD              currentframe
              680  CALL_METHOD_0         0  '0 positional arguments'
              682  LOAD_ATTR                f_lineno
              684  CALL_METHOD_1         1  '1 positional argument'
              686  LOAD_GLOBAL              refer_to_faq_msg
              688  LOAD_CONST               100
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  BINARY_ADD       
              694  LOAD_FAST                'node'
              696  LOAD_STR                 'debug_message'
              698  STORE_SUBSCR     

 L. 136       700  LOAD_FAST                'height_out_'
              702  LOAD_FAST                'zoom_factor'
              704  BINARY_MULTIPLY  
              706  STORE_FAST               'height_out_'

 L. 137       708  LOAD_FAST                'width_out_'
              710  LOAD_FAST                'zoom_factor'
              712  BINARY_MULTIPLY  
              714  STORE_FAST               'width_out_'
              716  JUMP_FORWARD        928  'to 928'
            718_0  COME_FROM           630  '630'
            718_1  COME_FROM           618  '618'

 L. 138       718  LOAD_FAST                'node'
              720  LOAD_ATTR                width
              722  LOAD_CONST               0
              724  COMPARE_OP               !=
          726_728  POP_JUMP_IF_FALSE   756  'to 756'
              730  LOAD_FAST                'node'
              732  LOAD_ATTR                height
              734  LOAD_CONST               0
              736  COMPARE_OP               !=
          738_740  POP_JUMP_IF_FALSE   756  'to 756'

 L. 139       742  LOAD_FAST                'node'
              744  LOAD_ATTR                height
              746  STORE_FAST               'height_out_'

 L. 140       748  LOAD_FAST                'node'
              750  LOAD_ATTR                width
              752  STORE_FAST               'width_out_'
              754  JUMP_FORWARD        928  'to 928'
            756_0  COME_FROM           738  '738'
            756_1  COME_FROM           726  '726'

 L. 141       756  LOAD_FAST                'node'
              758  LOAD_ATTR                shrink_factor
              760  LOAD_CONST               1
              762  COMPARE_OP               !=
          764_766  POP_JUMP_IF_FALSE   928  'to 928'
              768  LOAD_FAST                'node'
              770  LOAD_ATTR                zoom_factor
              772  LOAD_CONST               1
              774  COMPARE_OP               !=
          776_778  POP_JUMP_IF_FALSE   928  'to 928'

 L. 142       780  LOAD_FAST                'node'
              782  LOAD_ATTR                shrink_factor
              784  STORE_FAST               'shrink_factor'

 L. 143       786  LOAD_FAST                'node'
              788  LOAD_ATTR                zoom_factor
              790  STORE_FAST               'zoom_factor'

 L. 144       792  LOAD_FAST                'shrink_factor'
              794  LOAD_CONST               1
              796  COMPARE_OP               <
          798_800  POP_JUMP_IF_FALSE   824  'to 824'

 L. 145       802  LOAD_GLOBAL              log
              804  LOAD_METHOD              error
              806  LOAD_STR                 'Shrink factor should be positive in node {}'
              808  LOAD_METHOD              format
              810  LOAD_FAST                'node'
              812  LOAD_ATTR                id
              814  CALL_METHOD_1         1  '1 positional argument'
              816  CALL_METHOD_1         1  '1 positional argument'
              818  POP_TOP          

 L. 146       820  LOAD_CONST               None
              822  RETURN_VALUE     
            824_0  COME_FROM           798  '798'

 L. 147       824  LOAD_FAST                'zoom_factor'
              826  LOAD_CONST               1
              828  COMPARE_OP               <
          830_832  POP_JUMP_IF_FALSE   856  'to 856'

 L. 148       834  LOAD_GLOBAL              log
              836  LOAD_METHOD              error
              838  LOAD_STR                 'Zoom factor should be positive in node {}'
              840  LOAD_METHOD              format
              842  LOAD_FAST                'node'
              844  LOAD_ATTR                id
              846  CALL_METHOD_1         1  '1 positional argument'
              848  CALL_METHOD_1         1  '1 positional argument'
              850  POP_TOP          

 L. 149       852  LOAD_CONST               None
              854  RETURN_VALUE     
            856_0  COME_FROM           830  '830'

 L. 150       856  LOAD_FAST                'height_out_'
              858  LOAD_CONST               1
              860  BINARY_SUBTRACT  
              862  LOAD_FAST                'shrink_factor'
              864  BINARY_TRUE_DIVIDE
              866  LOAD_CONST               1
              868  BINARY_ADD       
              870  STORE_FAST               'height_out_'

 L. 151       872  LOAD_FAST                'width_out_'
              874  LOAD_CONST               1
              876  BINARY_SUBTRACT  
              878  LOAD_FAST                'shrink_factor'
              880  BINARY_TRUE_DIVIDE
              882  LOAD_CONST               1
              884  BINARY_ADD       
              886  STORE_FAST               'width_out_'

 L. 152       888  LOAD_FAST                'height_out_'
              890  LOAD_FAST                'height_out_'
              892  LOAD_CONST               1
              894  BINARY_SUBTRACT  
              896  LOAD_FAST                'zoom_factor'
              898  LOAD_CONST               1
              900  BINARY_SUBTRACT  
              902  BINARY_MULTIPLY  
              904  BINARY_ADD       
              906  STORE_FAST               'height_out_'

 L. 153       908  LOAD_FAST                'width_out_'
              910  LOAD_FAST                'width_out_'
              912  LOAD_CONST               1
              914  BINARY_SUBTRACT  
              916  LOAD_FAST                'zoom_factor'
              918  LOAD_CONST               1
              920  BINARY_SUBTRACT  
              922  BINARY_MULTIPLY  
              924  BINARY_ADD       
              926  STORE_FAST               'width_out_'
            928_0  COME_FROM           776  '776'
            928_1  COME_FROM           764  '764'
            928_2  COME_FROM           754  '754'
            928_3  COME_FROM           716  '716'
            928_4  COME_FROM           606  '606'

 L. 155       928  LOAD_GLOBAL              shape_for_layout
              930  LOAD_FAST                'layout'

 L. 156       932  LOAD_FAST                'num_'

 L. 157       934  LOAD_FAST                'channels_'

 L. 158       936  LOAD_FAST                'height_out_'

 L. 159       938  LOAD_FAST                'width_out_'
              940  LOAD_CONST               ('batch', 'features', 'height', 'width')
              942  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              944  LOAD_FAST                'outn'
              946  STORE_ATTR               shape
            948_0  COME_FROM           392  '392'

Parse error at or near `JUMP_FORWARD' instruction at offset 392_394