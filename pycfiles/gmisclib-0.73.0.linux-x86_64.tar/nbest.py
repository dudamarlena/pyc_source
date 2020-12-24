# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/nbest.py
# Compiled at: 2007-08-13 06:22:59
"""Beam search through a graph."""

class node:
    """This is a node of a graph, it includes links to other nodes."""

    def __init__(self, cost=0.0, label=None, terminal=0, comment=None):
        """Create a node, with a specified cost (used in the beam search),
                and a label (arbitrary information).
                Terminal nodes are marked, and terminate the search."""
        self.terminal = terminal
        self.out = []
        self.cost = cost
        self.label = label
        self.comment = comment

    def add(self, nextnode, cost=0.0, label=None):
        """Add a link from self to nextnode.
                Links can have a cost and label, too."""
        self.out.append((nextnode, cost, label))
        return nextnode

    def __str__(self):
        return '<node term=%d label=%s nout=%d cost=%f>' % (self.terminal, str(self.label),
         len(self.out), self.cost)

    __repr__ = __str__


class _l_list:
    """Linked list."""

    def __init__(self, contents, link):
        self.link = link
        self.contents = contents

    def walk(self):
        o = [
         self.contents]
        while self.link is not None:
            self = self.link
            o.append(self.contents)

        return o

    def rwalk(self):
        o = self.walk()
        o.reverse()
        return o


