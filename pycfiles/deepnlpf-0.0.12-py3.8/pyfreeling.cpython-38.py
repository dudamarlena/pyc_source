# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/helpers/freeling_api_py3/pyfreeling.py
# Compiled at: 2019-07-17 16:15:18
# Size of source mod 2**32: 289082 bytes
from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):

    def swig_import_helper--- This code section failed: ---

 L.  10         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              importlib
                6  STORE_FAST               'importlib'

 L.  11         8  LOAD_GLOBAL              __name__
               10  LOAD_METHOD              rpartition
               12  LOAD_STR                 '.'
               14  CALL_METHOD_1         1  ''
               16  LOAD_CONST               0
               18  BINARY_SUBSCR    
               20  STORE_FAST               'pkg'

 L.  12        22  LOAD_STR                 '.'
               24  LOAD_METHOD              join
               26  LOAD_FAST                'pkg'
               28  LOAD_STR                 '_pyfreeling'
               30  BUILD_TUPLE_2         2 
               32  CALL_METHOD_1         1  ''
               34  LOAD_METHOD              lstrip
               36  LOAD_STR                 '.'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'mname'

 L.  13        42  SETUP_FINALLY        56  'to 56'

 L.  14        44  LOAD_FAST                'importlib'
               46  LOAD_METHOD              import_module
               48  LOAD_FAST                'mname'
               50  CALL_METHOD_1         1  ''
               52  POP_BLOCK        
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY    42  '42'

 L.  15        56  DUP_TOP          
               58  LOAD_GLOBAL              ImportError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    84  'to 84'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.  16        70  LOAD_FAST                'importlib'
               72  LOAD_METHOD              import_module
               74  LOAD_STR                 '_pyfreeling'
               76  CALL_METHOD_1         1  ''
               78  ROT_FOUR         
               80  POP_EXCEPT       
               82  RETURN_VALUE     
             84_0  COME_FROM            62  '62'
               84  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 66


    _pyfreeling = swig_import_helper()
    del swig_import_helper
else:
    if _swig_python_version_info >= (2, 6, 0):

        def swig_import_helper():
            from os.path import dirname
            import imp
            fp = None
            try:
                fp, pathname, description = imp.find_module('_pyfreeling', [dirname(__file__)])
            except ImportError:
                import _pyfreeling
                return _pyfreeling
            else:
                try:
                    _mod = imp.load_module('_pyfreeling', fp, pathname, description)
                finally:
                    if fp is not None:
                        fp.close()

                return _mod


        _pyfreeling = swig_import_helper()
        del swig_import_helper
    else:
        import _pyfreeling
del _swig_python_version_info
try:
    _swig_property = property
