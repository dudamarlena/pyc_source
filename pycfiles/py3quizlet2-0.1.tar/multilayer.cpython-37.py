# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/visualization/multilayer.py
# Compiled at: 2020-03-18 05:16:51
# Size of source mod 2**32: 15052 bytes
import networkx as nx
try:
    from matplotlib.patches import Rectangle
    from matplotlib.patches import Circle
except:
    pass

import random
import matplotlib.pyplot as plt
from . import colors
from . import bezier
from . import polyfit
from .layout_algorithms import *
from . import drawing_machinery
main_figure = plt.figure()
shape_subplot = main_figure.add_subplot(111)
import numpy as np

def draw_multilayer_default--- This code section failed: ---

 L.  58         0  LOAD_FAST                'background_color'
                2  LOAD_STR                 'default'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    32  'to 32'

 L.  60         8  LOAD_GLOBAL              colors
               10  LOAD_ATTR                linear_gradient
               12  LOAD_STR                 '#4286f4'
               14  LOAD_GLOBAL              len
               16  LOAD_FAST                'network_list'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_CONST               ('n',)
               22  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               24  LOAD_STR                 'hex'
               26  BINARY_SUBSCR    
               28  STORE_FAST               'facecolor_list_background'
               30  JUMP_FORWARD         68  'to 68'
             32_0  COME_FROM             6  '6'

 L.  62        32  LOAD_FAST                'background_color'
               34  LOAD_STR                 'rainbow'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L.  64        40  LOAD_GLOBAL              colors
               42  LOAD_ATTR                colors_default
               44  STORE_FAST               'facecolor_list_background'
               46  JUMP_FORWARD         68  'to 68'
             48_0  COME_FROM            38  '38'

 L.  66        48  LOAD_FAST                'background_color'
               50  LOAD_CONST               None
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    68  'to 68'

 L.  68        56  LOAD_GLOBAL              colors
               58  LOAD_ATTR                colors_default
               60  STORE_FAST               'facecolor_list_background'

 L.  69        62  LOAD_CONST               0
               64  STORE_FAST               'alphalevel'
               66  JUMP_FORWARD         68  'to 68'
             68_0  COME_FROM            66  '66'
             68_1  COME_FROM            54  '54'
             68_2  COME_FROM            46  '46'
             68_3  COME_FROM            30  '30'

 L.  74        68  LOAD_FAST                'networks_color'
               70  LOAD_STR                 'rainbow'
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE    84  'to 84'

 L.  76        76  LOAD_GLOBAL              colors
               78  LOAD_ATTR                colors_default
               80  STORE_FAST               'facecolor_list'
               82  JUMP_FORWARD        108  'to 108'
             84_0  COME_FROM            74  '74'

 L.  78        84  LOAD_FAST                'networks_color'
               86  LOAD_STR                 'black'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   108  'to 108'

 L.  80        92  LOAD_STR                 'black'
               94  BUILD_LIST_1          1 
               96  LOAD_GLOBAL              len
               98  LOAD_FAST                'network_list'
              100  CALL_FUNCTION_1       1  ''
              102  BINARY_MULTIPLY  
              104  STORE_FAST               'facecolor_list'
              106  JUMP_FORWARD        108  'to 108'
            108_0  COME_FROM           106  '106'
            108_1  COME_FROM            90  '90'
            108_2  COME_FROM            82  '82'

 L.  85       108  LOAD_CONST               0
              110  STORE_FAST               'start_location_network'

 L.  86       112  LOAD_CONST               0
              114  STORE_FAST               'start_location_background'

 L.  87       116  LOAD_CONST               0
              118  STORE_FAST               'color'

 L.  88       120  LOAD_CONST               0.5
              122  STORE_FAST               'shadow_size'

 L.  89       124  LOAD_CONST               1.05
              126  STORE_FAST               'circle_size'

 L.  91   128_130  SETUP_LOOP          732  'to 732'
              132  LOAD_FAST                'network_list'
              134  GET_ITER         
          136_138  FOR_ITER            730  'to 730'
              140  STORE_FAST               'network'

 L.  92       142  LOAD_FAST                'remove_isolated_nodes'
              144  POP_JUMP_IF_FALSE   178  'to 178'

 L.  93       146  LOAD_GLOBAL              list
              148  LOAD_GLOBAL              nx
              150  LOAD_METHOD              isolates
              152  LOAD_FAST                'network'
              154  CALL_METHOD_1         1  ''
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'isolates'

 L.  94       160  LOAD_FAST                'network'
              162  LOAD_METHOD              copy
              164  CALL_METHOD_0         0  ''
              166  STORE_FAST               'network'

 L.  95       168  LOAD_FAST                'network'
              170  LOAD_METHOD              remove_nodes_from
              172  LOAD_FAST                'isolates'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
            178_0  COME_FROM           144  '144'

 L.  97       178  LOAD_FAST                'verbose'
              180  POP_JUMP_IF_FALSE   196  'to 196'

 L.  98       182  LOAD_GLOBAL              print
              184  LOAD_GLOBAL              nx
              186  LOAD_METHOD              info
              188  LOAD_FAST                'network'
              190  CALL_METHOD_1         1  ''
              192  CALL_FUNCTION_1       1  ''
              194  POP_TOP          
            196_0  COME_FROM           180  '180'

 L.  99       196  LOAD_GLOBAL              dict
              198  LOAD_GLOBAL              nx
              200  LOAD_METHOD              degree
              202  LOAD_GLOBAL              nx
              204  LOAD_METHOD              Graph
              206  LOAD_FAST                'network'
              208  CALL_METHOD_1         1  ''
              210  CALL_METHOD_1         1  ''
              212  CALL_FUNCTION_1       1  ''
              214  STORE_FAST               'degrees'

 L. 100       216  LOAD_CONST               0
              218  STORE_FAST               'cntr'

 L. 101       220  LOAD_CONST               0
              222  STORE_FAST               'cntr_all'

 L. 102       224  BUILD_LIST_0          0 
              226  STORE_FAST               'no_position'

 L. 103       228  BUILD_LIST_0          0 
              230  STORE_FAST               'all_positions'

 L. 104       232  SETUP_LOOP          318  'to 318'
              234  LOAD_FAST                'network'
              236  LOAD_ATTR                nodes
              238  LOAD_CONST               True
              240  LOAD_CONST               ('data',)
              242  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              244  GET_ITER         
              246  FOR_ITER            316  'to 316'
              248  STORE_FAST               'node'

 L. 105       250  LOAD_STR                 'pos'
              252  LOAD_FAST                'node'
              254  LOAD_CONST               1
              256  BINARY_SUBSCR    
              258  COMPARE_OP               not-in
          260_262  POP_JUMP_IF_FALSE   288  'to 288'

 L. 106       264  LOAD_FAST                'no_position'
              266  LOAD_METHOD              append
              268  LOAD_FAST                'node'
              270  LOAD_CONST               0
              272  BINARY_SUBSCR    
              274  CALL_METHOD_1         1  ''
              276  POP_TOP          

 L. 107       278  LOAD_FAST                'cntr'
              280  LOAD_CONST               1
              282  INPLACE_ADD      
              284  STORE_FAST               'cntr'
              286  JUMP_BACK           246  'to 246'
            288_0  COME_FROM           260  '260'

 L. 109       288  LOAD_FAST                'all_positions'
              290  LOAD_METHOD              append
              292  LOAD_FAST                'node'
              294  LOAD_CONST               1
              296  BINARY_SUBSCR    
              298  LOAD_STR                 'pos'
              300  BINARY_SUBSCR    
              302  CALL_METHOD_1         1  ''
              304  POP_TOP          

 L. 110       306  LOAD_FAST                'cntr_all'
              308  LOAD_CONST               1
              310  INPLACE_ADD      
              312  STORE_FAST               'cntr_all'
              314  JUMP_BACK           246  'to 246'
              316  POP_BLOCK        
            318_0  COME_FROM_LOOP      232  '232'

 L. 112       318  LOAD_GLOBAL              len
              320  LOAD_FAST                'no_position'
              322  CALL_FUNCTION_1       1  ''
              324  LOAD_CONST               0
              326  COMPARE_OP               >
          328_330  POP_JUMP_IF_FALSE   350  'to 350'

 L. 113       332  LOAD_FAST                'network'
              334  LOAD_METHOD              copy
              336  CALL_METHOD_0         0  ''
              338  STORE_FAST               'network'

 L. 114       340  LOAD_FAST                'network'
              342  LOAD_METHOD              remove_nodes_from
              344  LOAD_FAST                'no_position'
              346  CALL_METHOD_1         1  ''
              348  POP_TOP          
            350_0  COME_FROM           328  '328'

 L. 116       350  LOAD_GLOBAL              nx
              352  LOAD_METHOD              get_node_attributes
              354  LOAD_FAST                'network'
              356  LOAD_STR                 'pos'
              358  CALL_METHOD_2         2  ''
              360  STORE_FAST               'positions'

 L. 117       362  LOAD_CONST               0
              364  STORE_FAST               'cntr'

 L. 119       366  SETUP_LOOP          398  'to 398'
              368  LOAD_FAST                'positions'
              370  LOAD_METHOD              items
              372  CALL_METHOD_0         0  ''
              374  GET_ITER         
              376  FOR_ITER            396  'to 396'
              378  UNPACK_SEQUENCE_2     2 
              380  STORE_FAST               'node'
              382  STORE_FAST               'position'

 L. 120       384  LOAD_FAST                'position'
              386  LOAD_FAST                'start_location_network'
              388  INPLACE_ADD      
              390  STORE_FAST               'position'
          392_394  JUMP_BACK           376  'to 376'
              396  POP_BLOCK        
            398_0  COME_FROM_LOOP      366  '366'

 L. 123       398  LOAD_FAST                'labels'
              400  LOAD_CONST               False
              402  COMPARE_OP               !=
          404_406  POP_JUMP_IF_FALSE   484  'to 484'

 L. 124       408  SETUP_EXCEPT        440  'to 440'

 L. 125       410  LOAD_GLOBAL              shape_subplot
              412  LOAD_METHOD              text
              414  LOAD_FAST                'start_location_network'
              416  LOAD_FAST                'label_position'
              418  BINARY_ADD       
              420  LOAD_FAST                'start_location_network'
              422  LOAD_FAST                'label_position'
              424  BINARY_SUBTRACT  
              426  LOAD_FAST                'labels'
              428  LOAD_FAST                'color'
              430  BINARY_SUBSCR    
              432  CALL_METHOD_3         3  ''
              434  POP_TOP          
              436  POP_BLOCK        
              438  JUMP_FORWARD        484  'to 484'
            440_0  COME_FROM_EXCEPT    408  '408'

 L. 126       440  DUP_TOP          
              442  LOAD_GLOBAL              Exception
              444  COMPARE_OP               exception-match
          446_448  POP_JUMP_IF_FALSE   482  'to 482'
              450  POP_TOP          
              452  STORE_FAST               'es'
              454  POP_TOP          
              456  SETUP_FINALLY       470  'to 470'

 L. 127       458  LOAD_GLOBAL              print
              460  LOAD_FAST                'es'
              462  CALL_FUNCTION_1       1  ''
              464  POP_TOP          
              466  POP_BLOCK        
              468  LOAD_CONST               None
            470_0  COME_FROM_FINALLY   456  '456'
              470  LOAD_CONST               None
              472  STORE_FAST               'es'
              474  DELETE_FAST              'es'
              476  END_FINALLY      
              478  POP_EXCEPT       
              480  JUMP_FORWARD        484  'to 484'
            482_0  COME_FROM           446  '446'
              482  END_FINALLY      
            484_0  COME_FROM           480  '480'
            484_1  COME_FROM           438  '438'
            484_2  COME_FROM           404  '404'

 L. 129       484  LOAD_FAST                'background_shape'
              486  LOAD_STR                 'rectangle'
              488  COMPARE_OP               ==
          490_492  POP_JUMP_IF_FALSE   532  'to 532'

 L. 130       494  LOAD_GLOBAL              shape_subplot
              496  LOAD_METHOD              add_patch
              498  LOAD_GLOBAL              Rectangle

 L. 131       500  LOAD_FAST                'start_location_background'
              502  LOAD_FAST                'start_location_background'
              504  BUILD_TUPLE_2         2 
              506  LOAD_FAST                'rectanglex'
              508  LOAD_FAST                'rectangley'

 L. 132       510  LOAD_FAST                'alphalevel'
              512  LOAD_STR                 'dotted'
              514  LOAD_CONST               True
              516  LOAD_FAST                'facecolor_list_background'
              518  LOAD_FAST                'color'
              520  BINARY_SUBSCR    
              522  LOAD_CONST               ('alpha', 'linestyle', 'fill', 'facecolor')
              524  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              526  CALL_METHOD_1         1  ''
              528  POP_TOP          
              530  JUMP_FORWARD        582  'to 582'
            532_0  COME_FROM           490  '490'

 L. 134       532  LOAD_FAST                'background_shape'
              534  LOAD_STR                 'circle'
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   582  'to 582'

 L. 135       542  LOAD_GLOBAL              shape_subplot
              544  LOAD_METHOD              add_patch
              546  LOAD_GLOBAL              Circle
              548  LOAD_FAST                'start_location_background'
              550  LOAD_FAST                'shadow_size'
              552  BINARY_ADD       
              554  LOAD_FAST                'start_location_background'
              556  LOAD_FAST                'shadow_size'
              558  BINARY_ADD       
              560  BUILD_TUPLE_2         2 
              562  LOAD_FAST                'circle_size'
              564  LOAD_FAST                'facecolor_list_background'
              566  LOAD_FAST                'color'
              568  BINARY_SUBSCR    
              570  LOAD_FAST                'alphalevel'
              572  LOAD_CONST               ('color', 'alpha')
              574  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          
              580  JUMP_FORWARD        582  'to 582'
            582_0  COME_FROM           580  '580'
            582_1  COME_FROM           538  '538'
            582_2  COME_FROM           530  '530'

 L. 139       582  LOAD_FAST                'start_location_network'
              584  LOAD_CONST               1.5
              586  INPLACE_ADD      
              588  STORE_FAST               'start_location_network'

 L. 140       590  LOAD_FAST                'start_location_background'
              592  LOAD_CONST               1.5
              594  INPLACE_ADD      
              596  STORE_FAST               'start_location_background'

 L. 146       598  LOAD_FAST                'scale_by_size'
          600_602  POP_JUMP_IF_FALSE   628  'to 628'

 L. 147       604  LOAD_CLOSURE             'node_size'
              606  BUILD_TUPLE_1         1 
              608  LOAD_LISTCOMP            '<code_object <listcomp>>'
              610  LOAD_STR                 'draw_multilayer_default.<locals>.<listcomp>'
              612  MAKE_FUNCTION_8          'closure'
              614  LOAD_FAST                'degrees'
              616  LOAD_METHOD              values
              618  CALL_METHOD_0         0  ''
              620  GET_ITER         
              622  CALL_FUNCTION_1       1  ''
              624  STORE_FAST               'node_sizes'
              626  JUMP_FORWARD        650  'to 650'
            628_0  COME_FROM           600  '600'

 L. 149       628  LOAD_CLOSURE             'node_size'
              630  BUILD_TUPLE_1         1 
              632  LOAD_LISTCOMP            '<code_object <listcomp>>'
              634  LOAD_STR                 'draw_multilayer_default.<locals>.<listcomp>'
              636  MAKE_FUNCTION_8          'closure'
              638  LOAD_FAST                'degrees'
              640  LOAD_METHOD              values
              642  CALL_METHOD_0         0  ''
              644  GET_ITER         
              646  CALL_FUNCTION_1       1  ''
              648  STORE_FAST               'node_sizes'
            650_0  COME_FROM           626  '626'

 L. 151       650  LOAD_GLOBAL              np
              652  LOAD_METHOD              sum
              654  LOAD_FAST                'node_sizes'
              656  CALL_METHOD_1         1  ''
              658  LOAD_CONST               0
              660  COMPARE_OP               ==
          662_664  POP_JUMP_IF_FALSE   688  'to 688'

 L. 152       666  LOAD_CLOSURE             'node_size'
              668  BUILD_TUPLE_1         1 
              670  LOAD_LISTCOMP            '<code_object <listcomp>>'
              672  LOAD_STR                 'draw_multilayer_default.<locals>.<listcomp>'
              674  MAKE_FUNCTION_8          'closure'
              676  LOAD_FAST                'degrees'
              678  LOAD_METHOD              values
              680  CALL_METHOD_0         0  ''
              682  GET_ITER         
              684  CALL_FUNCTION_1       1  ''
              686  STORE_FAST               'node_sizes'
            688_0  COME_FROM           662  '662'

 L. 161       688  LOAD_GLOBAL              drawing_machinery
              690  LOAD_ATTR                draw
              692  LOAD_FAST                'network'
              694  LOAD_FAST                'positions'
              696  LOAD_FAST                'facecolor_list'
              698  LOAD_FAST                'color'
              700  BINARY_SUBSCR    
              702  LOAD_FAST                'node_labels'
              704  LOAD_FAST                'edge_size'
              706  LOAD_FAST                'node_sizes'
              708  LOAD_FAST                'arrowsize'
              710  LOAD_FAST                'axis'
              712  LOAD_FAST                'node_font_size'
              714  LOAD_CONST               ('node_color', 'with_labels', 'edge_size', 'node_size', 'arrowsize', 'ax', 'font_size')
              716  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              718  POP_TOP          

 L. 162       720  LOAD_FAST                'color'
              722  LOAD_CONST               1
              724  INPLACE_ADD      
              726  STORE_FAST               'color'
              728  JUMP_BACK           136  'to 136'
              730  POP_BLOCK        
            732_0  COME_FROM_LOOP      128  '128'

 L. 164       732  LOAD_FAST                'display'
              734  LOAD_CONST               True
              736  COMPARE_OP               ==
          738_740  POP_JUMP_IF_FALSE   750  'to 750'

 L. 165       742  LOAD_GLOBAL              plt
              744  LOAD_METHOD              show
              746  CALL_METHOD_0         0  ''
              748  POP_TOP          
            750_0  COME_FROM           738  '738'

