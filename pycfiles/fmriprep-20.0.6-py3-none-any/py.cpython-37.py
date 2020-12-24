# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_vendor/html5lib/_trie/py.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 1775 bytes
from __future__ import absolute_import, division, unicode_literals
from pip._vendor.six import text_type
from bisect import bisect_left
from ._base import Trie as ABCTrie

class Trie(ABCTrie):

    def __init__(self, data):
        if not all((isinstance(x, text_type) for x in data.keys())):
            raise TypeError('All keys must be strings')
        self._data = data
        self._keys = sorted(data.keys())
        self._cachestr = ''
        self._cachepoints = (0, len(data))

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def keys--- This code section failed: ---

 L.  32         0  LOAD_FAST                'prefix'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_TRUE     22  'to 22'
                8  LOAD_FAST                'prefix'
               10  LOAD_STR                 ''
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_TRUE     22  'to 22'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _keys
               20  POP_JUMP_IF_TRUE     32  'to 32'
             22_0  COME_FROM            14  '14'
             22_1  COME_FROM             6  '6'

 L.  33        22  LOAD_GLOBAL              set
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _keys
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  RETURN_VALUE     
             32_0  COME_FROM            20  '20'

 L.  35        32  LOAD_FAST                'prefix'
               34  LOAD_METHOD              startswith
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _cachestr
               40  CALL_METHOD_1         1  '1 positional argument'
               42  POP_JUMP_IF_FALSE    76  'to 76'

 L.  36        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _cachepoints
               48  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST               'lo'
               52  STORE_FAST               'hi'

 L.  37        54  LOAD_GLOBAL              bisect_left
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _keys
               60  LOAD_FAST                'prefix'
               62  LOAD_FAST                'lo'
               64  LOAD_FAST                'hi'
               66  CALL_FUNCTION_4       4  '4 positional arguments'
               68  DUP_TOP          
               70  STORE_FAST               'start'
               72  STORE_FAST               'i'
               74  JUMP_FORWARD         92  'to 92'
             76_0  COME_FROM            42  '42'

 L.  39        76  LOAD_GLOBAL              bisect_left
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _keys
               82  LOAD_FAST                'prefix'
               84  CALL_FUNCTION_2       2  '2 positional arguments'
               86  DUP_TOP          
               88  STORE_FAST               'start'
               90  STORE_FAST               'i'
             92_0  COME_FROM            74  '74'

 L.  41        92  LOAD_GLOBAL              set
               94  CALL_FUNCTION_0       0  '0 positional arguments'
               96  STORE_FAST               'keys'

 L.  42        98  LOAD_FAST                'start'
              100  LOAD_GLOBAL              len
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                _keys
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   116  'to 116'

 L.  43       112  LOAD_FAST                'keys'
              114  RETURN_VALUE     
            116_0  COME_FROM           110  '110'

 L.  45       116  SETUP_LOOP          162  'to 162'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                _keys
              122  LOAD_FAST                'i'
              124  BINARY_SUBSCR    
              126  LOAD_METHOD              startswith
              128  LOAD_FAST                'prefix'
              130  CALL_METHOD_1         1  '1 positional argument'
              132  POP_JUMP_IF_FALSE   160  'to 160'

 L.  46       134  LOAD_FAST                'keys'
              136  LOAD_METHOD              add
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                _keys
              142  LOAD_FAST                'i'
              144  BINARY_SUBSCR    
              146  CALL_METHOD_1         1  '1 positional argument'
              148  POP_TOP          

 L.  47       150  LOAD_FAST                'i'
              152  LOAD_CONST               1
              154  INPLACE_ADD      
              156  STORE_FAST               'i'
              158  JUMP_BACK           118  'to 118'
            160_0  COME_FROM           132  '132'
              160  POP_BLOCK        
            162_0  COME_FROM_LOOP      116  '116'

 L.  49       162  LOAD_FAST                'prefix'
              164  LOAD_FAST                'self'
              166  STORE_ATTR               _cachestr

 L.  50       168  LOAD_FAST                'start'
              170  LOAD_FAST                'i'
              172  BUILD_TUPLE_2         2 
              174  LOAD_FAST                'self'
              176  STORE_ATTR               _cachepoints

 L.  52       178  LOAD_FAST                'keys'
              180  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 180

    def has_keys_with_prefix(self, prefix):
        if prefix in self._data:
            return True
        elif prefix.startswithself._cachestr:
            lo, hi = self._cachepoints
            i = bisect_leftself._keysprefixlohi
        else:
            i = bisect_left(self._keys, prefix)
        if i == len(self._keys):
            return False
        return self._keys[i].startswithprefix