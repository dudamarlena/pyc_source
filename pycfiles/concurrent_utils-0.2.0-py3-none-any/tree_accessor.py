# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/tree_accessor.py
# Compiled at: 2011-09-28 13:50:09
import logging, threading
from concurrent_tree_crawler.abstract_tree_accessor import AbstractTreeAccessor, NodeAction
from concurrent_tree_crawler.abstract_node import NodeState

class TreeAccessor(AbstractTreeAccessor):
    """
        An interface for the tree made of L{AbstractNode}s. 
        Access to sensitive methods is protected by concurrent programming objects:
        locks and conditions.
        """

    def __init__(self, sentinel):
        """
                @param sentinel: a technical node which will be made parent of the 
                        root node.
                @type sentinel: L{AbstractNode}
                """
        self.__sentinel = sentinel
        self.__root = None
        if self.__sentinel.has_child('root'):
            self.__root = self.__sentinel.get_child('root')
        else:
            self.__root = self.__sentinel.add_child('root', NodeState.OPEN)
        return

    def get_sentinel(self):
        return self.__sentinel

    def get_root(self):
        return self.__root

    def update_and_get_child--- This code section failed: ---

 L.  45         0  SETUP_LOOP          279  'to 282'
                3  LOAD_GLOBAL           0  'True'
                6  POP_JUMP_IF_FALSE   281  'to 281'

 L.  46         9  LOAD_FAST             1  'node'
               12  LOAD_ATTR             1  'get_children_cond'
               15  CALL_FUNCTION_0       0  None
               18  LOAD_ATTR             2  'acquire'
               21  CALL_FUNCTION_0       0  None
               24  POP_TOP          

 L.  47        25  SETUP_FINALLY       233  'to 261'

 L.  48        28  LOAD_FAST             1  'node'
               31  LOAD_ATTR             3  'update_and_get_child'
               34  LOAD_FAST             2  'possible_children_names'
               37  CALL_FUNCTION_1       1  None
               40  STORE_FAST            3  'child'

 L.  49        43  LOAD_FAST             3  'child'
               46  LOAD_CONST               None
               49  COMPARE_OP            8  is
               52  POP_JUMP_IF_FALSE    59  'to 59'

 L.  50        55  LOAD_CONST               None
               58  RETURN_END_IF    
             59_0  COME_FROM            52  '52'

 L.  51        59  LOAD_FAST             3  'child'
               62  LOAD_ATTR             5  'get_state'
               65  CALL_FUNCTION_0       0  None
               68  STORE_FAST            4  'state'

 L.  52        71  LOAD_FAST             4  'state'
               74  LOAD_GLOBAL           6  'NodeState'
               77  LOAD_ATTR             7  'OPEN'
               80  COMPARE_OP            2  ==
               83  POP_JUMP_IF_FALSE   115  'to 115'

 L.  53        86  LOAD_FAST             3  'child'
               89  LOAD_ATTR             8  'set_state'
               92  LOAD_GLOBAL           6  'NodeState'
               95  LOAD_ATTR             9  'PROCESSING'
               98  CALL_FUNCTION_1       1  None
              101  POP_TOP          

 L.  54       102  LOAD_FAST             3  'child'
              105  LOAD_GLOBAL          10  'NodeAction'
              108  LOAD_ATTR            11  'TO_PROCESS'
              111  BUILD_TUPLE_2         2 
              114  RETURN_END_IF    
            115_0  COME_FROM            83  '83'

 L.  55       115  LOAD_FAST             4  'state'
              118  LOAD_GLOBAL           6  'NodeState'
              121  LOAD_ATTR            12  'VISITED'
              124  COMPARE_OP            2  ==
              127  POP_JUMP_IF_FALSE   143  'to 143'

 L.  56       130  LOAD_FAST             3  'child'
              133  LOAD_GLOBAL          10  'NodeAction'
              136  LOAD_ATTR            13  'TO_VISIT'
              139  BUILD_TUPLE_2         2 
              142  RETURN_END_IF    
            143_0  COME_FROM           127  '127'

 L.  57       143  LOAD_FAST             4  'state'
              146  LOAD_GLOBAL           6  'NodeState'
              149  LOAD_ATTR             9  'PROCESSING'
              152  COMPARE_OP            2  ==
              155  POP_JUMP_IF_FALSE   233  'to 233'

 L.  58       158  LOAD_FAST             0  'self'
              161  LOAD_ATTR            14  '__log'
              164  LOAD_CONST               'Starting to wait on "{}" node children'
              167  LOAD_ATTR            15  'format'

 L.  59       170  LOAD_FAST             1  'node'
              173  LOAD_ATTR            16  'get_name'
              176  CALL_FUNCTION_0       0  None
              179  CALL_FUNCTION_1       1  None
              182  CALL_FUNCTION_1       1  None
              185  POP_TOP          

 L.  60       186  LOAD_FAST             1  'node'
              189  LOAD_ATTR             1  'get_children_cond'
              192  CALL_FUNCTION_0       0  None
              195  LOAD_ATTR            17  'wait'
              198  CALL_FUNCTION_0       0  None
              201  POP_TOP          

 L.  61       202  LOAD_FAST             0  'self'
              205  LOAD_ATTR            14  '__log'
              208  LOAD_CONST               'Done waiting on "{}" node children'
              211  LOAD_ATTR            15  'format'

 L.  62       214  LOAD_FAST             1  'node'
              217  LOAD_ATTR            16  'get_name'
              220  CALL_FUNCTION_0       0  None
              223  CALL_FUNCTION_1       1  None
              226  CALL_FUNCTION_1       1  None
              229  POP_TOP          
              230  JUMP_FORWARD         24  'to 257'

 L.  64       233  LOAD_GLOBAL          18  'False'
              236  POP_JUMP_IF_TRUE    257  'to 257'
              239  LOAD_ASSERT              AssertionError
              242  LOAD_CONST               'Unknown node state: {}'
              245  LOAD_ATTR            15  'format'
              248  LOAD_FAST             4  'state'
              251  CALL_FUNCTION_1       1  None
              254  RAISE_VARARGS_2       2  None
            257_0  COME_FROM           230  '230'
              257  POP_BLOCK        
              258  LOAD_CONST               None
            261_0  COME_FROM_FINALLY    25  '25'

 L.  66       261  LOAD_FAST             1  'node'
              264  LOAD_ATTR             1  'get_children_cond'
              267  CALL_FUNCTION_0       0  None
              270  LOAD_ATTR            20  'release'
              273  CALL_FUNCTION_0       0  None
              276  POP_TOP          
              277  END_FINALLY      
              278  JUMP_BACK             3  'to 3'
              281  POP_BLOCK        
            282_0  COME_FROM             0  '0'
              282  LOAD_CONST               None
              285  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 257_0

    def set_node_type--- This code section failed: ---

 L.  69         0  LOAD_FAST             1  'node'
                3  LOAD_FAST             0  'self'
                6  LOAD_ATTR             0  '__sentinel'
                9  COMPARE_OP            3  !=
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'Processing sentinel is not allowed'
               21  RAISE_VARARGS_2       2  None

 L.  70        24  LOAD_FAST             1  'node'
               27  LOAD_ATTR             2  'get_parent'
               30  CALL_FUNCTION_0       0  None
               33  STORE_FAST            3  'parent'

 L.  71        36  LOAD_FAST             3  'parent'
               39  LOAD_ATTR             3  'get_children_cond'
               42  CALL_FUNCTION_0       0  None
               45  LOAD_ATTR             4  'acquire'
               48  CALL_FUNCTION_0       0  None
               51  POP_TOP          

 L.  72        52  SETUP_FINALLY        58  'to 113'

 L.  73        55  LOAD_FAST             2  'is_leaf'
               58  POP_JUMP_IF_FALSE    93  'to 93'

 L.  74        61  LOAD_FAST             1  'node'
               64  LOAD_ATTR             5  'set_state'
               67  LOAD_GLOBAL           6  'NodeState'
               70  LOAD_ATTR             7  'CLOSED'
               73  CALL_FUNCTION_1       1  None
               76  POP_TOP          

 L.  75        77  LOAD_FAST             0  'self'
               80  LOAD_ATTR             8  '__internal_update_node_state'
               83  LOAD_FAST             3  'parent'
               86  CALL_FUNCTION_1       1  None
               89  POP_TOP          
               90  JUMP_FORWARD         16  'to 109'

 L.  77        93  LOAD_FAST             1  'node'
               96  LOAD_ATTR             5  'set_state'
               99  LOAD_GLOBAL           6  'NodeState'
              102  LOAD_ATTR             9  'VISITED'
              105  CALL_FUNCTION_1       1  None
              108  POP_TOP          
            109_0  COME_FROM            90  '90'
              109  POP_BLOCK        
              110  LOAD_CONST               None
            113_0  COME_FROM_FINALLY    52  '52'

 L.  79       113  LOAD_FAST             3  'parent'
              116  LOAD_ATTR             3  'get_children_cond'
              119  CALL_FUNCTION_0       0  None
              122  LOAD_ATTR            10  'notify_all'
              125  CALL_FUNCTION_0       0  None
              128  POP_TOP          

 L.  80       129  LOAD_FAST             3  'parent'
              132  LOAD_ATTR             3  'get_children_cond'
              135  CALL_FUNCTION_0       0  None
              138  LOAD_ATTR            11  'release'
              141  CALL_FUNCTION_0       0  None
              144  POP_TOP          
              145  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 144

    def set_error(self, node):
        self.__set_node_state_and_update(node, NodeState.ERROR)

    def __set_node_state_and_update--- This code section failed: ---

 L.  86         0  LOAD_FAST             1  'node'
                3  LOAD_FAST             0  'self'
                6  LOAD_ATTR             0  '__sentinel'
                9  COMPARE_OP            3  !=
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'Changing sentinel state is not allowed'
               21  RAISE_VARARGS_2       2  None

 L.  87        24  LOAD_FAST             1  'node'
               27  LOAD_ATTR             2  'get_parent'
               30  CALL_FUNCTION_0       0  None
               33  STORE_FAST            3  'parent'

 L.  88        36  LOAD_FAST             3  'parent'
               39  LOAD_ATTR             3  'get_children_cond'
               42  CALL_FUNCTION_0       0  None
               45  LOAD_ATTR             4  'acquire'
               48  CALL_FUNCTION_0       0  None
               51  POP_TOP          

 L.  89        52  SETUP_FINALLY        30  'to 85'

 L.  90        55  LOAD_FAST             1  'node'
               58  LOAD_ATTR             5  'set_state'
               61  LOAD_FAST             2  'new_state'
               64  CALL_FUNCTION_1       1  None
               67  POP_TOP          

 L.  91        68  LOAD_FAST             0  'self'
               71  LOAD_ATTR             6  '__internal_update_node_state'
               74  LOAD_FAST             3  'parent'
               77  CALL_FUNCTION_1       1  None
               80  POP_TOP          
               81  POP_BLOCK        
               82  LOAD_CONST               None
             85_0  COME_FROM_FINALLY    52  '52'

 L.  93        85  LOAD_FAST             3  'parent'
               88  LOAD_ATTR             3  'get_children_cond'
               91  CALL_FUNCTION_0       0  None
               94  LOAD_ATTR             7  'notify_all'
               97  CALL_FUNCTION_0       0  None
              100  POP_TOP          

 L.  94       101  LOAD_FAST             3  'parent'
              104  LOAD_ATTR             3  'get_children_cond'
              107  CALL_FUNCTION_0       0  None
              110  LOAD_ATTR             8  'release'
              113  CALL_FUNCTION_0       0  None
              116  POP_TOP          
              117  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 116

    def __internal_update_node_state(self, node):
        """@param node: L{AbstractNode}"""
        if node == self.__sentinel:
            return
        else:
            new_state = None
            if node.all_children_are_in_one_of_states({NodeState.CLOSED}):
                new_state = NodeState.CLOSED
            else:
                if node.all_children_are_in_one_of_states({
                 NodeState.ERROR, NodeState.CLOSED}):
                    new_state = NodeState.ERROR
                if new_state is None:
                    return
            parent = node.get_parent()
            parent.get_children_cond().acquire()
            try:
                node.set_state(new_state)
                self.__internal_update_node_state(parent)
            finally:
                parent.get_children_cond().notify_all()
                parent.get_children_cond().release()

            return

    def __log(self, message):
        """
                @type message: string
                """
        logging.debug(('thread="{}", {}').format(threading.current_thread().name, message))