Parse error at or near `JUMP_BACK' instruction at offset 728


def draw_multiedges--- This code section failed: ---

 L. 169         0  LOAD_FAST                'input_type'
                2  LOAD_STR                 'nodes'
                4  COMPARE_OP               ==
              6_8  POP_JUMP_IF_FALSE   436  'to 436'

 L. 171        10  LOAD_LISTCOMP            '<code_object <listcomp>>'
               12  LOAD_STR                 'draw_multiedges.<locals>.<listcomp>'
               14  MAKE_FUNCTION_0          ''
               16  LOAD_FAST                'network_list'
               18  GET_ITER         
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'network_positions'

 L. 173        24  BUILD_MAP_0           0 
               26  STORE_FAST               'global_positions'

 L. 174        28  SETUP_LOOP           72  'to 72'
               30  LOAD_FAST                'network_positions'
               32  GET_ITER         
               34  FOR_ITER             70  'to 70'
               36  STORE_FAST               'position'

 L. 175        38  SETUP_LOOP           68  'to 68'
               40  LOAD_FAST                'position'
               42  LOAD_METHOD              items
               44  CALL_METHOD_0         0  ''
               46  GET_ITER         
               48  FOR_ITER             66  'to 66'
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'k'
               54  STORE_FAST               'v'

 L. 176        56  LOAD_FAST                'v'
               58  LOAD_FAST                'global_positions'
               60  LOAD_FAST                'k'
               62  STORE_SUBSCR     
               64  JUMP_BACK            48  'to 48'
               66  POP_BLOCK        
             68_0  COME_FROM_LOOP       38  '38'
               68  JUMP_BACK            34  'to 34'
               70  POP_BLOCK        
             72_0  COME_FROM_LOOP       28  '28'

 L. 178     72_74  SETUP_LOOP          436  'to 436'
               76  LOAD_FAST                'multi_edge_tuple'
               78  GET_ITER         
            80_82  FOR_ITER            434  'to 434'
               84  STORE_FAST               'pair'

 L. 179     86_88  SETUP_EXCEPT        388  'to 388'

 L. 181        90  LOAD_FAST                'global_positions'
               92  LOAD_FAST                'pair'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  BINARY_SUBSCR    
              100  STORE_FAST               'coordinates_node_first'

 L. 182       102  LOAD_FAST                'global_positions'
              104  LOAD_FAST                'pair'
              106  LOAD_CONST               1
              108  BINARY_SUBSCR    
              110  BINARY_SUBSCR    
              112  STORE_FAST               'coordinates_node_second'

 L. 184       114  LOAD_FAST                'coordinates_node_first'
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  LOAD_FAST                'coordinates_node_second'
              122  LOAD_CONST               0
              124  BINARY_SUBSCR    
              126  BUILD_LIST_2          2 
              128  STORE_FAST               'p1'

 L. 186       130  LOAD_FAST                'coordinates_node_first'
              132  LOAD_CONST               1
              134  BINARY_SUBSCR    
              136  LOAD_FAST                'coordinates_node_second'
              138  LOAD_CONST               1
              140  BINARY_SUBSCR    
              142  BUILD_LIST_2          2 
              144  STORE_FAST               'p2'

 L. 189       146  LOAD_FAST                'style'
              148  LOAD_STR                 'line'
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   178  'to 178'

 L. 191       154  LOAD_GLOBAL              plt
              156  LOAD_ATTR                plot
              158  LOAD_FAST                'p1'
              160  LOAD_FAST                'p2'
              162  LOAD_FAST                'linepoints'
              164  LOAD_CONST               1
              166  LOAD_FAST                'alphachannel'
              168  LOAD_FAST                'linecolor'
              170  LOAD_CONST               ('linestyle', 'lw', 'alpha', 'color')
              172  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              174  POP_TOP          
              176  JUMP_FORWARD        384  'to 384'
            178_0  COME_FROM           152  '152'

 L. 193       178  LOAD_FAST                'style'
              180  LOAD_STR                 'curve2_bezier'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   242  'to 242'

 L. 195       186  LOAD_GLOBAL              bezier
              188  LOAD_ATTR                draw_bezier
              190  LOAD_GLOBAL              len
              192  LOAD_FAST                'network_list'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_FAST                'p1'
              198  LOAD_FAST                'p2'
              200  LOAD_FAST                'curve_height'
              202  LOAD_FAST                'invert'
              204  LOAD_FAST                'linmod'
              206  LOAD_FAST                'resolution'
              208  LOAD_CONST               ('path_height', 'inversion', 'linemode', 'resolution')
              210  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              212  UNPACK_SEQUENCE_2     2 
              214  STORE_FAST               'x'
              216  STORE_FAST               'y'

 L. 197       218  LOAD_GLOBAL              plt
              220  LOAD_ATTR                plot
              222  LOAD_FAST                'x'
              224  LOAD_FAST                'y'
              226  LOAD_FAST                'linepoints'
              228  LOAD_FAST                'linewidth'
              230  LOAD_FAST                'alphachannel'
              232  LOAD_FAST                'linecolor'
              234  LOAD_CONST               ('linestyle', 'lw', 'alpha', 'color')
              236  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              238  POP_TOP          
              240  JUMP_FORWARD        384  'to 384'
            242_0  COME_FROM           184  '184'

 L. 199       242  LOAD_FAST                'style'
              244  LOAD_STR                 'curve3_bezier'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   282  'to 282'

 L. 201       252  LOAD_GLOBAL              bezier
              254  LOAD_ATTR                draw_bezier
              256  LOAD_GLOBAL              len
              258  LOAD_FAST                'network_list'
              260  CALL_FUNCTION_1       1  ''
              262  LOAD_FAST                'p1'
              264  LOAD_FAST                'p2'
              266  LOAD_STR                 'cubic'
              268  LOAD_FAST                'resolution'
              270  LOAD_CONST               ('mode', 'resolution')
              272  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              274  UNPACK_SEQUENCE_2     2 
              276  STORE_FAST               'x'
              278  STORE_FAST               'y'
              280  JUMP_FORWARD        384  'to 384'
            282_0  COME_FROM           248  '248'

 L. 203       282  LOAD_FAST                'style'
              284  LOAD_STR                 'curve3_fit'
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   328  'to 328'

 L. 205       292  LOAD_GLOBAL              polyfit
              294  LOAD_METHOD              draw_order3
              296  LOAD_GLOBAL              len
              298  LOAD_FAST                'network_list'
              300  CALL_FUNCTION_1       1  ''
              302  LOAD_FAST                'p1'
              304  LOAD_FAST                'p2'
              306  CALL_METHOD_3         3  ''
              308  UNPACK_SEQUENCE_2     2 
              310  STORE_FAST               'x'
              312  STORE_FAST               'y'

 L. 207       314  LOAD_GLOBAL              plt
              316  LOAD_METHOD              plot
              318  LOAD_FAST                'x'
              320  LOAD_FAST                'y'
              322  CALL_METHOD_2         2  ''
              324  POP_TOP          
              326  JUMP_FORWARD        384  'to 384'
            328_0  COME_FROM           288  '288'

 L. 209       328  LOAD_FAST                'style'
              330  LOAD_STR                 'piramidal'
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   384  'to 384'

 L. 211       338  LOAD_GLOBAL              polyfit
              340  LOAD_METHOD              draw_piramidal
              342  LOAD_GLOBAL              len
              344  LOAD_FAST                'network_list'
              346  CALL_FUNCTION_1       1  ''
              348  LOAD_FAST                'p1'
              350  LOAD_FAST                'p2'
              352  CALL_METHOD_3         3  ''
              354  UNPACK_SEQUENCE_2     2 
              356  STORE_FAST               'x'
              358  STORE_FAST               'y'

 L. 212       360  LOAD_GLOBAL              plt
              362  LOAD_ATTR                plot
              364  LOAD_FAST                'x'
              366  LOAD_FAST                'y'
              368  LOAD_FAST                'linepoints'
              370  LOAD_CONST               1
              372  LOAD_FAST                'alphachannel'
              374  LOAD_FAST                'linecolor'
              376  LOAD_CONST               ('linestyle', 'lw', 'alpha', 'color')
              378  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              380  POP_TOP          
              382  JUMP_FORWARD        384  'to 384'
            384_0  COME_FROM           382  '382'
            384_1  COME_FROM           334  '334'
            384_2  COME_FROM           326  '326'
            384_3  COME_FROM           280  '280'
            384_4  COME_FROM           240  '240'
            384_5  COME_FROM           176  '176'

 L. 215       384  POP_BLOCK        
              386  JUMP_BACK            80  'to 80'
            388_0  COME_FROM_EXCEPT     86  '86'

 L. 217       388  DUP_TOP          
              390  LOAD_GLOBAL              Exception
              392  COMPARE_OP               exception-match
          394_396  POP_JUMP_IF_FALSE   430  'to 430'
              398  POP_TOP          
              400  STORE_FAST               'err'
              402  POP_TOP          
              404  SETUP_FINALLY       418  'to 418'

 L. 218       406  LOAD_GLOBAL              print
              408  LOAD_FAST                'err'
              410  CALL_FUNCTION_1       1  ''
              412  POP_TOP          

 L. 219       414  POP_BLOCK        
              416  LOAD_CONST               None
            418_0  COME_FROM_FINALLY   404  '404'
              418  LOAD_CONST               None
              420  STORE_FAST               'err'
              422  DELETE_FAST              'err'
              424  END_FINALLY      
              426  POP_EXCEPT       
              428  JUMP_BACK            80  'to 80'
            430_0  COME_FROM           394  '394'
              430  END_FINALLY      
              432  JUMP_BACK            80  'to 80'
              434  POP_BLOCK        
            436_0  COME_FROM_LOOP       72  '72'
            436_1  COME_FROM             6  '6'

Parse error at or near `POP_BLOCK' instruction at offset 384