def go--- This code section failed: ---

 L.  61         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'graph'
                6  LOAD_GLOBAL           1  'node'
                9  CALL_FUNCTION_2       2  None
               12  POP_JUMP_IF_TRUE     34  'to 34'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'Non-node starts graph: %s'
               21  LOAD_GLOBAL           3  'str'
               24  LOAD_FAST             0  'graph'
               27  CALL_FUNCTION_1       1  None
               30  BINARY_MODULO    
               31  RAISE_VARARGS_2       2  None

 L.  63        34  LOAD_CONST               0.0
               37  LOAD_FAST             0  'graph'
               40  LOAD_GLOBAL           4  '_l_list'
               43  LOAD_FAST             0  'graph'
               46  LOAD_CONST               None
               49  CALL_FUNCTION_2       2  None
               52  BUILD_TUPLE_3         3 
               55  BUILD_LIST_1          1 
               58  STORE_FAST            3  'current'

 L.  64        61  BUILD_LIST_0          0 
               64  STORE_FAST            4  'terminate'

 L.  66        67  SETUP_LOOP          339  'to 409'

 L.  67        70  BUILD_LIST_0          0 
               73  STORE_FAST            5  'nextstep'

 L.  68        76  SETUP_LOOP          171  'to 250'
               79  LOAD_FAST             3  'current'
               82  GET_ITER         
               83  FOR_ITER            163  'to 249'
               86  UNPACK_SEQUENCE_3     3 
               89  STORE_FAST            6  'cost'
               92  STORE_FAST            7  'anode'
               95  STORE_FAST            8  'path'

 L.  69        98  LOAD_GLOBAL           0  'isinstance'
              101  LOAD_FAST             7  'anode'
              104  LOAD_GLOBAL           1  'node'
              107  CALL_FUNCTION_2       2  None
              110  POP_JUMP_IF_TRUE    132  'to 132'
              113  LOAD_ASSERT              AssertionError
              116  LOAD_CONST               'Non-node in graph: %s'
              119  LOAD_GLOBAL           3  'str'
              122  LOAD_FAST             7  'anode'
              125  CALL_FUNCTION_1       1  None
              128  BINARY_MODULO    
              129  RAISE_VARARGS_2       2  None

 L.  70       132  SETUP_LOOP          111  'to 246'
              135  LOAD_FAST             7  'anode'
              138  LOAD_ATTR             6  'out'
              141  GET_ITER         
              142  FOR_ITER            100  'to 245'
              145  UNPACK_SEQUENCE_3     3 
              148  STORE_FAST            9  'nnode'
              151  STORE_FAST           10  'c'
              154  STORE_FAST           11  'll'

 L.  72       157  LOAD_FAST             6  'cost'
              160  LOAD_FAST             9  'nnode'
              163  LOAD_ATTR             7  'cost'
              166  BINARY_ADD       
              167  LOAD_FAST            10  'c'
              170  BINARY_ADD       
              171  STORE_FAST           12  'newcost'

 L.  73       174  LOAD_GLOBAL           4  '_l_list'
              177  LOAD_FAST             9  'nnode'
              180  LOAD_FAST             8  'path'
              183  CALL_FUNCTION_2       2  None
              186  STORE_FAST           13  'newpath'

 L.  75       189  LOAD_FAST             9  'nnode'
              192  LOAD_ATTR             8  'terminal'
              195  POP_JUMP_IF_FALSE   220  'to 220'

 L.  76       198  LOAD_FAST             4  'terminate'
              201  LOAD_ATTR             9  'append'
              204  LOAD_FAST            12  'newcost'
              207  LOAD_FAST            13  'newpath'
              210  BUILD_TUPLE_2         2 
              213  CALL_FUNCTION_1       1  None
              216  POP_TOP          
              217  JUMP_BACK           142  'to 142'

 L.  78       220  LOAD_FAST             5  'nextstep'
              223  LOAD_ATTR             9  'append'
              226  LOAD_FAST            12  'newcost'
              229  LOAD_FAST             9  'nnode'
              232  LOAD_FAST            13  'newpath'
              235  BUILD_TUPLE_3         3 
              238  CALL_FUNCTION_1       1  None
              241  POP_TOP          
              242  JUMP_BACK           142  'to 142'
              245  POP_BLOCK        
            246_0  COME_FROM           132  '132'
              246  JUMP_BACK            83  'to 83'
              249  POP_BLOCK        
            250_0  COME_FROM            76  '76'

 L.  79       250  LOAD_GLOBAL          10  'len'
              253  LOAD_FAST             5  'nextstep'
              256  CALL_FUNCTION_1       1  None
              259  LOAD_CONST               0
              262  COMPARE_OP            2  ==
              265  POP_JUMP_IF_FALSE   272  'to 272'

 L.  80       268  BREAK_LOOP       
              269  JUMP_FORWARD          0  'to 272'
            272_0  COME_FROM           269  '269'

 L.  81       272  LOAD_FAST             5  'nextstep'
              275  LOAD_ATTR            11  'sort'
              278  CALL_FUNCTION_0       0  None
              281  POP_TOP          

 L.  82       282  LOAD_GLOBAL          10  'len'
              285  LOAD_FAST             5  'nextstep'
              288  CALL_FUNCTION_1       1  None
              291  LOAD_FAST             1  'nbeam'
              294  COMPARE_OP            4  >
              297  POP_JUMP_IF_FALSE   313  'to 313'

 L.  83       300  LOAD_FAST             5  'nextstep'
              303  LOAD_FAST             1  'nbeam'
              306  SLICE+2          
              307  STORE_FAST            5  'nextstep'
              310  JUMP_FORWARD          0  'to 313'
            313_0  COME_FROM           310  '310'

 L.  84       313  LOAD_FAST             5  'nextstep'
              316  LOAD_CONST               0
              319  BINARY_SUBSCR    
              320  LOAD_CONST               0
              323  BINARY_SUBSCR    
              324  LOAD_FAST             2  'cbeam'
              327  BINARY_ADD       
              328  STORE_FAST           14  'costlimit'

 L.  85       331  LOAD_CONST               0
              334  STORE_FAST           15  'i'

 L.  86       337  SETUP_LOOP           56  'to 396'
              340  LOAD_FAST            15  'i'
              343  LOAD_GLOBAL          10  'len'
              346  LOAD_FAST             5  'nextstep'
              349  CALL_FUNCTION_1       1  None
              352  COMPARE_OP            0  <
              355  POP_JUMP_IF_FALSE   395  'to 395'

 L.  87       358  LOAD_FAST             5  'nextstep'
              361  LOAD_FAST            15  'i'
              364  BINARY_SUBSCR    
              365  LOAD_CONST               0
              368  BINARY_SUBSCR    
              369  LOAD_FAST            14  'costlimit'
              372  COMPARE_OP            4  >
              375  POP_JUMP_IF_FALSE   382  'to 382'

 L.  88       378  BREAK_LOOP       
              379  JUMP_FORWARD          0  'to 382'
            382_0  COME_FROM           379  '379'

 L.  89       382  LOAD_FAST            15  'i'
              385  LOAD_CONST               1
              388  INPLACE_ADD      
              389  STORE_FAST           15  'i'
              392  JUMP_BACK           340  'to 340'
              395  POP_BLOCK        
            396_0  COME_FROM           337  '337'

 L.  90       396  LOAD_FAST             5  'nextstep'
              399  LOAD_FAST            15  'i'
              402  SLICE+2          
              403  STORE_FAST            3  'current'
              406  JUMP_BACK            70  'to 70'
            409_0  COME_FROM            67  '67'

 L.  91       409  LOAD_FAST             4  'terminate'
              412  LOAD_ATTR            11  'sort'
              415  CALL_FUNCTION_0       0  None
              418  POP_TOP          

 L.  92       419  LOAD_GLOBAL          10  'len'
              422  LOAD_FAST             4  'terminate'
              425  CALL_FUNCTION_1       1  None
              428  LOAD_FAST             1  'nbeam'
              431  COMPARE_OP            4  >
              434  POP_JUMP_IF_FALSE   450  'to 450'

 L.  93       437  LOAD_FAST             4  'terminate'
              440  LOAD_FAST             1  'nbeam'
              443  SLICE+2          
              444  STORE_FAST            4  'terminate'
              447  JUMP_FORWARD          0  'to 450'
            450_0  COME_FROM           447  '447'

 L.  94       450  LOAD_FAST             4  'terminate'
              453  LOAD_CONST               0
              456  BINARY_SUBSCR    
              457  LOAD_CONST               0
              460  BINARY_SUBSCR    
              461  LOAD_FAST             2  'cbeam'
              464  BINARY_ADD       
              465  STORE_FAST           14  'costlimit'

 L.  95       468  BUILD_LIST_0          0 
              471  STORE_FAST           16  'o'

 L.  96       474  SETUP_LOOP           61  'to 538'
              477  LOAD_FAST             4  'terminate'
              480  GET_ITER         
              481  FOR_ITER             53  'to 537'
              484  UNPACK_SEQUENCE_2     2 
              487  STORE_FAST            6  'cost'
              490  STORE_FAST            8  'path'

 L.  97       493  LOAD_FAST             6  'cost'
              496  LOAD_FAST            14  'costlimit'
              499  COMPARE_OP            4  >
              502  POP_JUMP_IF_FALSE   509  'to 509'

 L.  98       505  BREAK_LOOP       
              506  JUMP_FORWARD          0  'to 509'
            509_0  COME_FROM           506  '506'

 L.  99       509  LOAD_FAST            16  'o'
              512  LOAD_ATTR             9  'append'
              515  LOAD_FAST             6  'cost'
              518  LOAD_FAST             8  'path'
              521  LOAD_ATTR            12  'rwalk'
              524  CALL_FUNCTION_0       0  None
              527  BUILD_TUPLE_2         2 
              530  CALL_FUNCTION_1       1  None
              533  POP_TOP          
              534  JUMP_BACK           481  'to 481'
              537  POP_BLOCK        
            538_0  COME_FROM           474  '474'

 L. 100       538  LOAD_FAST            16  'o'
              541  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 249


def test():
    graph = node(0.0, 'A')
    graph.add(node(0.0, 'B')).add(node(0.1, 'C')).add(node(0.2, 'D')).add(node(-0.3, terminal=1, label='E'))
    graph.add(node(1.0, 'a')).add(node(1, 'b')).add(node(2, terminal=1, label='c'))
    graph.add(node(0.0, label='q', terminal=1), 1.0, label='edge')
    print go(graph, 100, 1000.0)


if __name__ == '__main__':
    test()