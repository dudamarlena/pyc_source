# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\junkdrawer.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 6250 bytes
"""A module for miscellaneous useful bits and bobs that don't
obviously belong anywhere else. If you spot a better home for
anything that lives here, please move it."""
import array

def array_or_list(code, contents):
    if code == 'O':
        return list(contents)
    return array.array(code, contents)


def replace_all(buffer, replacements):
    """Substitute multiple replacement values into a buffer.

    Replacements is a list of (start, end, value) triples.
    """
    result = bytearray()
    prev = 0
    offset = 0
    for u, v, r in replacements:
        result.extend(buffer[prev:u])
        result.extend(r)
        prev = v
        offset += len(r) - (v - u)
    else:
        result.extend(buffer[prev:])
        assert len(result) == len(buffer) + offset
        return bytes(result)


ARRAY_CODES = [
 'B', 'H', 'I', 'L', 'Q', 'O']
NEXT_ARRAY_CODE = dict(zip(ARRAY_CODES, ARRAY_CODES[1:]))

class IntList:
    __doc__ = 'Class for storing a list of non-negative integers compactly.\n\n    We store them as the smallest size integer array we can get\n    away with. When we try to add an integer that is too large,\n    we upgrade the array to the smallest word size needed to store\n    the new value.'
    __slots__ = ('__underlying', )

    def __init__--- This code section failed: ---

 L.  63         0  LOAD_GLOBAL              ARRAY_CODES
                2  GET_ITER         
                4  FOR_ITER             54  'to 54'
                6  STORE_FAST               'code'

 L.  64         8  SETUP_FINALLY        32  'to 32'

 L.  65        10  LOAD_GLOBAL              array_or_list
               12  LOAD_FAST                'code'
               14  LOAD_FAST                'values'
               16  CALL_FUNCTION_2       2  ''
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _IntList__underlying

 L.  66        22  POP_BLOCK        
               24  POP_TOP          
               26  JUMP_ABSOLUTE        68  'to 68'
               28  POP_BLOCK        
               30  JUMP_BACK             4  'to 4'
             32_0  COME_FROM_FINALLY     8  '8'

 L.  67        32  DUP_TOP          
               34  LOAD_GLOBAL              OverflowError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    50  'to 50'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.  68        46  POP_EXCEPT       
               48  JUMP_BACK             4  'to 4'
             50_0  COME_FROM            38  '38'
               50  END_FINALLY      
               52  JUMP_BACK             4  'to 4'

 L.  70        54  LOAD_GLOBAL              AssertionError
               56  LOAD_STR                 'Could not create storage for %r'
               58  LOAD_FAST                'values'
               60  BUILD_TUPLE_1         1 
               62  BINARY_MODULO    
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'

 L.  71        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _IntList__underlying
               74  LOAD_GLOBAL              list
               76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_FALSE   124  'to 124'

 L.  72        80  LOAD_FAST                'self'
               82  LOAD_ATTR                _IntList__underlying
               84  GET_ITER         
             86_0  COME_FROM           106  '106'
               86  FOR_ITER            124  'to 124'
               88  STORE_FAST               'v'

 L.  73        90  LOAD_FAST                'v'
               92  LOAD_CONST               0
               94  COMPARE_OP               <
               96  POP_JUMP_IF_TRUE    108  'to 108'
               98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'v'
              102  LOAD_GLOBAL              int
              104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_TRUE     86  'to 86'
            108_0  COME_FROM            96  '96'

 L.  74       108  LOAD_GLOBAL              ValueError
              110  LOAD_STR                 'Could not create IntList for %r'
              112  LOAD_FAST                'values'
              114  BUILD_TUPLE_1         1 
              116  BINARY_MODULO    
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
              122  JUMP_BACK            86  'to 86'
            124_0  COME_FROM            78  '78'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 26

    @classmethod
    def of_length(self, n):
        return IntList(array_or_list('B', [0]) * n)

    def count(self, n):
        return self._IntList__underlying.count(n)

    def __repr__(self):
        return 'IntList(%r)' % (list(self),)

    def __len__(self):
        return len(self._IntList__underlying)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return IntList(self._IntList__underlying[i])
        return self._IntList__underlying[i]

    def __delitem__(self, i):
        del self._IntList__underlying[i]

    def __iter__(self):
        return iter(self._IntList__underlying)

    def __eq__(self, other):
        if self is other:
            return True
        else:
            return isinstance(other, IntList) or NotImplemented
        return self._IntList__underlying == other._IntList__underlying

    def __ne__(self, other):
        if self is other:
            return False
        else:
            return isinstance(other, IntList) or NotImplemented
        return self._IntList__underlying != other._IntList__underlying

    def append(self, n):
        i = len(self)
        self._IntList__underlying.append(0)
        self[i] = n

    def __setitem__--- This code section failed: ---

 L. 121         0  SETUP_FINALLY        18  'to 18'

 L. 122         2  LOAD_FAST                'n'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _IntList__underlying
                8  LOAD_FAST                'i'
               10  STORE_SUBSCR     

 L. 123        12  POP_BLOCK        
               14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 124        18  DUP_TOP          
               20  LOAD_GLOBAL              OverflowError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    56  'to 56'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 125        32  LOAD_FAST                'n'
               34  LOAD_CONST               0
               36  COMPARE_OP               >
               38  POP_JUMP_IF_TRUE     44  'to 44'
               40  LOAD_ASSERT              AssertionError
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            38  '38'

 L. 126        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _IntList__upgrade
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
               52  POP_EXCEPT       
               54  JUMP_BACK             0  'to 0'
             56_0  COME_FROM            24  '24'
               56  END_FINALLY      
               58  JUMP_BACK             0  'to 0'

