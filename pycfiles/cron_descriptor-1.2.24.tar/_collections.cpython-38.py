# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/urllib3/_collections.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 10792 bytes
from __future__ import absolute_import
try:
    from collections.abc import Mapping, MutableMapping
except ImportError:
    from collections import Mapping, MutableMapping
else:
    try:
        from threading import RLock
    except ImportError:

        class RLock:

            def __enter__(self):
                pass

            def __exit__(self, exc_type, exc_value, traceback):
                pass


    else:
        from collections import OrderedDict
        from .exceptions import InvalidHeader
        from packages.six import iterkeys, itervalues, PY3
        __all__ = [
         'RecentlyUsedContainer', 'HTTPHeaderDict']
        _Null = object()

        class RecentlyUsedContainer(MutableMapping):
            """RecentlyUsedContainer"""
            ContainerCls = OrderedDict

            def __init__(self, maxsize=10, dispose_func=None):
                self._maxsize = maxsize
                self.dispose_func = dispose_func
                self._container = self.ContainerCls()
                self.lock = RLock()

            def __getitem__--- This code section failed: ---

 L.  55         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lock
                4  SETUP_WITH           46  'to 46'
                6  POP_TOP          

 L.  56         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _container
               12  LOAD_METHOD              pop
               14  LOAD_FAST                'key'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'item'

 L.  57        20  LOAD_FAST                'item'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                _container
               26  LOAD_FAST                'key'
               28  STORE_SUBSCR     

 L.  58        30  LOAD_FAST                'item'
               32  POP_BLOCK        
               34  ROT_TWO          
               36  BEGIN_FINALLY    
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  POP_FINALLY           0  ''
               44  RETURN_VALUE     
             46_0  COME_FROM_WITH        4  '4'
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 32

            def __setitem__(self, key, value):
                evicted_value = _Null
                with self.lock:
                    evicted_value = self._container.get(key, _Null)
                    self._container[key] = value
                    if len(self._container) > self._maxsize:
                        _key, evicted_value = self._container.popitem(last=False)
                if self.dispose_func:
                    if evicted_value is not _Null:
                        self.dispose_funcevicted_value

            def __delitem__(self, key):
                with self.lock:
                    value = self._container.popkey
                if self.dispose_func:
                    self.dispose_funcvalue

            def __len__--- This code section failed: ---

 L.  83         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lock
                4  SETUP_WITH           30  'to 30'
                6  POP_TOP          

 L.  84         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _container
               14  CALL_FUNCTION_1       1  ''
               16  POP_BLOCK        
               18  ROT_TWO          
               20  BEGIN_FINALLY    
               22  WITH_CLEANUP_START
               24  WITH_CLEANUP_FINISH
               26  POP_FINALLY           0  ''
               28  RETURN_VALUE     
             30_0  COME_FROM_WITH        4  '4'
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 18

            def __iter__(self):
                raise NotImplementedError('Iteration over this class is unlikely to be threadsafe.')

            def clear(self):
                with self.lock:
                    values = list(itervalues(self._container))
                    self._container.clear()
                if self.dispose_func:
                    for value in values:
                        self.dispose_funcvalue

            def keys--- This code section failed: ---

 L. 102         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lock
                4  SETUP_WITH           34  'to 34'
                6  POP_TOP          

 L. 103         8  LOAD_GLOBAL              list
               10  LOAD_GLOBAL              iterkeys
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _container
               16  CALL_FUNCTION_1       1  ''
               18  CALL_FUNCTION_1       1  ''
               20  POP_BLOCK        
               22  ROT_TWO          
               24  BEGIN_FINALLY    
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  POP_FINALLY           0  ''
               32  RETURN_VALUE     
             34_0  COME_FROM_WITH        4  '4'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 22


        class HTTPHeaderDict(MutableMapping):
            """HTTPHeaderDict"""

            def __init__(self, headers=None, **kwargs):
                super(HTTPHeaderDict, self).__init__()
                self._container = OrderedDict()
                if headers is not None:
                    if isinstance(headers, HTTPHeaderDict):
                        self._copy_fromheaders
                    else:
                        self.extendheaders
                if kwargs:
                    self.extendkwargs

            def __setitem__(self, key, val):
                self._container[key.lower()] = [key, val]
                return self._container[key.lower()]

            def __getitem__(self, key):
                val = self._container[key.lower()]
                return ', '.joinval[1:]

            def __delitem__(self, key):
                del self._container[key.lower()]

            def __contains__(self, key):
                return key.lower() in self._container

            def __eq__(self, other):
                if not isinstance(other, Mapping):
                    if not hasattr(other, 'keys'):
                        return False
                if not isinstance(other, type(self)):
                    other = type(self)(other)
                return dict(((k.lower(), v) for k, v in self.itermerged())) == dict(((k.lower(), v) for k, v in other.itermerged()))

            def __ne__(self, other):
                return not self.__eq__other

            if not PY3:
                iterkeys = MutableMapping.iterkeys
                itervalues = MutableMapping.itervalues
            _HTTPHeaderDict__marker = object()

            def __len__(self):
                return len(self._container)

            def __iter__(self):
                for vals in self._container.values():
                    yield vals[0]

            def pop--- This code section failed: ---

 L. 198         0  SETUP_FINALLY        14  'to 14'

 L. 199         2  LOAD_FAST                'self'
                4  LOAD_FAST                'key'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'value'
               10  POP_BLOCK        
               12  JUMP_FORWARD         50  'to 50'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 200        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    48  'to 48'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 201        28  LOAD_FAST                'default'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _HTTPHeaderDict__marker
               34  COMPARE_OP               is
               36  POP_JUMP_IF_FALSE    40  'to 40'

 L. 202        38  RAISE_VARARGS_0       0  ''
             40_0  COME_FROM            36  '36'

 L. 203        40  LOAD_FAST                'default'
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  RETURN_VALUE     
             48_0  COME_FROM            20  '20'
               48  END_FINALLY      
             50_0  COME_FROM            12  '12'

 L. 205        50  LOAD_FAST                'self'
               52  LOAD_FAST                'key'
               54  DELETE_SUBSCR    

 L. 206        56  LOAD_FAST                'value'
               58  RETURN_VALUE     

