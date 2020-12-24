# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/visualize/visualize.py
# Compiled at: 2019-11-29 02:38:56
# Size of source mod 2**32: 10149 bytes
"""Utilities related to model visualization."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
from keras.layers.wrappers import Wrapper
from keras.models import Model
try:
    import pydot_ng as pydot
except ImportError:
    pydot = None

def _check_pydot():
    """Raise errors if `pydot` or GraphViz unavailable."""
    if pydot is None:
        raise ImportError('Failed to import `pydot`. Please install `pydot`. For example with `pip install pydot`.')
    try:
        pydot.Dot.create(pydot.Dot())
    except OSError:
        raise OSError('`pydot` failed to call GraphViz.Please install GraphViz (https://www.graphviz.org/) and ensure that its executables are in the $PATH.')


def is_model(layer):
    return isinstance(layer, Model)


def is_wrapped_model(layer):
    return isinstance(layer, Wrapper) and isinstance(layer.layer, Model)


def add_edge(dot, src, dst):
    if not dot.get_edge(src, dst):
        dot.add_edge(pydot.Edge(src, dst))


def model_to_dot--- This code section failed: ---

 L.  74         0  LOAD_CONST               0
                2  LOAD_CONST               ('Wrapper',)
                4  IMPORT_NAME_ATTR         keras.layers.wrappers
                6  IMPORT_FROM              Wrapper
                8  STORE_FAST               'Wrapper'
               10  POP_TOP          

 L.  75        12  LOAD_CONST               0
               14  LOAD_CONST               ('Model',)
               16  IMPORT_NAME_ATTR         keras.models
               18  IMPORT_FROM              Model
               20  STORE_FAST               'Model'
               22  POP_TOP          

 L.  76        24  LOAD_CONST               0
               26  LOAD_CONST               ('Sequential',)
               28  IMPORT_NAME_ATTR         keras.models
               30  IMPORT_FROM              Sequential
               32  STORE_FAST               'Sequential'
               34  POP_TOP          

 L.  78        36  LOAD_GLOBAL              _check_pydot
               38  CALL_FUNCTION_0       0  '0 positional arguments'
               40  POP_TOP          

 L.  79        42  LOAD_FAST                'subgraph'
               44  POP_JUMP_IF_FALSE    90  'to 90'

 L.  80        46  LOAD_GLOBAL              pydot
               48  LOAD_ATTR                Cluster
               50  LOAD_STR                 'dashed'
               52  LOAD_FAST                'model'
               54  LOAD_ATTR                name
               56  LOAD_CONST               ('style', 'graph_name')
               58  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               60  STORE_FAST               'dot'

 L.  81        62  LOAD_FAST                'dot'
               64  LOAD_METHOD              set
               66  LOAD_STR                 'label'
               68  LOAD_FAST                'model'
               70  LOAD_ATTR                name
               72  CALL_METHOD_2         2  '2 positional arguments'
               74  POP_TOP          

 L.  82        76  LOAD_FAST                'dot'
               78  LOAD_METHOD              set
               80  LOAD_STR                 'labeljust'
               82  LOAD_STR                 'l'
               84  CALL_METHOD_2         2  '2 positional arguments'
               86  POP_TOP          
               88  JUMP_FORWARD        146  'to 146'
             90_0  COME_FROM            44  '44'

 L.  84        90  LOAD_GLOBAL              pydot
               92  LOAD_METHOD              Dot
               94  CALL_METHOD_0         0  '0 positional arguments'
               96  STORE_FAST               'dot'

 L.  85        98  LOAD_FAST                'dot'
              100  LOAD_METHOD              set
              102  LOAD_STR                 'rankdir'
              104  LOAD_FAST                'rankdir'
              106  CALL_METHOD_2         2  '2 positional arguments'
              108  POP_TOP          

 L.  86       110  LOAD_FAST                'dot'
              112  LOAD_METHOD              set
              114  LOAD_STR                 'concentrate'
              116  LOAD_CONST               True
              118  CALL_METHOD_2         2  '2 positional arguments'
              120  POP_TOP          

 L.  87       122  LOAD_FAST                'dot'
              124  LOAD_METHOD              set
              126  LOAD_STR                 'dpi'
              128  LOAD_FAST                'dpi'
              130  CALL_METHOD_2         2  '2 positional arguments'
              132  POP_TOP          

 L.  88       134  LOAD_FAST                'dot'
              136  LOAD_ATTR                set_node_defaults
              138  LOAD_STR                 'record'
              140  LOAD_CONST               ('shape',)
              142  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              144  POP_TOP          
            146_0  COME_FROM            88  '88'

 L.  90       146  BUILD_MAP_0           0 
              148  STORE_FAST               'sub_n_first_node'

 L.  91       150  BUILD_MAP_0           0 
              152  STORE_FAST               'sub_n_last_node'

 L.  92       154  BUILD_MAP_0           0 
              156  STORE_FAST               'sub_w_first_node'

 L.  93       158  BUILD_MAP_0           0 
              160  STORE_FAST               'sub_w_last_node'

 L.  95       162  LOAD_GLOBAL              isinstance
              164  LOAD_FAST                'model'
              166  LOAD_FAST                'Sequential'
              168  CALL_FUNCTION_2       2  '2 positional arguments'
              170  POP_JUMP_IF_FALSE   186  'to 186'

 L.  96       172  LOAD_FAST                'model'
              174  LOAD_ATTR                built
              176  POP_JUMP_IF_TRUE    186  'to 186'

 L.  97       178  LOAD_FAST                'model'
              180  LOAD_METHOD              build
              182  CALL_METHOD_0         0  '0 positional arguments'
              184  POP_TOP          
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           170  '170'

 L.  98       186  LOAD_FAST                'model'
              188  LOAD_ATTR                _layers
              190  STORE_FAST               'layers'

 L. 101   192_194  SETUP_LOOP          662  'to 662'
              196  LOAD_GLOBAL              enumerate
              198  LOAD_FAST                'layers'
              200  CALL_FUNCTION_1       1  '1 positional argument'
              202  GET_ITER         
            204_0  COME_FROM           632  '632'
          204_206  FOR_ITER            660  'to 660'
              208  UNPACK_SEQUENCE_2     2 
              210  STORE_FAST               'i'
              212  STORE_FAST               'layer'

 L. 102       214  LOAD_GLOBAL              str
              216  LOAD_GLOBAL              id
              218  LOAD_FAST                'layer'
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  STORE_FAST               'layer_id'

 L. 105       226  LOAD_FAST                'layer'
              228  LOAD_ATTR                name
              230  STORE_FAST               'layer_name'

 L. 106       232  LOAD_FAST                'layer'
              234  LOAD_ATTR                __class__
              236  LOAD_ATTR                __name__
              238  STORE_FAST               'class_name'

 L. 108       240  LOAD_GLOBAL              isinstance
              242  LOAD_FAST                'layer'
              244  LOAD_FAST                'Wrapper'
              246  CALL_FUNCTION_2       2  '2 positional arguments'
          248_250  POP_JUMP_IF_FALSE   384  'to 384'

 L. 109       252  LOAD_FAST                'expand_nested'
          254_256  POP_JUMP_IF_FALSE   346  'to 346'
              258  LOAD_GLOBAL              isinstance
              260  LOAD_FAST                'layer'
              262  LOAD_ATTR                layer
              264  LOAD_FAST                'Model'
              266  CALL_FUNCTION_2       2  '2 positional arguments'
          268_270  POP_JUMP_IF_FALSE   346  'to 346'

 L. 110       272  LOAD_GLOBAL              model_to_dot
              274  LOAD_FAST                'layer'
              276  LOAD_ATTR                layer
              278  LOAD_FAST                'show_shapes'

 L. 111       280  LOAD_FAST                'show_layer_names'
              282  LOAD_FAST                'rankdir'

 L. 112       284  LOAD_FAST                'expand_nested'

 L. 113       286  LOAD_CONST               True
              288  LOAD_CONST               ('subgraph',)
              290  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              292  STORE_FAST               'submodel_wrapper'

 L. 115       294  LOAD_FAST                'submodel_wrapper'
              296  LOAD_METHOD              get_nodes
              298  CALL_METHOD_0         0  '0 positional arguments'
              300  STORE_FAST               'sub_w_nodes'

 L. 116       302  LOAD_FAST                'sub_w_nodes'
              304  LOAD_CONST               0
              306  BINARY_SUBSCR    
              308  LOAD_FAST                'sub_w_first_node'
              310  LOAD_FAST                'layer'
              312  LOAD_ATTR                layer
              314  LOAD_ATTR                name
              316  STORE_SUBSCR     

 L. 117       318  LOAD_FAST                'sub_w_nodes'
              320  LOAD_CONST               -1
              322  BINARY_SUBSCR    
              324  LOAD_FAST                'sub_w_last_node'
              326  LOAD_FAST                'layer'
              328  LOAD_ATTR                layer
              330  LOAD_ATTR                name
              332  STORE_SUBSCR     

 L. 118       334  LOAD_FAST                'dot'
              336  LOAD_METHOD              add_subgraph
              338  LOAD_FAST                'submodel_wrapper'
              340  CALL_METHOD_1         1  '1 positional argument'
              342  POP_TOP          
              344  JUMP_FORWARD        384  'to 384'
            346_0  COME_FROM           268  '268'
            346_1  COME_FROM           254  '254'

 L. 120       346  LOAD_STR                 '{}({})'
              348  LOAD_METHOD              format
              350  LOAD_FAST                'layer_name'
              352  LOAD_FAST                'layer'
              354  LOAD_ATTR                layer
              356  LOAD_ATTR                name
              358  CALL_METHOD_2         2  '2 positional arguments'
              360  STORE_FAST               'layer_name'

 L. 121       362  LOAD_FAST                'layer'
              364  LOAD_ATTR                layer
              366  LOAD_ATTR                __class__
              368  LOAD_ATTR                __name__
              370  STORE_FAST               'child_class_name'

 L. 122       372  LOAD_STR                 '{}({})'
              374  LOAD_METHOD              format
              376  LOAD_FAST                'class_name'
              378  LOAD_FAST                'child_class_name'
              380  CALL_METHOD_2         2  '2 positional arguments'
              382  STORE_FAST               'class_name'
            384_0  COME_FROM           344  '344'
            384_1  COME_FROM           248  '248'

 L. 124       384  LOAD_FAST                'expand_nested'
          386_388  POP_JUMP_IF_FALSE   468  'to 468'
              390  LOAD_GLOBAL              isinstance
              392  LOAD_FAST                'layer'
              394  LOAD_FAST                'Model'
              396  CALL_FUNCTION_2       2  '2 positional arguments'
          398_400  POP_JUMP_IF_FALSE   468  'to 468'

 L. 125       402  LOAD_GLOBAL              model_to_dot
              404  LOAD_FAST                'layer'
              406  LOAD_FAST                'show_shapes'

 L. 126       408  LOAD_FAST                'show_layer_names'
              410  LOAD_FAST                'rankdir'

 L. 127       412  LOAD_FAST                'expand_nested'

 L. 128       414  LOAD_CONST               True
              416  LOAD_CONST               ('subgraph',)
              418  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              420  STORE_FAST               'submodel_not_wrapper'

 L. 130       422  LOAD_FAST                'submodel_not_wrapper'
              424  LOAD_METHOD              get_nodes
              426  CALL_METHOD_0         0  '0 positional arguments'
              428  STORE_FAST               'sub_n_nodes'

 L. 131       430  LOAD_FAST                'sub_n_nodes'
              432  LOAD_CONST               0
              434  BINARY_SUBSCR    
              436  LOAD_FAST                'sub_n_first_node'
              438  LOAD_FAST                'layer'
              440  LOAD_ATTR                name
              442  STORE_SUBSCR     

 L. 132       444  LOAD_FAST                'sub_n_nodes'
              446  LOAD_CONST               -1
              448  BINARY_SUBSCR    
              450  LOAD_FAST                'sub_n_last_node'
              452  LOAD_FAST                'layer'
              454  LOAD_ATTR                name
              456  STORE_SUBSCR     

 L. 133       458  LOAD_FAST                'dot'
              460  LOAD_METHOD              add_subgraph
              462  LOAD_FAST                'submodel_not_wrapper'
              464  CALL_METHOD_1         1  '1 positional argument'
              466  POP_TOP          
            468_0  COME_FROM           398  '398'
            468_1  COME_FROM           386  '386'

 L. 136       468  LOAD_FAST                'show_layer_names'
          470_472  POP_JUMP_IF_FALSE   488  'to 488'

 L. 137       474  LOAD_STR                 '{}: {}'
              476  LOAD_METHOD              format
              478  LOAD_FAST                'layer_name'
              480  LOAD_FAST                'class_name'
              482  CALL_METHOD_2         2  '2 positional arguments'
              484  STORE_FAST               'label'
              486  JUMP_FORWARD        492  'to 492'
            488_0  COME_FROM           470  '470'

 L. 139       488  LOAD_FAST                'class_name'
              490  STORE_FAST               'label'
            492_0  COME_FROM           486  '486'

 L. 142       492  LOAD_FAST                'show_shapes'
          494_496  POP_JUMP_IF_FALSE   618  'to 618'

 L. 143       498  SETUP_EXCEPT        514  'to 514'

 L. 144       500  LOAD_GLOBAL              str
              502  LOAD_FAST                'layer'
              504  LOAD_ATTR                output_shape
              506  CALL_FUNCTION_1       1  '1 positional argument'
              508  STORE_FAST               'outputlabels'
              510  POP_BLOCK        
              512  JUMP_FORWARD        540  'to 540'
            514_0  COME_FROM_EXCEPT    498  '498'

 L. 145       514  DUP_TOP          
              516  LOAD_GLOBAL              AttributeError
              518  COMPARE_OP               exception-match
          520_522  POP_JUMP_IF_FALSE   538  'to 538'
              524  POP_TOP          
              526  POP_TOP          
              528  POP_TOP          

 L. 146       530  LOAD_STR                 'multiple'
              532  STORE_FAST               'outputlabels'
              534  POP_EXCEPT       
              536  JUMP_FORWARD        540  'to 540'
            538_0  COME_FROM           520  '520'
              538  END_FINALLY      
            540_0  COME_FROM           536  '536'
            540_1  COME_FROM           512  '512'

 L. 147       540  LOAD_GLOBAL              hasattr
              542  LOAD_FAST                'layer'
              544  LOAD_STR                 'input_shape'
              546  CALL_FUNCTION_2       2  '2 positional arguments'
          548_550  POP_JUMP_IF_FALSE   564  'to 564'

 L. 148       552  LOAD_GLOBAL              str
              554  LOAD_FAST                'layer'
              556  LOAD_ATTR                input_shape
              558  CALL_FUNCTION_1       1  '1 positional argument'
              560  STORE_FAST               'inputlabels'
              562  JUMP_FORWARD        604  'to 604'
            564_0  COME_FROM           548  '548'

 L. 149       564  LOAD_GLOBAL              hasattr
              566  LOAD_FAST                'layer'
              568  LOAD_STR                 'input_shapes'
              570  CALL_FUNCTION_2       2  '2 positional arguments'
          572_574  POP_JUMP_IF_FALSE   600  'to 600'

 L. 150       576  LOAD_STR                 ', '
              578  LOAD_METHOD              join

 L. 151       580  LOAD_LISTCOMP            '<code_object <listcomp>>'
              582  LOAD_STR                 'model_to_dot.<locals>.<listcomp>'
              584  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              586  LOAD_FAST                'layer'
              588  LOAD_ATTR                input_shapes
              590  GET_ITER         
              592  CALL_FUNCTION_1       1  '1 positional argument'
              594  CALL_METHOD_1         1  '1 positional argument'
              596  STORE_FAST               'inputlabels'
              598  JUMP_FORWARD        604  'to 604'
            600_0  COME_FROM           572  '572'

 L. 153       600  LOAD_STR                 'multiple'
              602  STORE_FAST               'inputlabels'
            604_0  COME_FROM           598  '598'
            604_1  COME_FROM           562  '562'

 L. 154       604  LOAD_STR                 '%s\n|{input:|output:}|{{%s}|{%s}}'
              606  LOAD_FAST                'label'

 L. 155       608  LOAD_FAST                'inputlabels'

 L. 156       610  LOAD_FAST                'outputlabels'
              612  BUILD_TUPLE_3         3 
              614  BINARY_MODULO    
              616  STORE_FAST               'label'
            618_0  COME_FROM           494  '494'

 L. 158       618  LOAD_FAST                'expand_nested'
          620_622  POP_JUMP_IF_FALSE   634  'to 634'
              624  LOAD_GLOBAL              isinstance
              626  LOAD_FAST                'layer'
              628  LOAD_FAST                'Model'
              630  CALL_FUNCTION_2       2  '2 positional arguments'
              632  POP_JUMP_IF_TRUE    204  'to 204'
            634_0  COME_FROM           620  '620'

 L. 159       634  LOAD_GLOBAL              pydot
              636  LOAD_ATTR                Node
              638  LOAD_FAST                'layer_id'
              640  LOAD_FAST                'label'
              642  LOAD_CONST               ('label',)
              644  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              646  STORE_FAST               'node'

 L. 160       648  LOAD_FAST                'dot'
              650  LOAD_METHOD              add_node
              652  LOAD_FAST                'node'
              654  CALL_METHOD_1         1  '1 positional argument'
              656  POP_TOP          
              658  JUMP_BACK           204  'to 204'
              660  POP_BLOCK        
            662_0  COME_FROM_LOOP      192  '192'

 L. 163   662_664  SETUP_LOOP         1142  'to 1142'
              666  LOAD_FAST                'layers'
              668  GET_ITER         
          670_672  FOR_ITER           1140  'to 1140'
              674  STORE_FAST               'layer'

 L. 164       676  LOAD_GLOBAL              str
              678  LOAD_GLOBAL              id
              680  LOAD_FAST                'layer'
              682  CALL_FUNCTION_1       1  '1 positional argument'
              684  CALL_FUNCTION_1       1  '1 positional argument'
              686  STORE_FAST               'layer_id'

 L. 165   688_690  SETUP_LOOP         1136  'to 1136'
              692  LOAD_GLOBAL              enumerate
              694  LOAD_FAST                'layer'
              696  LOAD_ATTR                _inbound_nodes
              698  CALL_FUNCTION_1       1  '1 positional argument'
              700  GET_ITER         
            702_0  COME_FROM           744  '744'
          702_704  FOR_ITER           1134  'to 1134'
              706  UNPACK_SEQUENCE_2     2 
              708  STORE_FAST               'i'
              710  STORE_FAST               'node'

 L. 166       712  LOAD_FAST                'layer'
              714  LOAD_ATTR                name
              716  LOAD_STR                 '_ib-'
              718  BINARY_ADD       
              720  LOAD_GLOBAL              str
              722  LOAD_FAST                'i'
              724  CALL_FUNCTION_1       1  '1 positional argument'
              726  BINARY_ADD       
              728  STORE_FAST               'node_key'

 L. 167       730  LOAD_CONST               True
          732_734  POP_JUMP_IF_TRUE    748  'to 748'
              736  LOAD_FAST                'node_key'
              738  LOAD_FAST                'model'
              740  LOAD_ATTR                _network_nodes
              742  COMPARE_OP               in
          744_746  POP_JUMP_IF_FALSE   702  'to 702'
            748_0  COME_FROM           732  '732'

 L. 168   748_750  SETUP_LOOP         1130  'to 1130'
              752  LOAD_FAST                'node'
              754  LOAD_ATTR                inbound_layers
              756  GET_ITER         
            758_0  COME_FROM          1092  '1092'
          758_760  FOR_ITER           1128  'to 1128'
              762  STORE_FAST               'inbound_layer'

 L. 169       764  LOAD_GLOBAL              str
              766  LOAD_GLOBAL              id
              768  LOAD_FAST                'inbound_layer'
              770  CALL_FUNCTION_1       1  '1 positional argument'
              772  CALL_FUNCTION_1       1  '1 positional argument'
              774  STORE_FAST               'inbound_layer_id'

 L. 170       776  LOAD_FAST                'expand_nested'
          778_780  POP_JUMP_IF_TRUE    836  'to 836'

 L. 171       782  LOAD_FAST                'dot'
              784  LOAD_METHOD              get_node
              786  LOAD_FAST                'inbound_layer_id'
              788  CALL_METHOD_1         1  '1 positional argument'
          790_792  POP_JUMP_IF_TRUE    798  'to 798'
              794  LOAD_ASSERT              AssertionError
              796  RAISE_VARARGS_1       1  'exception instance'
            798_0  COME_FROM           790  '790'

 L. 172       798  LOAD_FAST                'dot'
              800  LOAD_METHOD              get_node
              802  LOAD_FAST                'layer_id'
              804  CALL_METHOD_1         1  '1 positional argument'
          806_808  POP_JUMP_IF_TRUE    814  'to 814'
              810  LOAD_ASSERT              AssertionError
              812  RAISE_VARARGS_1       1  'exception instance'
            814_0  COME_FROM           806  '806'

 L. 173       814  LOAD_FAST                'dot'
              816  LOAD_METHOD              add_edge
              818  LOAD_GLOBAL              pydot
              820  LOAD_METHOD              Edge
              822  LOAD_FAST                'inbound_layer_id'
              824  LOAD_FAST                'layer_id'
              826  CALL_METHOD_2         2  '2 positional arguments'
              828  CALL_METHOD_1         1  '1 positional argument'
              830  POP_TOP          
          832_834  JUMP_BACK           758  'to 758'
            836_0  COME_FROM           778  '778'

 L. 176       836  LOAD_GLOBAL              is_model
              838  LOAD_FAST                'inbound_layer'
              840  CALL_FUNCTION_1       1  '1 positional argument'
          842_844  POP_JUMP_IF_TRUE   1010  'to 1010'

 L. 177       846  LOAD_GLOBAL              is_wrapped_model
              848  LOAD_FAST                'inbound_layer'
              850  CALL_FUNCTION_1       1  '1 positional argument'
          852_854  POP_JUMP_IF_TRUE   1010  'to 1010'

 L. 179       856  LOAD_GLOBAL              is_model
              858  LOAD_FAST                'layer'
              860  CALL_FUNCTION_1       1  '1 positional argument'
          862_864  POP_JUMP_IF_TRUE    912  'to 912'

 L. 180       866  LOAD_GLOBAL              is_wrapped_model
              868  LOAD_FAST                'layer'
              870  CALL_FUNCTION_1       1  '1 positional argument'
          872_874  POP_JUMP_IF_TRUE    912  'to 912'

 L. 182       876  LOAD_FAST                'dot'
              878  LOAD_METHOD              get_node
              880  LOAD_FAST                'layer_id'
              882  CALL_METHOD_1         1  '1 positional argument'
          884_886  POP_JUMP_IF_TRUE    892  'to 892'
              888  LOAD_ASSERT              AssertionError
              890  RAISE_VARARGS_1       1  'exception instance'
            892_0  COME_FROM           884  '884'

 L. 183       892  LOAD_FAST                'dot'
              894  LOAD_METHOD              add_edge
              896  LOAD_GLOBAL              pydot
              898  LOAD_METHOD              Edge
              900  LOAD_FAST                'inbound_layer_id'

 L. 184       902  LOAD_FAST                'layer_id'
              904  CALL_METHOD_2         2  '2 positional arguments'
              906  CALL_METHOD_1         1  '1 positional argument'
              908  POP_TOP          
              910  JUMP_FORWARD       1008  'to 1008'
            912_0  COME_FROM           872  '872'
            912_1  COME_FROM           862  '862'

 L. 186       912  LOAD_GLOBAL              is_model
              914  LOAD_FAST                'layer'
              916  CALL_FUNCTION_1       1  '1 positional argument'
          918_920  POP_JUMP_IF_FALSE   946  'to 946'

 L. 187       922  LOAD_GLOBAL              add_edge
              924  LOAD_FAST                'dot'
              926  LOAD_FAST                'inbound_layer_id'

 L. 188       928  LOAD_FAST                'sub_n_first_node'
              930  LOAD_FAST                'layer'
              932  LOAD_ATTR                name
              934  BINARY_SUBSCR    
              936  LOAD_METHOD              get_name
              938  CALL_METHOD_0         0  '0 positional arguments'
              940  CALL_FUNCTION_3       3  '3 positional arguments'
              942  POP_TOP          
              944  JUMP_FORWARD       1008  'to 1008'
            946_0  COME_FROM           918  '918'

 L. 190       946  LOAD_GLOBAL              is_wrapped_model
              948  LOAD_FAST                'layer'
              950  CALL_FUNCTION_1       1  '1 positional argument'
          952_954  POP_JUMP_IF_FALSE  1124  'to 1124'

 L. 191       956  LOAD_FAST                'dot'
              958  LOAD_METHOD              add_edge
              960  LOAD_GLOBAL              pydot
              962  LOAD_METHOD              Edge
              964  LOAD_FAST                'inbound_layer_id'

 L. 192       966  LOAD_FAST                'layer_id'
              968  CALL_METHOD_2         2  '2 positional arguments'
              970  CALL_METHOD_1         1  '1 positional argument'
              972  POP_TOP          

 L. 193       974  LOAD_FAST                'sub_w_first_node'
              976  LOAD_FAST                'layer'
              978  LOAD_ATTR                layer
              980  LOAD_ATTR                name
              982  BINARY_SUBSCR    
              984  LOAD_METHOD              get_name
              986  CALL_METHOD_0         0  '0 positional arguments'
              988  STORE_FAST               'name'

 L. 194       990  LOAD_FAST                'dot'
              992  LOAD_METHOD              add_edge
              994  LOAD_GLOBAL              pydot
              996  LOAD_METHOD              Edge
              998  LOAD_FAST                'layer_id'

 L. 195      1000  LOAD_FAST                'name'
             1002  CALL_METHOD_2         2  '2 positional arguments'
             1004  CALL_METHOD_1         1  '1 positional argument'
             1006  POP_TOP          
           1008_0  COME_FROM           944  '944'
           1008_1  COME_FROM           910  '910'
             1008  JUMP_BACK           758  'to 758'
           1010_0  COME_FROM           852  '852'
           1010_1  COME_FROM           842  '842'

 L. 197      1010  LOAD_GLOBAL              is_model
             1012  LOAD_FAST                'inbound_layer'
             1014  CALL_FUNCTION_1       1  '1 positional argument'
         1016_1018  POP_JUMP_IF_FALSE  1086  'to 1086'

 L. 198      1020  LOAD_FAST                'sub_n_last_node'
             1022  LOAD_FAST                'inbound_layer'
             1024  LOAD_ATTR                name
             1026  BINARY_SUBSCR    
             1028  LOAD_METHOD              get_name
             1030  CALL_METHOD_0         0  '0 positional arguments'
             1032  STORE_FAST               'name'

 L. 199      1034  LOAD_GLOBAL              is_model
             1036  LOAD_FAST                'layer'
             1038  CALL_FUNCTION_1       1  '1 positional argument'
         1040_1042  POP_JUMP_IF_FALSE  1072  'to 1072'

 L. 200      1044  LOAD_FAST                'sub_n_first_node'
             1046  LOAD_FAST                'layer'
             1048  LOAD_ATTR                name
             1050  BINARY_SUBSCR    
             1052  LOAD_METHOD              get_name
             1054  CALL_METHOD_0         0  '0 positional arguments'
             1056  STORE_FAST               'output_name'

 L. 201      1058  LOAD_GLOBAL              add_edge
             1060  LOAD_FAST                'dot'
             1062  LOAD_FAST                'name'
             1064  LOAD_FAST                'output_name'
             1066  CALL_FUNCTION_3       3  '3 positional arguments'
             1068  POP_TOP          
             1070  JUMP_FORWARD       1084  'to 1084'
           1072_0  COME_FROM          1040  '1040'

 L. 203      1072  LOAD_GLOBAL              add_edge
             1074  LOAD_FAST                'dot'
             1076  LOAD_FAST                'name'
             1078  LOAD_FAST                'layer_id'
             1080  CALL_FUNCTION_3       3  '3 positional arguments'
             1082  POP_TOP          
           1084_0  COME_FROM          1070  '1070'
             1084  JUMP_BACK           758  'to 758'
           1086_0  COME_FROM          1016  '1016'

 L. 205      1086  LOAD_GLOBAL              is_wrapped_model
             1088  LOAD_FAST                'inbound_layer'
             1090  CALL_FUNCTION_1       1  '1 positional argument'
         1092_1094  POP_JUMP_IF_FALSE   758  'to 758'

 L. 206      1096  LOAD_FAST                'inbound_layer'
             1098  LOAD_ATTR                layer
             1100  LOAD_ATTR                name
             1102  STORE_FAST               'inbound_layer_name'

 L. 207      1104  LOAD_GLOBAL              add_edge
             1106  LOAD_FAST                'dot'

 L. 208      1108  LOAD_FAST                'sub_w_last_node'
             1110  LOAD_FAST                'inbound_layer_name'
             1112  BINARY_SUBSCR    
             1114  LOAD_METHOD              get_name
             1116  CALL_METHOD_0         0  '0 positional arguments'

 L. 209      1118  LOAD_FAST                'layer_id'
             1120  CALL_FUNCTION_3       3  '3 positional arguments'
             1122  POP_TOP          
           1124_0  COME_FROM           952  '952'
         1124_1126  JUMP_BACK           758  'to 758'
             1128  POP_BLOCK        
           1130_0  COME_FROM_LOOP      748  '748'
         1130_1132  JUMP_BACK           702  'to 702'
             1134  POP_BLOCK        
           1136_0  COME_FROM_LOOP      688  '688'
         1136_1138  JUMP_BACK           670  'to 670'
             1140  POP_BLOCK        
           1142_0  COME_FROM_LOOP      662  '662'

 L. 210      1142  LOAD_FAST                'dot'
             1144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1010_1


def plot_model(model, to_file='model.png', show_shapes=False, show_layer_names=True, rankdir='TB', expand_nested=False, dpi=96, subgraph=False):
    """Converts a Keras model to dot format and save to a file.

    # Arguments
        model: A Keras model instance
        to_file: File name of the plot image.
        show_shapes: whether to display shape information.
        show_layer_names: whether to display layer names.
        rankdir: `rankdir` argument passed to PyDot,
            a string specifying the format of the plot:
            'TB' creates a vertical plot;
            'LR' creates a horizontal plot.
        expand_nested: whether to expand nested models into clusters.
        dpi: dot DPI.

    # Returns
        A Jupyter notebook Image object if Jupyter is installed.
        This enables in-line display of the model plots in notebooks.
    """
    dot = model_to_dot(model, show_shapes, show_layer_names, rankdir, expand_nested, dpi)
    _, extension = os.path.splitext(to_file)
    if not extension:
        extension = 'png'
    else:
        extension = extension[1:]
    dot.write(to_file, format=extension)
    if extension != 'pdf':
        try:
            from IPython import display
            return display.Image(filename=to_file)
        except ImportError:
            pass