# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/slice.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 5758 bytes
"""
 Copyright (C) 2018-2020 Intel Corporation

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
import logging as log, numpy as np
from mo.graph.graph import Node, Graph
from mo.ops.op import Op

class Slice(Op):
    op = 'Slice'
    enabled = True

    def __init__(self, graph, attrs):
        super().__init__(graph, {'type':__class__.op, 
         'op':'Slice', 
         'in_ports_count':3, 
         'out_ports_count':1, 
         'infer':__class__.infer}, attrs)

    def supported_attrs(self):
        return [
         'start', 'end', 'axis']

    @staticmethod
    def infer--- This code section failed: ---

 L.  43         0  LOAD_CONST               None
                2  STORE_FAST               'axis'

 L.  44         4  LOAD_CONST               None
                6  STORE_FAST               'steps'

 L.  45         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'node'
               12  LOAD_METHOD              in_nodes
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  LOAD_CONST               1
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE   144  'to 144'

 L.  47        24  LOAD_FAST                'node'
               26  LOAD_METHOD              has
               28  LOAD_STR                 'start'
               30  CALL_METHOD_1         1  '1 positional argument'
               32  POP_JUMP_IF_FALSE   120  'to 120'
               34  LOAD_FAST                'node'
               36  LOAD_METHOD              has
               38  LOAD_STR                 'end'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  POP_JUMP_IF_FALSE   120  'to 120'
               44  LOAD_FAST                'node'
               46  LOAD_METHOD              has
               48  LOAD_STR                 'axis'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  POP_JUMP_IF_FALSE   120  'to 120'

 L.  49        54  LOAD_FAST                'node'
               56  LOAD_METHOD              has_valid
               58  LOAD_STR                 'start'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  POP_JUMP_IF_FALSE   104  'to 104'
               64  LOAD_FAST                'node'
               66  LOAD_METHOD              has_valid
               68  LOAD_STR                 'end'
               70  CALL_METHOD_1         1  '1 positional argument'
               72  POP_JUMP_IF_FALSE   104  'to 104'
               74  LOAD_FAST                'node'
               76  LOAD_METHOD              has
               78  LOAD_STR                 'axis'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  POP_JUMP_IF_FALSE   104  'to 104'

 L.  50        84  LOAD_FAST                'node'
               86  LOAD_ATTR                start
               88  STORE_FAST               'start'

 L.  51        90  LOAD_FAST                'node'
               92  LOAD_ATTR                end
               94  STORE_FAST               'end'

 L.  52        96  LOAD_FAST                'node'
               98  LOAD_ATTR                axis
              100  STORE_FAST               'axis'
              102  JUMP_ABSOLUTE       140  'to 140'
            104_0  COME_FROM            82  '82'
            104_1  COME_FROM            72  '72'
            104_2  COME_FROM            62  '62'

 L.  54       104  LOAD_GLOBAL              log
              106  LOAD_METHOD              warning
              108  LOAD_STR                 'Incorrect slice operation: no starts or end attr'
              110  CALL_METHOD_1         1  '1 positional argument'
              112  POP_TOP          

 L.  55       114  LOAD_CONST               None
              116  RETURN_VALUE     
              118  JUMP_FORWARD        650  'to 650'
            120_0  COME_FROM            52  '52'
            120_1  COME_FROM            42  '42'
            120_2  COME_FROM            32  '32'

 L.  58       120  LOAD_CONST               0
              122  LOAD_CONST               ('caffe_slice_infer',)
              124  IMPORT_NAME_ATTR         mo.front.common.partial_infer.slice
              126  IMPORT_FROM              caffe_slice_infer
              128  STORE_FAST               'caffe_slice_infer'
              130  POP_TOP          

 L.  59       132  LOAD_FAST                'caffe_slice_infer'
              134  LOAD_FAST                'node'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  POP_TOP          
          140_142  JUMP_FORWARD        650  'to 650'
            144_0  COME_FROM            22  '22'

 L.  60       144  LOAD_GLOBAL              len
              146  LOAD_FAST                'node'
              148  LOAD_METHOD              in_nodes
              150  CALL_METHOD_0         0  '0 positional arguments'
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  LOAD_CONST               3
              156  COMPARE_OP               >=
          158_160  POP_JUMP_IF_FALSE   636  'to 636'

 L.  61       162  LOAD_FAST                'node'
              164  LOAD_METHOD              has
              166  LOAD_STR                 'format'
              168  CALL_METHOD_1         1  '1 positional argument'
          170_172  POP_JUMP_IF_FALSE   442  'to 442'
              174  LOAD_FAST                'node'
              176  LOAD_STR                 'format'
              178  BINARY_SUBSCR    
              180  LOAD_STR                 'onnx'
              182  COMPARE_OP               ==
          184_186  POP_JUMP_IF_FALSE   442  'to 442'

 L.  63       188  LOAD_FAST                'node'
              190  LOAD_METHOD              in_node
              192  LOAD_CONST               1
              194  CALL_METHOD_1         1  '1 positional argument'
              196  STORE_FAST               'starts_node'

 L.  64       198  LOAD_FAST                'node'
              200  LOAD_METHOD              in_node
              202  LOAD_CONST               2
              204  CALL_METHOD_1         1  '1 positional argument'
              206  STORE_FAST               'ends_node'

 L.  65       208  LOAD_FAST                'starts_node'
              210  LOAD_METHOD              has_valid
              212  LOAD_STR                 'value'
              214  CALL_METHOD_1         1  '1 positional argument'
          216_218  POP_JUMP_IF_FALSE   426  'to 426'
              220  LOAD_FAST                'ends_node'
              222  LOAD_METHOD              has_valid
              224  LOAD_STR                 'value'
              226  CALL_METHOD_1         1  '1 positional argument'
          228_230  POP_JUMP_IF_FALSE   426  'to 426'

 L.  66       232  LOAD_GLOBAL              np
              234  LOAD_ATTR                array
              236  LOAD_FAST                'node'
              238  LOAD_METHOD              in_node
              240  LOAD_CONST               1
              242  CALL_METHOD_1         1  '1 positional argument'
              244  LOAD_ATTR                value
              246  LOAD_GLOBAL              np
              248  LOAD_ATTR                int64
              250  LOAD_CONST               ('dtype',)
              252  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              254  STORE_FAST               'start'

 L.  67       256  LOAD_GLOBAL              np
              258  LOAD_ATTR                array
              260  LOAD_FAST                'node'
              262  LOAD_METHOD              in_node
              264  LOAD_CONST               2
              266  CALL_METHOD_1         1  '1 positional argument'
              268  LOAD_ATTR                value
              270  LOAD_GLOBAL              np
              272  LOAD_ATTR                int64
              274  LOAD_CONST               ('dtype',)
              276  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              278  STORE_FAST               'end'

 L.  68       280  LOAD_CONST               3
              282  LOAD_FAST                'node'
              284  LOAD_METHOD              in_nodes
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  COMPARE_OP               in
          290_292  POP_JUMP_IF_FALSE   352  'to 352'

 L.  69       294  LOAD_FAST                'node'
              296  LOAD_METHOD              in_node
              298  LOAD_CONST               3
              300  CALL_METHOD_1         1  '1 positional argument'
              302  LOAD_METHOD              has_valid
              304  LOAD_STR                 'value'
              306  CALL_METHOD_1         1  '1 positional argument'
          308_310  POP_JUMP_IF_FALSE   338  'to 338'

 L.  70       312  LOAD_GLOBAL              np
              314  LOAD_ATTR                array
              316  LOAD_FAST                'node'
              318  LOAD_METHOD              in_node
              320  LOAD_CONST               3
              322  CALL_METHOD_1         1  '1 positional argument'
              324  LOAD_ATTR                value
              326  LOAD_GLOBAL              np
              328  LOAD_ATTR                int64
              330  LOAD_CONST               ('dtype',)
              332  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              334  STORE_FAST               'axis'
              336  JUMP_FORWARD        352  'to 352'
            338_0  COME_FROM           308  '308'

 L.  72       338  LOAD_GLOBAL              log
              340  LOAD_METHOD              warning
              342  LOAD_STR                 'Incorrect slice operation: axes should be const'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  POP_TOP          

 L.  73       348  LOAD_CONST               None
              350  RETURN_VALUE     
            352_0  COME_FROM           336  '336'
            352_1  COME_FROM           290  '290'

 L.  74       352  LOAD_CONST               4
              354  LOAD_FAST                'node'
              356  LOAD_METHOD              in_nodes
              358  CALL_METHOD_0         0  '0 positional arguments'
              360  COMPARE_OP               in
          362_364  POP_JUMP_IF_FALSE   440  'to 440'

 L.  75       366  LOAD_FAST                'node'
              368  LOAD_METHOD              in_node
              370  LOAD_CONST               4
              372  CALL_METHOD_1         1  '1 positional argument'
              374  LOAD_METHOD              has_valid
              376  LOAD_STR                 'value'
              378  CALL_METHOD_1         1  '1 positional argument'
          380_382  POP_JUMP_IF_FALSE   410  'to 410'

 L.  76       384  LOAD_GLOBAL              np
              386  LOAD_ATTR                array
              388  LOAD_FAST                'node'
              390  LOAD_METHOD              in_node
              392  LOAD_CONST               4
              394  CALL_METHOD_1         1  '1 positional argument'
              396  LOAD_ATTR                value
              398  LOAD_GLOBAL              np
              400  LOAD_ATTR                int64
              402  LOAD_CONST               ('dtype',)
              404  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              406  STORE_FAST               'steps'
              408  JUMP_FORWARD        424  'to 424'
            410_0  COME_FROM           380  '380'

 L.  78       410  LOAD_GLOBAL              log
              412  LOAD_METHOD              warning
              414  LOAD_STR                 'Incorrect slice operation: steps should be const'
              416  CALL_METHOD_1         1  '1 positional argument'
              418  POP_TOP          

 L.  79       420  LOAD_CONST               None
              422  RETURN_VALUE     
            424_0  COME_FROM           408  '408'
              424  JUMP_FORWARD        440  'to 440'
            426_0  COME_FROM           228  '228'
            426_1  COME_FROM           216  '216'

 L.  81       426  LOAD_GLOBAL              log
              428  LOAD_METHOD              warning
              430  LOAD_STR                 'Incorrect slice operation: no starts or ends attr'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  POP_TOP          

 L.  82       436  LOAD_CONST               None
              438  RETURN_VALUE     
            440_0  COME_FROM           424  '424'
            440_1  COME_FROM           362  '362'
              440  JUMP_FORWARD        634  'to 634'
            442_0  COME_FROM           184  '184'
            442_1  COME_FROM           170  '170'

 L.  85       442  LOAD_FAST                'node'
              444  LOAD_METHOD              in_node
              446  LOAD_CONST               1
              448  CALL_METHOD_1         1  '1 positional argument'
              450  STORE_FAST               'start_node'

 L.  86       452  LOAD_FAST                'node'
              454  LOAD_METHOD              in_node
              456  LOAD_CONST               2
              458  CALL_METHOD_1         1  '1 positional argument'
              460  STORE_FAST               'size_node'

 L.  87       462  LOAD_FAST                'start_node'
              464  LOAD_METHOD              has_valid
              466  LOAD_STR                 'value'
              468  CALL_METHOD_1         1  '1 positional argument'
          470_472  POP_JUMP_IF_FALSE   620  'to 620'
              474  LOAD_FAST                'size_node'
              476  LOAD_METHOD              has_valid
              478  LOAD_STR                 'value'
              480  CALL_METHOD_1         1  '1 positional argument'
          482_484  POP_JUMP_IF_FALSE   620  'to 620'

 L.  88       486  LOAD_GLOBAL              np
              488  LOAD_ATTR                array
              490  LOAD_FAST                'node'
              492  LOAD_METHOD              in_node
              494  LOAD_CONST               1
              496  CALL_METHOD_1         1  '1 positional argument'
              498  LOAD_ATTR                value
              500  LOAD_GLOBAL              np
              502  LOAD_ATTR                int64
              504  LOAD_CONST               ('dtype',)
              506  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              508  STORE_FAST               'start'

 L.  89       510  LOAD_GLOBAL              np
              512  LOAD_ATTR                array
              514  LOAD_FAST                'node'
              516  LOAD_METHOD              in_node
              518  LOAD_CONST               2
              520  CALL_METHOD_1         1  '1 positional argument'
              522  LOAD_ATTR                value
              524  LOAD_GLOBAL              np
              526  LOAD_ATTR                int64
              528  LOAD_CONST               ('dtype',)
              530  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              532  STORE_FAST               'size'

 L.  90       534  LOAD_FAST                'start'
              536  LOAD_FAST                'size'
              538  BINARY_ADD       
              540  STORE_FAST               'end'

 L.  91       542  LOAD_CONST               None
              544  STORE_FAST               'axis'

 L.  94       546  LOAD_FAST                'node'
              548  LOAD_ATTR                graph
              550  LOAD_METHOD              remove_edge
              552  LOAD_FAST                'node'
              554  LOAD_METHOD              in_node
              556  LOAD_CONST               1
              558  CALL_METHOD_1         1  '1 positional argument'
              560  LOAD_ATTR                id
              562  LOAD_FAST                'node'
              564  LOAD_ATTR                id
              566  CALL_METHOD_2         2  '2 positional arguments'
              568  POP_TOP          

 L.  95       570  LOAD_FAST                'node'
              572  LOAD_ATTR                graph
              574  LOAD_METHOD              remove_edge
              576  LOAD_FAST                'node'
              578  LOAD_METHOD              in_node
              580  LOAD_CONST               2
              582  CALL_METHOD_1         1  '1 positional argument'
              584  LOAD_ATTR                id
              586  LOAD_FAST                'node'
              588  LOAD_ATTR                id
              590  CALL_METHOD_2         2  '2 positional arguments'
              592  POP_TOP          

 L.  97       594  LOAD_FAST                'start'
              596  LOAD_FAST                'node'
              598  LOAD_STR                 'start'
              600  STORE_SUBSCR     

 L.  98       602  LOAD_FAST                'end'
              604  LOAD_FAST                'node'
              606  LOAD_STR                 'end'
              608  STORE_SUBSCR     

 L.  99       610  LOAD_CONST               None
              612  LOAD_FAST                'node'
              614  LOAD_STR                 'axis'
              616  STORE_SUBSCR     
              618  JUMP_FORWARD        634  'to 634'
            620_0  COME_FROM           482  '482'
            620_1  COME_FROM           470  '470'

 L. 101       620  LOAD_GLOBAL              log
              622  LOAD_METHOD              warning
              624  LOAD_STR                 'Incorrect slice operation: no starts or end attr'
            626_0  COME_FROM           118  '118'
              626  CALL_METHOD_1         1  '1 positional argument'
              628  POP_TOP          

 L. 102       630  LOAD_CONST               None
              632  RETURN_VALUE     
            634_0  COME_FROM           618  '618'
            634_1  COME_FROM           440  '440'
              634  JUMP_FORWARD        650  'to 650'
            636_0  COME_FROM           158  '158'

 L. 104       636  LOAD_GLOBAL              log
              638  LOAD_METHOD              warning
              640  LOAD_STR                 'Incorrect number of input nodes in slice operation'
              642  CALL_METHOD_1         1  '1 positional argument'
              644  POP_TOP          

 L. 105       646  LOAD_CONST               None
              648  RETURN_VALUE     
            650_0  COME_FROM           634  '634'
            650_1  COME_FROM           140  '140'

 L. 107       650  LOAD_FAST                'node'
              652  LOAD_METHOD              in_node
              654  LOAD_CONST               0
              656  CALL_METHOD_1         1  '1 positional argument'
              658  LOAD_ATTR                shape
              660  STORE_FAST               'input_shape'

 L. 109       662  SETUP_LOOP          714  'to 714'
              664  LOAD_GLOBAL              range
              666  LOAD_FAST                'start'
              668  LOAD_ATTR                size
              670  CALL_FUNCTION_1       1  '1 positional argument'
              672  GET_ITER         
            674_0  COME_FROM           692  '692'
              674  FOR_ITER            712  'to 712'
              676  STORE_FAST               'i'

 L. 110       678  LOAD_FAST                'end'
              680  LOAD_FAST                'i'
              682  BINARY_SUBSCR    
              684  LOAD_FAST                'start'
              686  LOAD_FAST                'i'
              688  BINARY_SUBSCR    
              690  COMPARE_OP               <
          692_694  POP_JUMP_IF_FALSE   674  'to 674'

 L. 111       696  LOAD_FAST                'input_shape'
              698  LOAD_FAST                'i'
              700  BINARY_SUBSCR    
              702  LOAD_FAST                'end'
              704  LOAD_FAST                'i'
              706  STORE_SUBSCR     
          708_710  JUMP_BACK           674  'to 674'
              712  POP_BLOCK        
            714_0  COME_FROM_LOOP      662  '662'

 L. 113       714  LOAD_FAST                'end'
              716  LOAD_FAST                'node'
              718  STORE_ATTR               end

 L. 114       720  LOAD_FAST                'node'
              722  LOAD_METHOD              in_node
              724  LOAD_CONST               0
              726  CALL_METHOD_1         1  '1 positional argument'
              728  LOAD_ATTR                value
              730  STORE_FAST               'value'

 L. 117       732  LOAD_FAST                'value'
              734  LOAD_CONST               None
              736  COMPARE_OP               is
          738_740  POP_JUMP_IF_FALSE   752  'to 752'

 L. 118       742  LOAD_GLOBAL              np
              744  LOAD_METHOD              zeros
              746  LOAD_FAST                'input_shape'
              748  CALL_METHOD_1         1  '1 positional argument'
              750  STORE_FAST               'value'
            752_0  COME_FROM           738  '738'

 L. 121       752  LOAD_FAST                'axis'
              754  LOAD_CONST               None
              756  COMPARE_OP               is
          758_760  POP_JUMP_IF_FALSE   784  'to 784'

 L. 122       762  LOAD_LISTCOMP            '<code_object <listcomp>>'
              764  LOAD_STR                 'Slice.infer.<locals>.<listcomp>'
              766  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              768  LOAD_GLOBAL              range
              770  LOAD_GLOBAL              len
              772  LOAD_FAST                'start'
              774  CALL_FUNCTION_1       1  '1 positional argument'
              776  CALL_FUNCTION_1       1  '1 positional argument'
              778  GET_ITER         
              780  CALL_FUNCTION_1       1  '1 positional argument'
              782  STORE_FAST               'axis'
            784_0  COME_FROM           758  '758'

 L. 124       784  LOAD_FAST                'steps'
              786  LOAD_CONST               None
              788  COMPARE_OP               is
          790_792  POP_JUMP_IF_FALSE   812  'to 812'

 L. 125       794  LOAD_GLOBAL              np
              796  LOAD_ATTR                ones
              798  LOAD_FAST                'start'
              800  LOAD_ATTR                size
              802  LOAD_GLOBAL              np
              804  LOAD_ATTR                int64
              806  LOAD_CONST               ('dtype',)
              808  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              810  STORE_FAST               'steps'
            812_0  COME_FROM           790  '790'

 L. 128       812  LOAD_LISTCOMP            '<code_object <listcomp>>'
              814  LOAD_STR                 'Slice.infer.<locals>.<listcomp>'
              816  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              818  LOAD_GLOBAL              range
              820  LOAD_GLOBAL              len
              822  LOAD_FAST                'node'
              824  LOAD_METHOD              in_node
              826  CALL_METHOD_0         0  '0 positional arguments'
              828  LOAD_ATTR                shape
              830  CALL_FUNCTION_1       1  '1 positional argument'
              832  CALL_FUNCTION_1       1  '1 positional argument'
              834  GET_ITER         
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  STORE_FAST               'slice_idx'

 L. 129       840  LOAD_LISTCOMP            '<code_object <listcomp>>'
              842  LOAD_STR                 'Slice.infer.<locals>.<listcomp>'
              844  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              846  LOAD_GLOBAL              range
              848  LOAD_GLOBAL              len
              850  LOAD_FAST                'node'
              852  LOAD_METHOD              in_node
              854  CALL_METHOD_0         0  '0 positional arguments'
              856  LOAD_ATTR                shape
              858  CALL_FUNCTION_1       1  '1 positional argument'
              860  CALL_FUNCTION_1       1  '1 positional argument'
              862  GET_ITER         
              864  CALL_FUNCTION_1       1  '1 positional argument'
              866  STORE_FAST               'shrink_axis_mask'

 L. 130       868  SETUP_LOOP          924  'to 924'
              870  LOAD_GLOBAL              range
              872  LOAD_GLOBAL              len
              874  LOAD_FAST                'axis'
              876  CALL_FUNCTION_1       1  '1 positional argument'
              878  CALL_FUNCTION_1       1  '1 positional argument'
              880  GET_ITER         
              882  FOR_ITER            922  'to 922'
              884  STORE_FAST               'id'

 L. 132       886  LOAD_GLOBAL              slice
              888  LOAD_FAST                'start'
              890  LOAD_FAST                'id'
              892  BINARY_SUBSCR    
              894  LOAD_FAST                'end'
              896  LOAD_FAST                'id'
              898  BINARY_SUBSCR    
              900  LOAD_FAST                'steps'
              902  LOAD_FAST                'id'
              904  BINARY_SUBSCR    
              906  CALL_FUNCTION_3       3  '3 positional arguments'
              908  LOAD_FAST                'slice_idx'
              910  LOAD_FAST                'axis'
              912  LOAD_FAST                'id'
              914  BINARY_SUBSCR    
              916  STORE_SUBSCR     
          918_920  JUMP_BACK           882  'to 882'
              922  POP_BLOCK        
            924_0  COME_FROM_LOOP      868  '868'

 L. 135       924  SETUP_LOOP          978  'to 978'
              926  LOAD_GLOBAL              enumerate
              928  LOAD_FAST                'slice_idx'
              930  CALL_FUNCTION_1       1  '1 positional argument'
              932  GET_ITER         
            934_0  COME_FROM           948  '948'
              934  FOR_ITER            976  'to 976'
              936  UNPACK_SEQUENCE_2     2 
              938  STORE_FAST               'axis'
              940  STORE_FAST               's'

 L. 136       942  LOAD_FAST                's'
              944  LOAD_CONST               None
              946  COMPARE_OP               is
          948_950  POP_JUMP_IF_FALSE   934  'to 934'

 L. 137       952  LOAD_GLOBAL              slice
              954  LOAD_CONST               0
              956  LOAD_FAST                'input_shape'
              958  LOAD_FAST                'axis'
              960  BINARY_SUBSCR    
              962  LOAD_CONST               1
              964  CALL_FUNCTION_3       3  '3 positional arguments'
              966  LOAD_FAST                'slice_idx'
              968  LOAD_FAST                'axis'
              970  STORE_SUBSCR     
          972_974  JUMP_BACK           934  'to 934'
              976  POP_BLOCK        
            978_0  COME_FROM_LOOP      924  '924'

 L. 140       978  LOAD_GLOBAL              np
              980  LOAD_METHOD              array
              982  LOAD_FAST                'slice_idx'
              984  CALL_METHOD_1         1  '1 positional argument'
              986  LOAD_FAST                'node'
              988  LOAD_STR                 'slices'
              990  STORE_SUBSCR     

 L. 141       992  LOAD_GLOBAL              np
              994  LOAD_METHOD              array
              996  LOAD_FAST                'shrink_axis_mask'
              998  CALL_METHOD_1         1  '1 positional argument'
             1000  LOAD_FAST                'node'
             1002  LOAD_STR                 'shrink_axis_mask'
             1004  STORE_SUBSCR     

 L. 143      1006  LOAD_FAST                'value'
             1008  LOAD_GLOBAL              tuple
             1010  LOAD_FAST                'slice_idx'
             1012  CALL_FUNCTION_1       1  '1 positional argument'
             1014  BINARY_SUBSCR    
             1016  STORE_FAST               'value'

 L. 144      1018  LOAD_FAST                'node'
             1020  LOAD_METHOD              in_node
             1022  LOAD_CONST               0
             1024  CALL_METHOD_1         1  '1 positional argument'
             1026  LOAD_ATTR                value
             1028  LOAD_CONST               None
             1030  COMPARE_OP               is-not
         1032_1034  POP_JUMP_IF_FALSE  1044  'to 1044'
             1036  LOAD_FAST                'value'
             1038  LOAD_METHOD              copy
             1040  CALL_METHOD_0         0  '0 positional arguments'
             1042  JUMP_FORWARD       1046  'to 1046'
           1044_0  COME_FROM          1032  '1032'
             1044  LOAD_CONST               None
           1046_0  COME_FROM          1042  '1042'
             1046  LOAD_FAST                'node'
             1048  LOAD_METHOD              out_node
             1050  CALL_METHOD_0         0  '0 positional arguments'
             1052  STORE_ATTR               value

 L. 145      1054  LOAD_GLOBAL              np
             1056  LOAD_METHOD              array
             1058  LOAD_FAST                'value'
             1060  LOAD_ATTR                shape
             1062  CALL_METHOD_1         1  '1 positional argument'
             1064  LOAD_FAST                'node'
             1066  LOAD_METHOD              out_node
             1068  CALL_METHOD_0         0  '0 positional arguments'
             1070  STORE_ATTR               shape

Parse error at or near `COME_FROM' instruction at offset 626_0