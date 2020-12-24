# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/pms.py
# Compiled at: 2010-02-10 02:58:16
"""Permission Via Mapping and Hierarchy"""
import types

class PMSystem(object):
    """Mapping system for granting permissions for CRUDing access. The map
    object should in the following format."""

    def __init__(self, name, context, maps, children=[]):
        """context - must be a function that returns a literal
           map     - must be a permission map, supporting literal lookup.
           children- A children of PMSystem()"""
        self.name = name
        self.maps = maps
        self.context = context
        self.children = children

    def check--- This code section failed: ---

 L.  34         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'self'
                6  LOAD_ATTR             1  'maps'
                9  LOAD_GLOBAL           2  'types'
               12  LOAD_ATTR             3  'FunctionType'
               15  CALL_FUNCTION_2       2  None
               18  JUMP_IF_FALSE        16  'to 37'
               21  POP_TOP          

 L.  35        22  LOAD_FAST             0  'self'
               25  LOAD_ATTR             1  'maps'
               28  CALL_FUNCTION_0       0  None
               31  STORE_FAST            4  'maps'
               34  JUMP_FORWARD         10  'to 47'
             37_0  COME_FROM            18  '18'
               37  POP_TOP          

 L.  37        38  LOAD_FAST             0  'self'
               41  LOAD_ATTR             1  'maps'
               44  STORE_FAST            4  'maps'
             47_0  COME_FROM            34  '34'

 L.  40        47  LOAD_FAST             3  'context'
               50  JUMP_IF_FALSE         7  'to 60'
               53  POP_TOP          
               54  LOAD_FAST             3  'context'
             57_0  COME_FROM            50  '50'
               57  JUMP_IF_TRUE          7  'to 67'
               60  POP_TOP          
               61  LOAD_FAST             0  'self'
               64  LOAD_ATTR             4  'context'
             67_0  COME_FROM            57  '57'
               67  STORE_FAST            5  'ctxts'

 L.  41        70  LOAD_GLOBAL           0  'isinstance'
               73  LOAD_FAST             5  'ctxts'
               76  LOAD_GLOBAL           2  'types'
               79  LOAD_ATTR             3  'FunctionType'
               82  CALL_FUNCTION_2       2  None
               85  JUMP_IF_FALSE        13  'to 101'
               88  POP_TOP          

 L.  42        89  LOAD_FAST             5  'ctxts'
               92  CALL_FUNCTION_0       0  None
               95  STORE_FAST            5  'ctxts'
               98  JUMP_FORWARD          7  'to 108'
            101_0  COME_FROM            85  '85'
              101  POP_TOP          

 L.  44       102  LOAD_FAST             5  'ctxts'
              105  STORE_FAST            5  'ctxts'
            108_0  COME_FROM            98  '98'

 L.  50       108  LOAD_FAST             4  'maps'
              111  JUMP_IF_FALSE       147  'to 261'
              114  POP_TOP          
              115  LOAD_FAST             5  'ctxts'
              118  JUMP_IF_FALSE       140  'to 261'
            121_0  THEN                     262
              121  POP_TOP          

 L.  51       122  BUILD_LIST_0          0 
              125  STORE_FAST            6  'domain'

 L.  52       128  BUILD_LIST_0          0 
              131  DUP_TOP          
              132  STORE_FAST            7  '_[1]'
              135  LOAD_FAST             5  'ctxts'
              138  GET_ITER         
              139  FOR_ITER             34  'to 176'
              142  STORE_FAST            8  'ctxt'
              145  LOAD_FAST             7  '_[1]'
              148  LOAD_FAST             6  'domain'
              151  LOAD_ATTR             5  'extend'
              154  LOAD_FAST             4  'maps'
              157  LOAD_ATTR             6  'get'
              160  LOAD_FAST             8  'ctxt'
              163  BUILD_LIST_0          0 
              166  CALL_FUNCTION_2       2  None
              169  CALL_FUNCTION_1       1  None
              172  LIST_APPEND      
              173  JUMP_BACK           139  'to 139'
              176  DELETE_FAST           7  '_[1]'
              179  POP_TOP          

 L.  53       180  LOAD_FAST             2  'allliterals'
              183  JUMP_IF_FALSE         7  'to 193'
              186  POP_TOP          
              187  LOAD_GLOBAL           7  'all'
            190_0  COME_FROM           183  '183'
              190  JUMP_IF_TRUE          4  'to 197'
              193  POP_TOP          
              194  LOAD_GLOBAL           8  'any'
            197_0  COME_FROM           190  '190'
              197  STORE_FAST            9  'macro'

 L.  54       200  LOAD_FAST             1  'literals'
              203  JUMP_IF_FALSE        51  'to 257'
            206_0  THEN                     257
              206  POP_TOP          
              207  LOAD_FAST             9  'macro'
              210  BUILD_LIST_0          0 
              213  DUP_TOP          
              214  STORE_FAST           10  '_[2]'
              217  LOAD_FAST             1  'literals'
              220  GET_ITER         
              221  FOR_ITER             19  'to 243'
              224  STORE_FAST           11  'l'
              227  LOAD_FAST            10  '_[2]'
              230  LOAD_FAST            11  'l'
              233  LOAD_FAST             6  'domain'
              236  COMPARE_OP            6  in
              239  LIST_APPEND      
              240  JUMP_BACK           221  'to 221'
              243  DELETE_FAST          10  '_[2]'
              246  CALL_FUNCTION_1       1  None
              249  JUMP_IF_FALSE         5  'to 257'
            252_0  THEN                     257
              252  POP_TOP          

 L.  55       253  LOAD_GLOBAL           9  'True'
              256  RETURN_END_IF    
              257  POP_TOP          
              258  JUMP_FORWARD          1  'to 262'
            261_0  COME_FROM           118  '118'
            261_1  COME_FROM           111  '111'
              261  POP_TOP          
            262_0  COME_FROM           258  '258'

 L.  59       262  SETUP_LOOP           54  'to 319'
              265  LOAD_FAST             0  'self'
              268  LOAD_ATTR            10  'children'
              271  GET_ITER         
              272  FOR_ITER             39  'to 314'
              275  STORE_FAST           12  'c'

 L.  60       278  LOAD_FAST            12  'c'
              281  LOAD_ATTR            11  'check'
              284  LOAD_FAST             1  'literals'
              287  LOAD_CONST               'allliterals'
              290  LOAD_FAST             2  'allliterals'
              293  LOAD_CONST               'context'
              296  LOAD_FAST             3  'context'
              299  CALL_FUNCTION_513   513  None
              302  JUMP_IF_FALSE         5  'to 310'
            305_0  THEN                     310
              305  POP_TOP          

 L.  61       306  LOAD_GLOBAL           9  'True'
              309  RETURN_END_IF    
              310  POP_TOP          
              311  JUMP_BACK           272  'to 272'
              314  POP_BLOCK        

 L.  64       315  LOAD_GLOBAL          12  'False'
              318  RETURN_VALUE     
            319_0  COME_FROM           262  '262'

Parse error at or near `RETURN_VALUE' instruction at offset 318