Parse error at or near `ROT_FOUR' instruction at offset 42

            def discard(self, key):
                try:
                    del self[key]
                except KeyError:
                    pass

            def add(self, key, val):
                """Adds a (name, value) pair, doesn't overwrite the value if it already
        exists.

        >>> headers = HTTPHeaderDict(foo='bar')
        >>> headers.add('Foo', 'baz')
        >>> headers['foo']
        'bar, baz'
        """
                key_lower = key.lower()
                new_vals = [key, val]
                vals = self._container.setdefault(key_lower, new_vals)
                if new_vals is not vals:
                    vals.appendval

            def extend(self, *args, **kwargs):
                """Generic import function for any type of header-like object.
        Adapted version of MutableMapping.update in order to insert items
        with self.add instead of self.__setitem__
        """
                if len(args) > 1:
                    raise TypeError('extend() takes at most 1 positional arguments ({0} given)'.formatlen(args))
                else:
                    other = args[0] if len(args) >= 1 else ()
                    if isinstance(other, HTTPHeaderDict):
                        for key, val in other.iteritems():
                            self.add(key, val)

                    elif isinstance(other, Mapping):
                        for key in other:
                            self.add(key, other[key])

                    elif hasattr(other, 'keys'):
                        for key in other.keys():
                            self.add(key, other[key])

                    else:
                        for key, value in other:
                            self.add(key, value)

                for key, value in kwargs.items():
                    self.add(key, value)

            def getlist--- This code section failed: ---

 L. 261         0  SETUP_FINALLY        20  'to 20'

 L. 262         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _container
                6  LOAD_FAST                'key'
                8  LOAD_METHOD              lower
               10  CALL_METHOD_0         0  ''
               12  BINARY_SUBSCR    
               14  STORE_FAST               'vals'
               16  POP_BLOCK        
               18  JUMP_FORWARD         62  'to 62'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 263        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    60  'to 60'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 264        34  LOAD_FAST                'default'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _HTTPHeaderDict__marker
               40  COMPARE_OP               is
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 265        44  BUILD_LIST_0          0 
               46  ROT_FOUR         
               48  POP_EXCEPT       
               50  RETURN_VALUE     
             52_0  COME_FROM            42  '42'

 L. 266        52  LOAD_FAST                'default'
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  RETURN_VALUE     
             60_0  COME_FROM            26  '26'
               60  END_FINALLY      
             62_0  COME_FROM            18  '18'

 L. 268        62  LOAD_FAST                'vals'
               64  LOAD_CONST               1
               66  LOAD_CONST               None
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  RETURN_VALUE     

Parse error at or near `ROT_FOUR' instruction at offset 46

            getheaders = getlist
            getallmatchingheaders = getlist
            iget = getlist
            get_all = getlist

            def __repr__(self):
                return '%s(%s)' % (type(self).__name__, dict(self.itermerged()))

            def _copy_from(self, other):
                for key in other:
                    val = other.getlistkey
                    if isinstance(val, list):
                        val = list(val)
                    self._container[key.lower()] = [
                     key] + val

            def copy(self):
                clone = type(self)()
                clone._copy_fromself
                return clone

            def iteritems(self):
                """Iterate over all header lines, including duplicate ones."""
                for key in self:
                    vals = self._container[key.lower()]
                    for val in vals[1:]:
                        yield (
                         vals[0], val)

            def itermerged(self):
                """Iterate over all headers, merging duplicate ones together."""
                for key in self:
                    val = self._container[key.lower()]
                    yield (val[0], ', '.joinval[1:])

            def items(self):
                return list(self.iteritems())

            @classmethod
            def from_httplib(cls, message):
                """Read headers from a Python 2 httplib message object."""
                obs_fold_continued_leaders = (' ', '\t')
                headers = []
                for line in message.headers:
                    if line.startswithobs_fold_continued_leaders:
                        if not headers:
                            raise InvalidHeader('Header continuation with no previous header: %s' % line)
                        else:
                            key, value = headers[(-1)]
                            headers[-1] = (key, value + ' ' + line.strip())
                    else:
                        key, value = line.split(':', 1)
                        headers.append(key, value.strip())

                return cls(headers)