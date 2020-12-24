# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\templ\stack.py
# Compiled at: 2013-07-26 11:14:51
"""
Copyright 2013 Brian Mearns

This file is part of templ.

templ is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

templ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with templ.  If not, see <http://www.gnu.org/licenses/>.
"""
import collections, ttypes

class Scope(dict):
    """
    A scope is just a simple dictionary of TType values, used for tracking variables in a particular
    scope.
    """

    def __init__(self, d=None, **kwargs):
        super(Scope, self).__init__()
        self.__locked = []
        if isinstance(d, collections.Mapping):
            for k, v in d.items():
                self[k] = v

        for k, v in kwargs.items():
            self[k] = v

    def __setitem__(self, key, val):
        try:
            key = ttypes.String(key)
        except TypeError:
            raise TypeError('Invalid key, requires a String, received a %s' % type(key))

        if not isinstance(val, ttypes.TType):
            raise TypeError('Invalid value, requires a TType, received a %s' % type(val))
        if key in self.__locked:
            raise KeyError('Key is locked, and cannot be modified: %s' % key)
        super(Scope, self).__setitem__(key, val)

    def lock(self, key):
        try:
            key = ttypes.String(key)
        except TypeError:
            raise TypeError('Invalid key, requires a String, received a %s' % type(key))

        if key in self.__locked:
            raise KeyError('Key is already locked: %s' % key)
        self.__locked.append(key)

    def unlock(self, key):
        try:
            key = ttypes.String(key)
        except TypeError:
            raise TypeError('Invalid key, requires a String, received a %s' % type(key))

        if key not in self.__locked:
            raise KeyError('Key is not locked, cannot be unlocked: %s' % key)
        self.__locked.remove(key)

    def islocked(self, key):
        try:
            key = ttypes.String(key)
        except TypeError:
            raise TypeError('Invalid key, requires a String, received a %s' % type(key))

        return key in self.__locked


class Stack(collections.Sequence):
    """
    The Stack is a simple list of Scopes, with the deepest/most-recent scope at the highest
    index. The list has the interface of an *immutable* sequence, plus the push and pop
    methods so you can add and remove scopes.
    """

    def __init__(self, scope=None):
        super(Stack, self).__init__()
        self.__list = collections.deque()
        if scope is None:
            self.__list.append(Scope())
        elif isinstance(scope, Scope):
            self.__list.append(scope)
        elif isinstance(scope, collections.Mapping):
            self.__list.append(Scope(scope))
        else:
            raise TypeError('Scope must be a Scope object.')
        return

    def push(self):
        """
        Creates and returns a new empty scope to the end of the stack.
        """
        scope = Scope()
        self.__list.append(scope)
        return scope

    def pop(self):
        """
        Removes the bottom scope from the stack.
        """
        if len(self.__list) < 2:
            raise Exception('Cannot pop global scope.')
        self.__list.pop()

    def find(self, symbol):
        """
        Returns the index into the stack of the deepest (highest index) scope in which the specified
        key is defined. Returns None if there is no such key defined in the stack.
        """
        try:
            symbol = ttypes.String(symbol)
        except TypeError:
            raise TypeError('Invalid name: can only lookup Strings, not %s' % type(symbol))

        for i in reversed(range(len(self.__list))):
            if symbol in self.__list[i]:
                return i

        return

    def lookup--- This code section failed: ---

 L. 132         0  SETUP_EXCEPT         19  'to 22'

 L. 133         3  LOAD_GLOBAL           0  'ttypes'
                6  LOAD_ATTR             1  'String'
                9  LOAD_FAST             1  'symbol'
               12  CALL_FUNCTION_1       1  None
               15  STORE_FAST            1  'symbol'
               18  POP_BLOCK        
               19  JUMP_FORWARD         39  'to 61'
             22_0  COME_FROM             0  '0'

 L. 134        22  DUP_TOP          
               23  LOAD_GLOBAL           2  'TypeError'
               26  COMPARE_OP           10  exception-match
               29  POP_JUMP_IF_FALSE    60  'to 60'
               32  POP_TOP          
               33  POP_TOP          
               34  POP_TOP          

 L. 135        35  LOAD_GLOBAL           2  'TypeError'
               38  LOAD_CONST               'Invalid name: can only lookup Strings, not %s'
               41  LOAD_GLOBAL           3  'type'
               44  LOAD_FAST             1  'symbol'
               47  CALL_FUNCTION_1       1  None
               50  BINARY_MODULO    
               51  CALL_FUNCTION_1       1  None
               54  RAISE_VARARGS_1       1  None
               57  JUMP_FORWARD          1  'to 61'
               60  END_FINALLY      
             61_0  COME_FROM            60  '60'
             61_1  COME_FROM            19  '19'

 L. 137        61  LOAD_FAST             0  'self'
               64  LOAD_ATTR             4  'find'
               67  LOAD_FAST             1  'symbol'
               70  CALL_FUNCTION_1       1  None
               73  STORE_FAST            2  'i'

 L. 138        76  LOAD_FAST             2  'i'
               79  LOAD_CONST               None
               82  COMPARE_OP            8  is
               85  POP_JUMP_IF_FALSE    92  'to 92'

 L. 139        88  LOAD_CONST               None
               91  RETURN_END_IF    
             92_0  COME_FROM            85  '85'

 L. 141        92  LOAD_FAST             0  'self'
               95  LOAD_ATTR             6  '__list'
               98  LOAD_FAST             2  'i'
              101  BINARY_SUBSCR    
              102  LOAD_FAST             1  'symbol'
              105  BINARY_SUBSCR    
              106  STORE_FAST            3  'val'

 L. 142       109  LOAD_GLOBAL           7  'isinstance'
              112  LOAD_FAST             3  'val'
              115  LOAD_GLOBAL           0  'ttypes'
              118  LOAD_ATTR             8  'TType'
              121  CALL_FUNCTION_2       2  None
              124  POP_JUMP_IF_TRUE    142  'to 142'
              127  LOAD_ASSERT              AssertionError
              130  LOAD_GLOBAL          10  'repr'
              133  LOAD_FAST             3  'val'
              136  CALL_FUNCTION_1       1  None
              139  RAISE_VARARGS_2       2  None

 L. 143       142  LOAD_FAST             3  'val'
              145  RETURN_VALUE     
              146  LOAD_CONST               None
              149  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 146

    def exists(self, symbol):
        """
        checks if the specified symbol exists anywhere in the stack.
        """
        return self.find(symbol) is not None

    def localExists(self, symbol):
        """
        Determines if the specified symbol is defined in the deepest scope.
        """
        return symbol in self.__list[(-1)]

    def set(self, symbol, val):
        """
        If the named symbol exists in anywhere in the stack, it's value is set to val.
        Otherwise, a new variable is alloced in the deepest scope and and set to val.
        """
        idx = self.find(symbol)
        if idx is None:
            idx = -1
        self.__list[idx][symbol] = val
        return

    def new(self, symbol, val):
        """
        Allocates a new variable in the deepest scope, sets it's value to val. If it already
        exists in that scope, raises a KeyError. Use localExists to test in advance.
        """
        if symbol in self.__list[(-1)]:
            raise KeyError('Local variable already exists: %s' % symbol)
        self.__list[(-1)][symbol] = val

    def local(self):
        """
        Returns the current deepest scope.
        """
        return self.__list[(-1)]

    def depth(self):
        """
        An alias for __len__, returns the number of scopes currently in the stack.
        """
        return len(self.__list)

    def __getitem__(self, idx):
        return self.__list[idx]

    def __len__(self):
        return len(self.__list)