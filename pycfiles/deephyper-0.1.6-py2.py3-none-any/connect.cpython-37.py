# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/op/connect.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 1409 bytes
from ..op import Operation

class Connect(Operation):
    __doc__ = 'Connection node.\n\n    Represents a possibility to create a connection between n1 -> n2.\n\n    Args:\n        graph (nx.DiGraph): a graph\n        source_node (Node): source\n    '

    def __init__(self, search_space, source_node, *args, **kwargs):
        self.search_space = search_space
        self.source_node = source_node
        self.destin_node = None

    def __str__--- This code section failed: ---

 L.  20         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                source_node
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  LOAD_GLOBAL              list
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    94  'to 94'

 L.  21        14  LOAD_GLOBAL              len
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                source_node
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  LOAD_CONST               0
               24  COMPARE_OP               >
               26  POP_JUMP_IF_FALSE    88  'to 88'

 L.  22        28  LOAD_GLOBAL              str
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                source_node
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  LOAD_ATTR                id
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  STORE_FAST               'ids'

 L.  23        44  SETUP_LOOP           92  'to 92'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                source_node
               50  LOAD_CONST               1
               52  LOAD_CONST               None
               54  BUILD_SLICE_2         2 
               56  BINARY_SUBSCR    
               58  GET_ITER         
               60  FOR_ITER             84  'to 84'
               62  STORE_FAST               'n'

 L.  24        64  LOAD_FAST                'ids'
               66  LOAD_STR                 ','
               68  LOAD_GLOBAL              str
               70  LOAD_FAST                'n'
               72  LOAD_ATTR                id
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  BINARY_ADD       
               78  INPLACE_ADD      
               80  STORE_FAST               'ids'
               82  JUMP_BACK            60  'to 60'
               84  POP_BLOCK        
               86  JUMP_ABSOLUTE       102  'to 102'
             88_0  COME_FROM            26  '26'

 L.  26        88  LOAD_STR                 'None'
               90  STORE_FAST               'ids'
             92_0  COME_FROM_LOOP       44  '44'
               92  JUMP_FORWARD        102  'to 102'
             94_0  COME_FROM            12  '12'

 L.  28        94  LOAD_FAST                'self'
               96  LOAD_ATTR                source_node
               98  LOAD_ATTR                id
              100  STORE_FAST               'ids'
            102_0  COME_FROM            92  '92'

 L.  29       102  LOAD_FAST                'self'
              104  LOAD_ATTR                destin_node
              106  LOAD_CONST               None
              108  COMPARE_OP               is
              110  POP_JUMP_IF_FALSE   134  'to 134'

 L.  30       112  LOAD_GLOBAL              type
              114  LOAD_FAST                'self'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  LOAD_ATTR                __name__
              120  FORMAT_VALUE          0  ''
              122  LOAD_STR                 '_'
              124  LOAD_FAST                'ids'
              126  FORMAT_VALUE          0  ''
              128  LOAD_STR                 '->?'
              130  BUILD_STRING_4        4 
              132  RETURN_VALUE     
            134_0  COME_FROM           110  '110'

 L.  32       134  LOAD_GLOBAL              type
              136  LOAD_FAST                'self'
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  LOAD_ATTR                __name__
              142  FORMAT_VALUE          0  ''
              144  LOAD_STR                 '_'
              146  LOAD_FAST                'ids'
              148  FORMAT_VALUE          0  ''
              150  LOAD_STR                 '->'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                destin_node
              156  LOAD_ATTR                id
              158  FORMAT_VALUE          0  ''
              160  BUILD_STRING_5        5 
              162  RETURN_VALUE     

Parse error at or near `COME_FROM_LOOP' instruction at offset 92_0

    def init(self, current_node):
        """Set the connection in the search_space graph from [n1] -> n2.
        """
        self.destin_node = current_node
        if type(self.source_node) is list:
            for n in self.source_node:
                self.search_space.connect(n, self.destin_node)

        else:
            self.search_space.connect(self.source_node, self.destin_node)

    def __call__(self, value, *args, **kwargs):
        return value