def generate_random_multiedges--- This code section failed: ---

 L. 226         0  LOAD_GLOBAL              main_figure
                2  LOAD_METHOD              add_subplot
                4  LOAD_CONST               111
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'edge_subplot'

 L. 227        10  BUILD_LIST_0          0 
               12  STORE_FAST               'return_list'

 L. 230     14_16  SETUP_LOOP          420  'to 420'
               18  LOAD_GLOBAL              range
               20  LOAD_FAST                'random_edges'
               22  CALL_FUNCTION_1       1  ''
               24  GET_ITER         
            26_28  FOR_ITER            418  'to 418'
               30  STORE_FAST               'k'

 L. 231     32_34  SETUP_EXCEPT        404  'to 404'

 L. 232        36  LOAD_GLOBAL              random
               38  LOAD_METHOD              randint
               40  LOAD_CONST               0
               42  LOAD_FAST                'upper_first'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'random_network1'

 L. 233        48  LOAD_GLOBAL              random
               50  LOAD_METHOD              randint
               52  LOAD_FAST                'lower_second'
               54  LOAD_GLOBAL              len
               56  LOAD_FAST                'network_list'
               58  CALL_FUNCTION_1       1  ''
               60  CALL_METHOD_2         2  ''
               62  STORE_FAST               'random_network2'

 L. 235        64  LOAD_GLOBAL              random
               66  LOAD_METHOD              randint
               68  LOAD_CONST               1
               70  LOAD_CONST               3
               72  CALL_METHOD_2         2  ''
               74  STORE_FAST               'node_first'

 L. 236        76  LOAD_GLOBAL              random
               78  LOAD_METHOD              randint
               80  LOAD_CONST               1
               82  LOAD_CONST               3
               84  CALL_METHOD_2         2  ''
               86  STORE_FAST               'node_second'

 L. 238        88  LOAD_GLOBAL              nx
               90  LOAD_METHOD              get_node_attributes
               92  LOAD_FAST                'network_list'
               94  LOAD_FAST                'random_network1'
               96  BINARY_SUBSCR    
               98  LOAD_STR                 'pos'
              100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'positions_first_net'

 L. 239       104  LOAD_GLOBAL              nx
              106  LOAD_METHOD              get_node_attributes
              108  LOAD_FAST                'network_list'
              110  LOAD_FAST                'random_network2'
              112  BINARY_SUBSCR    
              114  LOAD_STR                 'pos'
              116  CALL_METHOD_2         2  ''
              118  STORE_FAST               'positions_second_net'

 L. 241       120  LOAD_FAST                'positions_first_net'
              122  LOAD_FAST                'node_first'
              124  BINARY_SUBSCR    
              126  LOAD_CONST               0
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'positions_second_net'
              132  LOAD_FAST                'node_second'
              134  BINARY_SUBSCR    
              136  LOAD_CONST               0
              138  BINARY_SUBSCR    
              140  BUILD_LIST_2          2 
              142  STORE_FAST               'p1'

 L. 242       144  LOAD_FAST                'positions_first_net'
              146  LOAD_FAST                'node_first'
              148  BINARY_SUBSCR    
              150  LOAD_CONST               1
              152  BINARY_SUBSCR    
              154  LOAD_FAST                'positions_second_net'
              156  LOAD_FAST                'node_second'
              158  BINARY_SUBSCR    
              160  LOAD_CONST               1
              162  BINARY_SUBSCR    
              164  BUILD_LIST_2          2 
              166  STORE_FAST               'p2'

 L. 244       168  LOAD_FAST                'style'
              170  LOAD_STR                 'line'
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   200  'to 200'

 L. 246       176  LOAD_GLOBAL              plt
              178  LOAD_ATTR                plot
              180  LOAD_FAST                'p1'
              182  LOAD_FAST                'p2'
              184  LOAD_STR                 'k-'
              186  LOAD_CONST               1
              188  LOAD_STR                 'black'
              190  LOAD_STR                 'dotted'
              192  LOAD_CONST               ('lw', 'color', 'linestyle')
              194  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              196  POP_TOP          
              198  JUMP_FORWARD        400  'to 400'
            200_0  COME_FROM           174  '174'

 L. 248       200  LOAD_FAST                'style'
              202  LOAD_STR                 'curve2_bezier'
              204  COMPARE_OP               ==
          206_208  POP_JUMP_IF_FALSE   260  'to 260'

 L. 250       210  LOAD_GLOBAL              bezier
              212  LOAD_ATTR                draw_bezier
              214  LOAD_GLOBAL              len
              216  LOAD_FAST                'network_list'
              218  CALL_FUNCTION_1       1  ''
              220  LOAD_FAST                'p1'
              222  LOAD_FAST                'p2'
              224  LOAD_FAST                'inverse_tag'
              226  LOAD_FAST                'pheight'
              228  LOAD_CONST               ('inversion', 'path_height')
              230  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              232  UNPACK_SEQUENCE_2     2 
              234  STORE_FAST               'x'
              236  STORE_FAST               'y'

 L. 251       238  LOAD_GLOBAL              plt
              240  LOAD_ATTR                plot
              242  LOAD_FAST                'x'
              244  LOAD_FAST                'y'
              246  LOAD_FAST                'linepoints'
              248  LOAD_CONST               1
              250  LOAD_CONST               0.3
              252  LOAD_CONST               ('linestyle', 'lw', 'alpha')
              254  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              256  POP_TOP          
              258  JUMP_FORWARD        400  'to 400'
            260_0  COME_FROM           206  '206'

 L. 254       260  LOAD_FAST                'style'
              262  LOAD_STR                 'curve3_bezier'
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   298  'to 298'

 L. 256       270  LOAD_GLOBAL              bezier
              272  LOAD_ATTR                draw_bezier
              274  LOAD_GLOBAL              len
              276  LOAD_FAST                'network_list'
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_FAST                'p1'
              282  LOAD_FAST                'p2'
              284  LOAD_STR                 'cubic'
              286  LOAD_CONST               ('mode',)
              288  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              290  UNPACK_SEQUENCE_2     2 
              292  STORE_FAST               'x'
              294  STORE_FAST               'y'
              296  JUMP_FORWARD        400  'to 400'
            298_0  COME_FROM           266  '266'

 L. 258       298  LOAD_FAST                'style'
              300  LOAD_STR                 'curve3_fit'
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   344  'to 344'

 L. 260       308  LOAD_GLOBAL              polyfit
              310  LOAD_METHOD              draw_order3
              312  LOAD_GLOBAL              len
              314  LOAD_FAST                'network_list'
              316  CALL_FUNCTION_1       1  ''
              318  LOAD_FAST                'p1'
              320  LOAD_FAST                'p2'
              322  CALL_METHOD_3         3  ''
              324  UNPACK_SEQUENCE_2     2 
              326  STORE_FAST               'x'
              328  STORE_FAST               'y'

 L. 262       330  LOAD_GLOBAL              plt
              332  LOAD_METHOD              plot
              334  LOAD_FAST                'x'
              336  LOAD_FAST                'y'
              338  CALL_METHOD_2         2  ''
              340  POP_TOP          
              342  JUMP_FORWARD        400  'to 400'
            344_0  COME_FROM           304  '304'

 L. 264       344  LOAD_FAST                'style'
              346  LOAD_STR                 'piramidal'
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   400  'to 400'

 L. 266       354  LOAD_GLOBAL              polyfit
              356  LOAD_METHOD              draw_piramidal
              358  LOAD_GLOBAL              len
              360  LOAD_FAST                'network_list'
              362  CALL_FUNCTION_1       1  ''
              364  LOAD_FAST                'p1'
              366  LOAD_FAST                'p2'
              368  CALL_METHOD_3         3  ''
              370  UNPACK_SEQUENCE_2     2 
              372  STORE_FAST               'x'
              374  STORE_FAST               'y'

 L. 267       376  LOAD_GLOBAL              plt
              378  LOAD_ATTR                plot
              380  LOAD_FAST                'x'
              382  LOAD_FAST                'y'
              384  LOAD_STR                 'black'
              386  LOAD_CONST               0.3
              388  LOAD_STR                 '-.'
              390  LOAD_CONST               1
              392  LOAD_CONST               ('color', 'alpha', 'linestyle', 'lw')
              394  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              396  POP_TOP          
              398  JUMP_FORWARD        400  'to 400'
            400_0  COME_FROM           398  '398'
            400_1  COME_FROM           350  '350'
            400_2  COME_FROM           342  '342'
            400_3  COME_FROM           296  '296'
            400_4  COME_FROM           258  '258'
            400_5  COME_FROM           198  '198'

 L. 270       400  POP_BLOCK        
              402  JUMP_BACK            26  'to 26'
            404_0  COME_FROM_EXCEPT     32  '32'

 L. 271       404  POP_TOP          
              406  POP_TOP          
              408  POP_TOP          

 L. 272       410  POP_EXCEPT       
              412  JUMP_BACK            26  'to 26'
              414  END_FINALLY      
              416  JUMP_BACK            26  'to 26'
              418  POP_BLOCK        
            420_0  COME_FROM_LOOP       14  '14'

