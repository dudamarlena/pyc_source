# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\cache.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 9406 bytes
import attr

@attr.s(slots=True)
class Entry:
    key = attr.ib()
    value = attr.ib()
    score = attr.ib()
    pins = attr.ib(default=0)

    @property
    def sort_key(self):
        if self.pins == 0:
            return (0, self.score)
        return (1, )


class GenericCache:
    __doc__ = 'Generic supertype for cache implementations.\n\n    Defines a dict-like mapping with a maximum size, where as well as mapping\n    to a value, each key also maps to a score. When a write would cause the\n    dict to exceed its maximum size, it first evicts the existing key with\n    the smallest score, then adds the new key to the map.\n\n    A key has the following lifecycle:\n\n    1. key is written for the first time, the key is given the score\n       self.new_entry(key, value)\n    2. whenever an existing key is read or written, self.on_access(key, value,\n       score) is called. This returns a new score for the key.\n    3. When a key is evicted, self.on_evict(key, value, score) is called.\n\n    The cache will be in a valid state in all of these cases.\n\n    Implementations are expected to implement new_entry and optionally\n    on_access and on_evict to implement a specific scoring strategy.\n    '
    __slots__ = ('keys_to_indices', 'data', 'max_size', '__pinned_entry_count')

    def __init__(self, max_size):
        self.max_size = max_size
        self.keys_to_indices = {}
        self.data = []
        self._GenericCache__pinned_entry_count = 0

    def __len__(self):
        assert len(self.keys_to_indices) == len(self.data)
        return len(self.data)

    def __contains__(self, key):
        return key in self.keys_to_indices

    def __getitem__(self, key):
        i = self.keys_to_indices[key]
        result = self.data[i]
        self.on_access(result.key, result.value, result.score)
        self._GenericCache__balance(i)
        return result.value

    def __setitem__(self, key, value):
        if self.max_size == 0:
            return
        evicted = None
        try:
            i = self.keys_to_indices[key]
        except KeyError:
            if self.max_size == self._GenericCache__pinned_entry_count:
                raise ValueError('Cannot increase size of cache where all keys have been pinned.')
            else:
                entry = Entry(key, value, self.new_entry(key, value))
                if len(self.data) >= self.max_size:
                    evicted = self.data[0]
                    assert evicted.pins == 0
                    del self.keys_to_indices[evicted.key]
                    i = 0
                    self.data[0] = entry
                else:
                    i = len(self.data)
                self.data.append(entry)
            self.keys_to_indices[key] = i
        else:
            entry = self.data[i]
            assert entry.key == key
            entry.value = value
            entry.score = self.on_access(entry.key, entry.value, entry.score)
        self._GenericCache__balance(i)
        if evicted is not None:
            if self.data[0] is not entry:
                assert evicted.score <= self.data[0].score
            self.on_evict(evicted.key, evicted.value, evicted.score)

    def __iter__(self):
        return iter(self.keys_to_indices)

    def pin(self, key):
        """Mark ``key`` as pinned. That is, it may not be evicted until
        ``unpin(key)`` has been called. The same key may be pinned multiple
        times and will not be unpinned until the same number of calls to
        unpin have been made."""
        i = self.keys_to_indices[key]
        entry = self.data[i]
        entry.pins += 1
        if entry.pins == 1:
            self._GenericCache__pinned_entry_count += 1
            assert self._GenericCache__pinned_entry_count <= self.max_size
            self._GenericCache__balance(i)

    def unpin(self, key):
        """Undo one previous call to ``pin(key)``. Once all calls are
        undone this key may be evicted as normal."""
        i = self.keys_to_indices[key]
        entry = self.data[i]
        if entry.pins == 0:
            raise ValueError('Key %r has not been pinned' % (key,))
        entry.pins -= 1
        if entry.pins == 0:
            self._GenericCache__pinned_entry_count -= 1
            self._GenericCache__balance(i)

    def is_pinned(self, key):
        """Returns True if the key is currently pinned."""
        i = self.keys_to_indices[key]
        return self.data[i].pins > 0

    def clear(self):
        """Remove all keys, clearing their pinned status."""
        del self.data[:]
        self.keys_to_indices.clear()
        self._GenericCache__pinned_entry_count = 0

    def __repr__(self):
        return '{%s}' % (', '.join(('%r: %r' % (e.key, e.value) for e in self.data)),)

    def new_entry(self, key, value):
        """Called when a key is written that does not currently appear in the
        map.

        Returns the score to associate with the key.
        """
        raise NotImplementedError()

    def on_access(self, key, value, score):
        """Called every time a key that is already in the map is read or
        written.

        Returns the new score for the key.
        """
        return score

    def on_evict(self, key, value, score):
        """Called after a key has been evicted, with the score it had had at
        the point of eviction."""
        pass

    def check_valid(self):
        """Debugging method for use in tests.

        Asserts that all of the cache's invariants hold. When everything
        is working correctly this should be an expensive no-op.
        """
        for i, e in enumerate(self.data):
            assert self.keys_to_indices[e.key] == i
            for j in (i * 2 + 1, i * 2 + 2):
                if j < len(self.data) and not e.score <= self.data[j].score:
                    raise AssertionError(self.data)

    def __swap(self, i, j):
        assert i < j
        assert self.data[j].sort_key < self.data[i].sort_key
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.keys_to_indices[self.data[i].key] = i
        self.keys_to_indices[self.data[j].key] = j

    def __balance--- This code section failed: ---

 L. 208         0  LOAD_FAST                'i'
                2  LOAD_CONST               0
                4  COMPARE_OP               >
                6  POP_JUMP_IF_FALSE    54  'to 54'

 L. 209         8  LOAD_FAST                'i'
               10  LOAD_CONST               1
               12  BINARY_SUBTRACT  
               14  LOAD_CONST               2
               16  BINARY_FLOOR_DIVIDE
               18  STORE_FAST               'parent'

 L. 210        20  LOAD_DEREF               'self'
               22  LOAD_METHOD              _GenericCache__out_of_order
               24  LOAD_FAST                'parent'
               26  LOAD_FAST                'i'
               28  CALL_METHOD_2         2  ''
               30  POP_JUMP_IF_FALSE    54  'to 54'

 L. 211        32  LOAD_DEREF               'self'
               34  LOAD_METHOD              _GenericCache__swap
               36  LOAD_FAST                'parent'
               38  LOAD_FAST                'i'
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          

 L. 212        44  LOAD_FAST                'parent'
               46  STORE_FAST               'i'
               48  JUMP_BACK             0  'to 0'

 L. 214        50  BREAK_LOOP           54  'to 54'
               52  JUMP_BACK             0  'to 0'
             54_0  COME_FROM            30  '30'
             54_1  COME_FROM             6  '6'

 L. 216        54  LOAD_CLOSURE             'self'
               56  BUILD_TUPLE_1         1 
               58  LOAD_LISTCOMP            '<code_object <listcomp>>'
               60  LOAD_STR                 'GenericCache.__balance.<locals>.<listcomp>'
               62  MAKE_FUNCTION_8          'closure'
               64  LOAD_CONST               2
               66  LOAD_FAST                'i'
               68  BINARY_MULTIPLY  
               70  LOAD_CONST               1
               72  BINARY_ADD       
               74  LOAD_CONST               2
               76  LOAD_FAST                'i'
               78  BINARY_MULTIPLY  
               80  LOAD_CONST               2
               82  BINARY_ADD       
               84  BUILD_TUPLE_2         2 
               86  GET_ITER         
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'children'

 L. 217        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'children'
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_CONST               2
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   124  'to 124'

 L. 218       104  LOAD_FAST                'children'
              106  LOAD_ATTR                sort
              108  LOAD_CLOSURE             'self'
              110  BUILD_TUPLE_1         1 
              112  LOAD_LAMBDA              '<code_object <lambda>>'
              114  LOAD_STR                 'GenericCache.__balance.<locals>.<lambda>'
              116  MAKE_FUNCTION_8          'closure'
              118  LOAD_CONST               ('key',)
              120  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              122  POP_TOP          
            124_0  COME_FROM           102  '102'

 L. 219       124  LOAD_FAST                'children'
              126  GET_ITER         
            128_0  COME_FROM           142  '142'
              128  FOR_ITER            166  'to 166'
              130  STORE_FAST               'j'

 L. 220       132  LOAD_DEREF               'self'
              134  LOAD_METHOD              _GenericCache__out_of_order
              136  LOAD_FAST                'i'
              138  LOAD_FAST                'j'
              140  CALL_METHOD_2         2  ''
              142  POP_JUMP_IF_FALSE   128  'to 128'

 L. 221       144  LOAD_DEREF               'self'
              146  LOAD_METHOD              _GenericCache__swap
              148  LOAD_FAST                'i'
              150  LOAD_FAST                'j'
              152  CALL_METHOD_2         2  ''
              154  POP_TOP          

 L. 222       156  LOAD_FAST                'j'
              158  STORE_FAST               'i'

 L. 223       160  POP_TOP          
              162  CONTINUE             54  'to 54'
              164  JUMP_BACK           128  'to 128'

 L. 225       166  BREAK_LOOP          170  'to 170'
              168  JUMP_BACK            54  'to 54'