Parse error at or near `RETURN_VALUE' instruction at offset 16

    def extend(self, ls):
        for n in ls:
            self.append(n)

    def __upgrade(self):
        code = NEXT_ARRAY_CODE[self._IntList__underlying.typecode]
        self._IntList__underlying = array_or_list(code, self._IntList__underlying)


def binary_search(lo, hi, f):
    """Binary searches in [lo , hi) to find
    n such that f(n) == f(lo) but f(n + 1) != f(lo).
    It is implicitly assumed and will not be checked
    that f(hi) != f(lo).
    """
    reference = f(lo)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if f(mid) == reference:
            lo = mid
        else:
            hi = mid

    return lo


def uniform(random, n):
    """Returns a bytestring of length n, distributed uniformly at random."""
    return random.getrandbits(n * 8).to_bytes(n, 'big')


class LazySequenceCopy:
    __doc__ = 'A "copy" of a sequence that works by inserting a mask in front\n    of the underlying sequence, so that you can mutate it without changing\n    the underlying sequence. Effectively behaves as if you could do list(x)\n    in O(1) time. The full list API is not supported yet but there\'s no reason\n    in principle it couldn\'t be.'

    def __init__(self, values):
        self._LazySequenceCopy__values = values
        self._LazySequenceCopy__len = len(values)
        self._LazySequenceCopy__mask = None

    def __len__(self):
        return self._LazySequenceCopy__len

    def pop(self):
        if len(self) == 0:
            raise IndexError('Cannot pop from empty list')
        result = self[(-1)]
        self._LazySequenceCopy__len -= 1
        if self._LazySequenceCopy__mask is not None:
            self._LazySequenceCopy__mask.pop(self._LazySequenceCopy__len, None)
        return result

    def __getitem__(self, i):
        i = self._LazySequenceCopy__check_index(i)
        default = self._LazySequenceCopy__values[i]
        if self._LazySequenceCopy__mask is None:
            return default
        return self._LazySequenceCopy__mask.get(i, default)

    def __setitem__(self, i, v):
        i = self._LazySequenceCopy__check_index(i)
        if self._LazySequenceCopy__mask is None:
            self._LazySequenceCopy__mask = {}
        self._LazySequenceCopy__mask[i] = v

    def __check_index(self, i):
        n = len(self)
        if i < -n or i >= n:
            raise IndexError('Index %d out of range [0, %d)' % (i, n))
        if i < 0:
            i += n
        assert 0 <= i < n
        return i


def clamp(lower, value, upper):
    """Given a value and lower/upper bounds, 'clamp' the value so that
    it satisfies lower <= value <= upper."""
    return max(lower, min(value, upper))


def swap(ls, i, j):
    """Swap the elements ls[i], ls[j]."""
    if i == j:
        return
    ls[i], ls[j] = ls[j], ls[i]