Parse error at or near `POP_BLOCK' instruction at offset 400


def generate_random_networks(number_of_networks):
    network_list = []
    for j in range(number_of_networks):
        tmp_graph = nx.gnm_random_graphrandom.randint60300random.randint5300
        tmp_pos = nx.spring_layout(tmp_graph)
        nx.set_node_attributestmp_graph'pos'tmp_pos
        network_list.append(tmp_graph)

    return network_list


def supra_adjacency_matrix_plot(matrix, display=False):
    plt.imshow(matrix, interpolation='nearest', cmap=(plt.cm.binary))
    if display:
        plt.show()


def hairball_plot(g, color_list=None, display=False, node_size=1, text_color='black', node_sizes=None, layout_parameters=None, legend=None, scale_by_size=True, layout_algorithm='force', edge_width=0.01, alpha_channel=0.5, labels=None, label_font_size=2):
    """A method for drawing force-directed plots
    Args:
    network (networkx): A network to be visualized
    color_list (list): A list of colors for nodes
    node_size (float): Size of nodes
    layout_parameters (dict): A dictionary of label parameters
    legend (bool): Display legend?
    scale_by_size (bool): Rescale nodes?
    layout_algorithm (string): What type of layout algorithm is to be used?
    edge_width (float): Width of edges
    alpha_channel (float): Transparency level.
    labels (bool): Display labels?
    label_font_size (int): Sizes of labels
    Returns:
        None
    """
    print('Beginning parsing..')
    nodes = g.nodes(data=True)
    potlabs = []
    for node in nodes:
        try:
            potlabs.append(node[0][1])
        except:
            potlabs.append('unlabeled')

    if color_list is None:
        unique_colors = np.unique(potlabs)
        color_mapping = dict(zip(list(unique_colors), colors.colors_default))
        try:
            final_color_mapping = [color_mapping[n[1]['type']] for n in nodes]
        except:
            print('Assigning colors..')
            final_color_mapping = [1] * len(nodes)

    else:
        print('Creating color mappings..')
        unique_colors = np.unique(color_list)
        color_mapping = dict(zip(list(unique_colors), colors.all_color_names))
        final_color_mapping = color_list
    print('plotting..')
    degrees = dict(nx.degree(nx.Graph(g)))
    if scale_by_size:
        nsizes = [np.log(v) * node_size if v > 10 else v for v in degrees.values()]
    else:
        nsizes = [node_size for x in g.nodes()]
    if node_sizes is not None:
        nsizes = node_sizes
    else:
        if layout_algorithm == 'force':
            pos = compute_force_directed_layout(g, layout_parameters)
        elif layout_algorithm == 'random':
            pos = compute_random_layout(g)
        elif layout_algorithm == 'custom_coordinates':
            pos = layout_parameters['pos']
        elif layout_algorithm == 'custom_coordinates_initial_force':
            pos = compute_force_directed_layout(g, layout_parameters)
        else:
            raise ValueError('Uknown layout algorithm: ' + str(layout_algorithm))
        nx.draw_networkx_edges(g, pos, alpha=alpha_channel, edge_color='black', width=edge_width, arrows=False)
        nx.draw_networkx_nodes(g, pos, nodelist=[n1[0] for n1 in nodes], node_color=final_color_mapping, node_size=nsizes, alpha=alpha_channel)
        if labels is not None:
            for el in labels:
                pos_el = pos[el]
                plt.text((pos_el[0]), (pos_el[1]), el, fontsize=label_font_size, color=text_color)

        plt.axis('off')
        if legend is not None:
            if legend:
                if type(legend) == bool:
                    markers = [plt.Line2D([0, 0], [0, 0], color=(color_mapping[item]), marker='o', linestyle='') for item in list(unique_colors)]
                    plt.legend(markers, (range(len(list(unique_colors)))), numpoints=1, fontsize='medium')
                else:
                    legend_colors = list(legend.keys())
                    markers = [plt.Line2D([0, 0], [0, 0], color=key, marker='o', linestyle='') for key in legend_colors]
                    plt.legend(markers, [legend[color] for color in legend_colors], numpoints=1, fontsize='medium')
    if display:
        plt.show()


if __name__ == '__main__':
    x = generate_random_networks(4)
    draw_multilayer_default(x, display=False, background_shape='circle')
    generate_random_multiedges(x, 12, style='curve2_bezier')
    plt.show()