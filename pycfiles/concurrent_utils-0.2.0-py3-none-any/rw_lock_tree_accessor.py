# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/rw_lock_tree_accessor.py
# Compiled at: 2011-09-28 13:50:09
from concurrent_tree_crawler.common.threads.rw_lock import RWLock
from concurrent_tree_crawler.tree_accessor import TreeAccessor
from concurrent_tree_crawler.abstract_node import NodeState
from concurrent_tree_crawler.abstract_tree_accessor import NodeAction

class RWLockTreeAccessor(TreeAccessor):
    """
        A version of the L{TreeAccessor} where sensitive methods are protected by
        readers-writers lock.
        """

    def __init__(self, sentinel):
        TreeAccessor.__init__(self, sentinel)
        self.__lock = RWLock()

    def get_lock(self):
        return self.__lock

    def update_and_get_child--- This code section failed: ---

 L.  20         0  SETUP_LOOP          210  'to 213'
                3  LOAD_GLOBAL           0  'True'
                6  POP_JUMP_IF_FALSE   212  'to 212'

 L.  21         9  LOAD_FAST             1  'node'
               12  LOAD_ATTR             1  'get_children_cond'
               15  CALL_FUNCTION_0       0  None
               18  LOAD_ATTR             2  'acquire'
               21  CALL_FUNCTION_0       0  None
               24  POP_TOP          

 L.  22        25  SETUP_FINALLY       164  'to 192'

 L.  23        28  LOAD_FAST             0  'self'
               31  LOAD_ATTR             3  '__update_with_potential_tree_change'

 L.  24        34  LOAD_FAST             1  'node'
               37  LOAD_FAST             2  'possible_children_names'
               40  CALL_FUNCTION_2       2  None
               43  STORE_FAST            3  'child_info'

 L.  25        46  LOAD_FAST             3  'child_info'
               49  LOAD_CONST               None
               52  COMPARE_OP            8  is
               55  POP_JUMP_IF_FALSE    62  'to 62'

 L.  26        58  LOAD_CONST               None
               61  RETURN_END_IF    
             62_0  COME_FROM            55  '55'

 L.  27        62  LOAD_FAST             3  'child_info'
               65  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST            4  'child'
               71  STORE_FAST            5  'state'

 L.  28        74  LOAD_FAST             5  'state'
               77  LOAD_GLOBAL           5  'NodeState'
               80  LOAD_ATTR             6  'OPEN'
               83  COMPARE_OP            2  ==
               86  POP_JUMP_IF_FALSE   102  'to 102'

 L.  29        89  LOAD_FAST             4  'child'
               92  LOAD_GLOBAL           7  'NodeAction'
               95  LOAD_ATTR             8  'TO_PROCESS'
               98  BUILD_TUPLE_2         2 
              101  RETURN_END_IF    
            102_0  COME_FROM            86  '86'

 L.  30       102  LOAD_FAST             5  'state'
              105  LOAD_GLOBAL           5  'NodeState'
              108  LOAD_ATTR             9  'VISITED'
              111  COMPARE_OP            2  ==
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L.  31       117  LOAD_FAST             4  'child'
              120  LOAD_GLOBAL           7  'NodeAction'
              123  LOAD_ATTR            10  'TO_VISIT'
              126  BUILD_TUPLE_2         2 
              129  RETURN_END_IF    
            130_0  COME_FROM           114  '114'

 L.  32       130  LOAD_FAST             5  'state'
              133  LOAD_GLOBAL           5  'NodeState'
              136  LOAD_ATTR            11  'PROCESSING'
              139  COMPARE_OP            2  ==
              142  POP_JUMP_IF_FALSE   164  'to 164'

 L.  33       145  LOAD_FAST             1  'node'
              148  LOAD_ATTR             1  'get_children_cond'
              151  CALL_FUNCTION_0       0  None
              154  LOAD_ATTR            12  'wait'
              157  CALL_FUNCTION_0       0  None
              160  POP_TOP          
              161  JUMP_FORWARD         24  'to 188'

 L.  35       164  LOAD_GLOBAL          13  'False'
              167  POP_JUMP_IF_TRUE    188  'to 188'
              170  LOAD_ASSERT              AssertionError
              173  LOAD_CONST               'Unknown node state: {}'
              176  LOAD_ATTR            15  'format'
              179  LOAD_FAST             5  'state'
              182  CALL_FUNCTION_1       1  None
              185  RAISE_VARARGS_2       2  None
            188_0  COME_FROM           161  '161'
              188  POP_BLOCK        
              189  LOAD_CONST               None
            192_0  COME_FROM_FINALLY    25  '25'

 L.  37       192  LOAD_FAST             1  'node'
              195  LOAD_ATTR             1  'get_children_cond'
              198  CALL_FUNCTION_0       0  None
              201  LOAD_ATTR            16  'release'
              204  CALL_FUNCTION_0       0  None
              207  POP_TOP          
              208  END_FINALLY      
              209  JUMP_BACK             3  'to 3'
              212  POP_BLOCK        
            213_0  COME_FROM             0  '0'
              213  LOAD_CONST               None
              216  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 188_0

    def __update_with_potential_tree_change(self, node, possible_children_names):
        self.__lock.reader_acquire()
        try:
            child = node.update_and_get_child(possible_children_names)
            if child is None:
                return
            state = child.get_state()
            if state == NodeState.OPEN:
                child.set_state(NodeState.PROCESSING)
            return (child, state)
        finally:
            self.__lock.reader_release()

        return

    def set_node_type(self, node, is_leaf):
        self.__lock.reader_acquire()
        try:
            TreeAccessor.set_node_type(self, node, is_leaf)
        finally:
            self.__lock.reader_release()

    def set_error(self, node):
        self.__lock.reader_acquire()
        try:
            TreeAccessor.set_error(self, node)
        finally:
            self.__lock.reader_release()