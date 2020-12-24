# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/abstract_node.py
# Compiled at: 2011-09-28 13:50:09


class NodeState:
    """Enumeration describing state of processing of a certain node"""
    OPEN = 0
    PROCESSING = 1
    VISITED = 2
    CLOSED = 3
    ERROR = 4
    MAX_ENUM_INDEX = ERROR

    @staticmethod
    def to_str(state):
        """@type state: L{NodeState} enum"""
        if state == NodeState.OPEN:
            return 'OPEN'
        else:
            if state == NodeState.PROCESSING:
                return 'PROCESSING'
            else:
                if state == NodeState.VISITED:
                    return 'VISITED'
                if state == NodeState.CLOSED:
                    return 'CLOSED'
                if state == NodeState.ERROR:
                    return 'ERROR'
                return

            return

    @staticmethod
    def from_str(string):
        """
                @return: enumeration corresponding to given string, C{None} if
                        we were unable to parse the string
                @rtype: L{NodeState} enum
                """
        if string == 'OPEN':
            return NodeState.OPEN
        else:
            if string == 'PROCESSING':
                return NodeState.PROCESSING
            else:
                if string == 'VISITED':
                    return NodeState.VISITED
                if string == 'CLOSED':
                    return NodeState.CLOSED
                if string == 'ERROR':
                    return NodeState.ERROR
                return

            return


class AbstractNode:
    """A node representing a single element of the tree traversed by the
                crawler"""

    def get_children_cond(self):
        """
                @return: condition object related to the children of this node
                @rtype: L{threading.Condition}
                """
        raise NotImplementedError

    def get_name(self):
        """
                @return: name of the node. It should be unique among children of
                        this node's parent"""
        raise NotImplementedError

    def get_state(self):
        """
                @return: state of the node
                @rtype: L{NodeState}
                """
        raise NotImplementedError

    def set_state(self, new_state):
        """
                @param new_state: new state of the node
                @type new_state: L{NodeState}
                """
        raise NotImplementedError

    def get_parent(self):
        """
                @rtype: L{AbstractNode}, it is C{None} if the node is the sentinel node
                """
        raise NotImplementedError

    def update_and_get_child(self, possible_children_names):
        """
                @rtype: L{AbstractNode}
                """
        accessible_children = {NodeState.OPEN: None, NodeState.VISITED: None, 
           NodeState.PROCESSING: None}
        for possible_name in possible_children_names:
            if not self.has_child(possible_name):
                self.add_child(possible_name, NodeState.OPEN)
            child = self.get_child(possible_name)
            state = child.get_state()
            if state in accessible_children:
                if accessible_children[state] is None:
                    accessible_children[state] = child

        accessible_children_state_priority = [
         NodeState.OPEN,
         NodeState.VISITED, NodeState.PROCESSING]
        for state in accessible_children_state_priority:
            if accessible_children[state] is not None:
                return accessible_children[state]

        return

    def has_child(self, name):
        """
                @return: True if node has child with given name
                """
        raise NotImplementedError

    def get_child(self, name):
        """
                @rtype: L{AbstractNode}
                """
        raise NotImplementedError

    def get_children(self):
        """
                @rtype: list of L{AbstractNode}s
                """
        raise NotImplementedError

    def add_child(self, child_name, state):
        """
                @type state: L{NodeState}
                @return: added child node
                @rtype: L{AbstractNode}
                """
        raise NotImplementedError

    def all_children_are_in_one_of_states--- This code section failed: ---

 L. 154         0  LOAD_GLOBAL           0  'True'
                3  STORE_FAST            2  'no_children_encountered'

 L. 155         6  SETUP_LOOP           91  'to 100'
                9  LOAD_GLOBAL           1  'xrange'
               12  LOAD_GLOBAL           2  'NodeState'
               15  LOAD_ATTR             3  'MAX_ENUM_INDEX'
               18  LOAD_CONST               1
               21  BINARY_ADD       
               22  CALL_FUNCTION_1       1  None
               25  GET_ITER         
               26  FOR_ITER             70  'to 99'
               29  STORE_FAST            3  'state'

 L. 156        32  LOAD_FAST             3  'state'
               35  LOAD_FAST             1  'states'
               38  COMPARE_OP            7  not-in
               41  POP_JUMP_IF_FALSE    66  'to 66'

 L. 157        44  LOAD_FAST             0  'self'
               47  LOAD_ATTR             4  '_has_children'
               50  LOAD_FAST             3  'state'
               53  CALL_FUNCTION_1       1  None
               56  POP_JUMP_IF_FALSE    96  'to 96'

 L. 158        59  LOAD_GLOBAL           5  'False'
               62  RETURN_END_IF    
             63_0  COME_FROM            56  '56'
               63  JUMP_BACK            26  'to 26'

 L. 160        66  LOAD_FAST             0  'self'
               69  LOAD_ATTR             4  '_has_children'
               72  LOAD_FAST             3  'state'
               75  CALL_FUNCTION_1       1  None
               78  LOAD_CONST               0
               81  COMPARE_OP            4  >
               84  POP_JUMP_IF_FALSE    26  'to 26'

 L. 161        87  LOAD_GLOBAL           5  'False'
               90  STORE_FAST            2  'no_children_encountered'
               93  JUMP_BACK            26  'to 26'
               96  JUMP_BACK            26  'to 26'
               99  POP_BLOCK        
            100_0  COME_FROM             6  '6'

 L. 162       100  LOAD_FAST             2  'no_children_encountered'
              103  UNARY_NOT        
              104  POP_JUMP_IF_TRUE    116  'to 116'
              107  LOAD_ASSERT              AssertionError
              110  LOAD_CONST               'The given node has no children'
              113  RAISE_VARARGS_2       2  None

 L. 163       116  LOAD_GLOBAL           0  'True'
              119  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 119

    def _has_children(self, state):
        """
                An auxiliary method used only by the 
                L{all_children_are_in_one_of_states} method
                
                @type state: L{NodeState}
                @return: C{True} iff the node has at least one child in given state
                """
        raise NotImplementedError

    def __str__(self):
        return ('name="{}", state="{}"').format(self.get_name(), NodeState.to_str(self.get_state()))