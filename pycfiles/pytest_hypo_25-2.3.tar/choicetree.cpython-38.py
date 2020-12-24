# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\choicetree.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 4271 bytes
from collections import defaultdict

class Chooser:
    __doc__ = 'A source of nondeterminism for use in shrink passes.'

    def __init__(self, tree, prefix):
        self._Chooser__prefix = prefix
        self._Chooser__tree = tree
        self._Chooser__node_trail = [tree.root]
        self._Chooser__choices = []
        self._Chooser__finished = False

    def choose(self, values, condition=lambda x: True):
        """Return some element of values satisfying the condition
        that will not lead to an exhausted branch, or raise DeadBranch
        if no such element exist".
        """
        if self._Chooser__finished:
            raise AssertionError
        else:
            node = self._Chooser__node_trail[(-1)]
            if node.live_child_count is None:
                node.live_child_count = len(values)
                node.n = len(values)
            elif not node.live_child_count > 0:
                assert len(values) == 0
            else:
                depth = len(self._Chooser__choices)
                if depth < len(self._Chooser__prefix):
                    i = self._Chooser__prefix[depth]
                    if i >= len(values):
                        i = 0
                else:
                    i = 0
            count = 0
            while True:
                if node.live_child_count > 0:
                    count += 1
                    assert count <= len(values)
                    if not node.children[i].exhausted:
                        v = values[i]
                        if condition(v):
                            self._Chooser__choices.append(i)
                            self._Chooser__node_trail.append(node.children[i])
                            return v
                        node.children[i] = DeadNode
                        node.live_child_count -= 1
                    i = (i + 1) % len(values)

        raise DeadBranch()

    def finish--- This code section failed: ---

 L.  70         0  LOAD_CONST               True
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _Chooser__finished

 L.  71         6  LOAD_GLOBAL              len
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _Chooser__node_trail
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_GLOBAL              len
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _Chooser__choices
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_CONST               1
               24  BINARY_ADD       
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  LOAD_ASSERT              AssertionError
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            28  '28'

 L.  73        34  LOAD_GLOBAL              list
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _Chooser__choices
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'next_value'

 L.  74        44  LOAD_FAST                'next_value'
               46  POP_JUMP_IF_FALSE   152  'to 152'

 L.  75        48  LOAD_FAST                'next_value'
               50  LOAD_CONST               -1
               52  DUP_TOP_TWO      
               54  BINARY_SUBSCR    
               56  LOAD_CONST               1
               58  INPLACE_ADD      
               60  ROT_THREE        
               62  STORE_SUBSCR     

 L.  76        64  LOAD_GLOBAL              range
               66  LOAD_GLOBAL              len
               68  LOAD_FAST                'next_value'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_CONST               1
               74  BINARY_SUBTRACT  
               76  LOAD_CONST               -1
               78  LOAD_CONST               -1
               80  CALL_FUNCTION_3       3  ''
               82  GET_ITER         
               84  FOR_ITER            152  'to 152'
               86  STORE_FAST               'i'

 L.  77        88  LOAD_FAST                'next_value'
               90  LOAD_FAST                'i'
               92  BINARY_SUBSCR    
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                _Chooser__node_trail
               98  LOAD_FAST                'i'
              100  BINARY_SUBSCR    
              102  LOAD_ATTR                n
              104  COMPARE_OP               >=
              106  POP_JUMP_IF_FALSE   146  'to 146'

 L.  78       108  LOAD_CONST               0
              110  LOAD_FAST                'next_value'
              112  LOAD_FAST                'i'
              114  STORE_SUBSCR     

 L.  79       116  LOAD_FAST                'i'
              118  LOAD_CONST               0
              120  COMPARE_OP               >
              122  POP_JUMP_IF_FALSE   150  'to 150'

 L.  80       124  LOAD_FAST                'next_value'
              126  LOAD_FAST                'i'
              128  LOAD_CONST               1
              130  BINARY_SUBTRACT  
              132  DUP_TOP_TWO      
              134  BINARY_SUBSCR    
              136  LOAD_CONST               1
              138  INPLACE_ADD      
              140  ROT_THREE        
              142  STORE_SUBSCR     
              144  JUMP_BACK            84  'to 84'
            146_0  COME_FROM           106  '106'

 L.  82       146  POP_TOP          
              148  JUMP_ABSOLUTE       152  'to 152'
            150_0  COME_FROM           122  '122'
              150  JUMP_BACK            84  'to 84'
            152_0  COME_FROM            46  '46'

 L.  84       152  LOAD_CONST               0
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                _Chooser__node_trail
              158  LOAD_CONST               -1
              160  BINARY_SUBSCR    
              162  STORE_ATTR               live_child_count

 L.  85       164  LOAD_GLOBAL              len
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                _Chooser__node_trail
              170  CALL_FUNCTION_1       1  ''
              172  LOAD_CONST               1
              174  COMPARE_OP               >
          176_178  POP_JUMP_IF_FALSE   274  'to 274'
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                _Chooser__node_trail
              184  LOAD_CONST               -1
              186  BINARY_SUBSCR    
              188  LOAD_ATTR                exhausted
          190_192  POP_JUMP_IF_FALSE   274  'to 274'

 L.  86       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _Chooser__node_trail
              198  LOAD_METHOD              pop
              200  CALL_METHOD_0         0  ''
              202  POP_TOP          

 L.  87       204  LOAD_GLOBAL              len
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                _Chooser__node_trail
              210  CALL_FUNCTION_1       1  ''
              212  LOAD_GLOBAL              len
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                _Chooser__choices
              218  CALL_FUNCTION_1       1  ''
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_TRUE    228  'to 228'
              224  LOAD_ASSERT              AssertionError
              226  RAISE_VARARGS_1       1  'exception instance'
            228_0  COME_FROM           222  '222'

 L.  88       228  LOAD_FAST                'self'
              230  LOAD_ATTR                _Chooser__choices
              232  LOAD_METHOD              pop
              234  CALL_METHOD_0         0  ''
              236  STORE_FAST               'i'

 L.  89       238  LOAD_FAST                'self'
              240  LOAD_ATTR                _Chooser__node_trail
              242  LOAD_CONST               -1
              244  BINARY_SUBSCR    
              246  STORE_FAST               'target'

 L.  90       248  LOAD_GLOBAL              DeadNode
              250  LOAD_FAST                'target'
              252  LOAD_ATTR                children
              254  LOAD_FAST                'i'
              256  STORE_SUBSCR     

 L.  91       258  LOAD_FAST                'target'
              260  DUP_TOP          
              262  LOAD_ATTR                live_child_count
              264  LOAD_CONST               1
              266  INPLACE_SUBTRACT 
              268  ROT_TWO          
              270  STORE_ATTR               live_child_count
              272  JUMP_BACK           164  'to 164'
            274_0  COME_FROM           190  '190'
            274_1  COME_FROM           176  '176'

 L.  93       274  LOAD_GLOBAL              len
              276  LOAD_FAST                'next_value'
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_CONST               0
              282  COMPARE_OP               >
          284_286  POP_JUMP_IF_FALSE   314  'to 314'
              288  LOAD_FAST                'next_value'
              290  LOAD_CONST               -1
              292  BINARY_SUBSCR    
              294  LOAD_CONST               0
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_FALSE   314  'to 314'

 L.  94       302  LOAD_FAST                'next_value'
              304  LOAD_METHOD              pop
              306  CALL_METHOD_0         0  ''
              308  POP_TOP          
          310_312  JUMP_BACK           274  'to 274'
            314_0  COME_FROM           298  '298'
            314_1  COME_FROM           284  '284'

 L.  96       314  LOAD_GLOBAL              tuple
              316  LOAD_FAST                'next_value'
              318  CALL_FUNCTION_1       1  ''
              320  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 148


class ChoiceTree:
    __doc__ = 'Records sequences of choices made during shrinking so that we\n    can track what parts of a pass has run. Used to create Chooser\n    objects that are the main interface that a pass uses to make\n    decisions about what to do.\n    '

    def __init__(self):
        self.root = TreeNode()

    @property
    def exhausted(self):
        return self.root.exhausted

    def step(self, prefix, f):
        assert not self.exhausted
        chooser = Chooser(self, prefix)
        try:
            f(chooser)
        except DeadBranch:
            pass
        else:
            return chooser.finish


class TreeNode:

    def __init__(self):
        self.children = defaultdict(TreeNode)
        self.live_child_count = None
        self.n = None

    @property
    def exhausted(self):
        return self.live_child_count == 0


DeadNode = TreeNode()
DeadNode.live_child_count = 0

class DeadBranch(Exception):
    pass