Parse error at or near `CONTINUE' instruction at offset 162

    def __out_of_order(self, i, j):
        """Returns True if the indices i, j are in the wrong order.

        i must be the parent of j.
        """
        assert i == (j - 1) // 2
        return self.data[j].sort_key < self.data[i].sort_key


class LRUReusedCache(GenericCache):
    __doc__ = 'The only concrete implementation of GenericCache we use outside of tests\n    currently.\n\n    Adopts a modified least-frequently used eviction policy: It evicts the key\n    that has been used least recently, but it will always preferentially evict\n    keys that have only ever been accessed once. Among keys that have been\n    accessed more than once, it ignores the number of accesses.\n\n    This retains most of the benefits of an LRU cache, but adds an element of\n    scan-resistance to the process: If we end up scanning through a large\n    number of keys without reusing them, this does not evict the existing\n    entries in preference for the new ones.\n    '
    __slots__ = ('__tick', )

    def __init__(self, max_size):
        super().__init__(max_size)
        self._LRUReusedCache__tick = 0

    def tick(self):
        self._LRUReusedCache__tick += 1
        return self._LRUReusedCache__tick

    def new_entry(self, key, value):
        return [
         1, self.tick()]

    def on_access(self, key, value, score):
        score[0] = 2
        score[1] = self.tick()
        return score