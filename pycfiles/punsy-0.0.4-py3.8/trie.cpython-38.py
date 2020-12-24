# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/punsy/structs/trie.py
# Compiled at: 2020-04-04 09:06:49
# Size of source mod 2**32: 2912 bytes
r"""
A python implementation of the Trie data structure.

    https://en.wikipedia.org/wiki/Trie

The Trie is a memory-optimised data store for strings. It stores strings using a
k-ary tree structure (a tree in which each node has up to `k` children)

e.g. to store the words `car`, `cat`, 'bar' and 'bat'

       /- t
  b - a - r
/
- c - a -|- r
       \- t

Usage:

t = Trie()  # create a trie

t.insert('cat')                   # insert a word into the trie
t.insert('cat', 'feline')         # insert a word and associated metadata into the trie
'cat' in t,     t.contains('cat') # check if the trie contains a word
t['cat'],       t.get('cat')      # retrieve a node from the trie
t,              print(t)          # print the contents of the trie
"""
import os, sys

class Trie(object):
    __doc__ = '\n    A Trie class which implements insert, contains and get methods.\n    '

    def __init__(self, value=None, data=None):
        self.value = value
        self.children = dict()
        self.final = False
        self.data = list()
        if data:
            self.data.extend((data,))

    def insert(self, word, data=None):
        """Insert a word into the trie, with optional data attached"""
        current = self
        for i, letter in enumerate(word):
            try:
                current = current.children[letter]
            except KeyError:
                current.children[letter] = Trie()
                current = current.children[letter]
            else:
                current.value = letter
        else:
            current.final = True
            if data:
                current.data.extend((data,))

    def __getitem__(self, word):
        """Retrieve a node (or branch) from the trie by key, otherwise raise KeyError"""
        current = self
        for i, letter in enumerate(word):
            try:
                current = current.children[letter]
            except KeyError:
                raise KeyError(f'word "{word}" not found')

        else:
            return current

    def asdict(self):
        """Return a representation of the node as a dict, for use with visualising using JSON"""
        d = {}
        for k in ('data', 'value', 'final'):
            if k in self.__dict__:
                d[k] = self.__dict__[k]
            if self.children:
                d['children'] = {v.asdict():k for k, v in self.children.items()}
            return d

    def __repr__(self):
        """Flat string representation of the node"""
        if self.value is None:
            return f"(root) -> {self.children}"
        return f"{self.value} ({self.data}) -> {self.children}"

    def __contains__--- This code section failed: ---

 L.  87         0  SETUP_FINALLY        14  'to 14'

 L.  88         2  LOAD_FAST                'self'
                4  LOAD_FAST                'value'
                6  BINARY_SUBSCR    
                8  LOAD_ATTR                final
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  89        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  LOAD_GLOBAL              IndexError
               20  BUILD_TUPLE_2         2 
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    38  'to 38'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  90        32  POP_EXCEPT       
               34  LOAD_CONST               False
               36  RETURN_VALUE     
             38_0  COME_FROM            24  '24'
               38  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 28


if __name__ == '__main__':
    from IPython import embed
    print(__doc__)
    embed()