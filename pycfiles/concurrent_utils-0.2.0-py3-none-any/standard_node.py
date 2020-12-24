# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/standard_node.py
# Compiled at: 2011-09-28 13:50:09
import threading
from collections import OrderedDict
from concurrent_tree_crawler.abstract_node import AbstractNode, NodeState

class StandardNode(AbstractNode):
    """A simple in-memory implementation of the L{AbstractNode}."""

    def __init__(self, parent=None, name='sentinel', state=NodeState.OPEN):
        """
                @type parent: L{StandardNode}, equals C{None} if node is 
                        the     sentinel node
                @type name: string
                @type state: L{NodeState}
                """
        self.__parent = parent
        self.__name = name
        self.__state = state
        self._children = [ OrderedDict() for _ in xrange(NodeState.MAX_ENUM_INDEX + 1) ]
        self.__cond = threading.Condition()

    def get_children_cond(self):
        return self.__cond

    def get_name(self):
        return self.__name

    def get_state(self):
        return self.__state

    def set_state--- This code section failed: ---

 L.  38         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '__parent'
                6  LOAD_CONST               None
                9  COMPARE_OP            9  is-not
               12  POP_JUMP_IF_FALSE   147  'to 147'

 L.  39        15  LOAD_GLOBAL           2  'False'
               18  STORE_FAST            2  'child_found'

 L.  40        21  SETUP_LOOP           82  'to 106'
               24  LOAD_GLOBAL           3  'xrange'
               27  LOAD_GLOBAL           4  'NodeState'
               30  LOAD_ATTR             5  'MAX_ENUM_INDEX'
               33  LOAD_CONST               1
               36  BINARY_ADD       
               37  CALL_FUNCTION_1       1  None
               40  GET_ITER         
               41  FOR_ITER             61  'to 105'
               44  STORE_FAST            3  'state'

 L.  41        47  LOAD_FAST             0  'self'
               50  LOAD_ATTR             6  '__name'
               53  LOAD_FAST             0  'self'
               56  LOAD_ATTR             0  '__parent'
               59  LOAD_ATTR             7  '_children'
               62  LOAD_FAST             3  'state'
               65  BINARY_SUBSCR    
               66  COMPARE_OP            6  in
               69  POP_JUMP_IF_FALSE    41  'to 41'

 L.  42        72  LOAD_FAST             0  'self'
               75  LOAD_ATTR             0  '__parent'
               78  LOAD_ATTR             7  '_children'
               81  LOAD_FAST             3  'state'
               84  BINARY_SUBSCR    
               85  LOAD_FAST             0  'self'
               88  LOAD_ATTR             6  '__name'
               91  DELETE_SUBSCR    

 L.  43        92  LOAD_GLOBAL           8  'True'
               95  STORE_FAST            2  'child_found'

 L.  44        98  BREAK_LOOP       
               99  JUMP_BACK            41  'to 41'
              102  JUMP_BACK            41  'to 41'
              105  POP_BLOCK        
            106_0  COME_FROM            21  '21'

 L.  45       106  LOAD_FAST             2  'child_found'
              109  POP_JUMP_IF_TRUE    121  'to 121'
              112  LOAD_ASSERT              AssertionError
              115  LOAD_CONST               "This node not found among parent's children"
              118  RAISE_VARARGS_2       2  None

 L.  46       121  LOAD_FAST             0  'self'
              124  LOAD_FAST             0  'self'
              127  LOAD_ATTR             0  '__parent'
              130  LOAD_ATTR             7  '_children'
              133  LOAD_FAST             1  'new_state'
              136  BINARY_SUBSCR    
              137  LOAD_FAST             0  'self'
              140  LOAD_ATTR             6  '__name'
              143  STORE_SUBSCR     
              144  JUMP_FORWARD          0  'to 147'
            147_0  COME_FROM           144  '144'

 L.  47       147  LOAD_FAST             1  'new_state'
              150  LOAD_FAST             0  'self'
              153  STORE_ATTR           10  '__state'
              156  LOAD_CONST               None
              159  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 156

    def get_parent(self):
        return self.__parent

    def has_child(self, name):
        for state in xrange(NodeState.MAX_ENUM_INDEX + 1):
            if name in self._children[state]:
                return True

        return False

    def get_child--- This code section failed: ---

 L.  59         0  SETUP_LOOP           61  'to 64'
                3  LOAD_GLOBAL           0  'xrange'
                6  LOAD_GLOBAL           1  'NodeState'
                9  LOAD_ATTR             2  'MAX_ENUM_INDEX'
               12  LOAD_CONST               1
               15  BINARY_ADD       
               16  CALL_FUNCTION_1       1  None
               19  GET_ITER         
               20  FOR_ITER             40  'to 63'
               23  STORE_FAST            2  'state'

 L.  60        26  LOAD_FAST             1  'name'
               29  LOAD_FAST             0  'self'
               32  LOAD_ATTR             3  '_children'
               35  LOAD_FAST             2  'state'
               38  BINARY_SUBSCR    
               39  COMPARE_OP            6  in
               42  POP_JUMP_IF_FALSE    20  'to 20'

 L.  61        45  LOAD_FAST             0  'self'
               48  LOAD_ATTR             3  '_children'
               51  LOAD_FAST             2  'state'
               54  BINARY_SUBSCR    
               55  LOAD_FAST             1  'name'
               58  BINARY_SUBSCR    
               59  RETURN_END_IF    
             60_0  COME_FROM            42  '42'
               60  JUMP_BACK            20  'to 20'
               63  POP_BLOCK        
             64_0  COME_FROM             0  '0'

 L.  62        64  LOAD_GLOBAL           4  'False'
               67  POP_JUMP_IF_TRUE     79  'to 79'
               70  LOAD_ASSERT              AssertionError
               73  LOAD_CONST               'Child with given name not found'
               76  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 73

    def get_children(self):
        children = []
        for state in xrange(NodeState.MAX_ENUM_INDEX + 1):
            for _, node in self._children[state].iteritems():
                children.append(node)

        return children

    def add_child(self, name, state):
        assert name not in self._children[state]
        new_child = StandardNode(self, name, state)
        self._children[state][name] = new_child
        return new_child

    def _has_children(self, state):
        return len(self._children[state]) > 0