except NameError:
    pass

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__
else:

    def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
        if name == 'thisown':
            return self.this.ownvalue
        else:
            if name == 'this':
                if type(value).__name__ == 'SwigPyObject':
                    self.__dict__[name] = value
                    return
            method = class_type.__swig_setmethods__.get(name, None)
            if method:
                return method(self, value)
                if not static:
                    if _newclass:
                        object.__setattr__(self, name, value)
                    else:
                        self.__dict__[name] = value
            else:
                raise AttributeError('You cannot add attributes to %s' % self)


    def _swig_setattr(self, class_type, name, value):
        return _swig_setattr_nondynamic(self, class_type, name, value, 0)


    def _swig_getattr(self, class_type, name):
        if name == 'thisown':
            return self.this.own()
        method = class_type.__swig_getmethods__.get(name, None)
        if method:
            return method(self)
        raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


    def _swig_repr(self):
        try:
            strthis = 'proxy of ' + self.this.__repr__()
        except __builtin__.Exception:
            strthis = ''
        else:
            return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


    try:
        _object = object
        _newclass = 1
    except __builtin__.Exception:

        class _object:
            pass


        _newclass = 0
    else:

        class SwigPyIterator(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

            def __init__(self, *args, **kwargs):
                raise AttributeError('No constructor defined - class is abstract')

            __repr__ = _swig_repr
            __swig_destroy__ = _pyfreeling.delete_SwigPyIterator
            __del__ = lambda self: None

            def value(self) -> 'PyObject *':
                return _pyfreeling.SwigPyIterator_valueself

            def incr(self, n: 'size_t'=1) -> 'swig::SwigPyIterator *':
                return _pyfreeling.SwigPyIterator_incr(self, n)

            def decr(self, n: 'size_t'=1) -> 'swig::SwigPyIterator *':
                return _pyfreeling.SwigPyIterator_decr(self, n)

            def distance(self, x: 'SwigPyIterator') -> 'ptrdiff_t':
                return _pyfreeling.SwigPyIterator_distance(self, x)

            def equal(self, x: 'SwigPyIterator') -> 'bool':
                return _pyfreeling.SwigPyIterator_equal(self, x)

            def copy(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.SwigPyIterator_copyself

            def next(self) -> 'PyObject *':
                return _pyfreeling.SwigPyIterator_nextself

            def __next__(self) -> 'PyObject *':
                return _pyfreeling.SwigPyIterator___next__self

            def previous(self) -> 'PyObject *':
                return _pyfreeling.SwigPyIterator_previousself

            def advance(self, n: 'ptrdiff_t') -> 'swig::SwigPyIterator *':
                return _pyfreeling.SwigPyIterator_advance(self, n)

            def __eq__(self, x: 'SwigPyIterator') -> 'bool':
                return _pyfreeling.SwigPyIterator___eq__(self, x)

            def __ne__(self, x: 'SwigPyIterator') -> 'bool':
                return _pyfreeling.SwigPyIterator___ne__(self, x)

            def __iadd__(self, n: 'ptrdiff_t') -> 'swig::SwigPyIterator &':
                return _pyfreeling.SwigPyIterator___iadd__(self, n)

            def __isub__(self, n: 'ptrdiff_t') -> 'swig::SwigPyIterator &':
                return _pyfreeling.SwigPyIterator___isub__(self, n)

            def __add__(self, n: 'ptrdiff_t') -> 'swig::SwigPyIterator *':
                return _pyfreeling.SwigPyIterator___add__(self, n)

            def __sub__(self, *args) -> 'ptrdiff_t':
                return (_pyfreeling.SwigPyIterator___sub__)(self, *args)

            def __iter__(self):
                return self


        SwigPyIterator_swigregister = _pyfreeling.SwigPyIterator_swigregister
        SwigPyIterator_swigregister(SwigPyIterator)

        class VectorWord(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorWord, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorWord, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorWord_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorWord___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorWord___bool__self

            def __len__(self) -> 'std::vector< freeling::word >::size_type':
                return _pyfreeling.VectorWord___len__self

            def __getslice__(self, i: 'std::vector< freeling::word >::difference_type', j: 'std::vector< freeling::word >::difference_type') -> 'std::vector< freeling::word,std::allocator< freeling::word > > *':
                return _pyfreeling.VectorWord___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorWord___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< freeling::word >::difference_type', j: 'std::vector< freeling::word >::difference_type') -> 'void':
                return _pyfreeling.VectorWord___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorWord___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< freeling::word >::value_type const &':
                return (_pyfreeling.VectorWord___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorWord___setitem__)(self, *args)

            def pop(self) -> 'std::vector< freeling::word >::value_type':
                return _pyfreeling.VectorWord_popself

            def append(self, x: 'word') -> 'void':
                return _pyfreeling.VectorWord_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorWord_emptyself

            def size(self) -> 'std::vector< freeling::word >::size_type':
                return _pyfreeling.VectorWord_sizeself

            def swap(self, v: 'VectorWord') -> 'void':
                return _pyfreeling.VectorWord_swap(self, v)

            def begin(self) -> 'std::vector< freeling::word >::iterator':
                return _pyfreeling.VectorWord_beginself

            def end(self) -> 'std::vector< freeling::word >::iterator':
                return _pyfreeling.VectorWord_endself

            def rbegin(self) -> 'std::vector< freeling::word >::reverse_iterator':
                return _pyfreeling.VectorWord_rbeginself

            def rend(self) -> 'std::vector< freeling::word >::reverse_iterator':
                return _pyfreeling.VectorWord_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorWord_clearself

            def get_allocator(self) -> 'std::vector< freeling::word >::allocator_type':
                return _pyfreeling.VectorWord_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorWord_pop_backself

            def erase(self, *args) -> 'std::vector< freeling::word >::iterator':
                return (_pyfreeling.VectorWord_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorWord)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'word') -> 'void':
                return _pyfreeling.VectorWord_push_back(self, x)

            def front(self) -> 'std::vector< freeling::word >::value_type const &':
                return _pyfreeling.VectorWord_frontself

            def back(self) -> 'std::vector< freeling::word >::value_type const &':
                return _pyfreeling.VectorWord_backself

            def assign(self, n: 'std::vector< freeling::word >::size_type', x: 'word') -> 'void':
                return _pyfreeling.VectorWord_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorWord_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorWord_insert)(self, *args)

            def reserve(self, n: 'std::vector< freeling::word >::size_type') -> 'void':
                return _pyfreeling.VectorWord_reserve(self, n)

            def capacity(self) -> 'std::vector< freeling::word >::size_type':
                return _pyfreeling.VectorWord_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorWord
            __del__ = lambda self: None


        VectorWord_swigregister = _pyfreeling.VectorWord_swigregister
        VectorWord_swigregister(VectorWord)

        class ListWord(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ListWord, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ListWord, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.ListWord_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.ListWord___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.ListWord___bool__self

            def __len__(self) -> 'std::list< freeling::word >::size_type':
                return _pyfreeling.ListWord___len__self

            def __getslice__(self, i: 'std::list< freeling::word >::difference_type', j: 'std::list< freeling::word >::difference_type') -> 'std::list< freeling::word,std::allocator< freeling::word > > *':
                return _pyfreeling.ListWord___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.ListWord___setslice__)(self, *args)

            def __delslice__(self, i: 'std::list< freeling::word >::difference_type', j: 'std::list< freeling::word >::difference_type') -> 'void':
                return _pyfreeling.ListWord___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.ListWord___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::list< freeling::word >::value_type const &':
                return (_pyfreeling.ListWord___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.ListWord___setitem__)(self, *args)

            def pop(self) -> 'std::list< freeling::word >::value_type':
                return _pyfreeling.ListWord_popself

            def append(self, x: 'word') -> 'void':
                return _pyfreeling.ListWord_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.ListWord_emptyself

            def size(self) -> 'std::list< freeling::word >::size_type':
                return _pyfreeling.ListWord_sizeself

            def swap(self, v: 'ListWord') -> 'void':
                return _pyfreeling.ListWord_swap(self, v)

            def begin(self) -> 'std::list< freeling::word >::iterator':
                return _pyfreeling.ListWord_beginself

            def end(self) -> 'std::list< freeling::word >::iterator':
                return _pyfreeling.ListWord_endself

            def rbegin(self) -> 'std::list< freeling::word >::reverse_iterator':
                return _pyfreeling.ListWord_rbeginself

            def rend(self) -> 'std::list< freeling::word >::reverse_iterator':
                return _pyfreeling.ListWord_rendself

            def clear(self) -> 'void':
                return _pyfreeling.ListWord_clearself

            def get_allocator(self) -> 'std::list< freeling::word >::allocator_type':
                return _pyfreeling.ListWord_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.ListWord_pop_backself

            def erase(self, *args) -> 'std::list< freeling::word >::iterator':
                return (_pyfreeling.ListWord_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_ListWord)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'word') -> 'void':
                return _pyfreeling.ListWord_push_back(self, x)

            def front(self) -> 'std::list< freeling::word >::value_type const &':
                return _pyfreeling.ListWord_frontself

            def back(self) -> 'std::list< freeling::word >::value_type const &':
                return _pyfreeling.ListWord_backself

            def assign(self, n: 'std::list< freeling::word >::size_type', x: 'word') -> 'void':
                return _pyfreeling.ListWord_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.ListWord_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.ListWord_insert)(self, *args)

            def pop_front(self) -> 'void':
                return _pyfreeling.ListWord_pop_frontself

            def push_front(self, x: 'word') -> 'void':
                return _pyfreeling.ListWord_push_front(self, x)

            def reverse(self) -> 'void':
                return _pyfreeling.ListWord_reverseself

            __swig_destroy__ = _pyfreeling.delete_ListWord
            __del__ = lambda self: None


        ListWord_swigregister = _pyfreeling.ListWord_swigregister
        ListWord_swigregister(ListWord)

        class ListAnalysis(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ListAnalysis, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ListAnalysis, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.ListAnalysis_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.ListAnalysis___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.ListAnalysis___bool__self

            def __len__(self) -> 'std::list< freeling::analysis >::size_type':
                return _pyfreeling.ListAnalysis___len__self

            def __getslice__(self, i: 'std::list< freeling::analysis >::difference_type', j: 'std::list< freeling::analysis >::difference_type') -> 'std::list< freeling::analysis,std::allocator< freeling::analysis > > *':
                return _pyfreeling.ListAnalysis___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.ListAnalysis___setslice__)(self, *args)

            def __delslice__(self, i: 'std::list< freeling::analysis >::difference_type', j: 'std::list< freeling::analysis >::difference_type') -> 'void':
                return _pyfreeling.ListAnalysis___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.ListAnalysis___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::list< freeling::analysis >::value_type const &':
                return (_pyfreeling.ListAnalysis___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.ListAnalysis___setitem__)(self, *args)

            def pop(self) -> 'std::list< freeling::analysis >::value_type':
                return _pyfreeling.ListAnalysis_popself

            def append(self, x: 'analysis') -> 'void':
                return _pyfreeling.ListAnalysis_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.ListAnalysis_emptyself

            def size(self) -> 'std::list< freeling::analysis >::size_type':
                return _pyfreeling.ListAnalysis_sizeself

            def swap(self, v: 'ListAnalysis') -> 'void':
                return _pyfreeling.ListAnalysis_swap(self, v)

            def begin(self) -> 'std::list< freeling::analysis >::iterator':
                return _pyfreeling.ListAnalysis_beginself

            def end(self) -> 'std::list< freeling::analysis >::iterator':
                return _pyfreeling.ListAnalysis_endself

            def rbegin(self) -> 'std::list< freeling::analysis >::reverse_iterator':
                return _pyfreeling.ListAnalysis_rbeginself

            def rend(self) -> 'std::list< freeling::analysis >::reverse_iterator':
                return _pyfreeling.ListAnalysis_rendself

            def clear(self) -> 'void':
                return _pyfreeling.ListAnalysis_clearself

            def get_allocator(self) -> 'std::list< freeling::analysis >::allocator_type':
                return _pyfreeling.ListAnalysis_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.ListAnalysis_pop_backself

            def erase(self, *args) -> 'std::list< freeling::analysis >::iterator':
                return (_pyfreeling.ListAnalysis_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_ListAnalysis)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'analysis') -> 'void':
                return _pyfreeling.ListAnalysis_push_back(self, x)

            def front(self) -> 'std::list< freeling::analysis >::value_type const &':
                return _pyfreeling.ListAnalysis_frontself

            def back(self) -> 'std::list< freeling::analysis >::value_type const &':
                return _pyfreeling.ListAnalysis_backself

            def assign(self, n: 'std::list< freeling::analysis >::size_type', x: 'analysis') -> 'void':
                return _pyfreeling.ListAnalysis_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.ListAnalysis_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.ListAnalysis_insert)(self, *args)

            def pop_front(self) -> 'void':
                return _pyfreeling.ListAnalysis_pop_frontself

            def push_front(self, x: 'analysis') -> 'void':
                return _pyfreeling.ListAnalysis_push_front(self, x)

            def reverse(self) -> 'void':
                return _pyfreeling.ListAnalysis_reverseself

            __swig_destroy__ = _pyfreeling.delete_ListAnalysis
            __del__ = lambda self: None


        ListAnalysis_swigregister = _pyfreeling.ListAnalysis_swigregister
        ListAnalysis_swigregister(ListAnalysis)

        class ListAlternative(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ListAlternative, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ListAlternative, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.ListAlternative_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.ListAlternative___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.ListAlternative___bool__self

            def __len__(self) -> 'std::list< freeling::alternative >::size_type':
                return _pyfreeling.ListAlternative___len__self

            def __getslice__(self, i: 'std::list< freeling::alternative >::difference_type', j: 'std::list< freeling::alternative >::difference_type') -> 'std::list< freeling::alternative,std::allocator< freeling::alternative > > *':
                return _pyfreeling.ListAlternative___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.ListAlternative___setslice__)(self, *args)

            def __delslice__(self, i: 'std::list< freeling::alternative >::difference_type', j: 'std::list< freeling::alternative >::difference_type') -> 'void':
                return _pyfreeling.ListAlternative___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.ListAlternative___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::list< freeling::alternative >::value_type const &':
                return (_pyfreeling.ListAlternative___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.ListAlternative___setitem__)(self, *args)

            def pop(self) -> 'std::list< freeling::alternative >::value_type':
                return _pyfreeling.ListAlternative_popself

            def append(self, x: 'alternative') -> 'void':
                return _pyfreeling.ListAlternative_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.ListAlternative_emptyself

            def size(self) -> 'std::list< freeling::alternative >::size_type':
                return _pyfreeling.ListAlternative_sizeself

            def swap(self, v: 'ListAlternative') -> 'void':
                return _pyfreeling.ListAlternative_swap(self, v)

            def begin(self) -> 'std::list< freeling::alternative >::iterator':
                return _pyfreeling.ListAlternative_beginself

            def end(self) -> 'std::list< freeling::alternative >::iterator':
                return _pyfreeling.ListAlternative_endself

            def rbegin(self) -> 'std::list< freeling::alternative >::reverse_iterator':
                return _pyfreeling.ListAlternative_rbeginself

            def rend(self) -> 'std::list< freeling::alternative >::reverse_iterator':
                return _pyfreeling.ListAlternative_rendself

            def clear(self) -> 'void':
                return _pyfreeling.ListAlternative_clearself

            def get_allocator(self) -> 'std::list< freeling::alternative >::allocator_type':
                return _pyfreeling.ListAlternative_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.ListAlternative_pop_backself

            def erase(self, *args) -> 'std::list< freeling::alternative >::iterator':
                return (_pyfreeling.ListAlternative_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_ListAlternative)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'alternative') -> 'void':
                return _pyfreeling.ListAlternative_push_back(self, x)

            def front(self) -> 'std::list< freeling::alternative >::value_type const &':
                return _pyfreeling.ListAlternative_frontself

            def back(self) -> 'std::list< freeling::alternative >::value_type const &':
                return _pyfreeling.ListAlternative_backself

            def assign(self, n: 'std::list< freeling::alternative >::size_type', x: 'alternative') -> 'void':
                return _pyfreeling.ListAlternative_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.ListAlternative_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.ListAlternative_insert)(self, *args)

            def pop_front(self) -> 'void':
                return _pyfreeling.ListAlternative_pop_frontself

            def push_front(self, x: 'alternative') -> 'void':
                return _pyfreeling.ListAlternative_push_front(self, x)

            def reverse(self) -> 'void':
                return _pyfreeling.ListAlternative_reverseself

            __swig_destroy__ = _pyfreeling.delete_ListAlternative
            __del__ = lambda self: None


        ListAlternative_swigregister = _pyfreeling.ListAlternative_swigregister
        ListAlternative_swigregister(ListAlternative)

        class ListSentence(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ListSentence, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ListSentence, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.ListSentence_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.ListSentence___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.ListSentence___bool__self

            def __len__(self) -> 'std::list< freeling::sentence >::size_type':
                return _pyfreeling.ListSentence___len__self

            def __getslice__(self, i: 'std::list< freeling::sentence >::difference_type', j: 'std::list< freeling::sentence >::difference_type') -> 'std::list< freeling::sentence,std::allocator< freeling::sentence > > *':
                return _pyfreeling.ListSentence___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.ListSentence___setslice__)(self, *args)

            def __delslice__(self, i: 'std::list< freeling::sentence >::difference_type', j: 'std::list< freeling::sentence >::difference_type') -> 'void':
                return _pyfreeling.ListSentence___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.ListSentence___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::list< freeling::sentence >::value_type const &':
                return (_pyfreeling.ListSentence___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.ListSentence___setitem__)(self, *args)

            def pop(self) -> 'std::list< freeling::sentence >::value_type':
                return _pyfreeling.ListSentence_popself

            def append(self, x: 'sentence') -> 'void':
                return _pyfreeling.ListSentence_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.ListSentence_emptyself

            def size(self) -> 'std::list< freeling::sentence >::size_type':
                return _pyfreeling.ListSentence_sizeself

            def swap(self, v: 'ListSentence') -> 'void':
                return _pyfreeling.ListSentence_swap(self, v)

            def begin(self) -> 'std::list< freeling::sentence >::iterator':
                return _pyfreeling.ListSentence_beginself

            def end(self) -> 'std::list< freeling::sentence >::iterator':
                return _pyfreeling.ListSentence_endself

            def rbegin(self) -> 'std::list< freeling::sentence >::reverse_iterator':
                return _pyfreeling.ListSentence_rbeginself

            def rend(self) -> 'std::list< freeling::sentence >::reverse_iterator':
                return _pyfreeling.ListSentence_rendself

            def clear(self) -> 'void':
                return _pyfreeling.ListSentence_clearself

            def get_allocator(self) -> 'std::list< freeling::sentence >::allocator_type':
                return _pyfreeling.ListSentence_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.ListSentence_pop_backself

            def erase(self, *args) -> 'std::list< freeling::sentence >::iterator':
                return (_pyfreeling.ListSentence_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_ListSentence)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'sentence') -> 'void':
                return _pyfreeling.ListSentence_push_back(self, x)

            def front(self) -> 'std::list< freeling::sentence >::value_type const &':
                return _pyfreeling.ListSentence_frontself

            def back(self) -> 'std::list< freeling::sentence >::value_type const &':
                return _pyfreeling.ListSentence_backself

            def assign(self, n: 'std::list< freeling::sentence >::size_type', x: 'sentence') -> 'void':
                return _pyfreeling.ListSentence_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.ListSentence_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.ListSentence_insert)(self, *args)

            def pop_front(self) -> 'void':
                return _pyfreeling.ListSentence_pop_frontself

            def push_front(self, x: 'sentence') -> 'void':
                return _pyfreeling.ListSentence_push_front(self, x)

            def reverse(self) -> 'void':
                return _pyfreeling.ListSentence_reverseself

            __swig_destroy__ = _pyfreeling.delete_ListSentence
            __del__ = lambda self: None


        ListSentence_swigregister = _pyfreeling.ListSentence_swigregister
        ListSentence_swigregister(ListSentence)

        class ListParagraph(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ListParagraph, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ListParagraph, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.ListParagraph_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.ListParagraph___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.ListParagraph___bool__self

            def __len__(self) -> 'std::list< freeling::paragraph >::size_type':
                return _pyfreeling.ListParagraph___len__self

            def __getslice__(self, i: 'std::list< freeling::paragraph >::difference_type', j: 'std::list< freeling::paragraph >::difference_type') -> 'std::list< freeling::paragraph,std::allocator< freeling::paragraph > > *':
                return _pyfreeling.ListParagraph___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.ListParagraph___setslice__)(self, *args)

            def __delslice__(self, i: 'std::list< freeling::paragraph >::difference_type', j: 'std::list< freeling::paragraph >::difference_type') -> 'void':
                return _pyfreeling.ListParagraph___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.ListParagraph___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::list< freeling::paragraph >::value_type const &':
                return (_pyfreeling.ListParagraph___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.ListParagraph___setitem__)(self, *args)

            def pop(self) -> 'std::list< freeling::paragraph >::value_type':
                return _pyfreeling.ListParagraph_popself

            def append(self, x: 'paragraph') -> 'void':
                return _pyfreeling.ListParagraph_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.ListParagraph_emptyself

            def size(self) -> 'std::list< freeling::paragraph >::size_type':
                return _pyfreeling.ListParagraph_sizeself

            def swap(self, v: 'ListParagraph') -> 'void':
                return _pyfreeling.ListParagraph_swap(self, v)

            def begin(self) -> 'std::list< freeling::paragraph >::iterator':
                return _pyfreeling.ListParagraph_beginself

            def end(self) -> 'std::list< freeling::paragraph >::iterator':
                return _pyfreeling.ListParagraph_endself

            def rbegin(self) -> 'std::list< freeling::paragraph >::reverse_iterator':
                return _pyfreeling.ListParagraph_rbeginself

            def rend(self) -> 'std::list< freeling::paragraph >::reverse_iterator':
                return _pyfreeling.ListParagraph_rendself

            def clear(self) -> 'void':
                return _pyfreeling.ListParagraph_clearself

            def get_allocator(self) -> 'std::list< freeling::paragraph >::allocator_type':
                return _pyfreeling.ListParagraph_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.ListParagraph_pop_backself

            def erase(self, *args) -> 'std::list< freeling::paragraph >::iterator':
                return (_pyfreeling.ListParagraph_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_ListParagraph)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'paragraph') -> 'void':
                return _pyfreeling.ListParagraph_push_back(self, x)

            def front(self) -> 'std::list< freeling::paragraph >::value_type const &':
                return _pyfreeling.ListParagraph_frontself

            def back(self) -> 'std::list< freeling::paragraph >::value_type const &':
                return _pyfreeling.ListParagraph_backself

            def assign(self, n: 'std::list< freeling::paragraph >::size_type', x: 'paragraph') -> 'void':
                return _pyfreeling.ListParagraph_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.ListParagraph_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.ListParagraph_insert)(self, *args)

            def pop_front(self) -> 'void':
                return _pyfreeling.ListParagraph_pop_frontself

            def push_front(self, x: 'paragraph') -> 'void':
                return _pyfreeling.ListParagraph_push_front(self, x)

            def reverse(self) -> 'void':
                return _pyfreeling.ListParagraph_reverseself

            __swig_destroy__ = _pyfreeling.delete_ListParagraph
            __del__ = lambda self: None


        ListParagraph_swigregister = _pyfreeling.ListParagraph_swigregister
        ListParagraph_swigregister(ListParagraph)

        class VectorArgument(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorArgument, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorArgument, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorArgument_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorArgument___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorArgument___bool__self

            def __len__(self) -> 'std::vector< freeling::argument >::size_type':
                return _pyfreeling.VectorArgument___len__self

            def __getslice__(self, i: 'std::vector< freeling::argument >::difference_type', j: 'std::vector< freeling::argument >::difference_type') -> 'std::vector< freeling::argument,std::allocator< freeling::argument > > *':
                return _pyfreeling.VectorArgument___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorArgument___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< freeling::argument >::difference_type', j: 'std::vector< freeling::argument >::difference_type') -> 'void':
                return _pyfreeling.VectorArgument___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorArgument___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< freeling::argument >::value_type const &':
                return (_pyfreeling.VectorArgument___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorArgument___setitem__)(self, *args)

            def pop(self) -> 'std::vector< freeling::argument >::value_type':
                return _pyfreeling.VectorArgument_popself

            def append(self, x: 'argument') -> 'void':
                return _pyfreeling.VectorArgument_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorArgument_emptyself

            def size(self) -> 'std::vector< freeling::argument >::size_type':
                return _pyfreeling.VectorArgument_sizeself

            def swap(self, v: 'VectorArgument') -> 'void':
                return _pyfreeling.VectorArgument_swap(self, v)

            def begin(self) -> 'std::vector< freeling::argument >::iterator':
                return _pyfreeling.VectorArgument_beginself

            def end(self) -> 'std::vector< freeling::argument >::iterator':
                return _pyfreeling.VectorArgument_endself

            def rbegin(self) -> 'std::vector< freeling::argument >::reverse_iterator':
                return _pyfreeling.VectorArgument_rbeginself

            def rend(self) -> 'std::vector< freeling::argument >::reverse_iterator':
                return _pyfreeling.VectorArgument_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorArgument_clearself

            def get_allocator(self) -> 'std::vector< freeling::argument >::allocator_type':
                return _pyfreeling.VectorArgument_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorArgument_pop_backself

            def erase(self, *args) -> 'std::vector< freeling::argument >::iterator':
                return (_pyfreeling.VectorArgument_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorArgument)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'argument') -> 'void':
                return _pyfreeling.VectorArgument_push_back(self, x)

            def front(self) -> 'std::vector< freeling::argument >::value_type const &':
                return _pyfreeling.VectorArgument_frontself

            def back(self) -> 'std::vector< freeling::argument >::value_type const &':
                return _pyfreeling.VectorArgument_backself

            def assign(self, n: 'std::vector< freeling::argument >::size_type', x: 'argument') -> 'void':
                return _pyfreeling.VectorArgument_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorArgument_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorArgument_insert)(self, *args)

            def reserve(self, n: 'std::vector< freeling::argument >::size_type') -> 'void':
                return _pyfreeling.VectorArgument_reserve(self, n)

            def capacity(self) -> 'std::vector< freeling::argument >::size_type':
                return _pyfreeling.VectorArgument_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorArgument
            __del__ = lambda self: None


        VectorArgument_swigregister = _pyfreeling.VectorArgument_swigregister
        VectorArgument_swigregister(VectorArgument)

        class VectorPredicate(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorPredicate, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorPredicate, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorPredicate_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorPredicate___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorPredicate___bool__self

            def __len__(self) -> 'std::vector< freeling::predicate >::size_type':
                return _pyfreeling.VectorPredicate___len__self

            def __getslice__(self, i: 'std::vector< freeling::predicate >::difference_type', j: 'std::vector< freeling::predicate >::difference_type') -> 'std::vector< freeling::predicate,std::allocator< freeling::predicate > > *':
                return _pyfreeling.VectorPredicate___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorPredicate___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< freeling::predicate >::difference_type', j: 'std::vector< freeling::predicate >::difference_type') -> 'void':
                return _pyfreeling.VectorPredicate___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorPredicate___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< freeling::predicate >::value_type const &':
                return (_pyfreeling.VectorPredicate___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorPredicate___setitem__)(self, *args)

            def pop(self) -> 'std::vector< freeling::predicate >::value_type':
                return _pyfreeling.VectorPredicate_popself

            def append(self, x: 'predicate') -> 'void':
                return _pyfreeling.VectorPredicate_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorPredicate_emptyself

            def size(self) -> 'std::vector< freeling::predicate >::size_type':
                return _pyfreeling.VectorPredicate_sizeself

            def swap(self, v: 'VectorPredicate') -> 'void':
                return _pyfreeling.VectorPredicate_swap(self, v)

            def begin(self) -> 'std::vector< freeling::predicate >::iterator':
                return _pyfreeling.VectorPredicate_beginself

            def end(self) -> 'std::vector< freeling::predicate >::iterator':
                return _pyfreeling.VectorPredicate_endself

            def rbegin(self) -> 'std::vector< freeling::predicate >::reverse_iterator':
                return _pyfreeling.VectorPredicate_rbeginself

            def rend(self) -> 'std::vector< freeling::predicate >::reverse_iterator':
                return _pyfreeling.VectorPredicate_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorPredicate_clearself

            def get_allocator(self) -> 'std::vector< freeling::predicate >::allocator_type':
                return _pyfreeling.VectorPredicate_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorPredicate_pop_backself

            def erase(self, *args) -> 'std::vector< freeling::predicate >::iterator':
                return (_pyfreeling.VectorPredicate_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorPredicate)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'predicate') -> 'void':
                return _pyfreeling.VectorPredicate_push_back(self, x)

            def front(self) -> 'std::vector< freeling::predicate >::value_type const &':
                return _pyfreeling.VectorPredicate_frontself

            def back(self) -> 'std::vector< freeling::predicate >::value_type const &':
                return _pyfreeling.VectorPredicate_backself

            def assign(self, n: 'std::vector< freeling::predicate >::size_type', x: 'predicate') -> 'void':
                return _pyfreeling.VectorPredicate_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorPredicate_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorPredicate_insert)(self, *args)

            def reserve(self, n: 'std::vector< freeling::predicate >::size_type') -> 'void':
                return _pyfreeling.VectorPredicate_reserve(self, n)

            def capacity(self) -> 'std::vector< freeling::predicate >::size_type':
                return _pyfreeling.VectorPredicate_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorPredicate
            __del__ = lambda self: None


        VectorPredicate_swigregister = _pyfreeling.VectorPredicate_swigregister
        VectorPredicate_swigregister(VectorPredicate)

        class VectorSGMention(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorSGMention, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorSGMention, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorSGMention_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorSGMention___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorSGMention___bool__self

            def __len__(self) -> 'std::vector< freeling::semgraph::SG_mention >::size_type':
                return _pyfreeling.VectorSGMention___len__self

            def __getslice__(self, i: 'std::vector< freeling::semgraph::SG_mention >::difference_type', j: 'std::vector< freeling::semgraph::SG_mention >::difference_type') -> 'std::vector< freeling::semgraph::SG_mention,std::allocator< freeling::semgraph::SG_mention > > *':
                return _pyfreeling.VectorSGMention___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGMention___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< freeling::semgraph::SG_mention >::difference_type', j: 'std::vector< freeling::semgraph::SG_mention >::difference_type') -> 'void':
                return _pyfreeling.VectorSGMention___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGMention___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< freeling::semgraph::SG_mention >::value_type const &':
                return (_pyfreeling.VectorSGMention___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGMention___setitem__)(self, *args)

            def pop(self) -> 'std::vector< freeling::semgraph::SG_mention >::value_type':
                return _pyfreeling.VectorSGMention_popself

            def append(self, x: 'SG_mention') -> 'void':
                return _pyfreeling.VectorSGMention_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorSGMention_emptyself

            def size(self) -> 'std::vector< freeling::semgraph::SG_mention >::size_type':
                return _pyfreeling.VectorSGMention_sizeself

            def swap(self, v: 'VectorSGMention') -> 'void':
                return _pyfreeling.VectorSGMention_swap(self, v)

            def begin(self) -> 'std::vector< freeling::semgraph::SG_mention >::iterator':
                return _pyfreeling.VectorSGMention_beginself

            def end(self) -> 'std::vector< freeling::semgraph::SG_mention >::iterator':
                return _pyfreeling.VectorSGMention_endself

            def rbegin(self) -> 'std::vector< freeling::semgraph::SG_mention >::reverse_iterator':
                return _pyfreeling.VectorSGMention_rbeginself

            def rend(self) -> 'std::vector< freeling::semgraph::SG_mention >::reverse_iterator':
                return _pyfreeling.VectorSGMention_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorSGMention_clearself

            def get_allocator(self) -> 'std::vector< freeling::semgraph::SG_mention >::allocator_type':
                return _pyfreeling.VectorSGMention_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorSGMention_pop_backself

            def erase(self, *args) -> 'std::vector< freeling::semgraph::SG_mention >::iterator':
                return (_pyfreeling.VectorSGMention_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorSGMention)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'SG_mention') -> 'void':
                return _pyfreeling.VectorSGMention_push_back(self, x)

            def front(self) -> 'std::vector< freeling::semgraph::SG_mention >::value_type const &':
                return _pyfreeling.VectorSGMention_frontself

            def back(self) -> 'std::vector< freeling::semgraph::SG_mention >::value_type const &':
                return _pyfreeling.VectorSGMention_backself

            def assign(self, n: 'std::vector< freeling::semgraph::SG_mention >::size_type', x: 'SG_mention') -> 'void':
                return _pyfreeling.VectorSGMention_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorSGMention_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorSGMention_insert)(self, *args)

            def reserve(self, n: 'std::vector< freeling::semgraph::SG_mention >::size_type') -> 'void':
                return _pyfreeling.VectorSGMention_reserve(self, n)

            def capacity(self) -> 'std::vector< freeling::semgraph::SG_mention >::size_type':
                return _pyfreeling.VectorSGMention_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorSGMention
            __del__ = lambda self: None


        VectorSGMention_swigregister = _pyfreeling.VectorSGMention_swigregister
        VectorSGMention_swigregister(VectorSGMention)

        class VectorSGArgument(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorSGArgument, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorSGArgument, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorSGArgument_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorSGArgument___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorSGArgument___bool__self

            def __len__(self) -> 'std::vector< freeling::semgraph::SG_argument >::size_type':
                return _pyfreeling.VectorSGArgument___len__self

            def __getslice__(self, i: 'std::vector< freeling::semgraph::SG_argument >::difference_type', j: 'std::vector< freeling::semgraph::SG_argument >::difference_type') -> 'std::vector< freeling::semgraph::SG_argument,std::allocator< freeling::semgraph::SG_argument > > *':
                return _pyfreeling.VectorSGArgument___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGArgument___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< freeling::semgraph::SG_argument >::difference_type', j: 'std::vector< freeling::semgraph::SG_argument >::difference_type') -> 'void':
                return _pyfreeling.VectorSGArgument___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGArgument___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< freeling::semgraph::SG_argument >::value_type const &':
                return (_pyfreeling.VectorSGArgument___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGArgument___setitem__)(self, *args)

            def pop(self) -> 'std::vector< freeling::semgraph::SG_argument >::value_type':
                return _pyfreeling.VectorSGArgument_popself

            def append(self, x: 'SG_argument') -> 'void':
                return _pyfreeling.VectorSGArgument_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorSGArgument_emptyself

            def size(self) -> 'std::vector< freeling::semgraph::SG_argument >::size_type':
                return _pyfreeling.VectorSGArgument_sizeself

            def swap(self, v: 'VectorSGArgument') -> 'void':
                return _pyfreeling.VectorSGArgument_swap(self, v)

            def begin(self) -> 'std::vector< freeling::semgraph::SG_argument >::iterator':
                return _pyfreeling.VectorSGArgument_beginself

            def end(self) -> 'std::vector< freeling::semgraph::SG_argument >::iterator':
                return _pyfreeling.VectorSGArgument_endself

            def rbegin(self) -> 'std::vector< freeling::semgraph::SG_argument >::reverse_iterator':
                return _pyfreeling.VectorSGArgument_rbeginself

            def rend(self) -> 'std::vector< freeling::semgraph::SG_argument >::reverse_iterator':
                return _pyfreeling.VectorSGArgument_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorSGArgument_clearself

            def get_allocator(self) -> 'std::vector< freeling::semgraph::SG_argument >::allocator_type':
                return _pyfreeling.VectorSGArgument_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorSGArgument_pop_backself

            def erase(self, *args) -> 'std::vector< freeling::semgraph::SG_argument >::iterator':
                return (_pyfreeling.VectorSGArgument_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorSGArgument)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'SG_argument') -> 'void':
                return _pyfreeling.VectorSGArgument_push_back(self, x)

            def front(self) -> 'std::vector< freeling::semgraph::SG_argument >::value_type const &':
                return _pyfreeling.VectorSGArgument_frontself

            def back(self) -> 'std::vector< freeling::semgraph::SG_argument >::value_type const &':
                return _pyfreeling.VectorSGArgument_backself

            def assign(self, n: 'std::vector< freeling::semgraph::SG_argument >::size_type', x: 'SG_argument') -> 'void':
                return _pyfreeling.VectorSGArgument_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorSGArgument_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorSGArgument_insert)(self, *args)

            def reserve(self, n: 'std::vector< freeling::semgraph::SG_argument >::size_type') -> 'void':
                return _pyfreeling.VectorSGArgument_reserve(self, n)

            def capacity(self) -> 'std::vector< freeling::semgraph::SG_argument >::size_type':
                return _pyfreeling.VectorSGArgument_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorSGArgument
            __del__ = lambda self: None


        VectorSGArgument_swigregister = _pyfreeling.VectorSGArgument_swigregister
        VectorSGArgument_swigregister(VectorSGArgument)

        class VectorSGEntity(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorSGEntity, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorSGEntity, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorSGEntity_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorSGEntity___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorSGEntity___bool__self

            def __len__(self) -> 'std::vector< freeling::semgraph::SG_entity >::size_type':
                return _pyfreeling.VectorSGEntity___len__self

            def __getslice__(self, i: 'std::vector< freeling::semgraph::SG_entity >::difference_type', j: 'std::vector< freeling::semgraph::SG_entity >::difference_type') -> 'std::vector< freeling::semgraph::SG_entity,std::allocator< freeling::semgraph::SG_entity > > *':
                return _pyfreeling.VectorSGEntity___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGEntity___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< freeling::semgraph::SG_entity >::difference_type', j: 'std::vector< freeling::semgraph::SG_entity >::difference_type') -> 'void':
                return _pyfreeling.VectorSGEntity___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGEntity___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< freeling::semgraph::SG_entity >::value_type const &':
                return (_pyfreeling.VectorSGEntity___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGEntity___setitem__)(self, *args)

            def pop(self) -> 'std::vector< freeling::semgraph::SG_entity >::value_type':
                return _pyfreeling.VectorSGEntity_popself

            def append(self, x: 'SG_entity') -> 'void':
                return _pyfreeling.VectorSGEntity_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorSGEntity_emptyself

            def size(self) -> 'std::vector< freeling::semgraph::SG_entity >::size_type':
                return _pyfreeling.VectorSGEntity_sizeself

            def swap(self, v: 'VectorSGEntity') -> 'void':
                return _pyfreeling.VectorSGEntity_swap(self, v)

            def begin(self) -> 'std::vector< freeling::semgraph::SG_entity >::iterator':
                return _pyfreeling.VectorSGEntity_beginself

            def end(self) -> 'std::vector< freeling::semgraph::SG_entity >::iterator':
                return _pyfreeling.VectorSGEntity_endself

            def rbegin(self) -> 'std::vector< freeling::semgraph::SG_entity >::reverse_iterator':
                return _pyfreeling.VectorSGEntity_rbeginself

            def rend(self) -> 'std::vector< freeling::semgraph::SG_entity >::reverse_iterator':
                return _pyfreeling.VectorSGEntity_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorSGEntity_clearself

            def get_allocator(self) -> 'std::vector< freeling::semgraph::SG_entity >::allocator_type':
                return _pyfreeling.VectorSGEntity_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorSGEntity_pop_backself

            def erase(self, *args) -> 'std::vector< freeling::semgraph::SG_entity >::iterator':
                return (_pyfreeling.VectorSGEntity_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorSGEntity)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'SG_entity') -> 'void':
                return _pyfreeling.VectorSGEntity_push_back(self, x)

            def front(self) -> 'std::vector< freeling::semgraph::SG_entity >::value_type const &':
                return _pyfreeling.VectorSGEntity_frontself

            def back(self) -> 'std::vector< freeling::semgraph::SG_entity >::value_type const &':
                return _pyfreeling.VectorSGEntity_backself

            def assign(self, n: 'std::vector< freeling::semgraph::SG_entity >::size_type', x: 'SG_entity') -> 'void':
                return _pyfreeling.VectorSGEntity_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorSGEntity_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorSGEntity_insert)(self, *args)

            def reserve(self, n: 'std::vector< freeling::semgraph::SG_entity >::size_type') -> 'void':
                return _pyfreeling.VectorSGEntity_reserve(self, n)

            def capacity(self) -> 'std::vector< freeling::semgraph::SG_entity >::size_type':
                return _pyfreeling.VectorSGEntity_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorSGEntity
            __del__ = lambda self: None


        VectorSGEntity_swigregister = _pyfreeling.VectorSGEntity_swigregister
        VectorSGEntity_swigregister(VectorSGEntity)

        class VectorSGFrame(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorSGFrame, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorSGFrame, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorSGFrame_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorSGFrame___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorSGFrame___bool__self

            def __len__(self) -> 'std::vector< freeling::semgraph::SG_frame >::size_type':
                return _pyfreeling.VectorSGFrame___len__self

            def __getslice__(self, i: 'std::vector< freeling::semgraph::SG_frame >::difference_type', j: 'std::vector< freeling::semgraph::SG_frame >::difference_type') -> 'std::vector< freeling::semgraph::SG_frame,std::allocator< freeling::semgraph::SG_frame > > *':
                return _pyfreeling.VectorSGFrame___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGFrame___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< freeling::semgraph::SG_frame >::difference_type', j: 'std::vector< freeling::semgraph::SG_frame >::difference_type') -> 'void':
                return _pyfreeling.VectorSGFrame___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGFrame___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< freeling::semgraph::SG_frame >::value_type const &':
                return (_pyfreeling.VectorSGFrame___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSGFrame___setitem__)(self, *args)

            def pop(self) -> 'std::vector< freeling::semgraph::SG_frame >::value_type':
                return _pyfreeling.VectorSGFrame_popself

            def append(self, x: 'SG_frame') -> 'void':
                return _pyfreeling.VectorSGFrame_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorSGFrame_emptyself

            def size(self) -> 'std::vector< freeling::semgraph::SG_frame >::size_type':
                return _pyfreeling.VectorSGFrame_sizeself

            def swap(self, v: 'VectorSGFrame') -> 'void':
                return _pyfreeling.VectorSGFrame_swap(self, v)

            def begin(self) -> 'std::vector< freeling::semgraph::SG_frame >::iterator':
                return _pyfreeling.VectorSGFrame_beginself

            def end(self) -> 'std::vector< freeling::semgraph::SG_frame >::iterator':
                return _pyfreeling.VectorSGFrame_endself

            def rbegin(self) -> 'std::vector< freeling::semgraph::SG_frame >::reverse_iterator':
                return _pyfreeling.VectorSGFrame_rbeginself

            def rend(self) -> 'std::vector< freeling::semgraph::SG_frame >::reverse_iterator':
                return _pyfreeling.VectorSGFrame_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorSGFrame_clearself

            def get_allocator(self) -> 'std::vector< freeling::semgraph::SG_frame >::allocator_type':
                return _pyfreeling.VectorSGFrame_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorSGFrame_pop_backself

            def erase(self, *args) -> 'std::vector< freeling::semgraph::SG_frame >::iterator':
                return (_pyfreeling.VectorSGFrame_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorSGFrame)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'SG_frame') -> 'void':
                return _pyfreeling.VectorSGFrame_push_back(self, x)

            def front(self) -> 'std::vector< freeling::semgraph::SG_frame >::value_type const &':
                return _pyfreeling.VectorSGFrame_frontself

            def back(self) -> 'std::vector< freeling::semgraph::SG_frame >::value_type const &':
                return _pyfreeling.VectorSGFrame_backself

            def assign(self, n: 'std::vector< freeling::semgraph::SG_frame >::size_type', x: 'SG_frame') -> 'void':
                return _pyfreeling.VectorSGFrame_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorSGFrame_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorSGFrame_insert)(self, *args)

            def reserve(self, n: 'std::vector< freeling::semgraph::SG_frame >::size_type') -> 'void':
                return _pyfreeling.VectorSGFrame_reserve(self, n)

            def capacity(self) -> 'std::vector< freeling::semgraph::SG_frame >::size_type':
                return _pyfreeling.VectorSGFrame_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorSGFrame
            __del__ = lambda self: None


        VectorSGFrame_swigregister = _pyfreeling.VectorSGFrame_swigregister
        VectorSGFrame_swigregister(VectorSGFrame)

        class ListString(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ListString, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ListString, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.ListString_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.ListString___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.ListString___bool__self

            def __len__(self) -> 'std::list< std::wstring >::size_type':
                return _pyfreeling.ListString___len__self

            def __getslice__(self, i: 'std::list< std::wstring >::difference_type', j: 'std::list< std::wstring >::difference_type') -> 'std::list< std::wstring,std::allocator< std::wstring > > *':
                return _pyfreeling.ListString___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.ListString___setslice__)(self, *args)

            def __delslice__(self, i: 'std::list< std::wstring >::difference_type', j: 'std::list< std::wstring >::difference_type') -> 'void':
                return _pyfreeling.ListString___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.ListString___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::list< std::wstring >::value_type const &':
                return (_pyfreeling.ListString___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.ListString___setitem__)(self, *args)

            def pop(self) -> 'std::list< std::wstring >::value_type':
                return _pyfreeling.ListString_popself

            def append(self, x: 'std::list< std::wstring >::value_type const &') -> 'void':
                return _pyfreeling.ListString_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.ListString_emptyself

            def size(self) -> 'std::list< std::wstring >::size_type':
                return _pyfreeling.ListString_sizeself

            def swap(self, v: 'ListString') -> 'void':
                return _pyfreeling.ListString_swap(self, v)

            def begin(self) -> 'std::list< std::wstring >::iterator':
                return _pyfreeling.ListString_beginself

            def end(self) -> 'std::list< std::wstring >::iterator':
                return _pyfreeling.ListString_endself

            def rbegin(self) -> 'std::list< std::wstring >::reverse_iterator':
                return _pyfreeling.ListString_rbeginself

            def rend(self) -> 'std::list< std::wstring >::reverse_iterator':
                return _pyfreeling.ListString_rendself

            def clear(self) -> 'void':
                return _pyfreeling.ListString_clearself

            def get_allocator(self) -> 'std::list< std::wstring >::allocator_type':
                return _pyfreeling.ListString_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.ListString_pop_backself

            def erase(self, *args) -> 'std::list< std::wstring >::iterator':
                return (_pyfreeling.ListString_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_ListString)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'std::list< std::wstring >::value_type const &') -> 'void':
                return _pyfreeling.ListString_push_back(self, x)

            def front(self) -> 'std::list< std::wstring >::value_type const &':
                return _pyfreeling.ListString_frontself

            def back(self) -> 'std::list< std::wstring >::value_type const &':
                return _pyfreeling.ListString_backself

            def assign(self, n: 'std::list< std::wstring >::size_type', x: 'std::list< std::wstring >::value_type const &') -> 'void':
                return _pyfreeling.ListString_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.ListString_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.ListString_insert)(self, *args)

            def pop_front(self) -> 'void':
                return _pyfreeling.ListString_pop_frontself

            def push_front(self, x: 'std::list< std::wstring >::value_type const &') -> 'void':
                return _pyfreeling.ListString_push_front(self, x)

            def reverse(self) -> 'void':
                return _pyfreeling.ListString_reverseself

            __swig_destroy__ = _pyfreeling.delete_ListString
            __del__ = lambda self: None


        ListString_swigregister = _pyfreeling.ListString_swigregister
        ListString_swigregister(ListString)

        class ListInt(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ListInt, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ListInt, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.ListInt_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.ListInt___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.ListInt___bool__self

            def __len__(self) -> 'std::list< int >::size_type':
                return _pyfreeling.ListInt___len__self

            def __getslice__(self, i: 'std::list< int >::difference_type', j: 'std::list< int >::difference_type') -> 'std::list< int,std::allocator< int > > *':
                return _pyfreeling.ListInt___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.ListInt___setslice__)(self, *args)

            def __delslice__(self, i: 'std::list< int >::difference_type', j: 'std::list< int >::difference_type') -> 'void':
                return _pyfreeling.ListInt___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.ListInt___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::list< int >::value_type const &':
                return (_pyfreeling.ListInt___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.ListInt___setitem__)(self, *args)

            def pop(self) -> 'std::list< int >::value_type':
                return _pyfreeling.ListInt_popself

            def append(self, x: 'std::list< int >::value_type const &') -> 'void':
                return _pyfreeling.ListInt_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.ListInt_emptyself

            def size(self) -> 'std::list< int >::size_type':
                return _pyfreeling.ListInt_sizeself

            def swap(self, v: 'ListInt') -> 'void':
                return _pyfreeling.ListInt_swap(self, v)

            def begin(self) -> 'std::list< int >::iterator':
                return _pyfreeling.ListInt_beginself

            def end(self) -> 'std::list< int >::iterator':
                return _pyfreeling.ListInt_endself

            def rbegin(self) -> 'std::list< int >::reverse_iterator':
                return _pyfreeling.ListInt_rbeginself

            def rend(self) -> 'std::list< int >::reverse_iterator':
                return _pyfreeling.ListInt_rendself

            def clear(self) -> 'void':
                return _pyfreeling.ListInt_clearself

            def get_allocator(self) -> 'std::list< int >::allocator_type':
                return _pyfreeling.ListInt_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.ListInt_pop_backself

            def erase(self, *args) -> 'std::list< int >::iterator':
                return (_pyfreeling.ListInt_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_ListInt)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'std::list< int >::value_type const &') -> 'void':
                return _pyfreeling.ListInt_push_back(self, x)

            def front(self) -> 'std::list< int >::value_type const &':
                return _pyfreeling.ListInt_frontself

            def back(self) -> 'std::list< int >::value_type const &':
                return _pyfreeling.ListInt_backself

            def assign(self, n: 'std::list< int >::size_type', x: 'std::list< int >::value_type const &') -> 'void':
                return _pyfreeling.ListInt_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.ListInt_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.ListInt_insert)(self, *args)

            def pop_front(self) -> 'void':
                return _pyfreeling.ListInt_pop_frontself

            def push_front(self, x: 'std::list< int >::value_type const &') -> 'void':
                return _pyfreeling.ListInt_push_front(self, x)

            def reverse(self) -> 'void':
                return _pyfreeling.ListInt_reverseself

            __swig_destroy__ = _pyfreeling.delete_ListInt
            __del__ = lambda self: None


        ListInt_swigregister = _pyfreeling.ListInt_swigregister
        ListInt_swigregister(ListInt)

        class VectorListInt(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorListInt, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorListInt, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorListInt_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorListInt___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorListInt___bool__self

            def __len__(self) -> 'std::vector< std::list< int > >::size_type':
                return _pyfreeling.VectorListInt___len__self

            def __getslice__(self, i: 'std::vector< std::list< int > >::difference_type', j: 'std::vector< std::list< int > >::difference_type') -> 'std::vector< std::list< int,std::allocator< int > >,std::allocator< std::list< int,std::allocator< int > > > > *':
                return _pyfreeling.VectorListInt___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorListInt___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< std::list< int > >::difference_type', j: 'std::vector< std::list< int > >::difference_type') -> 'void':
                return _pyfreeling.VectorListInt___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorListInt___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< std::list< int > >::value_type const &':
                return (_pyfreeling.VectorListInt___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorListInt___setitem__)(self, *args)

            def pop(self) -> 'std::vector< std::list< int > >::value_type':
                return _pyfreeling.VectorListInt_popself

            def append(self, x: 'ListInt') -> 'void':
                return _pyfreeling.VectorListInt_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorListInt_emptyself

            def size(self) -> 'std::vector< std::list< int > >::size_type':
                return _pyfreeling.VectorListInt_sizeself

            def swap(self, v: 'VectorListInt') -> 'void':
                return _pyfreeling.VectorListInt_swap(self, v)

            def begin(self) -> 'std::vector< std::list< int > >::iterator':
                return _pyfreeling.VectorListInt_beginself

            def end(self) -> 'std::vector< std::list< int > >::iterator':
                return _pyfreeling.VectorListInt_endself

            def rbegin(self) -> 'std::vector< std::list< int > >::reverse_iterator':
                return _pyfreeling.VectorListInt_rbeginself

            def rend(self) -> 'std::vector< std::list< int > >::reverse_iterator':
                return _pyfreeling.VectorListInt_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorListInt_clearself

            def get_allocator(self) -> 'std::vector< std::list< int > >::allocator_type':
                return _pyfreeling.VectorListInt_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorListInt_pop_backself

            def erase(self, *args) -> 'std::vector< std::list< int > >::iterator':
                return (_pyfreeling.VectorListInt_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorListInt)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'ListInt') -> 'void':
                return _pyfreeling.VectorListInt_push_back(self, x)

            def front(self) -> 'std::vector< std::list< int > >::value_type const &':
                return _pyfreeling.VectorListInt_frontself

            def back(self) -> 'std::vector< std::list< int > >::value_type const &':
                return _pyfreeling.VectorListInt_backself

            def assign(self, n: 'std::vector< std::list< int > >::size_type', x: 'ListInt') -> 'void':
                return _pyfreeling.VectorListInt_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorListInt_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorListInt_insert)(self, *args)

            def reserve(self, n: 'std::vector< std::list< int > >::size_type') -> 'void':
                return _pyfreeling.VectorListInt_reserve(self, n)

            def capacity(self) -> 'std::vector< std::list< int > >::size_type':
                return _pyfreeling.VectorListInt_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorListInt
            __del__ = lambda self: None


        VectorListInt_swigregister = _pyfreeling.VectorListInt_swigregister
        VectorListInt_swigregister(VectorListInt)

        class VectorListString(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorListString, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorListString, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorListString_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorListString___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorListString___bool__self

            def __len__(self) -> 'std::vector< std::list< std::wstring > >::size_type':
                return _pyfreeling.VectorListString___len__self

            def __getslice__(self, i: 'std::vector< std::list< std::wstring > >::difference_type', j: 'std::vector< std::list< std::wstring > >::difference_type') -> 'std::vector< std::list< std::wstring,std::allocator< std::wstring > >,std::allocator< std::list< std::wstring,std::allocator< std::wstring > > > > *':
                return _pyfreeling.VectorListString___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorListString___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< std::list< std::wstring > >::difference_type', j: 'std::vector< std::list< std::wstring > >::difference_type') -> 'void':
                return _pyfreeling.VectorListString___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorListString___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< std::list< std::wstring > >::value_type const &':
                return (_pyfreeling.VectorListString___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorListString___setitem__)(self, *args)

            def pop(self) -> 'std::vector< std::list< std::wstring > >::value_type':
                return _pyfreeling.VectorListString_popself

            def append(self, x: 'ListString') -> 'void':
                return _pyfreeling.VectorListString_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorListString_emptyself

            def size(self) -> 'std::vector< std::list< std::wstring > >::size_type':
                return _pyfreeling.VectorListString_sizeself

            def swap(self, v: 'VectorListString') -> 'void':
                return _pyfreeling.VectorListString_swap(self, v)

            def begin(self) -> 'std::vector< std::list< std::wstring > >::iterator':
                return _pyfreeling.VectorListString_beginself

            def end(self) -> 'std::vector< std::list< std::wstring > >::iterator':
                return _pyfreeling.VectorListString_endself

            def rbegin(self) -> 'std::vector< std::list< std::wstring > >::reverse_iterator':
                return _pyfreeling.VectorListString_rbeginself

            def rend(self) -> 'std::vector< std::list< std::wstring > >::reverse_iterator':
                return _pyfreeling.VectorListString_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorListString_clearself

            def get_allocator(self) -> 'std::vector< std::list< std::wstring > >::allocator_type':
                return _pyfreeling.VectorListString_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorListString_pop_backself

            def erase(self, *args) -> 'std::vector< std::list< std::wstring > >::iterator':
                return (_pyfreeling.VectorListString_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorListString)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'ListString') -> 'void':
                return _pyfreeling.VectorListString_push_back(self, x)

            def front(self) -> 'std::vector< std::list< std::wstring > >::value_type const &':
                return _pyfreeling.VectorListString_frontself

            def back(self) -> 'std::vector< std::list< std::wstring > >::value_type const &':
                return _pyfreeling.VectorListString_backself

            def assign(self, n: 'std::vector< std::list< std::wstring > >::size_type', x: 'ListString') -> 'void':
                return _pyfreeling.VectorListString_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorListString_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorListString_insert)(self, *args)

            def reserve(self, n: 'std::vector< std::list< std::wstring > >::size_type') -> 'void':
                return _pyfreeling.VectorListString_reserve(self, n)

            def capacity(self) -> 'std::vector< std::list< std::wstring > >::size_type':
                return _pyfreeling.VectorListString_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorListString
            __del__ = lambda self: None


        VectorListString_swigregister = _pyfreeling.VectorListString_swigregister
        VectorListString_swigregister(VectorListString)

        class VectorString(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorString, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorString, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorString_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorString___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorString___bool__self

            def __len__(self) -> 'std::vector< std::wstring >::size_type':
                return _pyfreeling.VectorString___len__self

            def __getslice__(self, i: 'std::vector< std::wstring >::difference_type', j: 'std::vector< std::wstring >::difference_type') -> 'std::vector< std::wstring,std::allocator< std::wstring > > *':
                return _pyfreeling.VectorString___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorString___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< std::wstring >::difference_type', j: 'std::vector< std::wstring >::difference_type') -> 'void':
                return _pyfreeling.VectorString___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorString___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< std::wstring >::value_type const &':
                return (_pyfreeling.VectorString___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorString___setitem__)(self, *args)

            def pop(self) -> 'std::vector< std::wstring >::value_type':
                return _pyfreeling.VectorString_popself

            def append(self, x: 'std::vector< std::wstring >::value_type const &') -> 'void':
                return _pyfreeling.VectorString_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorString_emptyself

            def size(self) -> 'std::vector< std::wstring >::size_type':
                return _pyfreeling.VectorString_sizeself

            def swap(self, v: 'VectorString') -> 'void':
                return _pyfreeling.VectorString_swap(self, v)

            def begin(self) -> 'std::vector< std::wstring >::iterator':
                return _pyfreeling.VectorString_beginself

            def end(self) -> 'std::vector< std::wstring >::iterator':
                return _pyfreeling.VectorString_endself

            def rbegin(self) -> 'std::vector< std::wstring >::reverse_iterator':
                return _pyfreeling.VectorString_rbeginself

            def rend(self) -> 'std::vector< std::wstring >::reverse_iterator':
                return _pyfreeling.VectorString_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorString_clearself

            def get_allocator(self) -> 'std::vector< std::wstring >::allocator_type':
                return _pyfreeling.VectorString_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorString_pop_backself

            def erase(self, *args) -> 'std::vector< std::wstring >::iterator':
                return (_pyfreeling.VectorString_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorString)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'std::vector< std::wstring >::value_type const &') -> 'void':
                return _pyfreeling.VectorString_push_back(self, x)

            def front(self) -> 'std::vector< std::wstring >::value_type const &':
                return _pyfreeling.VectorString_frontself

            def back(self) -> 'std::vector< std::wstring >::value_type const &':
                return _pyfreeling.VectorString_backself

            def assign(self, n: 'std::vector< std::wstring >::size_type', x: 'std::vector< std::wstring >::value_type const &') -> 'void':
                return _pyfreeling.VectorString_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorString_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorString_insert)(self, *args)

            def reserve(self, n: 'std::vector< std::wstring >::size_type') -> 'void':
                return _pyfreeling.VectorString_reserve(self, n)

            def capacity(self) -> 'std::vector< std::wstring >::size_type':
                return _pyfreeling.VectorString_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorString
            __del__ = lambda self: None


        VectorString_swigregister = _pyfreeling.VectorString_swigregister
        VectorString_swigregister(VectorString)

        class VectorSetString(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorSetString, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorSetString, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorSetString_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorSetString___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorSetString___bool__self

            def __len__(self) -> 'std::vector< std::set< std::wstring > >::size_type':
                return _pyfreeling.VectorSetString___len__self

            def __getslice__(self, i: 'std::vector< std::set< std::wstring > >::difference_type', j: 'std::vector< std::set< std::wstring > >::difference_type') -> 'std::vector< std::set< std::wstring,std::less< std::wstring >,std::allocator< std::wstring > >,std::allocator< std::set< std::wstring,std::less< std::wstring >,std::allocator< std::wstring > > > > *':
                return _pyfreeling.VectorSetString___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorSetString___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< std::set< std::wstring > >::difference_type', j: 'std::vector< std::set< std::wstring > >::difference_type') -> 'void':
                return _pyfreeling.VectorSetString___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSetString___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< std::set< std::wstring > >::value_type const &':
                return (_pyfreeling.VectorSetString___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSetString___setitem__)(self, *args)

            def pop(self) -> 'std::vector< std::set< std::wstring > >::value_type':
                return _pyfreeling.VectorSetString_popself

            def append(self, x: 'SetString') -> 'void':
                return _pyfreeling.VectorSetString_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorSetString_emptyself

            def size(self) -> 'std::vector< std::set< std::wstring > >::size_type':
                return _pyfreeling.VectorSetString_sizeself

            def swap(self, v: 'VectorSetString') -> 'void':
                return _pyfreeling.VectorSetString_swap(self, v)

            def begin(self) -> 'std::vector< std::set< std::wstring > >::iterator':
                return _pyfreeling.VectorSetString_beginself

            def end(self) -> 'std::vector< std::set< std::wstring > >::iterator':
                return _pyfreeling.VectorSetString_endself

            def rbegin(self) -> 'std::vector< std::set< std::wstring > >::reverse_iterator':
                return _pyfreeling.VectorSetString_rbeginself

            def rend(self) -> 'std::vector< std::set< std::wstring > >::reverse_iterator':
                return _pyfreeling.VectorSetString_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorSetString_clearself

            def get_allocator(self) -> 'std::vector< std::set< std::wstring > >::allocator_type':
                return _pyfreeling.VectorSetString_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorSetString_pop_backself

            def erase(self, *args) -> 'std::vector< std::set< std::wstring > >::iterator':
                return (_pyfreeling.VectorSetString_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorSetString)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'SetString') -> 'void':
                return _pyfreeling.VectorSetString_push_back(self, x)

            def front(self) -> 'std::vector< std::set< std::wstring > >::value_type const &':
                return _pyfreeling.VectorSetString_frontself

            def back(self) -> 'std::vector< std::set< std::wstring > >::value_type const &':
                return _pyfreeling.VectorSetString_backself

            def assign(self, n: 'std::vector< std::set< std::wstring > >::size_type', x: 'SetString') -> 'void':
                return _pyfreeling.VectorSetString_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorSetString_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorSetString_insert)(self, *args)

            def reserve(self, n: 'std::vector< std::set< std::wstring > >::size_type') -> 'void':
                return _pyfreeling.VectorSetString_reserve(self, n)

            def capacity(self) -> 'std::vector< std::set< std::wstring > >::size_type':
                return _pyfreeling.VectorSetString_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorSetString
            __del__ = lambda self: None


        VectorSetString_swigregister = _pyfreeling.VectorSetString_swigregister
        VectorSetString_swigregister(VectorSetString)

        class VectorSetInt(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorSetInt, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorSetInt, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorSetInt_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorSetInt___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorSetInt___bool__self

            def __len__(self) -> 'std::vector< std::set< int > >::size_type':
                return _pyfreeling.VectorSetInt___len__self

            def __getslice__(self, i: 'std::vector< std::set< int > >::difference_type', j: 'std::vector< std::set< int > >::difference_type') -> 'std::vector< std::set< int,std::less< int >,std::allocator< int > >,std::allocator< std::set< int,std::less< int >,std::allocator< int > > > > *':
                return _pyfreeling.VectorSetInt___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorSetInt___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< std::set< int > >::difference_type', j: 'std::vector< std::set< int > >::difference_type') -> 'void':
                return _pyfreeling.VectorSetInt___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSetInt___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< std::set< int > >::value_type const &':
                return (_pyfreeling.VectorSetInt___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorSetInt___setitem__)(self, *args)

            def pop(self) -> 'std::vector< std::set< int > >::value_type':
                return _pyfreeling.VectorSetInt_popself

            def append(self, x: 'std::vector< std::set< int > >::value_type const &') -> 'void':
                return _pyfreeling.VectorSetInt_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorSetInt_emptyself

            def size(self) -> 'std::vector< std::set< int > >::size_type':
                return _pyfreeling.VectorSetInt_sizeself

            def swap(self, v: 'VectorSetInt') -> 'void':
                return _pyfreeling.VectorSetInt_swap(self, v)

            def begin(self) -> 'std::vector< std::set< int > >::iterator':
                return _pyfreeling.VectorSetInt_beginself

            def end(self) -> 'std::vector< std::set< int > >::iterator':
                return _pyfreeling.VectorSetInt_endself

            def rbegin(self) -> 'std::vector< std::set< int > >::reverse_iterator':
                return _pyfreeling.VectorSetInt_rbeginself

            def rend(self) -> 'std::vector< std::set< int > >::reverse_iterator':
                return _pyfreeling.VectorSetInt_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorSetInt_clearself

            def get_allocator(self) -> 'std::vector< std::set< int > >::allocator_type':
                return _pyfreeling.VectorSetInt_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorSetInt_pop_backself

            def erase(self, *args) -> 'std::vector< std::set< int > >::iterator':
                return (_pyfreeling.VectorSetInt_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorSetInt)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'std::vector< std::set< int > >::value_type const &') -> 'void':
                return _pyfreeling.VectorSetInt_push_back(self, x)

            def front(self) -> 'std::vector< std::set< int > >::value_type const &':
                return _pyfreeling.VectorSetInt_frontself

            def back(self) -> 'std::vector< std::set< int > >::value_type const &':
                return _pyfreeling.VectorSetInt_backself

            def assign(self, n: 'std::vector< std::set< int > >::size_type', x: 'std::vector< std::set< int > >::value_type const &') -> 'void':
                return _pyfreeling.VectorSetInt_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorSetInt_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorSetInt_insert)(self, *args)

            def reserve(self, n: 'std::vector< std::set< int > >::size_type') -> 'void':
                return _pyfreeling.VectorSetInt_reserve(self, n)

            def capacity(self) -> 'std::vector< std::set< int > >::size_type':
                return _pyfreeling.VectorSetInt_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorSetInt
            __del__ = lambda self: None


        VectorSetInt_swigregister = _pyfreeling.VectorSetInt_swigregister
        VectorSetInt_swigregister(VectorSetInt)

        class SetString(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, SetString, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, SetString, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.SetString_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.SetString___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.SetString___bool__self

            def __len__(self) -> 'std::set< std::wstring >::size_type':
                return _pyfreeling.SetString___len__self

            def append(self, x: 'std::set< std::wstring >::value_type') -> 'void':
                return _pyfreeling.SetString_append(self, x)

            def __contains__(self, x: 'std::set< std::wstring >::value_type') -> 'bool':
                return _pyfreeling.SetString___contains__(self, x)

            def __getitem__(self, i: 'std::set< std::wstring >::difference_type') -> 'std::set< std::wstring >::value_type':
                return _pyfreeling.SetString___getitem__(self, i)

            def add(self, x: 'std::set< std::wstring >::value_type') -> 'void':
                return _pyfreeling.SetString_add(self, x)

            def discard(self, x: 'std::set< std::wstring >::value_type') -> 'void':
                return _pyfreeling.SetString_discard(self, x)

            def __init__(self, *args):
                this = (_pyfreeling.new_SetString)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def empty(self) -> 'bool':
                return _pyfreeling.SetString_emptyself

            def size(self) -> 'std::set< std::wstring >::size_type':
                return _pyfreeling.SetString_sizeself

            def clear(self) -> 'void':
                return _pyfreeling.SetString_clearself

            def swap(self, v: 'SetString') -> 'void':
                return _pyfreeling.SetString_swap(self, v)

            def count(self, x: 'std::set< std::wstring >::key_type const &') -> 'std::set< std::wstring >::size_type':
                return _pyfreeling.SetString_count(self, x)

            def begin(self) -> 'std::set< std::wstring >::iterator':
                return _pyfreeling.SetString_beginself

            def end(self) -> 'std::set< std::wstring >::iterator':
                return _pyfreeling.SetString_endself

            def rbegin(self) -> 'std::set< std::wstring >::reverse_iterator':
                return _pyfreeling.SetString_rbeginself

            def rend(self) -> 'std::set< std::wstring >::reverse_iterator':
                return _pyfreeling.SetString_rendself

            def erase(self, *args) -> 'void':
                return (_pyfreeling.SetString_erase)(self, *args)

            def find(self, x: 'std::set< std::wstring >::key_type const &') -> 'std::set< std::wstring >::iterator':
                return _pyfreeling.SetString_find(self, x)

            def lower_bound(self, x: 'std::set< std::wstring >::key_type const &') -> 'std::set< std::wstring >::iterator':
                return _pyfreeling.SetString_lower_bound(self, x)

            def upper_bound(self, x: 'std::set< std::wstring >::key_type const &') -> 'std::set< std::wstring >::iterator':
                return _pyfreeling.SetString_upper_bound(self, x)

            def equal_range(self, x: 'std::set< std::wstring >::key_type const &') -> 'std::pair< std::set< std::wstring >::iterator,std::set< std::wstring >::iterator >':
                return _pyfreeling.SetString_equal_range(self, x)

            def insert(self, _SetString__x: 'std::set< std::wstring >::value_type const &') -> 'std::pair< std::set< std::wstring >::iterator,bool >':
                return _pyfreeling.SetString_insert(self, _SetString__x)

            __swig_destroy__ = _pyfreeling.delete_SetString
            __del__ = lambda self: None


        SetString_swigregister = _pyfreeling.SetString_swigregister
        SetString_swigregister(SetString)

        class PairDoubleString(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, PairDoubleString, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, PairDoubleString, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_PairDoubleString)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_setmethods__['first'] = _pyfreeling.PairDoubleString_first_set
            __swig_getmethods__['first'] = _pyfreeling.PairDoubleString_first_get
            if _newclass:
                first = _swig_property(_pyfreeling.PairDoubleString_first_get, _pyfreeling.PairDoubleString_first_set)
            __swig_setmethods__['second'] = _pyfreeling.PairDoubleString_second_set
            __swig_getmethods__['second'] = _pyfreeling.PairDoubleString_second_get
            if _newclass:
                second = _swig_property(_pyfreeling.PairDoubleString_second_get, _pyfreeling.PairDoubleString_second_set)

            def __len__(self):
                return 2

            def __repr__(self):
                return str((self.first, self.second))

            def __getitem__(self, index):
                if not index % 2:
                    return self.first
                return self.second

            def __setitem__(self, index, val):
                if not index % 2:
                    self.first = val
                else:
                    self.second = val

            __swig_destroy__ = _pyfreeling.delete_PairDoubleString
            __del__ = lambda self: None


        PairDoubleString_swigregister = _pyfreeling.PairDoubleString_swigregister
        PairDoubleString_swigregister(PairDoubleString)

        class VectorPairDoubleString(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorPairDoubleString, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorPairDoubleString, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorPairDoubleString_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorPairDoubleString___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorPairDoubleString___bool__self

            def __len__(self) -> 'std::vector< std::pair< double,std::wstring > >::size_type':
                return _pyfreeling.VectorPairDoubleString___len__self

            def __getslice__(self, i: 'std::vector< std::pair< double,std::wstring > >::difference_type', j: 'std::vector< std::pair< double,std::wstring > >::difference_type') -> 'std::vector< std::pair< double,std::wstring >,std::allocator< std::pair< double,std::wstring > > > *':
                return _pyfreeling.VectorPairDoubleString___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorPairDoubleString___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< std::pair< double,std::wstring > >::difference_type', j: 'std::vector< std::pair< double,std::wstring > >::difference_type') -> 'void':
                return _pyfreeling.VectorPairDoubleString___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorPairDoubleString___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< std::pair< double,std::wstring > >::value_type const &':
                return (_pyfreeling.VectorPairDoubleString___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorPairDoubleString___setitem__)(self, *args)

            def pop(self) -> 'std::vector< std::pair< double,std::wstring > >::value_type':
                return _pyfreeling.VectorPairDoubleString_popself

            def append(self, x: 'PairDoubleString') -> 'void':
                return _pyfreeling.VectorPairDoubleString_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorPairDoubleString_emptyself

            def size(self) -> 'std::vector< std::pair< double,std::wstring > >::size_type':
                return _pyfreeling.VectorPairDoubleString_sizeself

            def swap(self, v: 'VectorPairDoubleString') -> 'void':
                return _pyfreeling.VectorPairDoubleString_swap(self, v)

            def begin(self) -> 'std::vector< std::pair< double,std::wstring > >::iterator':
                return _pyfreeling.VectorPairDoubleString_beginself

            def end(self) -> 'std::vector< std::pair< double,std::wstring > >::iterator':
                return _pyfreeling.VectorPairDoubleString_endself

            def rbegin(self) -> 'std::vector< std::pair< double,std::wstring > >::reverse_iterator':
                return _pyfreeling.VectorPairDoubleString_rbeginself

            def rend(self) -> 'std::vector< std::pair< double,std::wstring > >::reverse_iterator':
                return _pyfreeling.VectorPairDoubleString_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorPairDoubleString_clearself

            def get_allocator(self) -> 'std::vector< std::pair< double,std::wstring > >::allocator_type':
                return _pyfreeling.VectorPairDoubleString_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorPairDoubleString_pop_backself

            def erase(self, *args) -> 'std::vector< std::pair< double,std::wstring > >::iterator':
                return (_pyfreeling.VectorPairDoubleString_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorPairDoubleString)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'PairDoubleString') -> 'void':
                return _pyfreeling.VectorPairDoubleString_push_back(self, x)

            def front(self) -> 'std::vector< std::pair< double,std::wstring > >::value_type const &':
                return _pyfreeling.VectorPairDoubleString_frontself

            def back(self) -> 'std::vector< std::pair< double,std::wstring > >::value_type const &':
                return _pyfreeling.VectorPairDoubleString_backself

            def assign(self, n: 'std::vector< std::pair< double,std::wstring > >::size_type', x: 'PairDoubleString') -> 'void':
                return _pyfreeling.VectorPairDoubleString_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorPairDoubleString_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorPairDoubleString_insert)(self, *args)

            def reserve(self, n: 'std::vector< std::pair< double,std::wstring > >::size_type') -> 'void':
                return _pyfreeling.VectorPairDoubleString_reserve(self, n)

            def capacity(self) -> 'std::vector< std::pair< double,std::wstring > >::size_type':
                return _pyfreeling.VectorPairDoubleString_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorPairDoubleString
            __del__ = lambda self: None


        VectorPairDoubleString_swigregister = _pyfreeling.VectorPairDoubleString_swigregister
        VectorPairDoubleString_swigregister(VectorPairDoubleString)

        class PairStringString(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, PairStringString, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, PairStringString, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_PairStringString)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_setmethods__['first'] = _pyfreeling.PairStringString_first_set
            __swig_getmethods__['first'] = _pyfreeling.PairStringString_first_get
            if _newclass:
                first = _swig_property(_pyfreeling.PairStringString_first_get, _pyfreeling.PairStringString_first_set)
            __swig_setmethods__['second'] = _pyfreeling.PairStringString_second_set
            __swig_getmethods__['second'] = _pyfreeling.PairStringString_second_get
            if _newclass:
                second = _swig_property(_pyfreeling.PairStringString_second_get, _pyfreeling.PairStringString_second_set)

            def __len__(self):
                return 2

            def __repr__(self):
                return str((self.first, self.second))

            def __getitem__(self, index):
                if not index % 2:
                    return self.first
                return self.second

            def __setitem__(self, index, val):
                if not index % 2:
                    self.first = val
                else:
                    self.second = val

            __swig_destroy__ = _pyfreeling.delete_PairStringString
            __del__ = lambda self: None


        PairStringString_swigregister = _pyfreeling.PairStringString_swigregister
        PairStringString_swigregister(PairStringString)

        class VectorPairStringString(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, VectorPairStringString, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, VectorPairStringString, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.VectorPairStringString_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.VectorPairStringString___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.VectorPairStringString___bool__self

            def __len__(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::size_type':
                return _pyfreeling.VectorPairStringString___len__self

            def __getslice__(self, i: 'std::vector< std::pair< std::wstring,std::wstring > >::difference_type', j: 'std::vector< std::pair< std::wstring,std::wstring > >::difference_type') -> 'std::vector< std::pair< std::wstring,std::wstring >,std::allocator< std::pair< std::wstring,std::wstring > > > *':
                return _pyfreeling.VectorPairStringString___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.VectorPairStringString___setslice__)(self, *args)

            def __delslice__(self, i: 'std::vector< std::pair< std::wstring,std::wstring > >::difference_type', j: 'std::vector< std::pair< std::wstring,std::wstring > >::difference_type') -> 'void':
                return _pyfreeling.VectorPairStringString___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorPairStringString___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::vector< std::pair< std::wstring,std::wstring > >::value_type const &':
                return (_pyfreeling.VectorPairStringString___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.VectorPairStringString___setitem__)(self, *args)

            def pop(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::value_type':
                return _pyfreeling.VectorPairStringString_popself

            def append(self, x: 'PairStringString') -> 'void':
                return _pyfreeling.VectorPairStringString_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.VectorPairStringString_emptyself

            def size(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::size_type':
                return _pyfreeling.VectorPairStringString_sizeself

            def swap(self, v: 'VectorPairStringString') -> 'void':
                return _pyfreeling.VectorPairStringString_swap(self, v)

            def begin(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::iterator':
                return _pyfreeling.VectorPairStringString_beginself

            def end(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::iterator':
                return _pyfreeling.VectorPairStringString_endself

            def rbegin(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::reverse_iterator':
                return _pyfreeling.VectorPairStringString_rbeginself

            def rend(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::reverse_iterator':
                return _pyfreeling.VectorPairStringString_rendself

            def clear(self) -> 'void':
                return _pyfreeling.VectorPairStringString_clearself

            def get_allocator(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::allocator_type':
                return _pyfreeling.VectorPairStringString_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.VectorPairStringString_pop_backself

            def erase(self, *args) -> 'std::vector< std::pair< std::wstring,std::wstring > >::iterator':
                return (_pyfreeling.VectorPairStringString_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_VectorPairStringString)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'PairStringString') -> 'void':
                return _pyfreeling.VectorPairStringString_push_back(self, x)

            def front(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::value_type const &':
                return _pyfreeling.VectorPairStringString_frontself

            def back(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::value_type const &':
                return _pyfreeling.VectorPairStringString_backself

            def assign(self, n: 'std::vector< std::pair< std::wstring,std::wstring > >::size_type', x: 'PairStringString') -> 'void':
                return _pyfreeling.VectorPairStringString_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.VectorPairStringString_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.VectorPairStringString_insert)(self, *args)

            def reserve(self, n: 'std::vector< std::pair< std::wstring,std::wstring > >::size_type') -> 'void':
                return _pyfreeling.VectorPairStringString_reserve(self, n)

            def capacity(self) -> 'std::vector< std::pair< std::wstring,std::wstring > >::size_type':
                return _pyfreeling.VectorPairStringString_capacityself

            __swig_destroy__ = _pyfreeling.delete_VectorPairStringString
            __del__ = lambda self: None


        VectorPairStringString_swigregister = _pyfreeling.VectorPairStringString_swigregister
        VectorPairStringString_swigregister(VectorPairStringString)

        class PairStringInt(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, PairStringInt, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, PairStringInt, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_PairStringInt)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_setmethods__['first'] = _pyfreeling.PairStringInt_first_set
            __swig_getmethods__['first'] = _pyfreeling.PairStringInt_first_get
            if _newclass:
                first = _swig_property(_pyfreeling.PairStringInt_first_get, _pyfreeling.PairStringInt_first_set)
            __swig_setmethods__['second'] = _pyfreeling.PairStringInt_second_set
            __swig_getmethods__['second'] = _pyfreeling.PairStringInt_second_get
            if _newclass:
                second = _swig_property(_pyfreeling.PairStringInt_second_get, _pyfreeling.PairStringInt_second_set)

            def __len__(self):
                return 2

            def __repr__(self):
                return str((self.first, self.second))

            def __getitem__(self, index):
                if not index % 2:
                    return self.first
                return self.second

            def __setitem__(self, index, val):
                if not index % 2:
                    self.first = val
                else:
                    self.second = val

            __swig_destroy__ = _pyfreeling.delete_PairStringInt
            __del__ = lambda self: None


        PairStringInt_swigregister = _pyfreeling.PairStringInt_swigregister
        PairStringInt_swigregister(PairStringInt)

        class PairStringDouble(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, PairStringDouble, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, PairStringDouble, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_PairStringDouble)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_setmethods__['first'] = _pyfreeling.PairStringDouble_first_set
            __swig_getmethods__['first'] = _pyfreeling.PairStringDouble_first_get
            if _newclass:
                first = _swig_property(_pyfreeling.PairStringDouble_first_get, _pyfreeling.PairStringDouble_first_set)
            __swig_setmethods__['second'] = _pyfreeling.PairStringDouble_second_set
            __swig_getmethods__['second'] = _pyfreeling.PairStringDouble_second_get
            if _newclass:
                second = _swig_property(_pyfreeling.PairStringDouble_second_get, _pyfreeling.PairStringDouble_second_set)

            def __len__(self):
                return 2

            def __repr__(self):
                return str((self.first, self.second))

            def __getitem__(self, index):
                if not index % 2:
                    return self.first
                return self.second

            def __setitem__(self, index, val):
                if not index % 2:
                    self.first = val
                else:
                    self.second = val

            __swig_destroy__ = _pyfreeling.delete_PairStringDouble
            __del__ = lambda self: None


        PairStringDouble_swigregister = _pyfreeling.PairStringDouble_swigregister
        PairStringDouble_swigregister(PairStringDouble)

        class ListPairStringDouble(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ListPairStringDouble, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ListPairStringDouble, name)
            __repr__ = _swig_repr

            def iterator(self) -> 'swig::SwigPyIterator *':
                return _pyfreeling.ListPairStringDouble_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self) -> 'bool':
                return _pyfreeling.ListPairStringDouble___nonzero__self

            def __bool__(self) -> 'bool':
                return _pyfreeling.ListPairStringDouble___bool__self

            def __len__(self) -> 'std::list< std::pair< std::wstring,double > >::size_type':
                return _pyfreeling.ListPairStringDouble___len__self

            def __getslice__(self, i: 'std::list< std::pair< std::wstring,double > >::difference_type', j: 'std::list< std::pair< std::wstring,double > >::difference_type') -> 'std::list< std::pair< std::wstring,double >,std::allocator< std::pair< std::wstring,double > > > *':
                return _pyfreeling.ListPairStringDouble___getslice__(self, i, j)

            def __setslice__(self, *args) -> 'void':
                return (_pyfreeling.ListPairStringDouble___setslice__)(self, *args)

            def __delslice__(self, i: 'std::list< std::pair< std::wstring,double > >::difference_type', j: 'std::list< std::pair< std::wstring,double > >::difference_type') -> 'void':
                return _pyfreeling.ListPairStringDouble___delslice__(self, i, j)

            def __delitem__(self, *args) -> 'void':
                return (_pyfreeling.ListPairStringDouble___delitem__)(self, *args)

            def __getitem__(self, *args) -> 'std::list< std::pair< std::wstring,double > >::value_type const &':
                return (_pyfreeling.ListPairStringDouble___getitem__)(self, *args)

            def __setitem__(self, *args) -> 'void':
                return (_pyfreeling.ListPairStringDouble___setitem__)(self, *args)

            def pop(self) -> 'std::list< std::pair< std::wstring,double > >::value_type':
                return _pyfreeling.ListPairStringDouble_popself

            def append(self, x: 'PairStringDouble') -> 'void':
                return _pyfreeling.ListPairStringDouble_append(self, x)

            def empty(self) -> 'bool':
                return _pyfreeling.ListPairStringDouble_emptyself

            def size(self) -> 'std::list< std::pair< std::wstring,double > >::size_type':
                return _pyfreeling.ListPairStringDouble_sizeself

            def swap(self, v: 'ListPairStringDouble') -> 'void':
                return _pyfreeling.ListPairStringDouble_swap(self, v)

            def begin(self) -> 'std::list< std::pair< std::wstring,double > >::iterator':
                return _pyfreeling.ListPairStringDouble_beginself

            def end(self) -> 'std::list< std::pair< std::wstring,double > >::iterator':
                return _pyfreeling.ListPairStringDouble_endself

            def rbegin(self) -> 'std::list< std::pair< std::wstring,double > >::reverse_iterator':
                return _pyfreeling.ListPairStringDouble_rbeginself

            def rend(self) -> 'std::list< std::pair< std::wstring,double > >::reverse_iterator':
                return _pyfreeling.ListPairStringDouble_rendself

            def clear(self) -> 'void':
                return _pyfreeling.ListPairStringDouble_clearself

            def get_allocator(self) -> 'std::list< std::pair< std::wstring,double > >::allocator_type':
                return _pyfreeling.ListPairStringDouble_get_allocatorself

            def pop_back(self) -> 'void':
                return _pyfreeling.ListPairStringDouble_pop_backself

            def erase(self, *args) -> 'std::list< std::pair< std::wstring,double > >::iterator':
                return (_pyfreeling.ListPairStringDouble_erase)(self, *args)

            def __init__(self, *args):
                this = (_pyfreeling.new_ListPairStringDouble)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x: 'PairStringDouble') -> 'void':
                return _pyfreeling.ListPairStringDouble_push_back(self, x)

            def front(self) -> 'std::list< std::pair< std::wstring,double > >::value_type const &':
                return _pyfreeling.ListPairStringDouble_frontself

            def back(self) -> 'std::list< std::pair< std::wstring,double > >::value_type const &':
                return _pyfreeling.ListPairStringDouble_backself

            def assign(self, n: 'std::list< std::pair< std::wstring,double > >::size_type', x: 'PairStringDouble') -> 'void':
                return _pyfreeling.ListPairStringDouble_assign(self, n, x)

            def resize(self, *args) -> 'void':
                return (_pyfreeling.ListPairStringDouble_resize)(self, *args)

            def insert(self, *args) -> 'void':
                return (_pyfreeling.ListPairStringDouble_insert)(self, *args)

            def pop_front(self) -> 'void':
                return _pyfreeling.ListPairStringDouble_pop_frontself

            def push_front(self, x: 'PairStringDouble') -> 'void':
                return _pyfreeling.ListPairStringDouble_push_front(self, x)

            def reverse(self) -> 'void':
                return _pyfreeling.ListPairStringDouble_reverseself

            __swig_destroy__ = _pyfreeling.delete_ListPairStringDouble
            __del__ = lambda self: None


        ListPairStringDouble_swigregister = _pyfreeling.ListPairStringDouble_swigregister
        ListPairStringDouble_swigregister(ListPairStringDouble)

        class TreeOfNode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreeOfNode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreeOfNode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreeOfNode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreeOfNode
            __del__ = lambda self: None

            def clear(self) -> 'void':
                return _pyfreeling.TreeOfNode_clearself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreeOfNode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreeOfNode_emptyself

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreeOfNode_num_childrenself

            def has_ancestor(self, arg2: 'TreeOfNode') -> 'bool':
                return _pyfreeling.TreeOfNode_has_ancestor(self, arg2)

            def add_child(self, t: 'TreeOfNode', last: 'bool'=True) -> 'void':
                return _pyfreeling.TreeOfNode_add_child(self, t, last)

            def hang_child(self, *args) -> 'void':
                return (_pyfreeling.TreeOfNode_hang_child)(self, *args)

            def nth_child(self, *args) -> 'freeling::tree< freeling::node >::const_sibling_iterator':
                return (_pyfreeling.TreeOfNode_nth_child)(self, *args)

            def nth_child_ref(self, *args) -> 'freeling::tree< freeling::node > const &':
                return (_pyfreeling.TreeOfNode_nth_child_ref)(self, *args)

            def get_parent(self, *args) -> 'freeling::tree< freeling::node >::const_preorder_iterator':
                return (_pyfreeling.TreeOfNode_get_parent)(self, *args)

            def begin(self, *args) -> 'freeling::tree< freeling::node >::const_preorder_iterator':
                return (_pyfreeling.TreeOfNode_begin)(self, *args)

            def end(self, *args) -> 'freeling::tree< freeling::node >::const_preorder_iterator':
                return (_pyfreeling.TreeOfNode_end)(self, *args)

            def sibling_begin(self, *args) -> 'freeling::tree< freeling::node >::const_sibling_iterator':
                return (_pyfreeling.TreeOfNode_sibling_begin)(self, *args)

            def sibling_end(self, *args) -> 'freeling::tree< freeling::node >::const_sibling_iterator':
                return (_pyfreeling.TreeOfNode_sibling_end)(self, *args)

            def sibling_rbegin(self, *args) -> 'freeling::tree< freeling::node >::const_sibling_iterator':
                return (_pyfreeling.TreeOfNode_sibling_rbegin)(self, *args)

            def sibling_rend(self, *args) -> 'freeling::tree< freeling::node >::const_sibling_iterator':
                return (_pyfreeling.TreeOfNode_sibling_rend)(self, *args)


        TreeOfNode_swigregister = _pyfreeling.TreeOfNode_swigregister
        TreeOfNode_swigregister(TreeOfNode)

        class TreeOfDepnode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreeOfDepnode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreeOfDepnode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreeOfDepnode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreeOfDepnode
            __del__ = lambda self: None

            def clear(self) -> 'void':
                return _pyfreeling.TreeOfDepnode_clearself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreeOfDepnode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreeOfDepnode_emptyself

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreeOfDepnode_num_childrenself

            def has_ancestor(self, arg2: 'TreeOfDepnode') -> 'bool':
                return _pyfreeling.TreeOfDepnode_has_ancestor(self, arg2)

            def add_child(self, t: 'TreeOfDepnode', last: 'bool'=True) -> 'void':
                return _pyfreeling.TreeOfDepnode_add_child(self, t, last)

            def hang_child(self, *args) -> 'void':
                return (_pyfreeling.TreeOfDepnode_hang_child)(self, *args)

            def nth_child(self, *args) -> 'freeling::tree< freeling::depnode >::const_sibling_iterator':
                return (_pyfreeling.TreeOfDepnode_nth_child)(self, *args)

            def nth_child_ref(self, *args) -> 'freeling::tree< freeling::depnode > const &':
                return (_pyfreeling.TreeOfDepnode_nth_child_ref)(self, *args)

            def get_parent(self, *args) -> 'freeling::tree< freeling::depnode >::const_preorder_iterator':
                return (_pyfreeling.TreeOfDepnode_get_parent)(self, *args)

            def begin(self, *args) -> 'freeling::tree< freeling::depnode >::const_preorder_iterator':
                return (_pyfreeling.TreeOfDepnode_begin)(self, *args)

            def end(self, *args) -> 'freeling::tree< freeling::depnode >::const_preorder_iterator':
                return (_pyfreeling.TreeOfDepnode_end)(self, *args)

            def sibling_begin(self, *args) -> 'freeling::tree< freeling::depnode >::const_sibling_iterator':
                return (_pyfreeling.TreeOfDepnode_sibling_begin)(self, *args)

            def sibling_end(self, *args) -> 'freeling::tree< freeling::depnode >::const_sibling_iterator':
                return (_pyfreeling.TreeOfDepnode_sibling_end)(self, *args)

            def sibling_rbegin(self, *args) -> 'freeling::tree< freeling::depnode >::const_sibling_iterator':
                return (_pyfreeling.TreeOfDepnode_sibling_rbegin)(self, *args)

            def sibling_rend(self, *args) -> 'freeling::tree< freeling::depnode >::const_sibling_iterator':
                return (_pyfreeling.TreeOfDepnode_sibling_rend)(self, *args)


        TreeOfDepnode_swigregister = _pyfreeling.TreeOfDepnode_swigregister
        TreeOfDepnode_swigregister(TreeOfDepnode)

        class TreePreorderIteratorNode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreePreorderIteratorNode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreePreorderIteratorNode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreePreorderIteratorNode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreePreorderIteratorNode
            __del__ = lambda self: None

            def incr(self) -> 'void':
                return _pyfreeling.TreePreorderIteratorNode_incrself

            def decr(self) -> 'void':
                return _pyfreeling.TreePreorderIteratorNode_decrself

            def __eq__(self, t: 'TreePreorderIteratorNode') -> 'bool':
                return _pyfreeling.TreePreorderIteratorNode___eq__(self, t)

            def __ne__(self, t: 'TreePreorderIteratorNode') -> 'bool':
                return _pyfreeling.TreePreorderIteratorNode___ne__(self, t)

            def __ref__(self) -> 'freeling::node &':
                return _pyfreeling.TreePreorderIteratorNode___ref__self

            def __deref__(self) -> 'freeling::node *':
                return _pyfreeling.TreePreorderIteratorNode___deref__self

            def get_info(self) -> 'freeling::node *':
                return _pyfreeling.TreePreorderIteratorNode_get_infoself

            def is_defined(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorNode_is_definedself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorNode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorNode_emptyself

            def has_ancestor(self, p: 'TreeOfNode') -> 'bool':
                return _pyfreeling.TreePreorderIteratorNode_has_ancestor(self, p)

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreePreorderIteratorNode_num_childrenself

            def get_parent(self) -> 'freeling::tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreePreorderIteratorNode_get_parentself

            def nth_child(self, arg2: 'unsigned int') -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreePreorderIteratorNode_nth_child(self, arg2)

            def nth_child_ref(self, arg2: 'unsigned int') -> 'freeling::tree< freeling::node > &':
                return _pyfreeling.TreePreorderIteratorNode_nth_child_ref(self, arg2)

            def begin(self) -> 'freeling::tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreePreorderIteratorNode_beginself

            def end(self) -> 'freeling::tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreePreorderIteratorNode_endself

            def sibling_begin(self) -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreePreorderIteratorNode_sibling_beginself

            def sibling_end(self) -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreePreorderIteratorNode_sibling_endself

            def sibling_rbegin(self) -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreePreorderIteratorNode_sibling_rbeginself

            def sibling_rend(self) -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreePreorderIteratorNode_sibling_rendself

            def add_child(self, t: 'TreeOfNode', last: 'bool'=True) -> 'void':
                return _pyfreeling.TreePreorderIteratorNode_add_child(self, t, last)

            def hang_child(self, *args) -> 'void':
                return (_pyfreeling.TreePreorderIteratorNode_hang_child)(self, *args)

            def get_node_id(self) -> 'std::wstring':
                return _pyfreeling.TreePreorderIteratorNode_get_node_idself

            def set_node_id(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.TreePreorderIteratorNode_set_node_id(self, arg2)

            def get_label(self) -> 'std::wstring':
                return _pyfreeling.TreePreorderIteratorNode_get_labelself

            def has_word(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorNode_has_wordself

            def get_word(self, *args) -> 'freeling::word const &':
                return (_pyfreeling.TreePreorderIteratorNode_get_word)(self, *args)

            def set_label(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.TreePreorderIteratorNode_set_label(self, arg2)

            def set_word(self, arg2: 'word') -> 'void':
                return _pyfreeling.TreePreorderIteratorNode_set_word(self, arg2)

            def is_head(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorNode_is_headself

            def set_head(self, arg2: 'bool const') -> 'void':
                return _pyfreeling.TreePreorderIteratorNode_set_head(self, arg2)

            def is_chunk(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorNode_is_chunkself

            def set_chunk(self, arg2: 'int const') -> 'void':
                return _pyfreeling.TreePreorderIteratorNode_set_chunk(self, arg2)

            def get_chunk_ord(self) -> 'int':
                return _pyfreeling.TreePreorderIteratorNode_get_chunk_ordself


        TreePreorderIteratorNode_swigregister = _pyfreeling.TreePreorderIteratorNode_swigregister
        TreePreorderIteratorNode_swigregister(TreePreorderIteratorNode)

        class TreeSiblingIteratorNode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreeSiblingIteratorNode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreeSiblingIteratorNode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreeSiblingIteratorNode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreeSiblingIteratorNode
            __del__ = lambda self: None

            def incr(self) -> 'void':
                return _pyfreeling.TreeSiblingIteratorNode_incrself

            def decr(self) -> 'void':
                return _pyfreeling.TreeSiblingIteratorNode_decrself

            def __ref__(self) -> 'freeling::node &':
                return _pyfreeling.TreeSiblingIteratorNode___ref__self

            def __deref__(self) -> 'freeling::node *':
                return _pyfreeling.TreeSiblingIteratorNode___deref__self

            def get_info(self) -> 'freeling::node *':
                return _pyfreeling.TreeSiblingIteratorNode_get_infoself

            def __eq__(self, t: 'TreeSiblingIteratorNode') -> 'bool':
                return _pyfreeling.TreeSiblingIteratorNode___eq__(self, t)

            def __ne__(self, t: 'TreeSiblingIteratorNode') -> 'bool':
                return _pyfreeling.TreeSiblingIteratorNode___ne__(self, t)

            def get_parent(self) -> 'freeling::tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreeSiblingIteratorNode_get_parentself

            def nth_child(self, arg2: 'unsigned int') -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeSiblingIteratorNode_nth_child(self, arg2)

            def nth_child_ref(self, arg2: 'unsigned int') -> 'freeling::tree< freeling::node > &':
                return _pyfreeling.TreeSiblingIteratorNode_nth_child_ref(self, arg2)

            def is_defined(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorNode_is_definedself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorNode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorNode_emptyself

            def has_ancestor(self, p: 'TreeOfNode') -> 'bool':
                return _pyfreeling.TreeSiblingIteratorNode_has_ancestor(self, p)

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreeSiblingIteratorNode_num_childrenself

            def begin(self) -> 'freeling::tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreeSiblingIteratorNode_beginself

            def end(self) -> 'freeling::tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreeSiblingIteratorNode_endself

            def sibling_begin(self) -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeSiblingIteratorNode_sibling_beginself

            def sibling_end(self) -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeSiblingIteratorNode_sibling_endself

            def sibling_rbegin(self) -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeSiblingIteratorNode_sibling_rbeginself

            def sibling_rend(self) -> 'freeling::tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeSiblingIteratorNode_sibling_rendself

            def add_child(self, t: 'TreeOfNode', last: 'bool'=True) -> 'void':
                return _pyfreeling.TreeSiblingIteratorNode_add_child(self, t, last)

            def hang_child(self, *args) -> 'void':
                return (_pyfreeling.TreeSiblingIteratorNode_hang_child)(self, *args)

            def get_node_id(self) -> 'std::wstring':
                return _pyfreeling.TreeSiblingIteratorNode_get_node_idself

            def set_node_id(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.TreeSiblingIteratorNode_set_node_id(self, arg2)

            def get_label(self) -> 'std::wstring':
                return _pyfreeling.TreeSiblingIteratorNode_get_labelself

            def has_word(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorNode_has_wordself

            def get_word(self, *args) -> 'freeling::word const &':
                return (_pyfreeling.TreeSiblingIteratorNode_get_word)(self, *args)

            def set_label(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.TreeSiblingIteratorNode_set_label(self, arg2)

            def set_word(self, arg2: 'word') -> 'void':
                return _pyfreeling.TreeSiblingIteratorNode_set_word(self, arg2)

            def is_head(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorNode_is_headself

            def set_head(self, arg2: 'bool const') -> 'void':
                return _pyfreeling.TreeSiblingIteratorNode_set_head(self, arg2)

            def is_chunk(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorNode_is_chunkself

            def set_chunk(self, arg2: 'int const') -> 'void':
                return _pyfreeling.TreeSiblingIteratorNode_set_chunk(self, arg2)

            def get_chunk_ord(self) -> 'int':
                return _pyfreeling.TreeSiblingIteratorNode_get_chunk_ordself


        TreeSiblingIteratorNode_swigregister = _pyfreeling.TreeSiblingIteratorNode_swigregister
        TreeSiblingIteratorNode_swigregister(TreeSiblingIteratorNode)

        class TreePreorderIteratorDepnode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreePreorderIteratorDepnode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreePreorderIteratorDepnode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreePreorderIteratorDepnode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreePreorderIteratorDepnode
            __del__ = lambda self: None

            def incr(self) -> 'void':
                return _pyfreeling.TreePreorderIteratorDepnode_incrself

            def decr(self) -> 'void':
                return _pyfreeling.TreePreorderIteratorDepnode_decrself

            def __eq__(self, t: 'TreePreorderIteratorDepnode') -> 'bool':
                return _pyfreeling.TreePreorderIteratorDepnode___eq__(self, t)

            def __ne__(self, t: 'TreePreorderIteratorDepnode') -> 'bool':
                return _pyfreeling.TreePreorderIteratorDepnode___ne__(self, t)

            def __ref__(self) -> 'freeling::depnode &':
                return _pyfreeling.TreePreorderIteratorDepnode___ref__self

            def __deref__(self) -> 'freeling::depnode *':
                return _pyfreeling.TreePreorderIteratorDepnode___deref__self

            def get_info(self) -> 'freeling::depnode *':
                return _pyfreeling.TreePreorderIteratorDepnode_get_infoself

            def is_defined(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorDepnode_is_definedself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorDepnode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorDepnode_emptyself

            def has_ancestor(self, p: 'TreeOfDepnode') -> 'bool':
                return _pyfreeling.TreePreorderIteratorDepnode_has_ancestor(self, p)

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreePreorderIteratorDepnode_num_childrenself

            def get_parent(self) -> 'freeling::tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreePreorderIteratorDepnode_get_parentself

            def nth_child(self, arg2: 'unsigned int') -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreePreorderIteratorDepnode_nth_child(self, arg2)

            def nth_child_ref(self, arg2: 'unsigned int') -> 'freeling::tree< freeling::depnode > &':
                return _pyfreeling.TreePreorderIteratorDepnode_nth_child_ref(self, arg2)

            def begin(self) -> 'freeling::tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreePreorderIteratorDepnode_beginself

            def end(self) -> 'freeling::tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreePreorderIteratorDepnode_endself

            def sibling_begin(self) -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreePreorderIteratorDepnode_sibling_beginself

            def sibling_end(self) -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreePreorderIteratorDepnode_sibling_endself

            def sibling_rbegin(self) -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreePreorderIteratorDepnode_sibling_rbeginself

            def sibling_rend(self) -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreePreorderIteratorDepnode_sibling_rendself

            def add_child(self, t: 'TreeOfDepnode', last: 'bool'=True) -> 'void':
                return _pyfreeling.TreePreorderIteratorDepnode_add_child(self, t, last)

            def hang_child(self, *args) -> 'void':
                return (_pyfreeling.TreePreorderIteratorDepnode_hang_child)(self, *args)

            def set_link(self, arg2: 'TreePreorderIteratorNode') -> 'void':
                return _pyfreeling.TreePreorderIteratorDepnode_set_link(self, arg2)

            def get_link(self, *args) -> 'freeling::parse_tree::const_iterator':
                return (_pyfreeling.TreePreorderIteratorDepnode_get_link)(self, *args)

            def get_node_id(self) -> 'std::wstring':
                return _pyfreeling.TreePreorderIteratorDepnode_get_node_idself

            def set_node_id(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.TreePreorderIteratorDepnode_set_node_id(self, arg2)

            def get_label(self) -> 'std::wstring':
                return _pyfreeling.TreePreorderIteratorDepnode_get_labelself

            def has_word(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorDepnode_has_wordself

            def get_word(self, *args) -> 'freeling::word const &':
                return (_pyfreeling.TreePreorderIteratorDepnode_get_word)(self, *args)

            def set_label(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.TreePreorderIteratorDepnode_set_label(self, arg2)

            def set_word(self, arg2: 'word') -> 'void':
                return _pyfreeling.TreePreorderIteratorDepnode_set_word(self, arg2)

            def is_head(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorDepnode_is_headself

            def set_head(self, arg2: 'bool const') -> 'void':
                return _pyfreeling.TreePreorderIteratorDepnode_set_head(self, arg2)

            def is_chunk(self) -> 'bool':
                return _pyfreeling.TreePreorderIteratorDepnode_is_chunkself

            def set_chunk(self, arg2: 'int const') -> 'void':
                return _pyfreeling.TreePreorderIteratorDepnode_set_chunk(self, arg2)

            def get_chunk_ord(self) -> 'int':
                return _pyfreeling.TreePreorderIteratorDepnode_get_chunk_ordself


        TreePreorderIteratorDepnode_swigregister = _pyfreeling.TreePreorderIteratorDepnode_swigregister
        TreePreorderIteratorDepnode_swigregister(TreePreorderIteratorDepnode)

        class TreeSiblingIteratorDepnode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreeSiblingIteratorDepnode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreeSiblingIteratorDepnode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreeSiblingIteratorDepnode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreeSiblingIteratorDepnode
            __del__ = lambda self: None

            def incr(self) -> 'void':
                return _pyfreeling.TreeSiblingIteratorDepnode_incrself

            def decr(self) -> 'void':
                return _pyfreeling.TreeSiblingIteratorDepnode_decrself

            def __ref__(self) -> 'freeling::depnode &':
                return _pyfreeling.TreeSiblingIteratorDepnode___ref__self

            def __deref__(self) -> 'freeling::depnode *':
                return _pyfreeling.TreeSiblingIteratorDepnode___deref__self

            def get_info(self) -> 'freeling::depnode *':
                return _pyfreeling.TreeSiblingIteratorDepnode_get_infoself

            def __eq__(self, t: 'TreeSiblingIteratorDepnode') -> 'bool':
                return _pyfreeling.TreeSiblingIteratorDepnode___eq__(self, t)

            def __ne__(self, t: 'TreeSiblingIteratorDepnode') -> 'bool':
                return _pyfreeling.TreeSiblingIteratorDepnode___ne__(self, t)

            def get_parent(self) -> 'freeling::tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreeSiblingIteratorDepnode_get_parentself

            def nth_child(self, arg2: 'unsigned int') -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeSiblingIteratorDepnode_nth_child(self, arg2)

            def nth_child_ref(self, arg2: 'unsigned int') -> 'freeling::tree< freeling::depnode > &':
                return _pyfreeling.TreeSiblingIteratorDepnode_nth_child_ref(self, arg2)

            def is_defined(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorDepnode_is_definedself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorDepnode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorDepnode_emptyself

            def has_ancestor(self, p: 'TreeOfDepnode') -> 'bool':
                return _pyfreeling.TreeSiblingIteratorDepnode_has_ancestor(self, p)

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreeSiblingIteratorDepnode_num_childrenself

            def begin(self) -> 'freeling::tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreeSiblingIteratorDepnode_beginself

            def end(self) -> 'freeling::tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreeSiblingIteratorDepnode_endself

            def sibling_begin(self) -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeSiblingIteratorDepnode_sibling_beginself

            def sibling_end(self) -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeSiblingIteratorDepnode_sibling_endself

            def sibling_rbegin(self) -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeSiblingIteratorDepnode_sibling_rbeginself

            def sibling_rend(self) -> 'freeling::tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeSiblingIteratorDepnode_sibling_rendself

            def add_child(self, t: 'TreeOfDepnode', last: 'bool'=True) -> 'void':
                return _pyfreeling.TreeSiblingIteratorDepnode_add_child(self, t, last)

            def hang_child(self, *args) -> 'void':
                return (_pyfreeling.TreeSiblingIteratorDepnode_hang_child)(self, *args)

            def set_link(self, arg2: 'TreePreorderIteratorNode') -> 'void':
                return _pyfreeling.TreeSiblingIteratorDepnode_set_link(self, arg2)

            def get_link(self, *args) -> 'freeling::parse_tree::const_iterator':
                return (_pyfreeling.TreeSiblingIteratorDepnode_get_link)(self, *args)

            def get_node_id(self) -> 'std::wstring':
                return _pyfreeling.TreeSiblingIteratorDepnode_get_node_idself

            def set_node_id(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.TreeSiblingIteratorDepnode_set_node_id(self, arg2)

            def get_label(self) -> 'std::wstring':
                return _pyfreeling.TreeSiblingIteratorDepnode_get_labelself

            def has_word(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorDepnode_has_wordself

            def get_word(self, *args) -> 'freeling::word const &':
                return (_pyfreeling.TreeSiblingIteratorDepnode_get_word)(self, *args)

            def set_label(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.TreeSiblingIteratorDepnode_set_label(self, arg2)

            def set_word(self, arg2: 'word') -> 'void':
                return _pyfreeling.TreeSiblingIteratorDepnode_set_word(self, arg2)

            def is_head(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorDepnode_is_headself

            def set_head(self, arg2: 'bool const') -> 'void':
                return _pyfreeling.TreeSiblingIteratorDepnode_set_head(self, arg2)

            def is_chunk(self) -> 'bool':
                return _pyfreeling.TreeSiblingIteratorDepnode_is_chunkself

            def set_chunk(self, arg2: 'int const') -> 'void':
                return _pyfreeling.TreeSiblingIteratorDepnode_set_chunk(self, arg2)

            def get_chunk_ord(self) -> 'int':
                return _pyfreeling.TreeSiblingIteratorDepnode_get_chunk_ordself


        TreeSiblingIteratorDepnode_swigregister = _pyfreeling.TreeSiblingIteratorDepnode_swigregister
        TreeSiblingIteratorDepnode_swigregister(TreeSiblingIteratorDepnode)

        class TreeConstPreorderIteratorNode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreeConstPreorderIteratorNode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreeConstPreorderIteratorNode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreeConstPreorderIteratorNode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreeConstPreorderIteratorNode
            __del__ = lambda self: None

            def __ref__(self) -> 'freeling::node const &':
                return _pyfreeling.TreeConstPreorderIteratorNode___ref__self

            def __deref__(self) -> 'freeling::node const *':
                return _pyfreeling.TreeConstPreorderIteratorNode___deref__self

            def incr(self) -> 'void':
                return _pyfreeling.TreeConstPreorderIteratorNode_incrself

            def decr(self) -> 'void':
                return _pyfreeling.TreeConstPreorderIteratorNode_decrself

            def __eq__(self, t: 'TreeConstPreorderIteratorNode') -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorNode___eq__(self, t)

            def __ne__(self, t: 'TreeConstPreorderIteratorNode') -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorNode___ne__(self, t)

            def get_info(self) -> 'freeling::node const *':
                return _pyfreeling.TreeConstPreorderIteratorNode_get_infoself

            def is_defined(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorNode_is_definedself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorNode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorNode_emptyself

            def has_ancestor(self, p: 'TreeOfNode') -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorNode_has_ancestor(self, p)

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreeConstPreorderIteratorNode_num_childrenself

            def get_parent(self) -> 'freeling::const_tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreeConstPreorderIteratorNode_get_parentself

            def nth_child(self, n: 'unsigned int') -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstPreorderIteratorNode_nth_child(self, n)

            def nth_child_ref(self, n: 'unsigned int') -> 'freeling::tree< freeling::node > const &':
                return _pyfreeling.TreeConstPreorderIteratorNode_nth_child_ref(self, n)

            def begin(self) -> 'freeling::const_tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreeConstPreorderIteratorNode_beginself

            def end(self) -> 'freeling::const_tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreeConstPreorderIteratorNode_endself

            def sibling_begin(self) -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstPreorderIteratorNode_sibling_beginself

            def sibling_end(self) -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstPreorderIteratorNode_sibling_endself

            def sibling_rbegin(self) -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstPreorderIteratorNode_sibling_rbeginself

            def sibling_rend(self) -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstPreorderIteratorNode_sibling_rendself

            def get_node_id(self) -> 'std::wstring':
                return _pyfreeling.TreeConstPreorderIteratorNode_get_node_idself

            def get_label(self) -> 'std::wstring':
                return _pyfreeling.TreeConstPreorderIteratorNode_get_labelself

            def has_word(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorNode_has_wordself

            def get_word(self, *args) -> 'freeling::word const &':
                return (_pyfreeling.TreeConstPreorderIteratorNode_get_word)(self, *args)

            def is_head(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorNode_is_headself

            def is_chunk(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorNode_is_chunkself

            def get_chunk_ord(self) -> 'int':
                return _pyfreeling.TreeConstPreorderIteratorNode_get_chunk_ordself


        TreeConstPreorderIteratorNode_swigregister = _pyfreeling.TreeConstPreorderIteratorNode_swigregister
        TreeConstPreorderIteratorNode_swigregister(TreeConstPreorderIteratorNode)

        class TreeConstSiblingIteratorNode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreeConstSiblingIteratorNode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreeConstSiblingIteratorNode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreeConstSiblingIteratorNode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreeConstSiblingIteratorNode
            __del__ = lambda self: None

            def __ref__(self) -> 'freeling::node const &':
                return _pyfreeling.TreeConstSiblingIteratorNode___ref__self

            def __deref__(self) -> 'freeling::node const *':
                return _pyfreeling.TreeConstSiblingIteratorNode___deref__self

            def incr(self) -> 'void':
                return _pyfreeling.TreeConstSiblingIteratorNode_incrself

            def decr(self) -> 'void':
                return _pyfreeling.TreeConstSiblingIteratorNode_decrself

            def __eq__(self, t: 'TreeConstSiblingIteratorNode') -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorNode___eq__(self, t)

            def __ne__(self, t: 'TreeConstSiblingIteratorNode') -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorNode___ne__(self, t)

            def get_info(self) -> 'freeling::node const *':
                return _pyfreeling.TreeConstSiblingIteratorNode_get_infoself

            def is_defined(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorNode_is_definedself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorNode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorNode_emptyself

            def has_ancestor(self, p: 'TreeOfNode') -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorNode_has_ancestor(self, p)

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreeConstSiblingIteratorNode_num_childrenself

            def get_parent(self) -> 'freeling::const_tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreeConstSiblingIteratorNode_get_parentself

            def nth_child(self, n: 'unsigned int') -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstSiblingIteratorNode_nth_child(self, n)

            def nth_child_ref(self, n: 'unsigned int') -> 'freeling::tree< freeling::node > const &':
                return _pyfreeling.TreeConstSiblingIteratorNode_nth_child_ref(self, n)

            def begin(self) -> 'freeling::const_tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreeConstSiblingIteratorNode_beginself

            def end(self) -> 'freeling::const_tree_preorder_iterator< freeling::node >':
                return _pyfreeling.TreeConstSiblingIteratorNode_endself

            def sibling_begin(self) -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstSiblingIteratorNode_sibling_beginself

            def sibling_end(self) -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstSiblingIteratorNode_sibling_endself

            def sibling_rbegin(self) -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstSiblingIteratorNode_sibling_rbeginself

            def sibling_rend(self) -> 'freeling::const_tree_sibling_iterator< freeling::node >':
                return _pyfreeling.TreeConstSiblingIteratorNode_sibling_rendself

            def get_node_id(self) -> 'std::wstring':
                return _pyfreeling.TreeConstSiblingIteratorNode_get_node_idself

            def get_label(self) -> 'std::wstring':
                return _pyfreeling.TreeConstSiblingIteratorNode_get_labelself

            def has_word(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorNode_has_wordself

            def get_word(self, *args) -> 'freeling::word const &':
                return (_pyfreeling.TreeConstSiblingIteratorNode_get_word)(self, *args)

            def is_head(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorNode_is_headself

            def is_chunk(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorNode_is_chunkself

            def get_chunk_ord(self) -> 'int':
                return _pyfreeling.TreeConstSiblingIteratorNode_get_chunk_ordself


        TreeConstSiblingIteratorNode_swigregister = _pyfreeling.TreeConstSiblingIteratorNode_swigregister
        TreeConstSiblingIteratorNode_swigregister(TreeConstSiblingIteratorNode)

        class TreeConstPreorderIteratorDepnode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreeConstPreorderIteratorDepnode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreeConstPreorderIteratorDepnode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreeConstPreorderIteratorDepnode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreeConstPreorderIteratorDepnode
            __del__ = lambda self: None

            def __ref__(self) -> 'freeling::depnode const &':
                return _pyfreeling.TreeConstPreorderIteratorDepnode___ref__self

            def __deref__(self) -> 'freeling::depnode const *':
                return _pyfreeling.TreeConstPreorderIteratorDepnode___deref__self

            def incr(self) -> 'void':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_incrself

            def decr(self) -> 'void':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_decrself

            def __eq__(self, t: 'TreeConstPreorderIteratorDepnode') -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorDepnode___eq__(self, t)

            def __ne__(self, t: 'TreeConstPreorderIteratorDepnode') -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorDepnode___ne__(self, t)

            def get_info(self) -> 'freeling::depnode const *':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_get_infoself

            def is_defined(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_is_definedself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_emptyself

            def has_ancestor(self, p: 'TreeOfDepnode') -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_has_ancestor(self, p)

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_num_childrenself

            def get_parent(self) -> 'freeling::const_tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_get_parentself

            def nth_child(self, n: 'unsigned int') -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_nth_child(self, n)

            def nth_child_ref(self, n: 'unsigned int') -> 'freeling::tree< freeling::depnode > const &':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_nth_child_ref(self, n)

            def begin(self) -> 'freeling::const_tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_beginself

            def end(self) -> 'freeling::const_tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_endself

            def sibling_begin(self) -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_sibling_beginself

            def sibling_end(self) -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_sibling_endself

            def sibling_rbegin(self) -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_sibling_rbeginself

            def sibling_rend(self) -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_sibling_rendself

            def get_link(self, *args) -> 'freeling::parse_tree::const_iterator':
                return (_pyfreeling.TreeConstPreorderIteratorDepnode_get_link)(self, *args)

            def get_node_id(self) -> 'std::wstring':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_get_node_idself

            def get_label(self) -> 'std::wstring':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_get_labelself

            def has_word(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_has_wordself

            def get_word(self, *args) -> 'freeling::word const &':
                return (_pyfreeling.TreeConstPreorderIteratorDepnode_get_word)(self, *args)

            def is_head(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_is_headself

            def is_chunk(self) -> 'bool':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_is_chunkself

            def get_chunk_ord(self) -> 'int':
                return _pyfreeling.TreeConstPreorderIteratorDepnode_get_chunk_ordself


        TreeConstPreorderIteratorDepnode_swigregister = _pyfreeling.TreeConstPreorderIteratorDepnode_swigregister
        TreeConstPreorderIteratorDepnode_swigregister(TreeConstPreorderIteratorDepnode)

        class TreeConstSiblingIteratorDepnode(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, TreeConstSiblingIteratorDepnode, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, TreeConstSiblingIteratorDepnode, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_TreeConstSiblingIteratorDepnode)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_TreeConstSiblingIteratorDepnode
            __del__ = lambda self: None

            def __ref__(self) -> 'freeling::depnode const &':
                return _pyfreeling.TreeConstSiblingIteratorDepnode___ref__self

            def __deref__(self) -> 'freeling::depnode const *':
                return _pyfreeling.TreeConstSiblingIteratorDepnode___deref__self

            def incr(self) -> 'void':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_incrself

            def decr(self) -> 'void':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_decrself

            def __eq__(self, t: 'TreeConstSiblingIteratorDepnode') -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorDepnode___eq__(self, t)

            def __ne__(self, t: 'TreeConstSiblingIteratorDepnode') -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorDepnode___ne__(self, t)

            def get_info(self) -> 'freeling::depnode const *':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_get_infoself

            def is_defined(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_is_definedself

            def is_root(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_is_rootself

            def empty(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_emptyself

            def has_ancestor(self, p: 'TreeOfDepnode') -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_has_ancestor(self, p)

            def num_children(self) -> 'unsigned int':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_num_childrenself

            def get_parent(self) -> 'freeling::const_tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_get_parentself

            def nth_child(self, n: 'unsigned int') -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_nth_child(self, n)

            def nth_child_ref(self, n: 'unsigned int') -> 'freeling::tree< freeling::depnode > const &':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_nth_child_ref(self, n)

            def begin(self) -> 'freeling::const_tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_beginself

            def end(self) -> 'freeling::const_tree_preorder_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_endself

            def sibling_begin(self) -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_sibling_beginself

            def sibling_end(self) -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_sibling_endself

            def sibling_rbegin(self) -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_sibling_rbeginself

            def sibling_rend(self) -> 'freeling::const_tree_sibling_iterator< freeling::depnode >':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_sibling_rendself

            def get_link(self, *args) -> 'freeling::parse_tree::const_iterator':
                return (_pyfreeling.TreeConstSiblingIteratorDepnode_get_link)(self, *args)

            def get_node_id(self) -> 'std::wstring':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_get_node_idself

            def get_label(self) -> 'std::wstring':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_get_labelself

            def has_word(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_has_wordself

            def get_word(self, *args) -> 'freeling::word const &':
                return (_pyfreeling.TreeConstSiblingIteratorDepnode_get_word)(self, *args)

            def is_head(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_is_headself

            def is_chunk(self) -> 'bool':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_is_chunkself

            def get_chunk_ord(self) -> 'int':
                return _pyfreeling.TreeConstSiblingIteratorDepnode_get_chunk_ordself


        TreeConstSiblingIteratorDepnode_swigregister = _pyfreeling.TreeConstSiblingIteratorDepnode_swigregister
        TreeConstSiblingIteratorDepnode_swigregister(TreeConstSiblingIteratorDepnode)

        class analysis(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, analysis, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, analysis, name)
            __repr__ = _swig_repr
            __swig_setmethods__['user'] = _pyfreeling.analysis_user_set
            __swig_getmethods__['user'] = _pyfreeling.analysis_user_get
            if _newclass:
                user = _swig_property(_pyfreeling.analysis_user_get, _pyfreeling.analysis_user_set)

            def __init__(self, *args):
                this = (_pyfreeling.new_analysis)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_analysis
            __del__ = lambda self: None

            def init(self, l: 'std::wstring const &', t: 'std::wstring const &') -> 'void':
                return _pyfreeling.analysis_init(self, l, t)

            def set_lemma(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.analysis_set_lemma(self, arg2)

            def set_tag(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.analysis_set_tag(self, arg2)

            def set_prob(self, arg2: 'double') -> 'void':
                return _pyfreeling.analysis_set_prob(self, arg2)

            def set_distance(self, arg2: 'double') -> 'void':
                return _pyfreeling.analysis_set_distance(self, arg2)

            def set_retokenizable(self, arg2: 'ListWord') -> 'void':
                return _pyfreeling.analysis_set_retokenizable(self, arg2)

            def has_prob(self) -> 'bool':
                return _pyfreeling.analysis_has_probself

            def has_distance(self) -> 'bool':
                return _pyfreeling.analysis_has_distanceself

            def get_lemma(self) -> 'std::wstring':
                return _pyfreeling.analysis_get_lemmaself

            def get_tag(self) -> 'std::wstring':
                return _pyfreeling.analysis_get_tagself

            def get_prob(self) -> 'double':
                return _pyfreeling.analysis_get_probself

            def get_distance(self) -> 'double':
                return _pyfreeling.analysis_get_distanceself

            def is_retokenizable(self) -> 'bool':
                return _pyfreeling.analysis_is_retokenizableself

            def get_retokenizable(self) -> 'std::list< freeling::word,std::allocator< freeling::word > >':
                return _pyfreeling.analysis_get_retokenizableself

            def get_senses(self) -> 'std::list< std::pair< std::wstring,double >,std::allocator< std::pair< std::wstring,double > > >':
                return _pyfreeling.analysis_get_sensesself

            def set_senses(self, arg2: 'ListPairStringDouble') -> 'void':
                return _pyfreeling.analysis_set_senses(self, arg2)

            def get_senses_string(self) -> 'std::wstring':
                return _pyfreeling.analysis_get_senses_stringself

            def __gt__(self, arg2: 'analysis') -> 'bool':
                return _pyfreeling.analysis___gt__(self, arg2)

            def __lt__(self, arg2: 'analysis') -> 'bool':
                return _pyfreeling.analysis___lt__(self, arg2)

            def __eq__(self, arg2: 'analysis') -> 'bool':
                return _pyfreeling.analysis___eq__(self, arg2)

            def is_selected(self, k: 'int'=0) -> 'bool':
                return _pyfreeling.analysis_is_selected(self, k)

            def mark_selected(self, k: 'int'=0) -> 'void':
                return _pyfreeling.analysis_mark_selected(self, k)

            def unmark_selected(self, k: 'int'=0) -> 'void':
                return _pyfreeling.analysis_unmark_selected(self, k)


        analysis_swigregister = _pyfreeling.analysis_swigregister
        analysis_swigregister(analysis)

        class alternative(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, alternative, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, alternative, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_alternative)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def __eq__(self, arg2: 'alternative') -> 'bool':
                return _pyfreeling.alternative___eq__(self, arg2)

            def get_form(self) -> 'std::wstring':
                return _pyfreeling.alternative_get_formself

            def get_distance(self) -> 'int':
                return _pyfreeling.alternative_get_distanceself

            def get_probability(self) -> 'float':
                return _pyfreeling.alternative_get_probabilityself

            def is_selected(self, k: 'int'=1) -> 'bool':
                return _pyfreeling.alternative_is_selected(self, k)

            def clear_selections(self) -> 'void':
                return _pyfreeling.alternative_clear_selectionsself

            def add_selection(self, arg2: 'int') -> 'void':
                return _pyfreeling.alternative_add_selection(self, arg2)

            def set_form(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.alternative_set_form(self, arg2)

            def set_distance(self, arg2: 'int') -> 'void':
                return _pyfreeling.alternative_set_distance(self, arg2)

            def set_probability(self, arg2: 'float') -> 'void':
                return _pyfreeling.alternative_set_probability(self, arg2)

            __swig_destroy__ = _pyfreeling.delete_alternative
            __del__ = lambda self: None


        alternative_swigregister = _pyfreeling.alternative_swigregister
        alternative_swigregister(alternative)

        class word(ListAnalysis):
            __swig_setmethods__ = {}
            for _s in (
             ListAnalysis,):
                __swig_setmethods__.updategetattr(_s, '__swig_setmethods__', {})
            else:
                __setattr__ = lambda self, name, value: _swig_setattr(self, word, name, value)
                __swig_getmethods__ = {}
                for _s in (ListAnalysis,):
                    __swig_getmethods__.updategetattr(_s, '__swig_getmethods__', {})
                else:
                    __getattr__ = lambda self, name: _swig_getattr(self, word, name)
                    __repr__ = _swig_repr
                    USERMAP = _pyfreeling.word_USERMAP
                    NUMBERS = _pyfreeling.word_NUMBERS
                    PUNCTUATION = _pyfreeling.word_PUNCTUATION
                    DATES = _pyfreeling.word_DATES
                    DICTIONARY = _pyfreeling.word_DICTIONARY
                    AFFIXES = _pyfreeling.word_AFFIXES
                    COMPOUNDS = _pyfreeling.word_COMPOUNDS
                    MULTIWORDS = _pyfreeling.word_MULTIWORDS
                    NER = _pyfreeling.word_NER
                    QUANTITIES = _pyfreeling.word_QUANTITIES
                    PROBABILITIES = _pyfreeling.word_PROBABILITIES
                    GUESSER = _pyfreeling.word_GUESSER
                    __swig_setmethods__['user'] = _pyfreeling.word_user_set
                    __swig_getmethods__['user'] = _pyfreeling.word_user_get
                    if _newclass:
                        user = _swig_property(_pyfreeling.word_user_get, _pyfreeling.word_user_set)

                    def __init__(self, *args):
                        this = (_pyfreeling.new_word)(*args)
                        try:
                            self.this.appendthis
                        except __builtin__.Exception:
                            self.this = this

                    __swig_destroy__ = _pyfreeling.delete_word
                    __del__ = lambda self: None

                    def copy_analysis(self, arg2: 'word') -> 'void':
                        return _pyfreeling.word_copy_analysis(self, arg2)

                    def get_n_selected(self) -> 'int':
                        return _pyfreeling.word_get_n_selectedself

                    def get_n_unselected(self) -> 'int':
                        return _pyfreeling.word_get_n_unselectedself

                    def is_multiword(self) -> 'bool':
                        return _pyfreeling.word_is_multiwordself

                    def is_ambiguous_mw(self) -> 'bool':
                        return _pyfreeling.word_is_ambiguous_mwself

                    def set_ambiguous_mw(self, arg2: 'bool') -> 'void':
                        return _pyfreeling.word_set_ambiguous_mw(self, arg2)

                    def get_n_words_mw(self) -> 'int':
                        return _pyfreeling.word_get_n_words_mwself

                    def get_words_mw(self) -> 'std::list< freeling::word,std::allocator< freeling::word > > const &':
                        return _pyfreeling.word_get_words_mwself

                    def get_form(self) -> 'std::wstring':
                        return _pyfreeling.word_get_formself

                    def get_lc_form(self) -> 'std::wstring':
                        return _pyfreeling.word_get_lc_formself

                    def get_ph_form(self) -> 'std::wstring':
                        return _pyfreeling.word_get_ph_formself

                    def selected_begin(self, *args) -> 'freeling::word::const_iterator':
                        return (_pyfreeling.word_selected_begin)(self, *args)

                    def selected_end(self, *args) -> 'freeling::word::const_iterator':
                        return (_pyfreeling.word_selected_end)(self, *args)

                    def unselected_begin(self, *args) -> 'freeling::word::const_iterator':
                        return (_pyfreeling.word_unselected_begin)(self, *args)

                    def unselected_end(self, *args) -> 'freeling::word::const_iterator':
                        return (_pyfreeling.word_unselected_end)(self, *args)

                    def num_kbest(self) -> 'unsigned int':
                        return _pyfreeling.word_num_kbestself

                    def get_lemma(self, k: 'int'=0) -> 'std::wstring':
                        return _pyfreeling.word_get_lemma(self, k)

                    def get_tag(self, k: 'int'=0) -> 'std::wstring':
                        return _pyfreeling.word_get_tag(self, k)

                    def get_senses(self, k: 'int'=0) -> 'std::list< std::pair< std::wstring,double >,std::allocator< std::pair< std::wstring,double > > >':
                        return _pyfreeling.word_get_senses(self, k)

                    def get_senses_string(self, k: 'int'=0) -> 'std::wstring':
                        return _pyfreeling.word_get_senses_string(self, k)

                    def set_senses(self, arg2: 'ListPairStringDouble', k: 'int'=0) -> 'void':
                        return _pyfreeling.word_set_senses(self, arg2, k)

                    def get_span_start(self) -> 'unsigned long':
                        return _pyfreeling.word_get_span_startself

                    def get_span_finish(self) -> 'unsigned long':
                        return _pyfreeling.word_get_span_finishself

                    def has_retokenizable(self) -> 'bool':
                        return _pyfreeling.word_has_retokenizableself

                    def lock_analysis(self) -> 'void':
                        return _pyfreeling.word_lock_analysisself

                    def unlock_analysis(self) -> 'void':
                        return _pyfreeling.word_unlock_analysisself

                    def is_locked_analysis(self) -> 'bool':
                        return _pyfreeling.word_is_locked_analysisself

                    def lock_multiwords(self) -> 'void':
                        return _pyfreeling.word_lock_multiwordsself

                    def unlock_multiwords(self) -> 'void':
                        return _pyfreeling.word_unlock_multiwordsself

                    def is_locked_multiwords(self) -> 'bool':
                        return _pyfreeling.word_is_locked_multiwordsself

                    def set_analyzed_by(self, arg2: 'unsigned int') -> 'void':
                        return _pyfreeling.word_set_analyzed_by(self, arg2)

                    def is_analyzed_by(self, arg2: 'unsigned int') -> 'bool':
                        return _pyfreeling.word_is_analyzed_by(self, arg2)

                    def get_analyzed_by(self) -> 'unsigned int':
                        return _pyfreeling.word_get_analyzed_byself

                    def add_alternative(self, *args) -> 'void':
                        return (_pyfreeling.word_add_alternative)(self, *args)

                    def set_alternatives(self, arg2: 'std::list< std::pair< std::wstring,int >,std::allocator< std::pair< std::wstring,int > > > const &') -> 'void':
                        return _pyfreeling.word_set_alternatives(self, arg2)

                    def clear_alternatives(self) -> 'void':
                        return _pyfreeling.word_clear_alternativesself

                    def has_alternatives(self) -> 'bool':
                        return _pyfreeling.word_has_alternativesself

                    def get_alternatives(self, *args) -> 'std::list< freeling::alternative,std::allocator< freeling::alternative > > const &':
                        return (_pyfreeling.word_get_alternatives)(self, *args)

                    def alternatives_begin(self, *args) -> 'std::list< freeling::alternative,std::allocator< freeling::alternative > >::const_iterator':
                        return (_pyfreeling.word_alternatives_begin)(self, *args)

                    def alternatives_end(self, *args) -> 'std::list< freeling::alternative,std::allocator< freeling::alternative > >::const_iterator':
                        return (_pyfreeling.word_alternatives_end)(self, *args)

                    def add_analysis(self, arg2: 'analysis') -> 'void':
                        return _pyfreeling.word_add_analysis(self, arg2)

                    def set_analysis(self, *args) -> 'void':
                        return (_pyfreeling.word_set_analysis)(self, *args)

                    def set_form(self, arg2: 'std::wstring const &') -> 'void':
                        return _pyfreeling.word_set_form(self, arg2)

                    def set_ph_form(self, arg2: 'std::wstring const &') -> 'void':
                        return _pyfreeling.word_set_ph_form(self, arg2)

                    def set_span(self, arg2: 'unsigned long', arg3: 'unsigned long') -> 'void':
                        return _pyfreeling.word_set_span(self, arg2, arg3)

                    def set_position(self, arg2: 'size_t') -> 'void':
                        return _pyfreeling.word_set_position(self, arg2)

                    def get_position(self) -> 'size_t':
                        return _pyfreeling.word_get_positionself

                    def find_tag_match(self, arg2: 'freeling::regexp &') -> 'bool':
                        return _pyfreeling.word_find_tag_match(self, arg2)

                    def get_n_analysis(self) -> 'int':
                        return _pyfreeling.word_get_n_analysisself

                    def unselect_all_analysis(self, k: 'int'=0) -> 'void':
                        return _pyfreeling.word_unselect_all_analysis(self, k)

                    def select_all_analysis(self, k: 'int'=0) -> 'void':
                        return _pyfreeling.word_select_all_analysis(self, k)

                    def select_analysis(self, arg2: 'freeling::word::iterator', k: 'int'=0) -> 'void':
                        return _pyfreeling.word_select_analysis(self, arg2, k)

                    def unselect_analysis(self, arg2: 'freeling::word::iterator', k: 'int'=0) -> 'void':
                        return _pyfreeling.word_unselect_analysis(self, arg2, k)

                    def get_analysis(self) -> 'std::list< freeling::analysis,std::allocator< freeling::analysis > >':
                        return _pyfreeling.word_get_analysisself

                    def analysis_begin(self, *args) -> 'freeling::word::const_iterator':
                        return (_pyfreeling.word_analysis_begin)(self, *args)

                    def analysis_end(self, *args) -> 'freeling::word::const_iterator':
                        return (_pyfreeling.word_analysis_end)(self, *args)


        word_swigregister = _pyfreeling.word_swigregister
        word_swigregister(word)

        class node(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, node, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, node, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_node)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_node
            __del__ = lambda self: None

            def get_node_id(self) -> 'std::wstring':
                return _pyfreeling.node_get_node_idself

            def set_node_id(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.node_set_node_id(self, arg2)

            def get_label(self) -> 'std::wstring':
                return _pyfreeling.node_get_labelself

            def has_word(self) -> 'bool':
                return _pyfreeling.node_has_wordself

            def get_word(self, *args) -> 'freeling::word const &':
                return (_pyfreeling.node_get_word)(self, *args)

            def set_label(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.node_set_label(self, arg2)

            def set_word(self, arg2: 'word') -> 'void':
                return _pyfreeling.node_set_word(self, arg2)

            def is_head(self) -> 'bool':
                return _pyfreeling.node_is_headself

            def set_head(self, arg2: 'bool const') -> 'void':
                return _pyfreeling.node_set_head(self, arg2)

            def is_chunk(self) -> 'bool':
                return _pyfreeling.node_is_chunkself

            def set_chunk(self, arg2: 'int const') -> 'void':
                return _pyfreeling.node_set_chunk(self, arg2)

            def get_chunk_ord(self) -> 'int':
                return _pyfreeling.node_get_chunk_ordself


        node_swigregister = _pyfreeling.node_swigregister
        node_swigregister(node)

        class parse_tree(TreeOfNode):
            __swig_setmethods__ = {}
            for _s in (
             TreeOfNode,):
                __swig_setmethods__.updategetattr(_s, '__swig_setmethods__', {})
            else:
                __setattr__ = lambda self, name, value: _swig_setattr(self, parse_tree, name, value)
                __swig_getmethods__ = {}
                for _s in (TreeOfNode,):
                    __swig_getmethods__.updategetattr(_s, '__swig_getmethods__', {})
                else:
                    __getattr__ = lambda self, name: _swig_getattr(self, parse_tree, name)
                    __repr__ = _swig_repr

                    def __init__(self, *args):
                        this = (_pyfreeling.new_parse_tree)(*args)
                        try:
                            self.this.appendthis
                        except __builtin__.Exception:
                            self.this = this

                    def build_node_index(self, arg2: 'std::wstring const &') -> 'void':
                        return _pyfreeling.parse_tree_build_node_index(self, arg2)

                    def rebuild_node_index(self) -> 'void':
                        return _pyfreeling.parse_tree_rebuild_node_indexself

                    def get_node_by_id(self, *args) -> 'freeling::parse_tree::const_iterator':
                        return (_pyfreeling.parse_tree_get_node_by_id)(self, *args)

                    def get_node_by_pos(self, *args) -> 'freeling::parse_tree::const_iterator':
                        return (_pyfreeling.parse_tree_get_node_by_pos)(self, *args)

                    if _newclass:
                        get_head_word = staticmethod(_pyfreeling.parse_tree_get_head_word)
                    else:
                        get_head_word = _pyfreeling.parse_tree_get_head_word
                    if _newclass:
                        get_head_position = staticmethod(_pyfreeling.parse_tree_get_head_position)
                    else:
                        get_head_position = _pyfreeling.parse_tree_get_head_position
                    if _newclass:
                        C_commands = staticmethod(_pyfreeling.parse_tree_C_commands)
                    else:
                        C_commands = _pyfreeling.parse_tree_C_commands

                    def nth_child_ref(self, arg2: 'unsigned int') -> 'freeling::parse_tree &':
                        return _pyfreeling.parse_tree_nth_child_ref(self, arg2)

                    __swig_destroy__ = _pyfreeling.delete_parse_tree
                    __del__ = lambda self: None


        parse_tree_swigregister = _pyfreeling.parse_tree_swigregister
        parse_tree_swigregister(parse_tree)

        def parse_tree_get_head_word(arg2: 'TreeConstPreorderIteratorNode') -> 'freeling::word const &':
            return _pyfreeling.parse_tree_get_head_wordarg2


        parse_tree_get_head_word = _pyfreeling.parse_tree_get_head_word

        def parse_tree_get_head_position(pt: 'TreeConstPreorderIteratorNode') -> 'int':
            return _pyfreeling.parse_tree_get_head_positionpt


        parse_tree_get_head_position = _pyfreeling.parse_tree_get_head_position

        def parse_tree_C_commands(arg2: 'TreeConstPreorderIteratorNode', arg3: 'TreeConstPreorderIteratorNode') -> 'bool':
            return _pyfreeling.parse_tree_C_commands(arg2, arg3)


        parse_tree_C_commands = _pyfreeling.parse_tree_C_commands

        class depnode(node):
            __swig_setmethods__ = {}
            for _s in (
             node,):
                __swig_setmethods__.updategetattr(_s, '__swig_setmethods__', {})
            else:
                __setattr__ = lambda self, name, value: _swig_setattr(self, depnode, name, value)
                __swig_getmethods__ = {}
                for _s in (node,):
                    __swig_getmethods__.updategetattr(_s, '__swig_getmethods__', {})
                else:
                    __getattr__ = lambda self, name: _swig_getattr(self, depnode, name)
                    __repr__ = _swig_repr

                    def __init__(self, *args):
                        this = (_pyfreeling.new_depnode)(*args)
                        try:
                            self.this.appendthis
                        except __builtin__.Exception:
                            self.this = this

                    __swig_destroy__ = _pyfreeling.delete_depnode
                    __del__ = lambda self: None

                    def set_link(self, arg2: 'TreePreorderIteratorNode') -> 'void':
                        return _pyfreeling.depnode_set_link(self, arg2)

                    def get_link(self, *args) -> 'freeling::parse_tree::const_iterator':
                        return (_pyfreeling.depnode_get_link)(self, *args)


        depnode_swigregister = _pyfreeling.depnode_swigregister
        depnode_swigregister(depnode)

        class dep_tree(TreeOfDepnode):
            __swig_setmethods__ = {}
            for _s in (
             TreeOfDepnode,):
                __swig_setmethods__.updategetattr(_s, '__swig_setmethods__', {})
            else:
                __setattr__ = lambda self, name, value: _swig_setattr(self, dep_tree, name, value)
                __swig_getmethods__ = {}
                for _s in (TreeOfDepnode,):
                    __swig_getmethods__.updategetattr(_s, '__swig_getmethods__', {})
                else:
                    __getattr__ = lambda self, name: _swig_getattr(self, dep_tree, name)
                    __repr__ = _swig_repr

                    def __init__(self, *args):
                        this = (_pyfreeling.new_dep_tree)(*args)
                        try:
                            self.this.appendthis
                        except __builtin__.Exception:
                            self.this = this

                    def get_node_by_pos(self, *args) -> 'freeling::dep_tree::const_iterator':
                        return (_pyfreeling.dep_tree_get_node_by_pos)(self, *args)

                    def rebuild_node_index(self) -> 'void':
                        return _pyfreeling.dep_tree_rebuild_node_indexself

                    if _newclass:
                        get_first_word = staticmethod(_pyfreeling.dep_tree_get_first_word)
                    else:
                        get_first_word = _pyfreeling.dep_tree_get_first_word
                    if _newclass:
                        get_last_word = staticmethod(_pyfreeling.dep_tree_get_last_word)
                    else:
                        get_last_word = _pyfreeling.dep_tree_get_last_word

                    def nth_child_ref(self, arg2: 'unsigned int') -> 'freeling::dep_tree &':
                        return _pyfreeling.dep_tree_nth_child_ref(self, arg2)

                    __swig_destroy__ = _pyfreeling.delete_dep_tree
                    __del__ = lambda self: None


        dep_tree_swigregister = _pyfreeling.dep_tree_swigregister
        dep_tree_swigregister(dep_tree)

        def dep_tree_get_first_word(arg2: 'TreeConstPreorderIteratorDepnode') -> 'size_t':
            return _pyfreeling.dep_tree_get_first_wordarg2


        dep_tree_get_first_word = _pyfreeling.dep_tree_get_first_word

        def dep_tree_get_last_word(arg2: 'TreeConstPreorderIteratorDepnode') -> 'size_t':
            return _pyfreeling.dep_tree_get_last_wordarg2


        dep_tree_get_last_word = _pyfreeling.dep_tree_get_last_word

        class argument(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, argument, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, argument, name)
            __repr__ = _swig_repr
            __swig_destroy__ = _pyfreeling.delete_argument
            __del__ = lambda self: None

            def __init__(self, *args):
                this = (_pyfreeling.new_argument)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def get_position(self) -> 'int':
                return _pyfreeling.argument_get_positionself

            def get_role(self) -> 'std::wstring':
                return _pyfreeling.argument_get_roleself


        argument_swigregister = _pyfreeling.argument_swigregister
        argument_swigregister(argument)
        cvar = _pyfreeling.cvar
        argument.EMPTY_ROLE = _pyfreeling.cvar.argument_EMPTY_ROLE

        class predicate(VectorArgument):
            __swig_setmethods__ = {}
            for _s in (
             VectorArgument,):
                __swig_setmethods__.updategetattr(_s, '__swig_setmethods__', {})
            else:
                __setattr__ = lambda self, name, value: _swig_setattr(self, predicate, name, value)
                __swig_getmethods__ = {}
                for _s in (VectorArgument,):
                    __swig_getmethods__.updategetattr(_s, '__swig_getmethods__', {})
                else:
                    __getattr__ = lambda self, name: _swig_getattr(self, predicate, name)
                    __repr__ = _swig_repr
                    __swig_destroy__ = _pyfreeling.delete_predicate
                    __del__ = lambda self: None

                    def __init__(self, *args):
                        this = (_pyfreeling.new_predicate)(*args)
                        try:
                            self.this.appendthis
                        except __builtin__.Exception:
                            self.this = this

                    def get_sense(self) -> 'std::wstring':
                        return _pyfreeling.predicate_get_senseself

                    def get_position(self) -> 'int':
                        return _pyfreeling.predicate_get_positionself

                    def has_argument(self, p: 'int') -> 'bool':
                        return _pyfreeling.predicate_has_argument(self, p)

                    def add_argument(self, p: 'int', r: 'std::wstring const &') -> 'void':
                        return _pyfreeling.predicate_add_argument(self, p, r)

                    def get_argument_by_pos(self, p: 'int') -> 'freeling::argument const &':
                        return _pyfreeling.predicate_get_argument_by_pos(self, p)


        predicate_swigregister = _pyfreeling.predicate_swigregister
        predicate_swigregister(predicate)

        class sentence(ListWord):
            __swig_setmethods__ = {}
            for _s in (
             ListWord,):
                __swig_setmethods__.updategetattr(_s, '__swig_setmethods__', {})
            else:
                __setattr__ = lambda self, name, value: _swig_setattr(self, sentence, name, value)
                __swig_getmethods__ = {}
                for _s in (ListWord,):
                    __swig_getmethods__.updategetattr(_s, '__swig_getmethods__', {})
                else:
                    __getattr__ = lambda self, name: _swig_getattr(self, sentence, name)
                    __repr__ = _swig_repr

                    def __init__(self, *args):
                        this = (_pyfreeling.new_sentence)(*args)
                        try:
                            self.this.appendthis
                        except __builtin__.Exception:
                            self.this = this

                    __swig_destroy__ = _pyfreeling.delete_sentence
                    __del__ = lambda self: None

                    def num_kbest(self) -> 'unsigned int':
                        return _pyfreeling.sentence_num_kbestself

                    def push_back(self, arg2: 'word') -> 'void':
                        return _pyfreeling.sentence_push_back(self, arg2)

                    def rebuild_word_index(self) -> 'void':
                        return _pyfreeling.sentence_rebuild_word_indexself

                    def clear(self) -> 'void':
                        return _pyfreeling.sentence_clearself

                    def set_sentence_id(self, arg2: 'std::wstring const &') -> 'void':
                        return _pyfreeling.sentence_set_sentence_id(self, arg2)

                    def get_sentence_id(self) -> 'std::wstring':
                        return _pyfreeling.sentence_get_sentence_idself

                    def set_is_tagged(self, arg2: 'bool') -> 'void':
                        return _pyfreeling.sentence_set_is_tagged(self, arg2)

                    def is_tagged(self) -> 'bool':
                        return _pyfreeling.sentence_is_taggedself

                    def set_best_seq(self, k: 'int') -> 'void':
                        return _pyfreeling.sentence_set_best_seq(self, k)

                    def get_best_seq(self) -> 'int':
                        return _pyfreeling.sentence_get_best_seqself

                    def set_parse_tree(self, arg2: 'parse_tree', k: 'int'=0) -> 'void':
                        return _pyfreeling.sentence_set_parse_tree(self, arg2, k)

                    def get_parse_tree(self, *args) -> 'freeling::parse_tree const &':
                        return (_pyfreeling.sentence_get_parse_tree)(self, *args)

                    def is_parsed(self) -> 'bool':
                        return _pyfreeling.sentence_is_parsedself

                    def set_dep_tree(self, arg2: 'dep_tree', k: 'int'=0) -> 'void':
                        return _pyfreeling.sentence_set_dep_tree(self, arg2, k)

                    def get_dep_tree(self, *args) -> 'freeling::dep_tree const &':
                        return (_pyfreeling.sentence_get_dep_tree)(self, *args)

                    def is_dep_parsed(self) -> 'bool':
                        return _pyfreeling.sentence_is_dep_parsedself

                    def get_words(self) -> 'std::vector< freeling::word,std::allocator< freeling::word > >':
                        return _pyfreeling.sentence_get_wordsself

                    def words_begin(self, *args) -> 'freeling::sentence::const_iterator':
                        return (_pyfreeling.sentence_words_begin)(self, *args)

                    def words_end(self, *args) -> 'freeling::sentence::const_iterator':
                        return (_pyfreeling.sentence_words_end)(self, *args)

                    def get_word_iterator(self, *args) -> 'freeling::sentence::iterator':
                        return (_pyfreeling.sentence_get_word_iterator)(self, *args)

                    def add_predicate(self, pr: 'predicate') -> 'void':
                        return _pyfreeling.sentence_add_predicate(self, pr)

                    def is_predicate(self, p: 'int') -> 'bool':
                        return _pyfreeling.sentence_is_predicate(self, p)

                    def get_predicate_number(self, p: 'int') -> 'int':
                        return _pyfreeling.sentence_get_predicate_number(self, p)

                    def get_predicate_position(self, n: 'int') -> 'int':
                        return _pyfreeling.sentence_get_predicate_position(self, n)

                    def get_predicate_by_pos(self, n: 'int') -> 'freeling::predicate const &':
                        return _pyfreeling.sentence_get_predicate_by_pos(self, n)

                    def get_predicate_by_number(self, n: 'int') -> 'freeling::predicate const &':
                        return _pyfreeling.sentence_get_predicate_by_number(self, n)

                    def get_predicates(self) -> 'freeling::sentence::predicates const &':
                        return _pyfreeling.sentence_get_predicatesself


        sentence_swigregister = _pyfreeling.sentence_swigregister
        sentence_swigregister(sentence)

        class paragraph(ListSentence):
            __swig_setmethods__ = {}
            for _s in (
             ListSentence,):
                __swig_setmethods__.updategetattr(_s, '__swig_setmethods__', {})
            else:
                __setattr__ = lambda self, name, value: _swig_setattr(self, paragraph, name, value)
                __swig_getmethods__ = {}
                for _s in (ListSentence,):
                    __swig_getmethods__.updategetattr(_s, '__swig_getmethods__', {})
                else:
                    __getattr__ = lambda self, name: _swig_getattr(self, paragraph, name)
                    __repr__ = _swig_repr

                    def __init__(self, *args):
                        this = (_pyfreeling.new_paragraph)(*args)
                        try:
                            self.this.appendthis
                        except __builtin__.Exception:
                            self.this = this

                    def set_paragraph_id(self, arg2: 'std::wstring const &') -> 'void':
                        return _pyfreeling.paragraph_set_paragraph_id(self, arg2)

                    def get_paragraph_id(self) -> 'std::wstring':
                        return _pyfreeling.paragraph_get_paragraph_idself

                    __swig_destroy__ = _pyfreeling.delete_paragraph
                    __del__ = lambda self: None


        paragraph_swigregister = _pyfreeling.paragraph_swigregister
        paragraph_swigregister(paragraph)

        class mention(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, mention, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, mention, name)
            __repr__ = _swig_repr
            PROPER_NOUN = _pyfreeling.mention_PROPER_NOUN
            PRONOUN = _pyfreeling.mention_PRONOUN
            NOUN_PHRASE = _pyfreeling.mention_NOUN_PHRASE
            COMPOSITE = _pyfreeling.mention_COMPOSITE
            VERB_PHRASE = _pyfreeling.mention_VERB_PHRASE
            PER = _pyfreeling.mention_PER
            MALE = _pyfreeling.mention_MALE
            FEMALE = _pyfreeling.mention_FEMALE
            NOTPER = _pyfreeling.mention_NOTPER
            ORG = _pyfreeling.mention_ORG
            GEO = _pyfreeling.mention_GEO
            OTHER = _pyfreeling.mention_OTHER

            def __init__(self, *args):
                this = (_pyfreeling.new_mention)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def __lt__(self, m: 'mention') -> 'bool':
                return _pyfreeling.mention___lt__(self, m)

            def set_id(self, arg2: 'int') -> 'void':
                return _pyfreeling.mention_set_id(self, arg2)

            def set_type(self, arg2: 'freeling::mention::mentionType') -> 'void':
                return _pyfreeling.mention_set_type(self, arg2)

            def set_initial(self, arg2: 'bool') -> 'void':
                return _pyfreeling.mention_set_initial(self, arg2)

            def set_group(self, arg2: 'int') -> 'void':
                return _pyfreeling.mention_set_group(self, arg2)

            def set_maximal(self, b: 'bool') -> 'void':
                return _pyfreeling.mention_set_maximal(self, b)

            def get_id(self) -> 'int':
                return _pyfreeling.mention_get_idself

            def get_n_sentence(self) -> 'int':
                return _pyfreeling.mention_get_n_sentenceself

            def get_sentence(self) -> 'freeling::paragraph::const_iterator':
                return _pyfreeling.mention_get_sentenceself

            def get_pos_begin(self) -> 'int':
                return _pyfreeling.mention_get_pos_beginself

            def get_pos_end(self) -> 'int':
                return _pyfreeling.mention_get_pos_endself

            def get_it_begin(self) -> 'freeling::sentence::const_iterator':
                return _pyfreeling.mention_get_it_beginself

            def get_it_end(self) -> 'freeling::sentence::const_iterator':
                return _pyfreeling.mention_get_it_endself

            def get_it_head(self) -> 'freeling::sentence::const_iterator':
                return _pyfreeling.mention_get_it_headself

            def get_type(self) -> 'freeling::mention::mentionType':
                return _pyfreeling.mention_get_typeself

            def get_group(self) -> 'int':
                return _pyfreeling.mention_get_groupself

            def is_type(self, arg2: 'freeling::mention::mentionType') -> 'bool':
                return _pyfreeling.mention_is_type(self, arg2)

            def is_initial(self) -> 'bool':
                return _pyfreeling.mention_is_initialself

            def is_maximal(self) -> 'bool':
                return _pyfreeling.mention_is_maximalself

            def get_ptree(self) -> 'freeling::parse_tree::const_iterator':
                return _pyfreeling.mention_get_ptreeself

            def get_head(self) -> 'freeling::word const &':
                return _pyfreeling.mention_get_headself

            def value(self) -> 'std::wstring':
                return _pyfreeling.mention_valueself

            __swig_destroy__ = _pyfreeling.delete_mention
            __del__ = lambda self: None


        mention_swigregister = _pyfreeling.mention_swigregister
        mention_swigregister(mention)

        class SG_mention(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, SG_mention, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, SG_mention, name)
            __repr__ = _swig_repr

            def __init__(self, mid: 'std::wstring const &', sid: 'std::wstring const &', wds: 'ListString'):
                this = _pyfreeling.new_SG_mention(mid, sid, wds)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_SG_mention
            __del__ = lambda self: None

            def get_id(self) -> 'std::wstring':
                return _pyfreeling.SG_mention_get_idself

            def get_sentence_id(self) -> 'std::wstring':
                return _pyfreeling.SG_mention_get_sentence_idself

            def get_words(self) -> 'std::list< std::wstring,std::allocator< std::wstring > > const &':
                return _pyfreeling.SG_mention_get_wordsself


        SG_mention_swigregister = _pyfreeling.SG_mention_swigregister
        SG_mention_swigregister(SG_mention)
        ENTITY = _pyfreeling.ENTITY
        WORD = _pyfreeling.WORD

        class SG_entity(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, SG_entity, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, SG_entity, name)
            __repr__ = _swig_repr

            def __init__(self, elemma: 'std::wstring const &', eclass: 'std::wstring const &', type: 'freeling::semgraph::entityType', sense: 'std::wstring const &'):
                this = _pyfreeling.new_SG_entity(elemma, eclass, type, sense)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_SG_entity
            __del__ = lambda self: None

            def set_lemma(self, lem: 'std::wstring const &') -> 'void':
                return _pyfreeling.SG_entity_set_lemma(self, lem)

            def get_id(self) -> 'std::wstring':
                return _pyfreeling.SG_entity_get_idself

            def get_lemma(self) -> 'std::wstring':
                return _pyfreeling.SG_entity_get_lemmaself

            def get_semclass(self) -> 'std::wstring':
                return _pyfreeling.SG_entity_get_semclassself

            def get_type(self) -> 'freeling::semgraph::entityType':
                return _pyfreeling.SG_entity_get_typeself

            def get_sense(self) -> 'std::wstring':
                return _pyfreeling.SG_entity_get_senseself

            def get_mentions(self) -> 'std::vector< freeling::semgraph::SG_mention,std::allocator< freeling::semgraph::SG_mention > > const &':
                return _pyfreeling.SG_entity_get_mentionsself


        SG_entity_swigregister = _pyfreeling.SG_entity_swigregister
        SG_entity_swigregister(SG_entity)

        class SG_argument(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, SG_argument, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, SG_argument, name)
            __repr__ = _swig_repr

            def __init__(self, r: 'std::wstring const &', e: 'std::wstring const &'):
                this = _pyfreeling.new_SG_argument(r, e)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_SG_argument
            __del__ = lambda self: None

            def get_role(self) -> 'std::wstring':
                return _pyfreeling.SG_argument_get_roleself

            def get_entity(self) -> 'std::wstring':
                return _pyfreeling.SG_argument_get_entityself


        SG_argument_swigregister = _pyfreeling.SG_argument_swigregister
        SG_argument_swigregister(SG_argument)

        class SG_frame(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, SG_frame, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, SG_frame, name)
            __repr__ = _swig_repr

            def __init__(self, lem: 'std::wstring const &', sns: 'std::wstring const &', tk: 'std::wstring const &', sid: 'std::wstring const &'):
                this = _pyfreeling.new_SG_frame(lem, sns, tk, sid)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_SG_frame
            __del__ = lambda self: None

            def get_id(self) -> 'std::wstring':
                return _pyfreeling.SG_frame_get_idself

            def get_lemma(self) -> 'std::wstring':
                return _pyfreeling.SG_frame_get_lemmaself

            def get_sense(self) -> 'std::wstring':
                return _pyfreeling.SG_frame_get_senseself

            def get_token_id(self) -> 'std::wstring':
                return _pyfreeling.SG_frame_get_token_idself

            def get_sentence_id(self) -> 'std::wstring':
                return _pyfreeling.SG_frame_get_sentence_idself

            def get_arguments(self) -> 'std::vector< freeling::semgraph::SG_argument,std::allocator< freeling::semgraph::SG_argument > > const &':
                return _pyfreeling.SG_frame_get_argumentsself


        SG_frame_swigregister = _pyfreeling.SG_frame_swigregister
        SG_frame_swigregister(SG_frame)

        class semantic_graph(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, semantic_graph, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, semantic_graph, name)
            __repr__ = _swig_repr

            def __init__(self):
                this = _pyfreeling.new_semantic_graph()
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_semantic_graph
            __del__ = lambda self: None

            def add_entity(self, ent: 'SG_entity') -> 'std::wstring':
                return _pyfreeling.semantic_graph_add_entity(self, ent)

            def add_frame(self, fr: 'SG_frame') -> 'std::wstring':
                return _pyfreeling.semantic_graph_add_frame(self, fr)

            def get_frame(self, *args) -> 'freeling::semgraph::SG_frame &':
                return (_pyfreeling.semantic_graph_get_frame)(self, *args)

            def get_entity_id_by_mention(self, sid: 'std::wstring const &', wid: 'std::wstring const &') -> 'std::wstring':
                return _pyfreeling.semantic_graph_get_entity_id_by_mention(self, sid, wid)

            def get_entity_id_by_lemma(self, lemma: 'std::wstring const &', sens: 'std::wstring const &') -> 'std::wstring':
                return _pyfreeling.semantic_graph_get_entity_id_by_lemma(self, lemma, sens)

            def get_entity(self, *args) -> 'freeling::semgraph::SG_entity &':
                return (_pyfreeling.semantic_graph_get_entity)(self, *args)

            def get_entities(self, *args) -> 'std::vector< freeling::semgraph::SG_entity,std::allocator< freeling::semgraph::SG_entity > > &':
                return (_pyfreeling.semantic_graph_get_entities)(self, *args)

            def get_frames(self, *args) -> 'std::vector< freeling::semgraph::SG_frame,std::allocator< freeling::semgraph::SG_frame > > &':
                return (_pyfreeling.semantic_graph_get_frames)(self, *args)

            def add_mention_to_entity(self, eid: 'std::wstring const &', m: 'SG_mention') -> 'void':
                return _pyfreeling.semantic_graph_add_mention_to_entity(self, eid, m)

            def add_argument_to_frame(self, fid: 'std::wstring const &', role: 'std::wstring const &', eid: 'std::wstring const &') -> 'void':
                return _pyfreeling.semantic_graph_add_argument_to_frame(self, fid, role, eid)

            def is_argument(self, eid: 'std::wstring const &') -> 'bool':
                return _pyfreeling.semantic_graph_is_argument(self, eid)

            def has_arguments(self, fid: 'std::wstring const &') -> 'bool':
                return _pyfreeling.semantic_graph_has_arguments(self, fid)

            def empty(self) -> 'bool':
                return _pyfreeling.semantic_graph_emptyself


        semantic_graph_swigregister = _pyfreeling.semantic_graph_swigregister
        semantic_graph_swigregister(semantic_graph)

        class document(ListParagraph):
            __swig_setmethods__ = {}
            for _s in (
             ListParagraph,):
                __swig_setmethods__.updategetattr(_s, '__swig_setmethods__', {})
            else:
                __setattr__ = lambda self, name, value: _swig_setattr(self, document, name, value)
                __swig_getmethods__ = {}
                for _s in (ListParagraph,):
                    __swig_getmethods__.updategetattr(_s, '__swig_getmethods__', {})
                else:
                    __getattr__ = lambda self, name: _swig_getattr(self, document, name)
                    __repr__ = _swig_repr

                    def __init__(self, *args):
                        this = (_pyfreeling.new_document)(*args)
                        try:
                            self.this.appendthis
                        except __builtin__.Exception:
                            self.this = this

                    def is_parsed(self) -> 'bool':
                        return _pyfreeling.document_is_parsedself

                    def is_dep_parsed(self) -> 'bool':
                        return _pyfreeling.document_is_dep_parsedself

                    def add_mention(self, m: 'mention') -> 'void':
                        return _pyfreeling.document_add_mention(self, m)

                    def get_num_words(self) -> 'int':
                        return _pyfreeling.document_get_num_wordsself

                    def get_num_groups(self) -> 'int':
                        return _pyfreeling.document_get_num_groupsself

                    def get_groups(self) -> 'std::list< int,std::allocator< int > > const &':
                        return _pyfreeling.document_get_groupsself

                    def begin_mentions(self, *args) -> 'std::vector< freeling::mention,std::allocator< freeling::mention > >::const_iterator':
                        return (_pyfreeling.document_begin_mentions)(self, *args)

                    def end_mentions(self, *args) -> 'std::vector< freeling::mention,std::allocator< freeling::mention > >::const_iterator':
                        return (_pyfreeling.document_end_mentions)(self, *args)

                    def get_semantic_graph(self, *args) -> 'freeling::semgraph::semantic_graph &':
                        return (_pyfreeling.document_get_semantic_graph)(self, *args)

                    def get_mention(self, arg2: 'int') -> 'freeling::mention const &':
                        return _pyfreeling.document_get_mention(self, arg2)

                    def get_coref_id_mentions(self, arg2: 'int') -> 'std::list< int,std::allocator< int > >':
                        return _pyfreeling.document_get_coref_id_mentions(self, arg2)

                    __swig_destroy__ = _pyfreeling.delete_document
                    __del__ = lambda self: None


        document_swigregister = _pyfreeling.document_swigregister
        document_swigregister(document)
        TEXT = _pyfreeling.TEXT
        IDENT = _pyfreeling.IDENT
        TOKEN = _pyfreeling.TOKEN
        SPLITTED = _pyfreeling.SPLITTED
        MORFO = _pyfreeling.MORFO
        TAGGED = _pyfreeling.TAGGED
        SENSES = _pyfreeling.SENSES
        SHALLOW = _pyfreeling.SHALLOW
        PARSED = _pyfreeling.PARSED
        DEP = _pyfreeling.DEP
        COREF = _pyfreeling.COREF
        SEMGRAPH = _pyfreeling.SEMGRAPH
        NO_TAGGER = _pyfreeling.NO_TAGGER
        HMM = _pyfreeling.HMM
        RELAX = _pyfreeling.RELAX
        NO_DEP = _pyfreeling.NO_DEP
        TXALA = _pyfreeling.TXALA
        TREELER = _pyfreeling.TREELER
        NO_WSD = _pyfreeling.NO_WSD
        ALL = _pyfreeling.ALL
        MFS = _pyfreeling.MFS
        UKB = _pyfreeling.UKB
        NO_FORCE = _pyfreeling.NO_FORCE
        TAGGER = _pyfreeling.TAGGER
        RETOK = _pyfreeling.RETOK

        class config_options(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, config_options, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, config_options, name)
            __repr__ = _swig_repr
            __swig_setmethods__['Lang'] = _pyfreeling.config_options_Lang_set
            __swig_getmethods__['Lang'] = _pyfreeling.config_options_Lang_get
            if _newclass:
                Lang = _swig_property(_pyfreeling.config_options_Lang_get, _pyfreeling.config_options_Lang_set)
            __swig_setmethods__['TOK_TokenizerFile'] = _pyfreeling.config_options_TOK_TokenizerFile_set
            __swig_getmethods__['TOK_TokenizerFile'] = _pyfreeling.config_options_TOK_TokenizerFile_get
            if _newclass:
                TOK_TokenizerFile = _swig_property(_pyfreeling.config_options_TOK_TokenizerFile_get, _pyfreeling.config_options_TOK_TokenizerFile_set)
            __swig_setmethods__['SPLIT_SplitterFile'] = _pyfreeling.config_options_SPLIT_SplitterFile_set
            __swig_getmethods__['SPLIT_SplitterFile'] = _pyfreeling.config_options_SPLIT_SplitterFile_get
            if _newclass:
                SPLIT_SplitterFile = _swig_property(_pyfreeling.config_options_SPLIT_SplitterFile_get, _pyfreeling.config_options_SPLIT_SplitterFile_set)
            __swig_setmethods__['MACO_Decimal'] = _pyfreeling.config_options_MACO_Decimal_set
            __swig_getmethods__['MACO_Decimal'] = _pyfreeling.config_options_MACO_Decimal_get
            if _newclass:
                MACO_Decimal = _swig_property(_pyfreeling.config_options_MACO_Decimal_get, _pyfreeling.config_options_MACO_Decimal_set)
            __swig_setmethods__['MACO_Thousand'] = _pyfreeling.config_options_MACO_Thousand_set
            __swig_getmethods__['MACO_Thousand'] = _pyfreeling.config_options_MACO_Thousand_get
            if _newclass:
                MACO_Thousand = _swig_property(_pyfreeling.config_options_MACO_Thousand_get, _pyfreeling.config_options_MACO_Thousand_set)
            __swig_setmethods__['MACO_UserMapFile'] = _pyfreeling.config_options_MACO_UserMapFile_set
            __swig_getmethods__['MACO_UserMapFile'] = _pyfreeling.config_options_MACO_UserMapFile_get
            if _newclass:
                MACO_UserMapFile = _swig_property(_pyfreeling.config_options_MACO_UserMapFile_get, _pyfreeling.config_options_MACO_UserMapFile_set)
            __swig_setmethods__['MACO_LocutionsFile'] = _pyfreeling.config_options_MACO_LocutionsFile_set
            __swig_getmethods__['MACO_LocutionsFile'] = _pyfreeling.config_options_MACO_LocutionsFile_get
            if _newclass:
                MACO_LocutionsFile = _swig_property(_pyfreeling.config_options_MACO_LocutionsFile_get, _pyfreeling.config_options_MACO_LocutionsFile_set)
            __swig_setmethods__['MACO_QuantitiesFile'] = _pyfreeling.config_options_MACO_QuantitiesFile_set
            __swig_getmethods__['MACO_QuantitiesFile'] = _pyfreeling.config_options_MACO_QuantitiesFile_get
            if _newclass:
                MACO_QuantitiesFile = _swig_property(_pyfreeling.config_options_MACO_QuantitiesFile_get, _pyfreeling.config_options_MACO_QuantitiesFile_set)
            __swig_setmethods__['MACO_AffixFile'] = _pyfreeling.config_options_MACO_AffixFile_set
            __swig_getmethods__['MACO_AffixFile'] = _pyfreeling.config_options_MACO_AffixFile_get
            if _newclass:
                MACO_AffixFile = _swig_property(_pyfreeling.config_options_MACO_AffixFile_get, _pyfreeling.config_options_MACO_AffixFile_set)
            __swig_setmethods__['MACO_ProbabilityFile'] = _pyfreeling.config_options_MACO_ProbabilityFile_set
            __swig_getmethods__['MACO_ProbabilityFile'] = _pyfreeling.config_options_MACO_ProbabilityFile_get
            if _newclass:
                MACO_ProbabilityFile = _swig_property(_pyfreeling.config_options_MACO_ProbabilityFile_get, _pyfreeling.config_options_MACO_ProbabilityFile_set)
            __swig_setmethods__['MACO_DictionaryFile'] = _pyfreeling.config_options_MACO_DictionaryFile_set
            __swig_getmethods__['MACO_DictionaryFile'] = _pyfreeling.config_options_MACO_DictionaryFile_get
            if _newclass:
                MACO_DictionaryFile = _swig_property(_pyfreeling.config_options_MACO_DictionaryFile_get, _pyfreeling.config_options_MACO_DictionaryFile_set)
            __swig_setmethods__['MACO_NPDataFile'] = _pyfreeling.config_options_MACO_NPDataFile_set
            __swig_getmethods__['MACO_NPDataFile'] = _pyfreeling.config_options_MACO_NPDataFile_get
            if _newclass:
                MACO_NPDataFile = _swig_property(_pyfreeling.config_options_MACO_NPDataFile_get, _pyfreeling.config_options_MACO_NPDataFile_set)
            __swig_setmethods__['MACO_PunctuationFile'] = _pyfreeling.config_options_MACO_PunctuationFile_set
            __swig_getmethods__['MACO_PunctuationFile'] = _pyfreeling.config_options_MACO_PunctuationFile_get
            if _newclass:
                MACO_PunctuationFile = _swig_property(_pyfreeling.config_options_MACO_PunctuationFile_get, _pyfreeling.config_options_MACO_PunctuationFile_set)
            __swig_setmethods__['MACO_CompoundFile'] = _pyfreeling.config_options_MACO_CompoundFile_set
            __swig_getmethods__['MACO_CompoundFile'] = _pyfreeling.config_options_MACO_CompoundFile_get
            if _newclass:
                MACO_CompoundFile = _swig_property(_pyfreeling.config_options_MACO_CompoundFile_get, _pyfreeling.config_options_MACO_CompoundFile_set)
            __swig_setmethods__['MACO_ProbabilityThreshold'] = _pyfreeling.config_options_MACO_ProbabilityThreshold_set
            __swig_getmethods__['MACO_ProbabilityThreshold'] = _pyfreeling.config_options_MACO_ProbabilityThreshold_get
            if _newclass:
                MACO_ProbabilityThreshold = _swig_property(_pyfreeling.config_options_MACO_ProbabilityThreshold_get, _pyfreeling.config_options_MACO_ProbabilityThreshold_set)
            __swig_setmethods__['PHON_PhoneticsFile'] = _pyfreeling.config_options_PHON_PhoneticsFile_set
            __swig_getmethods__['PHON_PhoneticsFile'] = _pyfreeling.config_options_PHON_PhoneticsFile_get
            if _newclass:
                PHON_PhoneticsFile = _swig_property(_pyfreeling.config_options_PHON_PhoneticsFile_get, _pyfreeling.config_options_PHON_PhoneticsFile_set)
            __swig_setmethods__['NEC_NECFile'] = _pyfreeling.config_options_NEC_NECFile_set
            __swig_getmethods__['NEC_NECFile'] = _pyfreeling.config_options_NEC_NECFile_get
            if _newclass:
                NEC_NECFile = _swig_property(_pyfreeling.config_options_NEC_NECFile_get, _pyfreeling.config_options_NEC_NECFile_set)
            __swig_setmethods__['SENSE_ConfigFile'] = _pyfreeling.config_options_SENSE_ConfigFile_set
            __swig_getmethods__['SENSE_ConfigFile'] = _pyfreeling.config_options_SENSE_ConfigFile_get
            if _newclass:
                SENSE_ConfigFile = _swig_property(_pyfreeling.config_options_SENSE_ConfigFile_get, _pyfreeling.config_options_SENSE_ConfigFile_set)
            __swig_setmethods__['UKB_ConfigFile'] = _pyfreeling.config_options_UKB_ConfigFile_set
            __swig_getmethods__['UKB_ConfigFile'] = _pyfreeling.config_options_UKB_ConfigFile_get
            if _newclass:
                UKB_ConfigFile = _swig_property(_pyfreeling.config_options_UKB_ConfigFile_get, _pyfreeling.config_options_UKB_ConfigFile_set)
            __swig_setmethods__['TAGGER_HMMFile'] = _pyfreeling.config_options_TAGGER_HMMFile_set
            __swig_getmethods__['TAGGER_HMMFile'] = _pyfreeling.config_options_TAGGER_HMMFile_get
            if _newclass:
                TAGGER_HMMFile = _swig_property(_pyfreeling.config_options_TAGGER_HMMFile_get, _pyfreeling.config_options_TAGGER_HMMFile_set)
            __swig_setmethods__['TAGGER_RelaxFile'] = _pyfreeling.config_options_TAGGER_RelaxFile_set
            __swig_getmethods__['TAGGER_RelaxFile'] = _pyfreeling.config_options_TAGGER_RelaxFile_get
            if _newclass:
                TAGGER_RelaxFile = _swig_property(_pyfreeling.config_options_TAGGER_RelaxFile_get, _pyfreeling.config_options_TAGGER_RelaxFile_set)
            __swig_setmethods__['TAGGER_RelaxMaxIter'] = _pyfreeling.config_options_TAGGER_RelaxMaxIter_set
            __swig_getmethods__['TAGGER_RelaxMaxIter'] = _pyfreeling.config_options_TAGGER_RelaxMaxIter_get
            if _newclass:
                TAGGER_RelaxMaxIter = _swig_property(_pyfreeling.config_options_TAGGER_RelaxMaxIter_get, _pyfreeling.config_options_TAGGER_RelaxMaxIter_set)
            __swig_setmethods__['TAGGER_RelaxScaleFactor'] = _pyfreeling.config_options_TAGGER_RelaxScaleFactor_set
            __swig_getmethods__['TAGGER_RelaxScaleFactor'] = _pyfreeling.config_options_TAGGER_RelaxScaleFactor_get
            if _newclass:
                TAGGER_RelaxScaleFactor = _swig_property(_pyfreeling.config_options_TAGGER_RelaxScaleFactor_get, _pyfreeling.config_options_TAGGER_RelaxScaleFactor_set)
            __swig_setmethods__['TAGGER_RelaxEpsilon'] = _pyfreeling.config_options_TAGGER_RelaxEpsilon_set
            __swig_getmethods__['TAGGER_RelaxEpsilon'] = _pyfreeling.config_options_TAGGER_RelaxEpsilon_get
            if _newclass:
                TAGGER_RelaxEpsilon = _swig_property(_pyfreeling.config_options_TAGGER_RelaxEpsilon_get, _pyfreeling.config_options_TAGGER_RelaxEpsilon_set)
            __swig_setmethods__['TAGGER_Retokenize'] = _pyfreeling.config_options_TAGGER_Retokenize_set
            __swig_getmethods__['TAGGER_Retokenize'] = _pyfreeling.config_options_TAGGER_Retokenize_get
            if _newclass:
                TAGGER_Retokenize = _swig_property(_pyfreeling.config_options_TAGGER_Retokenize_get, _pyfreeling.config_options_TAGGER_Retokenize_set)
            __swig_setmethods__['TAGGER_ForceSelect'] = _pyfreeling.config_options_TAGGER_ForceSelect_set
            __swig_getmethods__['TAGGER_ForceSelect'] = _pyfreeling.config_options_TAGGER_ForceSelect_get
            if _newclass:
                TAGGER_ForceSelect = _swig_property(_pyfreeling.config_options_TAGGER_ForceSelect_get, _pyfreeling.config_options_TAGGER_ForceSelect_set)
            __swig_setmethods__['PARSER_GrammarFile'] = _pyfreeling.config_options_PARSER_GrammarFile_set
            __swig_getmethods__['PARSER_GrammarFile'] = _pyfreeling.config_options_PARSER_GrammarFile_get
            if _newclass:
                PARSER_GrammarFile = _swig_property(_pyfreeling.config_options_PARSER_GrammarFile_get, _pyfreeling.config_options_PARSER_GrammarFile_set)
            __swig_setmethods__['DEP_TxalaFile'] = _pyfreeling.config_options_DEP_TxalaFile_set
            __swig_getmethods__['DEP_TxalaFile'] = _pyfreeling.config_options_DEP_TxalaFile_get
            if _newclass:
                DEP_TxalaFile = _swig_property(_pyfreeling.config_options_DEP_TxalaFile_get, _pyfreeling.config_options_DEP_TxalaFile_set)
            __swig_setmethods__['DEP_TreelerFile'] = _pyfreeling.config_options_DEP_TreelerFile_set
            __swig_getmethods__['DEP_TreelerFile'] = _pyfreeling.config_options_DEP_TreelerFile_get
            if _newclass:
                DEP_TreelerFile = _swig_property(_pyfreeling.config_options_DEP_TreelerFile_get, _pyfreeling.config_options_DEP_TreelerFile_set)
            __swig_setmethods__['COREF_CorefFile'] = _pyfreeling.config_options_COREF_CorefFile_set
            __swig_getmethods__['COREF_CorefFile'] = _pyfreeling.config_options_COREF_CorefFile_get
            if _newclass:
                COREF_CorefFile = _swig_property(_pyfreeling.config_options_COREF_CorefFile_get, _pyfreeling.config_options_COREF_CorefFile_set)
            __swig_setmethods__['SEMGRAPH_SemGraphFile'] = _pyfreeling.config_options_SEMGRAPH_SemGraphFile_set
            __swig_getmethods__['SEMGRAPH_SemGraphFile'] = _pyfreeling.config_options_SEMGRAPH_SemGraphFile_get
            if _newclass:
                SEMGRAPH_SemGraphFile = _swig_property(_pyfreeling.config_options_SEMGRAPH_SemGraphFile_get, _pyfreeling.config_options_SEMGRAPH_SemGraphFile_set)

            def __init__(self):
                this = _pyfreeling.new_config_options()
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_config_options
            __del__ = lambda self: None


        config_options_swigregister = _pyfreeling.config_options_swigregister
        config_options_swigregister(config_options)

        class invoke_options(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, invoke_options, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, invoke_options, name)
            __repr__ = _swig_repr
            __swig_setmethods__['InputLevel'] = _pyfreeling.invoke_options_InputLevel_set
            __swig_getmethods__['InputLevel'] = _pyfreeling.invoke_options_InputLevel_get
            if _newclass:
                InputLevel = _swig_property(_pyfreeling.invoke_options_InputLevel_get, _pyfreeling.invoke_options_InputLevel_set)
            __swig_setmethods__['OutputLevel'] = _pyfreeling.invoke_options_OutputLevel_set
            __swig_getmethods__['OutputLevel'] = _pyfreeling.invoke_options_OutputLevel_get
            if _newclass:
                OutputLevel = _swig_property(_pyfreeling.invoke_options_OutputLevel_get, _pyfreeling.invoke_options_OutputLevel_set)
            __swig_setmethods__['MACO_UserMap'] = _pyfreeling.invoke_options_MACO_UserMap_set
            __swig_getmethods__['MACO_UserMap'] = _pyfreeling.invoke_options_MACO_UserMap_get
            if _newclass:
                MACO_UserMap = _swig_property(_pyfreeling.invoke_options_MACO_UserMap_get, _pyfreeling.invoke_options_MACO_UserMap_set)
            __swig_setmethods__['MACO_AffixAnalysis'] = _pyfreeling.invoke_options_MACO_AffixAnalysis_set
            __swig_getmethods__['MACO_AffixAnalysis'] = _pyfreeling.invoke_options_MACO_AffixAnalysis_get
            if _newclass:
                MACO_AffixAnalysis = _swig_property(_pyfreeling.invoke_options_MACO_AffixAnalysis_get, _pyfreeling.invoke_options_MACO_AffixAnalysis_set)
            __swig_setmethods__['MACO_MultiwordsDetection'] = _pyfreeling.invoke_options_MACO_MultiwordsDetection_set
            __swig_getmethods__['MACO_MultiwordsDetection'] = _pyfreeling.invoke_options_MACO_MultiwordsDetection_get
            if _newclass:
                MACO_MultiwordsDetection = _swig_property(_pyfreeling.invoke_options_MACO_MultiwordsDetection_get, _pyfreeling.invoke_options_MACO_MultiwordsDetection_set)
            __swig_setmethods__['MACO_NumbersDetection'] = _pyfreeling.invoke_options_MACO_NumbersDetection_set
            __swig_getmethods__['MACO_NumbersDetection'] = _pyfreeling.invoke_options_MACO_NumbersDetection_get
            if _newclass:
                MACO_NumbersDetection = _swig_property(_pyfreeling.invoke_options_MACO_NumbersDetection_get, _pyfreeling.invoke_options_MACO_NumbersDetection_set)
            __swig_setmethods__['MACO_PunctuationDetection'] = _pyfreeling.invoke_options_MACO_PunctuationDetection_set
            __swig_getmethods__['MACO_PunctuationDetection'] = _pyfreeling.invoke_options_MACO_PunctuationDetection_get
            if _newclass:
                MACO_PunctuationDetection = _swig_property(_pyfreeling.invoke_options_MACO_PunctuationDetection_get, _pyfreeling.invoke_options_MACO_PunctuationDetection_set)
            __swig_setmethods__['MACO_DatesDetection'] = _pyfreeling.invoke_options_MACO_DatesDetection_set
            __swig_getmethods__['MACO_DatesDetection'] = _pyfreeling.invoke_options_MACO_DatesDetection_get
            if _newclass:
                MACO_DatesDetection = _swig_property(_pyfreeling.invoke_options_MACO_DatesDetection_get, _pyfreeling.invoke_options_MACO_DatesDetection_set)
            __swig_setmethods__['MACO_QuantitiesDetection'] = _pyfreeling.invoke_options_MACO_QuantitiesDetection_set
            __swig_getmethods__['MACO_QuantitiesDetection'] = _pyfreeling.invoke_options_MACO_QuantitiesDetection_get
            if _newclass:
                MACO_QuantitiesDetection = _swig_property(_pyfreeling.invoke_options_MACO_QuantitiesDetection_get, _pyfreeling.invoke_options_MACO_QuantitiesDetection_set)
            __swig_setmethods__['MACO_DictionarySearch'] = _pyfreeling.invoke_options_MACO_DictionarySearch_set
            __swig_getmethods__['MACO_DictionarySearch'] = _pyfreeling.invoke_options_MACO_DictionarySearch_get
            if _newclass:
                MACO_DictionarySearch = _swig_property(_pyfreeling.invoke_options_MACO_DictionarySearch_get, _pyfreeling.invoke_options_MACO_DictionarySearch_set)
            __swig_setmethods__['MACO_ProbabilityAssignment'] = _pyfreeling.invoke_options_MACO_ProbabilityAssignment_set
            __swig_getmethods__['MACO_ProbabilityAssignment'] = _pyfreeling.invoke_options_MACO_ProbabilityAssignment_get
            if _newclass:
                MACO_ProbabilityAssignment = _swig_property(_pyfreeling.invoke_options_MACO_ProbabilityAssignment_get, _pyfreeling.invoke_options_MACO_ProbabilityAssignment_set)
            __swig_setmethods__['MACO_CompoundAnalysis'] = _pyfreeling.invoke_options_MACO_CompoundAnalysis_set
            __swig_getmethods__['MACO_CompoundAnalysis'] = _pyfreeling.invoke_options_MACO_CompoundAnalysis_get
            if _newclass:
                MACO_CompoundAnalysis = _swig_property(_pyfreeling.invoke_options_MACO_CompoundAnalysis_get, _pyfreeling.invoke_options_MACO_CompoundAnalysis_set)
            __swig_setmethods__['MACO_NERecognition'] = _pyfreeling.invoke_options_MACO_NERecognition_set
            __swig_getmethods__['MACO_NERecognition'] = _pyfreeling.invoke_options_MACO_NERecognition_get
            if _newclass:
                MACO_NERecognition = _swig_property(_pyfreeling.invoke_options_MACO_NERecognition_get, _pyfreeling.invoke_options_MACO_NERecognition_set)
            __swig_setmethods__['MACO_RetokContractions'] = _pyfreeling.invoke_options_MACO_RetokContractions_set
            __swig_getmethods__['MACO_RetokContractions'] = _pyfreeling.invoke_options_MACO_RetokContractions_get
            if _newclass:
                MACO_RetokContractions = _swig_property(_pyfreeling.invoke_options_MACO_RetokContractions_get, _pyfreeling.invoke_options_MACO_RetokContractions_set)
            __swig_setmethods__['PHON_Phonetics'] = _pyfreeling.invoke_options_PHON_Phonetics_set
            __swig_getmethods__['PHON_Phonetics'] = _pyfreeling.invoke_options_PHON_Phonetics_get
            if _newclass:
                PHON_Phonetics = _swig_property(_pyfreeling.invoke_options_PHON_Phonetics_get, _pyfreeling.invoke_options_PHON_Phonetics_set)
            __swig_setmethods__['NEC_NEClassification'] = _pyfreeling.invoke_options_NEC_NEClassification_set
            __swig_getmethods__['NEC_NEClassification'] = _pyfreeling.invoke_options_NEC_NEClassification_get
            if _newclass:
                NEC_NEClassification = _swig_property(_pyfreeling.invoke_options_NEC_NEClassification_get, _pyfreeling.invoke_options_NEC_NEClassification_set)
            __swig_setmethods__['SENSE_WSD_which'] = _pyfreeling.invoke_options_SENSE_WSD_which_set
            __swig_getmethods__['SENSE_WSD_which'] = _pyfreeling.invoke_options_SENSE_WSD_which_get
            if _newclass:
                SENSE_WSD_which = _swig_property(_pyfreeling.invoke_options_SENSE_WSD_which_get, _pyfreeling.invoke_options_SENSE_WSD_which_set)
            __swig_setmethods__['TAGGER_which'] = _pyfreeling.invoke_options_TAGGER_which_set
            __swig_getmethods__['TAGGER_which'] = _pyfreeling.invoke_options_TAGGER_which_get
            if _newclass:
                TAGGER_which = _swig_property(_pyfreeling.invoke_options_TAGGER_which_get, _pyfreeling.invoke_options_TAGGER_which_set)
            __swig_setmethods__['DEP_which'] = _pyfreeling.invoke_options_DEP_which_set
            __swig_getmethods__['DEP_which'] = _pyfreeling.invoke_options_DEP_which_get
            if _newclass:
                DEP_which = _swig_property(_pyfreeling.invoke_options_DEP_which_get, _pyfreeling.invoke_options_DEP_which_set)

            def __init__(self):
                this = _pyfreeling.new_invoke_options()
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_invoke_options
            __del__ = lambda self: None


        invoke_options_swigregister = _pyfreeling.invoke_options_swigregister
        invoke_options_swigregister(invoke_options)

        class analyzer(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, analyzer, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, analyzer, name)
            __repr__ = _swig_repr

            def __init__(self, cfg: 'config_options'):
                this = _pyfreeling.new_analyzercfg
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def set_current_invoke_options(self, opt: 'invoke_options', check: 'bool'=True) -> 'void':
                return _pyfreeling.analyzer_set_current_invoke_options(self, opt, check)

            def get_current_invoke_options(self) -> 'freeling::analyzer::invoke_options const &':
                return _pyfreeling.analyzer_get_current_invoke_optionsself

            __swig_destroy__ = _pyfreeling.delete_analyzer
            __del__ = lambda self: None

            def analyze(self, *args) -> 'std::list< freeling::sentence,std::allocator< freeling::sentence > >':
                return (_pyfreeling.analyzer_analyze)(self, *args)

            def analyze_as_document(self, text: 'std::wstring const &', parag: 'bool'=False) -> 'freeling::document':
                return _pyfreeling.analyzer_analyze_as_document(self, text, parag)

            def flush_buffer(self, ls: 'ListSentence') -> 'void':
                return _pyfreeling.analyzer_flush_buffer(self, ls)

            def reset_offset(self) -> 'void':
                return _pyfreeling.analyzer_reset_offsetself


        analyzer_swigregister = _pyfreeling.analyzer_swigregister
        analyzer_swigregister(analyzer)

        class traces(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, traces, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, traces, name)
            __repr__ = _swig_repr
            __swig_setmethods__['TraceLevel'] = _pyfreeling.traces_TraceLevel_set
            __swig_getmethods__['TraceLevel'] = _pyfreeling.traces_TraceLevel_get
            if _newclass:
                TraceLevel = _swig_property(_pyfreeling.traces_TraceLevel_get, _pyfreeling.traces_TraceLevel_set)
            __swig_setmethods__['TraceModule'] = _pyfreeling.traces_TraceModule_set
            __swig_getmethods__['TraceModule'] = _pyfreeling.traces_TraceModule_get
            if _newclass:
                TraceModule = _swig_property(_pyfreeling.traces_TraceModule_get, _pyfreeling.traces_TraceModule_set)

            def __init__(self):
                this = _pyfreeling.new_traces()
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_traces
            __del__ = lambda self: None


        traces_swigregister = _pyfreeling.traces_swigregister
        traces_swigregister(traces)

        class lang_ident(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, lang_ident, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, lang_ident, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_lang_ident)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_lang_ident
            __del__ = lambda self: None

            def add_language(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.lang_ident_add_language(self, arg2)

            def train_language(self, arg2: 'std::wstring const &', arg3: 'std::wstring const &', arg4: 'std::wstring const &', order: 'size_t') -> 'void':
                return _pyfreeling.lang_ident_train_language(self, arg2, arg3, arg4, order)

            def identify_language(self, *args) -> 'std::wstring':
                return (_pyfreeling.lang_ident_identify_language)(self, *args)

            def rank_languages(self, *args) -> 'std::vector< std::pair< double,std::wstring >,std::allocator< std::pair< double,std::wstring > > >':
                return (_pyfreeling.lang_ident_rank_languages)(self, *args)


        lang_ident_swigregister = _pyfreeling.lang_ident_swigregister
        lang_ident_swigregister(lang_ident)

        class tokenizer(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, tokenizer, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, tokenizer, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_tokenizerarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_tokenizer
            __del__ = lambda self: None

            def tokenize(self, *args) -> 'void':
                return (_pyfreeling.tokenizer_tokenize)(self, *args)


        tokenizer_swigregister = _pyfreeling.tokenizer_swigregister
        tokenizer_swigregister(tokenizer)

        class splitter(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, splitter, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, splitter, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_splitterarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_splitter
            __del__ = lambda self: None

            def open_session(self) -> 'freeling::splitter::session_id':
                return _pyfreeling.splitter_open_sessionself

            def close_session(self, arg2: 'freeling::splitter::session_id') -> 'void':
                return _pyfreeling.splitter_close_session(self, arg2)

            def split(self, *args) -> 'std::list< freeling::sentence,std::allocator< freeling::sentence > >':
                return (_pyfreeling.splitter_split)(self, *args)


        splitter_swigregister = _pyfreeling.splitter_swigregister
        splitter_swigregister(splitter)

        class maco_options(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, maco_options, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, maco_options, name)
            __repr__ = _swig_repr
            __swig_setmethods__['Lang'] = _pyfreeling.maco_options_Lang_set
            __swig_getmethods__['Lang'] = _pyfreeling.maco_options_Lang_get
            if _newclass:
                Lang = _swig_property(_pyfreeling.maco_options_Lang_get, _pyfreeling.maco_options_Lang_set)
            __swig_setmethods__['LocutionsFile'] = _pyfreeling.maco_options_LocutionsFile_set
            __swig_getmethods__['LocutionsFile'] = _pyfreeling.maco_options_LocutionsFile_get
            if _newclass:
                LocutionsFile = _swig_property(_pyfreeling.maco_options_LocutionsFile_get, _pyfreeling.maco_options_LocutionsFile_set)
            __swig_setmethods__['QuantitiesFile'] = _pyfreeling.maco_options_QuantitiesFile_set
            __swig_getmethods__['QuantitiesFile'] = _pyfreeling.maco_options_QuantitiesFile_get
            if _newclass:
                QuantitiesFile = _swig_property(_pyfreeling.maco_options_QuantitiesFile_get, _pyfreeling.maco_options_QuantitiesFile_set)
            __swig_setmethods__['AffixFile'] = _pyfreeling.maco_options_AffixFile_set
            __swig_getmethods__['AffixFile'] = _pyfreeling.maco_options_AffixFile_get
            if _newclass:
                AffixFile = _swig_property(_pyfreeling.maco_options_AffixFile_get, _pyfreeling.maco_options_AffixFile_set)
            __swig_setmethods__['CompoundFile'] = _pyfreeling.maco_options_CompoundFile_set
            __swig_getmethods__['CompoundFile'] = _pyfreeling.maco_options_CompoundFile_get
            if _newclass:
                CompoundFile = _swig_property(_pyfreeling.maco_options_CompoundFile_get, _pyfreeling.maco_options_CompoundFile_set)
            __swig_setmethods__['DictionaryFile'] = _pyfreeling.maco_options_DictionaryFile_set
            __swig_getmethods__['DictionaryFile'] = _pyfreeling.maco_options_DictionaryFile_get
            if _newclass:
                DictionaryFile = _swig_property(_pyfreeling.maco_options_DictionaryFile_get, _pyfreeling.maco_options_DictionaryFile_set)
            __swig_setmethods__['ProbabilityFile'] = _pyfreeling.maco_options_ProbabilityFile_set
            __swig_getmethods__['ProbabilityFile'] = _pyfreeling.maco_options_ProbabilityFile_get
            if _newclass:
                ProbabilityFile = _swig_property(_pyfreeling.maco_options_ProbabilityFile_get, _pyfreeling.maco_options_ProbabilityFile_set)
            __swig_setmethods__['NPdataFile'] = _pyfreeling.maco_options_NPdataFile_set
            __swig_getmethods__['NPdataFile'] = _pyfreeling.maco_options_NPdataFile_get
            if _newclass:
                NPdataFile = _swig_property(_pyfreeling.maco_options_NPdataFile_get, _pyfreeling.maco_options_NPdataFile_set)
            __swig_setmethods__['PunctuationFile'] = _pyfreeling.maco_options_PunctuationFile_set
            __swig_getmethods__['PunctuationFile'] = _pyfreeling.maco_options_PunctuationFile_get
            if _newclass:
                PunctuationFile = _swig_property(_pyfreeling.maco_options_PunctuationFile_get, _pyfreeling.maco_options_PunctuationFile_set)
            __swig_setmethods__['UserMapFile'] = _pyfreeling.maco_options_UserMapFile_set
            __swig_getmethods__['UserMapFile'] = _pyfreeling.maco_options_UserMapFile_get
            if _newclass:
                UserMapFile = _swig_property(_pyfreeling.maco_options_UserMapFile_get, _pyfreeling.maco_options_UserMapFile_set)
            __swig_setmethods__['Decimal'] = _pyfreeling.maco_options_Decimal_set
            __swig_getmethods__['Decimal'] = _pyfreeling.maco_options_Decimal_get
            if _newclass:
                Decimal = _swig_property(_pyfreeling.maco_options_Decimal_get, _pyfreeling.maco_options_Decimal_set)
            __swig_setmethods__['Thousand'] = _pyfreeling.maco_options_Thousand_set
            __swig_getmethods__['Thousand'] = _pyfreeling.maco_options_Thousand_get
            if _newclass:
                Thousand = _swig_property(_pyfreeling.maco_options_Thousand_get, _pyfreeling.maco_options_Thousand_set)
            __swig_setmethods__['ProbabilityThreshold'] = _pyfreeling.maco_options_ProbabilityThreshold_set
            __swig_getmethods__['ProbabilityThreshold'] = _pyfreeling.maco_options_ProbabilityThreshold_get
            if _newclass:
                ProbabilityThreshold = _swig_property(_pyfreeling.maco_options_ProbabilityThreshold_get, _pyfreeling.maco_options_ProbabilityThreshold_set)
            __swig_setmethods__['InverseDict'] = _pyfreeling.maco_options_InverseDict_set
            __swig_getmethods__['InverseDict'] = _pyfreeling.maco_options_InverseDict_get
            if _newclass:
                InverseDict = _swig_property(_pyfreeling.maco_options_InverseDict_get, _pyfreeling.maco_options_InverseDict_set)
            __swig_setmethods__['RetokContractions'] = _pyfreeling.maco_options_RetokContractions_set
            __swig_getmethods__['RetokContractions'] = _pyfreeling.maco_options_RetokContractions_get
            if _newclass:
                RetokContractions = _swig_property(_pyfreeling.maco_options_RetokContractions_get, _pyfreeling.maco_options_RetokContractions_set)

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_maco_optionsarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_maco_options
            __del__ = lambda self: None

            def set_data_files(self, usr: 'std::wstring const &', pun: 'std::wstring const &', dic: 'std::wstring const &', aff: 'std::wstring const &', comp: 'std::wstring const &', loc: 'std::wstring const &', nps: 'std::wstring const &', qty: 'std::wstring const &', prb: 'std::wstring const &') -> 'void':
                return _pyfreeling.maco_options_set_data_files(self, usr, pun, dic, aff, comp, loc, nps, qty, prb)

            def set_nummerical_points(self, dec: 'std::wstring const &', tho: 'std::wstring const &') -> 'void':
                return _pyfreeling.maco_options_set_nummerical_points(self, dec, tho)

            def set_threshold(self, arg2: 'double') -> 'void':
                return _pyfreeling.maco_options_set_threshold(self, arg2)

            def set_inverse_dict(self, arg2: 'bool') -> 'void':
                return _pyfreeling.maco_options_set_inverse_dict(self, arg2)

            def set_retok_contractions(self, arg2: 'bool') -> 'void':
                return _pyfreeling.maco_options_set_retok_contractions(self, arg2)


        maco_options_swigregister = _pyfreeling.maco_options_swigregister
        maco_options_swigregister(maco_options)

        class maco(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, maco, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, maco, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'maco_options'):
                this = _pyfreeling.new_macoarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_maco
            __del__ = lambda self: None

            def set_active_options(self, umap: 'bool', num: 'bool', pun: 'bool', dat: 'bool', dic: 'bool', aff: 'bool', comp: 'bool', rtk: 'bool', mw: 'bool', ner: 'bool', qt: 'bool', prb: 'bool') -> 'void':
                return _pyfreeling.maco_set_active_options(self, umap, num, pun, dat, dic, aff, comp, rtk, mw, ner, qt, prb)

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.maco_analyze)(self, *args)


        maco_swigregister = _pyfreeling.maco_swigregister
        maco_swigregister(maco)

        class RE_map(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, RE_map, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, RE_map, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_RE_maparg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_RE_map
            __del__ = lambda self: None

            def annotate_word(self, arg2: 'word') -> 'void':
                return _pyfreeling.RE_map_annotate_word(self, arg2)

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.RE_map_analyze)(self, *args)


        RE_map_swigregister = _pyfreeling.RE_map_swigregister
        RE_map_swigregister(RE_map)

        class numbers(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, numbers, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, numbers, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &', arg3: 'std::wstring const &', arg4: 'std::wstring const &'):
                this = _pyfreeling.new_numbers(arg2, arg3, arg4)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_numbers
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.numbers_analyze)(self, *args)


        numbers_swigregister = _pyfreeling.numbers_swigregister
        numbers_swigregister(numbers)

        class punts(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, punts, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, punts, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_puntsarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_punts
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.punts_analyze)(self, *args)


        punts_swigregister = _pyfreeling.punts_swigregister
        punts_swigregister(punts)

        class dates(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, dates, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, dates, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_datesarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_dates
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.dates_analyze)(self, *args)


        dates_swigregister = _pyfreeling.dates_swigregister
        dates_swigregister(dates)

        class dictionary(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, dictionary, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, dictionary, name)
            __repr__ = _swig_repr
            OFF = _pyfreeling.dictionary_OFF
            ON = _pyfreeling.dictionary_ON
            DEFAULT = _pyfreeling.dictionary_DEFAULT

            def __init__(self, Lang: 'std::wstring const &', dicFile: 'std::wstring const &', sufFile: 'std::wstring const &', compFile: 'std::wstring const &', invDic: 'bool'=False, retok: 'bool'=True):
                this = _pyfreeling.new_dictionary(Lang, dicFile, sufFile, compFile, invDic, retok)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_dictionary
            __del__ = lambda self: None

            def add_analysis(self, arg2: 'std::wstring const &', arg3: 'analysis') -> 'void':
                return _pyfreeling.dictionary_add_analysis(self, arg2, arg3)

            def remove_entry(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.dictionary_remove_entry(self, arg2)

            def set_retokenize_contractions(self, arg2: 'bool') -> 'void':
                return _pyfreeling.dictionary_set_retokenize_contractions(self, arg2)

            def set_affix_analysis(self, arg2: 'bool') -> 'void':
                return _pyfreeling.dictionary_set_affix_analysis(self, arg2)

            def set_compound_analysis(self, arg2: 'bool') -> 'void':
                return _pyfreeling.dictionary_set_compound_analysis(self, arg2)

            def has_affixes(self) -> 'bool':
                return _pyfreeling.dictionary_has_affixesself

            def has_compounds(self) -> 'bool':
                return _pyfreeling.dictionary_has_compoundsself

            def search_form(self, arg2: 'std::wstring const &', arg3: 'ListAnalysis') -> 'void':
                return _pyfreeling.dictionary_search_form(self, arg2, arg3)

            def annotate_word(self, *args) -> 'void':
                return (_pyfreeling.dictionary_annotate_word)(self, *args)

            def get_forms(self, arg2: 'std::wstring const &', arg3: 'std::wstring const &') -> 'std::list< std::wstring,std::allocator< std::wstring > >':
                return _pyfreeling.dictionary_get_forms(self, arg2, arg3)

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.dictionary_analyze)(self, *args)


        dictionary_swigregister = _pyfreeling.dictionary_swigregister
        dictionary_swigregister(dictionary)

        class locutions(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, locutions, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, locutions, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_locutionsarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_locutions
            __del__ = lambda self: None

            def add_locution(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.locutions_add_locution(self, arg2)

            def set_OnlySelected(self, arg2: 'bool') -> 'void':
                return _pyfreeling.locutions_set_OnlySelected(self, arg2)

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.locutions_analyze)(self, *args)


        locutions_swigregister = _pyfreeling.locutions_swigregister
        locutions_swigregister(locutions)

        class ner(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ner, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ner, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_nerarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_ner
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.ner_analyze)(self, *args)


        ner_swigregister = _pyfreeling.ner_swigregister
        ner_swigregister(ner)

        class quantities(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, quantities, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, quantities, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &', arg3: 'std::wstring const &'):
                this = _pyfreeling.new_quantities(arg2, arg3)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_quantities
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.quantities_analyze)(self, *args)


        quantities_swigregister = _pyfreeling.quantities_swigregister
        quantities_swigregister(quantities)

        class probabilities(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, probabilities, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, probabilities, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &', arg3: 'double'):
                this = _pyfreeling.new_probabilities(arg2, arg3)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_probabilities
            __del__ = lambda self: None

            def annotate_word(self, arg2: 'word') -> 'void':
                return _pyfreeling.probabilities_annotate_word(self, arg2)

            def set_activate_guesser(self, arg2: 'bool') -> 'void':
                return _pyfreeling.probabilities_set_activate_guesser(self, arg2)

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.probabilities_analyze)(self, *args)


        probabilities_swigregister = _pyfreeling.probabilities_swigregister
        probabilities_swigregister(probabilities)

        class hmm_tagger(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, hmm_tagger, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, hmm_tagger, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &', arg3: 'bool', arg4: 'unsigned int', kb: 'unsigned int'=1):
                this = _pyfreeling.new_hmm_tagger(arg2, arg3, arg4, kb)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_hmm_tagger
            __del__ = lambda self: None

            def SequenceProb_log(self, arg2: 'sentence', k: 'int'=0) -> 'double':
                return _pyfreeling.hmm_tagger_SequenceProb_log(self, arg2, k)

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.hmm_tagger_analyze)(self, *args)


        hmm_tagger_swigregister = _pyfreeling.hmm_tagger_swigregister
        hmm_tagger_swigregister(hmm_tagger)

        class relax_tagger(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, relax_tagger, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, relax_tagger, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &', arg3: 'int', arg4: 'double', arg5: 'double', arg6: 'bool', arg7: 'unsigned int'):
                this = _pyfreeling.new_relax_tagger(arg2, arg3, arg4, arg5, arg6, arg7)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_relax_tagger
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.relax_tagger_analyze)(self, *args)


        relax_tagger_swigregister = _pyfreeling.relax_tagger_swigregister
        relax_tagger_swigregister(relax_tagger)

        class alternatives(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, alternatives, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, alternatives, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_alternativesarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_alternatives
            __del__ = lambda self: None

            def get_similar_words(self, arg2: 'std::wstring const &', arg3: 'ListAlternative') -> 'void':
                return _pyfreeling.alternatives_get_similar_words(self, arg2, arg3)

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.alternatives_analyze)(self, *args)


        alternatives_swigregister = _pyfreeling.alternatives_swigregister
        alternatives_swigregister(alternatives)

        class phonetics(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, phonetics, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, phonetics, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_phoneticsarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_phonetics
            __del__ = lambda self: None

            def get_sound(self, arg2: 'std::wstring const &') -> 'std::wstring':
                return _pyfreeling.phonetics_get_sound(self, arg2)

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.phonetics_analyze)(self, *args)


        phonetics_swigregister = _pyfreeling.phonetics_swigregister
        phonetics_swigregister(phonetics)

        class nec(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, nec, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, nec, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_necarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_nec
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.nec_analyze)(self, *args)


        nec_swigregister = _pyfreeling.nec_swigregister
        nec_swigregister(nec)

        class chart_parser(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, chart_parser, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, chart_parser, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_chart_parserarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_chart_parser
            __del__ = lambda self: None

            def get_start_symbol(self) -> 'std::wstring':
                return _pyfreeling.chart_parser_get_start_symbolself

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.chart_parser_analyze)(self, *args)


        chart_parser_swigregister = _pyfreeling.chart_parser_swigregister
        chart_parser_swigregister(chart_parser)

        class dep_txala(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, dep_txala, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, dep_txala, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &', arg3: 'std::wstring const &'):
                this = _pyfreeling.new_dep_txala(arg2, arg3)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_dep_txala
            __del__ = lambda self: None

            def complete_parse_tree(self, *args) -> 'void':
                return (_pyfreeling.dep_txala_complete_parse_tree)(self, *args)

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.dep_txala_analyze)(self, *args)


        dep_txala_swigregister = _pyfreeling.dep_txala_swigregister
        dep_txala_swigregister(dep_txala)

        class dep_treeler(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, dep_treeler, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, dep_treeler, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_dep_treelerarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_dep_treeler
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.dep_treeler_analyze)(self, *args)


        dep_treeler_swigregister = _pyfreeling.dep_treeler_swigregister
        dep_treeler_swigregister(dep_treeler)

        class senses(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, senses, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, senses, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_sensesarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_senses
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.senses_analyze)(self, *args)


        senses_swigregister = _pyfreeling.senses_swigregister
        senses_swigregister(senses)

        class relaxcor(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, relaxcor, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, relaxcor, name)
            __repr__ = _swig_repr

            def __init__(self, fname: 'std::wstring const &'):
                this = _pyfreeling.new_relaxcorfname
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_relaxcor
            __del__ = lambda self: None

            def set_provide_singletons(self, arg2: 'bool') -> 'void':
                return _pyfreeling.relaxcor_set_provide_singletons(self, arg2)

            def get_provide_singletons(self) -> 'bool':
                return _pyfreeling.relaxcor_get_provide_singletonsself

            def analyze(self, arg2: 'document') -> 'void':
                return _pyfreeling.relaxcor_analyze(self, arg2)


        relaxcor_swigregister = _pyfreeling.relaxcor_swigregister
        relaxcor_swigregister(relaxcor)

        class semgraph_extract(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, semgraph_extract, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, semgraph_extract, name)
            __repr__ = _swig_repr

            def __init__(self, erFile: 'std::wstring const &'):
                this = _pyfreeling.new_semgraph_extracterFile
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_semgraph_extract
            __del__ = lambda self: None

            def extract(self, doc: 'document') -> 'void':
                return _pyfreeling.semgraph_extract_extract(self, doc)


        semgraph_extract_swigregister = _pyfreeling.semgraph_extract_swigregister
        semgraph_extract_swigregister(semgraph_extract)

        class ukb(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, ukb, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, ukb, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_ukbarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_ukb
            __del__ = lambda self: None

            def analyze(self, *args) -> 'freeling::document':
                return (_pyfreeling.ukb_analyze)(self, *args)


        ukb_swigregister = _pyfreeling.ukb_swigregister
        ukb_swigregister(ukb)

        class sense_info(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, sense_info, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, sense_info, name)
            __repr__ = _swig_repr
            __swig_setmethods__['sense'] = _pyfreeling.sense_info_sense_set
            __swig_getmethods__['sense'] = _pyfreeling.sense_info_sense_get
            if _newclass:
                sense = _swig_property(_pyfreeling.sense_info_sense_get, _pyfreeling.sense_info_sense_set)
            __swig_setmethods__['parents'] = _pyfreeling.sense_info_parents_set
            __swig_getmethods__['parents'] = _pyfreeling.sense_info_parents_get
            if _newclass:
                parents = _swig_property(_pyfreeling.sense_info_parents_get, _pyfreeling.sense_info_parents_set)
            __swig_setmethods__['semfile'] = _pyfreeling.sense_info_semfile_set
            __swig_getmethods__['semfile'] = _pyfreeling.sense_info_semfile_get
            if _newclass:
                semfile = _swig_property(_pyfreeling.sense_info_semfile_get, _pyfreeling.sense_info_semfile_set)
            __swig_setmethods__['words'] = _pyfreeling.sense_info_words_set
            __swig_getmethods__['words'] = _pyfreeling.sense_info_words_get
            if _newclass:
                words = _swig_property(_pyfreeling.sense_info_words_get, _pyfreeling.sense_info_words_set)
            __swig_setmethods__['tonto'] = _pyfreeling.sense_info_tonto_set
            __swig_getmethods__['tonto'] = _pyfreeling.sense_info_tonto_get
            if _newclass:
                tonto = _swig_property(_pyfreeling.sense_info_tonto_get, _pyfreeling.sense_info_tonto_set)
            __swig_setmethods__['sumo'] = _pyfreeling.sense_info_sumo_set
            __swig_getmethods__['sumo'] = _pyfreeling.sense_info_sumo_get
            if _newclass:
                sumo = _swig_property(_pyfreeling.sense_info_sumo_get, _pyfreeling.sense_info_sumo_set)
            __swig_setmethods__['cyc'] = _pyfreeling.sense_info_cyc_set
            __swig_getmethods__['cyc'] = _pyfreeling.sense_info_cyc_get
            if _newclass:
                cyc = _swig_property(_pyfreeling.sense_info_cyc_get, _pyfreeling.sense_info_cyc_set)

            def __init__(self, arg2: 'std::wstring const &', arg3: 'std::wstring const &'):
                this = _pyfreeling.new_sense_info(arg2, arg3)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def get_parents_string(self) -> 'std::wstring':
                return _pyfreeling.sense_info_get_parents_stringself

            __swig_destroy__ = _pyfreeling.delete_sense_info
            __del__ = lambda self: None


        sense_info_swigregister = _pyfreeling.sense_info_swigregister
        sense_info_swigregister(sense_info)

        class semanticDB(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, semanticDB, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, semanticDB, name)
            __repr__ = _swig_repr

            def __init__(self, arg2: 'std::wstring const &'):
                this = _pyfreeling.new_semanticDBarg2
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_semanticDB
            __del__ = lambda self: None

            def get_WN_keys(self, arg2: 'std::wstring const &', arg3: 'std::wstring const &', arg4: 'std::wstring const &', arg5: 'std::list< std::pair< std::wstring,std::wstring >,std::allocator< std::pair< std::wstring,std::wstring > > > &') -> 'void':
                return _pyfreeling.semanticDB_get_WN_keys(self, arg2, arg3, arg4, arg5)

            def get_sense_words(self, arg2: 'std::wstring const &') -> 'std::list< std::wstring,std::allocator< std::wstring > >':
                return _pyfreeling.semanticDB_get_sense_words(self, arg2)

            def get_word_senses(self, arg2: 'std::wstring const &', arg3: 'std::wstring const &', arg4: 'std::wstring const &') -> 'std::list< std::wstring,std::allocator< std::wstring > >':
                return _pyfreeling.semanticDB_get_word_senses(self, arg2, arg3, arg4)

            def get_sense_info(self, arg2: 'std::wstring const &') -> 'freeling::sense_info':
                return _pyfreeling.semanticDB_get_sense_info(self, arg2)


        semanticDB_swigregister = _pyfreeling.semanticDB_swigregister
        semanticDB_swigregister(semanticDB)

        class tagset(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, tagset, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, tagset, name)
            __repr__ = _swig_repr

            def __init__(self, f: 'std::wstring const &'):
                this = _pyfreeling.new_tagsetf
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_tagset
            __del__ = lambda self: None

            def get_short_tag(self, tag: 'std::wstring const &') -> 'std::wstring':
                return _pyfreeling.tagset_get_short_tag(self, tag)

            def get_msd_features_map(self, tag: 'std::wstring const &') -> 'std::map< std::wstring,std::wstring,std::less< std::wstring >,std::allocator< std::pair< std::wstring const,std::wstring > > >':
                return _pyfreeling.tagset_get_msd_features_map(self, tag)

            def get_msd_features(self, tag: 'std::wstring const &') -> 'std::list< std::pair< std::wstring,std::wstring >,std::allocator< std::pair< std::wstring,std::wstring > > >':
                return _pyfreeling.tagset_get_msd_features(self, tag)

            def get_msd_string(self, tag: 'std::wstring const &') -> 'std::wstring':
                return _pyfreeling.tagset_get_msd_string(self, tag)

            def msd_to_tag(self, *args) -> 'std::wstring':
                return (_pyfreeling.tagset_msd_to_tag)(self, *args)


        tagset_swigregister = _pyfreeling.tagset_swigregister
        tagset_swigregister(tagset)

        class foma_FSM(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, foma_FSM, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, foma_FSM, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_foma_FSM)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_foma_FSM
            __del__ = lambda self: None

            def get_similar_words(self, arg2: 'std::wstring const &', arg3: 'ListAlternative') -> 'void':
                return _pyfreeling.foma_FSM_get_similar_words(self, arg2, arg3)

            def set_cutoff_threshold(self, arg2: 'int') -> 'void':
                return _pyfreeling.foma_FSM_set_cutoff_threshold(self, arg2)

            def set_num_matches(self, arg2: 'int') -> 'void':
                return _pyfreeling.foma_FSM_set_num_matches(self, arg2)

            def set_basic_operation_cost(self, arg2: 'int') -> 'void':
                return _pyfreeling.foma_FSM_set_basic_operation_cost(self, arg2)

            def set_operation_cost(self, arg2: 'std::wstring const &', arg3: 'std::wstring const &', arg4: 'int') -> 'void':
                return _pyfreeling.foma_FSM_set_operation_cost(self, arg2, arg3, arg4)

            def get_alphabet(self) -> 'std::set< std::wstring,std::less< std::wstring >,std::allocator< std::wstring > >':
                return _pyfreeling.foma_FSM_get_alphabetself


        foma_FSM_swigregister = _pyfreeling.foma_FSM_swigregister
        foma_FSM_swigregister(foma_FSM)

        class fex(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, fex, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, fex, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_fex)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_fex
            __del__ = lambda self: None

            def encode_all(self, arg2: 'sentence', arg3: 'VectorSetString', arg4: 'VectorSetInt') -> 'void':
                return _pyfreeling.fex_encode_all(self, arg2, arg3, arg4)

            def encode_name(self, *args) -> 'std::vector< std::set< std::wstring,std::less< std::wstring >,std::allocator< std::wstring > >,std::allocator< std::set< std::wstring,std::less< std::wstring >,std::allocator< std::wstring > > > >':
                return (_pyfreeling.fex_encode_name)(self, *args)

            def encode_int(self, *args) -> 'std::vector< std::set< int,std::less< int >,std::allocator< int > >,std::allocator< std::set< int,std::less< int >,std::allocator< int > > > >':
                return (_pyfreeling.fex_encode_int)(self, *args)

            def clear_lexicon(self) -> 'void':
                return _pyfreeling.fex_clear_lexiconself

            def encode_to_lexicon(self, arg2: 'sentence') -> 'void':
                return _pyfreeling.fex_encode_to_lexicon(self, arg2)

            def save_lexicon(self, arg2: 'std::wstring const &', arg3: 'double') -> 'void':
                return _pyfreeling.fex_save_lexicon(self, arg2, arg3)


        fex_swigregister = _pyfreeling.fex_swigregister
        fex_swigregister(fex)

        class fex_lexicon(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, fex_lexicon, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, fex_lexicon, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_fex_lexicon)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def clear_lexicon(self) -> 'void':
                return _pyfreeling.fex_lexicon_clear_lexiconself

            def add_occurrence(self, arg2: 'std::wstring const &') -> 'void':
                return _pyfreeling.fex_lexicon_add_occurrence(self, arg2)

            def save_lexicon(self, arg2: 'std::wstring const &', arg3: 'double') -> 'void':
                return _pyfreeling.fex_lexicon_save_lexicon(self, arg2, arg3)

            def get_code(self, arg2: 'std::wstring const &') -> 'unsigned int':
                return _pyfreeling.fex_lexicon_get_code(self, arg2)

            def get_freq(self, arg2: 'std::wstring const &') -> 'unsigned int':
                return _pyfreeling.fex_lexicon_get_freq(self, arg2)

            def contains_code(self, arg2: 'unsigned int') -> 'bool':
                return _pyfreeling.fex_lexicon_contains_code(self, arg2)

            def is_empty(self) -> 'bool':
                return _pyfreeling.fex_lexicon_is_emptyself

            __swig_destroy__ = _pyfreeling.delete_fex_lexicon
            __del__ = lambda self: None


        fex_lexicon_swigregister = _pyfreeling.fex_lexicon_swigregister
        fex_lexicon_swigregister(fex_lexicon)

        class util(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, util, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, util, name)
            __repr__ = _swig_repr
            if _newclass:
                init_locale = staticmethod(_pyfreeling.util_init_locale)
            else:
                init_locale = _pyfreeling.util_init_locale
            if _newclass:
                wstring2int = staticmethod(_pyfreeling.util_wstring2int)
            else:
                wstring2int = _pyfreeling.util_wstring2int
            if _newclass:
                int2wstring = staticmethod(_pyfreeling.util_int2wstring)
            else:
                int2wstring = _pyfreeling.util_int2wstring
            if _newclass:
                wstring2double = staticmethod(_pyfreeling.util_wstring2double)
            else:
                wstring2double = _pyfreeling.util_wstring2double
            if _newclass:
                double2wstring = staticmethod(_pyfreeling.util_double2wstring)
            else:
                double2wstring = _pyfreeling.util_double2wstring
            if _newclass:
                wstring2longdouble = staticmethod(_pyfreeling.util_wstring2longdouble)
            else:
                wstring2longdouble = _pyfreeling.util_wstring2longdouble
            if _newclass:
                longdouble2wstring = staticmethod(_pyfreeling.util_longdouble2wstring)
            else:
                longdouble2wstring = _pyfreeling.util_longdouble2wstring
            if _newclass:
                vector2wstring = staticmethod(_pyfreeling.util_vector2wstring)
            else:
                vector2wstring = _pyfreeling.util_vector2wstring
            if _newclass:
                list2wstring = staticmethod(_pyfreeling.util_list2wstring)
            else:
                list2wstring = _pyfreeling.util_list2wstring
            if _newclass:
                pairlist2wstring = staticmethod(_pyfreeling.util_pairlist2wstring)
            else:
                pairlist2wstring = _pyfreeling.util_pairlist2wstring
            if _newclass:
                wstring2list = staticmethod(_pyfreeling.util_wstring2list)
            else:
                wstring2list = _pyfreeling.util_wstring2list
            if _newclass:
                wstring2vector = staticmethod(_pyfreeling.util_wstring2vector)
            else:
                wstring2vector = _pyfreeling.util_wstring2vector
            if _newclass:
                capitalization = staticmethod(_pyfreeling.util_capitalization)
            else:
                capitalization = _pyfreeling.util_capitalization
            if _newclass:
                capitalize = staticmethod(_pyfreeling.util_capitalize)
            else:
                capitalize = _pyfreeling.util_capitalize
            if _newclass:
                lowercase = staticmethod(_pyfreeling.util_lowercase)
            else:
                lowercase = _pyfreeling.util_lowercase
            if _newclass:
                uppercase = staticmethod(_pyfreeling.util_uppercase)
            else:
                uppercase = _pyfreeling.util_uppercase

            def __init__(self):
                this = _pyfreeling.new_util()
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_util
            __del__ = lambda self: None


        util_swigregister = _pyfreeling.util_swigregister
        util_swigregister(util)

        def util_init_locale(arg2: 'std::wstring const &') -> 'void':
            return _pyfreeling.util_init_localearg2


        util_init_locale = _pyfreeling.util_init_locale

        def util_wstring2int(arg2: 'std::wstring const &') -> 'int':
            return _pyfreeling.util_wstring2intarg2


        util_wstring2int = _pyfreeling.util_wstring2int

        def util_int2wstring(arg2: 'int const') -> 'std::wstring':
            return _pyfreeling.util_int2wstringarg2


        util_int2wstring = _pyfreeling.util_int2wstring

        def util_wstring2double(arg2: 'std::wstring const &') -> 'double':
            return _pyfreeling.util_wstring2doublearg2


        util_wstring2double = _pyfreeling.util_wstring2double

        def util_double2wstring(arg2: 'double const') -> 'std::wstring':
            return _pyfreeling.util_double2wstringarg2


        util_double2wstring = _pyfreeling.util_double2wstring

        def util_wstring2longdouble(arg2: 'std::wstring const &') -> 'long double':
            return _pyfreeling.util_wstring2longdoublearg2


        util_wstring2longdouble = _pyfreeling.util_wstring2longdouble

        def util_longdouble2wstring(arg2: 'long double const') -> 'std::wstring':
            return _pyfreeling.util_longdouble2wstringarg2


        util_longdouble2wstring = _pyfreeling.util_longdouble2wstring

        def util_vector2wstring(arg2: 'VectorString', arg3: 'std::wstring const &') -> 'std::wstring':
            return _pyfreeling.util_vector2wstring(arg2, arg3)


        util_vector2wstring = _pyfreeling.util_vector2wstring

        def util_list2wstring(arg2: 'ListString', arg3: 'std::wstring const &') -> 'std::wstring':
            return _pyfreeling.util_list2wstring(arg2, arg3)


        util_list2wstring = _pyfreeling.util_list2wstring

        def util_pairlist2wstring(*args) -> 'std::wstring':
            return (_pyfreeling.util_pairlist2wstring)(*args)


        util_pairlist2wstring = _pyfreeling.util_pairlist2wstring

        def util_wstring2list(arg2: 'std::wstring const &', arg3: 'std::wstring const &') -> 'std::list< std::wstring,std::allocator< std::wstring > >':
            return _pyfreeling.util_wstring2list(arg2, arg3)


        util_wstring2list = _pyfreeling.util_wstring2list

        def util_wstring2vector(arg2: 'std::wstring const &', arg3: 'std::wstring const &') -> 'std::vector< std::wstring,std::allocator< std::wstring > >':
            return _pyfreeling.util_wstring2vector(arg2, arg3)


        util_wstring2vector = _pyfreeling.util_wstring2vector

        def util_capitalization(arg2: 'std::wstring const &') -> 'int':
            return _pyfreeling.util_capitalizationarg2


        util_capitalization = _pyfreeling.util_capitalization

        def util_capitalize(arg2: 'std::wstring const &', arg3: 'int', arg4: 'bool') -> 'std::wstring':
            return _pyfreeling.util_capitalize(arg2, arg3, arg4)


        util_capitalize = _pyfreeling.util_capitalize

        def util_lowercase(arg2: 'std::wstring const &') -> 'std::wstring':
            return _pyfreeling.util_lowercasearg2


        util_lowercase = _pyfreeling.util_lowercase

        def util_uppercase(arg2: 'std::wstring const &') -> 'std::wstring':
            return _pyfreeling.util_uppercasearg2


        util_uppercase = _pyfreeling.util_uppercase

        class input_conll(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, input_conll, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, input_conll, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_input_conll)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_input_conll
            __del__ = lambda self: None

            def input_sentences(self, lines: 'std::wstring const &', ls: 'ListSentence') -> 'void':
                return _pyfreeling.input_conll_input_sentences(self, lines, ls)

            def input_document(self, lines: 'std::wstring const &', doc: 'document') -> 'void':
                return _pyfreeling.input_conll_input_document(self, lines, doc)


        input_conll_swigregister = _pyfreeling.input_conll_swigregister
        input_conll_swigregister(input_conll)

        class output_conll(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, output_conll, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, output_conll, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_output_conll)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_output_conll
            __del__ = lambda self: None

            def PrintHeader(self, sout: 'std::wostream &') -> 'void':
                return _pyfreeling.output_conll_PrintHeader(self, sout)

            def PrintFooter(self, sout: 'std::wostream &') -> 'void':
                return _pyfreeling.output_conll_PrintFooter(self, sout)

            def PrintResults(self, *args) -> 'std::wstring':
                return (_pyfreeling.output_conll_PrintResults)(self, *args)


        output_conll_swigregister = _pyfreeling.output_conll_swigregister
        output_conll_swigregister(output_conll)

        class input_freeling(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, input_freeling, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, input_freeling, name)
            __repr__ = _swig_repr

            def __init__(self):
                this = _pyfreeling.new_input_freeling()
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_input_freeling
            __del__ = lambda self: None

            def input_sentences(self, lines: 'std::wstring const &', ls: 'ListSentence') -> 'void':
                return _pyfreeling.input_freeling_input_sentences(self, lines, ls)


        input_freeling_swigregister = _pyfreeling.input_freeling_swigregister
        input_freeling_swigregister(input_freeling)

        class output_freeling(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, output_freeling, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, output_freeling, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_output_freeling)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_output_freeling
            __del__ = lambda self: None

            def PrintTree(self, sout: 'std::wostream &', n: 'TreeConstPreorderIteratorNode', depth: 'int') -> 'void':
                return _pyfreeling.output_freeling_PrintTree(self, sout, n, depth)

            def PrintDepTree(self, sout: 'std::wostream &', n: 'TreeConstPreorderIteratorDepnode', depth: 'int') -> 'void':
                return _pyfreeling.output_freeling_PrintDepTree(self, sout, n, depth)

            def PrintPredArgs(self, sout: 'std::wostream &', s: 'sentence') -> 'void':
                return _pyfreeling.output_freeling_PrintPredArgs(self, sout, s)

            def PrintWord(self, sout: 'std::wostream &', w: 'word', only_sel: 'bool'=True, probs: 'bool'=True) -> 'void':
                return _pyfreeling.output_freeling_PrintWord(self, sout, w, only_sel, probs)

            def PrintCorefs(self, sout: 'std::wostream &', doc: 'document') -> 'void':
                return _pyfreeling.output_freeling_PrintCorefs(self, sout, doc)

            def PrintSemgraph(self, sout: 'std::wostream &', doc: 'document') -> 'void':
                return _pyfreeling.output_freeling_PrintSemgraph(self, sout, doc)

            def PrintResults(self, *args) -> 'std::wstring':
                return (_pyfreeling.output_freeling_PrintResults)(self, *args)

            def output_senses(self, arg2: 'bool') -> 'void':
                return _pyfreeling.output_freeling_output_senses(self, arg2)

            def output_all_senses(self, arg2: 'bool') -> 'void':
                return _pyfreeling.output_freeling_output_all_senses(self, arg2)

            def output_phonetics(self, arg2: 'bool') -> 'void':
                return _pyfreeling.output_freeling_output_phonetics(self, arg2)

            def output_dep_tree(self, arg2: 'bool') -> 'void':
                return _pyfreeling.output_freeling_output_dep_tree(self, arg2)

            def output_corefs(self, arg2: 'bool') -> 'void':
                return _pyfreeling.output_freeling_output_corefs(self, arg2)

            def output_semgraph(self, arg2: 'bool') -> 'void':
                return _pyfreeling.output_freeling_output_semgraph(self, arg2)


        output_freeling_swigregister = _pyfreeling.output_freeling_swigregister
        output_freeling_swigregister(output_freeling)

        class output_json(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, output_json, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, output_json, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_output_json)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_output_json
            __del__ = lambda self: None

            def PrintResults(self, *args) -> 'std::wstring':
                return (_pyfreeling.output_json_PrintResults)(self, *args)


        output_json_swigregister = _pyfreeling.output_json_swigregister
        output_json_swigregister(output_json)

        class output_naf(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, output_naf, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, output_naf, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_output_naf)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_output_naf
            __del__ = lambda self: None

            def PrintResults(self, *args) -> 'std::wstring':
                return (_pyfreeling.output_naf_PrintResults)(self, *args)

            def PrintHeader(self, sout: 'std::wostream &') -> 'void':
                return _pyfreeling.output_naf_PrintHeader(self, sout)

            def PrintFooter(self, sout: 'std::wostream &') -> 'void':
                return _pyfreeling.output_naf_PrintFooter(self, sout)

            def ActivateLayer(self, ly: 'std::wstring const &', b: 'bool') -> 'void':
                return _pyfreeling.output_naf_ActivateLayer(self, ly, b)


        output_naf_swigregister = _pyfreeling.output_naf_swigregister
        output_naf_swigregister(output_naf)

        class output_train(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, output_train, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, output_train, name)
            __repr__ = _swig_repr

            def __init__(self):
                this = _pyfreeling.new_output_train()
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_output_train
            __del__ = lambda self: None

            def PrintResults(self, *args) -> 'std::wstring':
                return (_pyfreeling.output_train_PrintResults)(self, *args)


        output_train_swigregister = _pyfreeling.output_train_swigregister
        output_train_swigregister(output_train)

        class output_xml(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, output_xml, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, output_xml, name)
            __repr__ = _swig_repr

            def __init__(self, *args):
                this = (_pyfreeling.new_output_xml)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _pyfreeling.delete_output_xml
            __del__ = lambda self: None

            def PrintHeader(self, sout: 'std::wostream &') -> 'void':
                return _pyfreeling.output_xml_PrintHeader(self, sout)

            def PrintFooter(self, sout: 'std::wostream &') -> 'void':
                return _pyfreeling.output_xml_PrintFooter(self, sout)

            def PrintResults(self, *args) -> 'std::wstring':
                return (_pyfreeling.output_xml_PrintResults)(self, *args)


        output_xml_swigregister = _pyfreeling.output_xml_swigregister
        output_xml_swigregister(output_xml)