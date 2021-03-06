# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: CVXcanon.py
# Compiled at: 2015-06-06 13:26:45
from sys import version_info
if version_info >= (2, 6, 0):

    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_CVXcanon', [dirname(__file__)])
        except ImportError:
            import _CVXcanon
            return _CVXcanon

        if fp is not None:
            try:
                _mod = imp.load_module('_CVXcanon', fp, pathname, description)
            finally:
                fp.close()

            return _mod
        else:
            return


    _CVXcanon = swig_import_helper()
    del swig_import_helper
else:
    import _CVXcanon
del version_info
try:
    _swig_property = property
except NameError:
    pass

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == 'thisown':
        return self.this.own(value)
    else:
        if name == 'this':
            if type(value).__name__ == 'SwigPyObject':
                self.__dict__[name] = value
                return
        method = class_type.__swig_setmethods__.get(name, None)
        if method:
            return method(self, value)
        if not static:
            self.__dict__[name] = value
        else:
            raise AttributeError('You cannot add attributes to %s' % self)
        return


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == 'thisown':
        return self.this.own()
    else:
        method = class_type.__swig_getmethods__.get(name, None)
        if method:
            return method(self)
        raise AttributeError(name)
        return


def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except:
        strthis = ''

    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


try:
    _object = object
    _newclass = 1
except AttributeError:

    class _object:
        pass


    _newclass = 0

class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined - class is abstract')

    __repr__ = _swig_repr
    __swig_destroy__ = _CVXcanon.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self):
        return _CVXcanon.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _CVXcanon.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _CVXcanon.SwigPyIterator_decr(self, n)

    def distance(self, *args):
        return _CVXcanon.SwigPyIterator_distance(self, *args)

    def equal(self, *args):
        return _CVXcanon.SwigPyIterator_equal(self, *args)

    def copy(self):
        return _CVXcanon.SwigPyIterator_copy(self)

    def next(self):
        return _CVXcanon.SwigPyIterator_next(self)

    def __next__(self):
        return _CVXcanon.SwigPyIterator___next__(self)

    def previous(self):
        return _CVXcanon.SwigPyIterator_previous(self)

    def advance(self, *args):
        return _CVXcanon.SwigPyIterator_advance(self, *args)

    def __eq__(self, *args):
        return _CVXcanon.SwigPyIterator___eq__(self, *args)

    def __ne__(self, *args):
        return _CVXcanon.SwigPyIterator___ne__(self, *args)

    def __iadd__(self, *args):
        return _CVXcanon.SwigPyIterator___iadd__(self, *args)

    def __isub__(self, *args):
        return _CVXcanon.SwigPyIterator___isub__(self, *args)

    def __add__(self, *args):
        return _CVXcanon.SwigPyIterator___add__(self, *args)

    def __sub__(self, *args):
        return _CVXcanon.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


SwigPyIterator_swigregister = _CVXcanon.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)
VARIABLE = _CVXcanon.VARIABLE
PROMOTE = _CVXcanon.PROMOTE
MUL = _CVXcanon.MUL
RMUL = _CVXcanon.RMUL
MUL_ELEM = _CVXcanon.MUL_ELEM
DIV = _CVXcanon.DIV
SUM = _CVXcanon.SUM
NEG = _CVXcanon.NEG
INDEX = _CVXcanon.INDEX
TRANSPOSE = _CVXcanon.TRANSPOSE
SUM_ENTRIES = _CVXcanon.SUM_ENTRIES
TRACE = _CVXcanon.TRACE
RESHAPE = _CVXcanon.RESHAPE
DIAG_VEC = _CVXcanon.DIAG_VEC
DIAG_MAT = _CVXcanon.DIAG_MAT
UPPER_TRI = _CVXcanon.UPPER_TRI
CONV = _CVXcanon.CONV
HSTACK = _CVXcanon.HSTACK
VSTACK = _CVXcanon.VSTACK
SCALAR_CONST = _CVXcanon.SCALAR_CONST
DENSE_CONST = _CVXcanon.DENSE_CONST
SPARSE_CONST = _CVXcanon.SPARSE_CONST
NO_OP = _CVXcanon.NO_OP

class LinOp(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LinOp, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LinOp, name)
    __repr__ = _swig_repr
    __swig_setmethods__['type'] = _CVXcanon.LinOp_type_set
    __swig_getmethods__['type'] = _CVXcanon.LinOp_type_get
    if _newclass:
        type = _swig_property(_CVXcanon.LinOp_type_get, _CVXcanon.LinOp_type_set)
    __swig_setmethods__['size'] = _CVXcanon.LinOp_size_set
    __swig_getmethods__['size'] = _CVXcanon.LinOp_size_get
    if _newclass:
        size = _swig_property(_CVXcanon.LinOp_size_get, _CVXcanon.LinOp_size_set)
    __swig_setmethods__['args'] = _CVXcanon.LinOp_args_set
    __swig_getmethods__['args'] = _CVXcanon.LinOp_args_get
    if _newclass:
        args = _swig_property(_CVXcanon.LinOp_args_get, _CVXcanon.LinOp_args_set)
    __swig_setmethods__['sparse'] = _CVXcanon.LinOp_sparse_set
    __swig_getmethods__['sparse'] = _CVXcanon.LinOp_sparse_get
    if _newclass:
        sparse = _swig_property(_CVXcanon.LinOp_sparse_get, _CVXcanon.LinOp_sparse_set)
    __swig_setmethods__['sparse_data'] = _CVXcanon.LinOp_sparse_data_set
    __swig_getmethods__['sparse_data'] = _CVXcanon.LinOp_sparse_data_get
    if _newclass:
        sparse_data = _swig_property(_CVXcanon.LinOp_sparse_data_get, _CVXcanon.LinOp_sparse_data_set)
    __swig_setmethods__['dense_data'] = _CVXcanon.LinOp_dense_data_set
    __swig_getmethods__['dense_data'] = _CVXcanon.LinOp_dense_data_get
    if _newclass:
        dense_data = _swig_property(_CVXcanon.LinOp_dense_data_get, _CVXcanon.LinOp_dense_data_set)
    __swig_setmethods__['slice'] = _CVXcanon.LinOp_slice_set
    __swig_getmethods__['slice'] = _CVXcanon.LinOp_slice_get
    if _newclass:
        slice = _swig_property(_CVXcanon.LinOp_slice_get, _CVXcanon.LinOp_slice_set)

    def has_constant_type(self):
        return _CVXcanon.LinOp_has_constant_type(self)

    def set_dense_data(self, *args):
        return _CVXcanon.LinOp_set_dense_data(self, *args)

    def set_sparse_data(self, *args):
        return _CVXcanon.LinOp_set_sparse_data(self, *args)

    def __init__(self):
        this = _CVXcanon.new_LinOp()
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _CVXcanon.delete_LinOp
    __del__ = lambda self: None


LinOp_swigregister = _CVXcanon.LinOp_swigregister
LinOp_swigregister(LinOp)
cvar = _CVXcanon.cvar
CONSTANT_ID = cvar.CONSTANT_ID

class ProblemData(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ProblemData, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ProblemData, name)
    __repr__ = _swig_repr
    __swig_setmethods__['V'] = _CVXcanon.ProblemData_V_set
    __swig_getmethods__['V'] = _CVXcanon.ProblemData_V_get
    if _newclass:
        V = _swig_property(_CVXcanon.ProblemData_V_get, _CVXcanon.ProblemData_V_set)
    __swig_setmethods__['I'] = _CVXcanon.ProblemData_I_set
    __swig_getmethods__['I'] = _CVXcanon.ProblemData_I_get
    if _newclass:
        I = _swig_property(_CVXcanon.ProblemData_I_get, _CVXcanon.ProblemData_I_set)
    __swig_setmethods__['J'] = _CVXcanon.ProblemData_J_set
    __swig_getmethods__['J'] = _CVXcanon.ProblemData_J_get
    if _newclass:
        J = _swig_property(_CVXcanon.ProblemData_J_get, _CVXcanon.ProblemData_J_set)
    __swig_setmethods__['const_vec'] = _CVXcanon.ProblemData_const_vec_set
    __swig_getmethods__['const_vec'] = _CVXcanon.ProblemData_const_vec_get
    if _newclass:
        const_vec = _swig_property(_CVXcanon.ProblemData_const_vec_get, _CVXcanon.ProblemData_const_vec_set)
    __swig_setmethods__['id_to_col'] = _CVXcanon.ProblemData_id_to_col_set
    __swig_getmethods__['id_to_col'] = _CVXcanon.ProblemData_id_to_col_get
    if _newclass:
        id_to_col = _swig_property(_CVXcanon.ProblemData_id_to_col_get, _CVXcanon.ProblemData_id_to_col_set)
    __swig_setmethods__['const_to_row'] = _CVXcanon.ProblemData_const_to_row_set
    __swig_getmethods__['const_to_row'] = _CVXcanon.ProblemData_const_to_row_get
    if _newclass:
        const_to_row = _swig_property(_CVXcanon.ProblemData_const_to_row_get, _CVXcanon.ProblemData_const_to_row_set)

    def getV(self, *args):
        return _CVXcanon.ProblemData_getV(self, *args)

    def getI(self, *args):
        return _CVXcanon.ProblemData_getI(self, *args)

    def getJ(self, *args):
        return _CVXcanon.ProblemData_getJ(self, *args)

    def getConstVec(self, *args):
        return _CVXcanon.ProblemData_getConstVec(self, *args)

    def __init__(self):
        this = _CVXcanon.new_ProblemData()
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _CVXcanon.delete_ProblemData
    __del__ = lambda self: None


ProblemData_swigregister = _CVXcanon.ProblemData_swigregister
ProblemData_swigregister(ProblemData)

class IntVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IntVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IntVector, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _CVXcanon.IntVector_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CVXcanon.IntVector___nonzero__(self)

    def __bool__(self):
        return _CVXcanon.IntVector___bool__(self)

    def __len__(self):
        return _CVXcanon.IntVector___len__(self)

    def pop(self):
        return _CVXcanon.IntVector_pop(self)

    def __getslice__(self, *args):
        return _CVXcanon.IntVector___getslice__(self, *args)

    def __setslice__(self, *args):
        return _CVXcanon.IntVector___setslice__(self, *args)

    def __delslice__(self, *args):
        return _CVXcanon.IntVector___delslice__(self, *args)

    def __delitem__(self, *args):
        return _CVXcanon.IntVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CVXcanon.IntVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CVXcanon.IntVector___setitem__(self, *args)

    def append(self, *args):
        return _CVXcanon.IntVector_append(self, *args)

    def empty(self):
        return _CVXcanon.IntVector_empty(self)

    def size(self):
        return _CVXcanon.IntVector_size(self)

    def clear(self):
        return _CVXcanon.IntVector_clear(self)

    def swap(self, *args):
        return _CVXcanon.IntVector_swap(self, *args)

    def get_allocator(self):
        return _CVXcanon.IntVector_get_allocator(self)

    def begin(self):
        return _CVXcanon.IntVector_begin(self)

    def end(self):
        return _CVXcanon.IntVector_end(self)

    def rbegin(self):
        return _CVXcanon.IntVector_rbegin(self)

    def rend(self):
        return _CVXcanon.IntVector_rend(self)

    def pop_back(self):
        return _CVXcanon.IntVector_pop_back(self)

    def erase(self, *args):
        return _CVXcanon.IntVector_erase(self, *args)

    def __init__(self, *args):
        this = _CVXcanon.new_IntVector(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def push_back(self, *args):
        return _CVXcanon.IntVector_push_back(self, *args)

    def front(self):
        return _CVXcanon.IntVector_front(self)

    def back(self):
        return _CVXcanon.IntVector_back(self)

    def assign(self, *args):
        return _CVXcanon.IntVector_assign(self, *args)

    def resize(self, *args):
        return _CVXcanon.IntVector_resize(self, *args)

    def insert(self, *args):
        return _CVXcanon.IntVector_insert(self, *args)

    def reserve(self, *args):
        return _CVXcanon.IntVector_reserve(self, *args)

    def capacity(self):
        return _CVXcanon.IntVector_capacity(self)

    __swig_destroy__ = _CVXcanon.delete_IntVector
    __del__ = lambda self: None


IntVector_swigregister = _CVXcanon.IntVector_swigregister
IntVector_swigregister(IntVector)

class DoubleVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DoubleVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DoubleVector, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _CVXcanon.DoubleVector_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CVXcanon.DoubleVector___nonzero__(self)

    def __bool__(self):
        return _CVXcanon.DoubleVector___bool__(self)

    def __len__(self):
        return _CVXcanon.DoubleVector___len__(self)

    def pop(self):
        return _CVXcanon.DoubleVector_pop(self)

    def __getslice__(self, *args):
        return _CVXcanon.DoubleVector___getslice__(self, *args)

    def __setslice__(self, *args):
        return _CVXcanon.DoubleVector___setslice__(self, *args)

    def __delslice__(self, *args):
        return _CVXcanon.DoubleVector___delslice__(self, *args)

    def __delitem__(self, *args):
        return _CVXcanon.DoubleVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CVXcanon.DoubleVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CVXcanon.DoubleVector___setitem__(self, *args)

    def append(self, *args):
        return _CVXcanon.DoubleVector_append(self, *args)

    def empty(self):
        return _CVXcanon.DoubleVector_empty(self)

    def size(self):
        return _CVXcanon.DoubleVector_size(self)

    def clear(self):
        return _CVXcanon.DoubleVector_clear(self)

    def swap(self, *args):
        return _CVXcanon.DoubleVector_swap(self, *args)

    def get_allocator(self):
        return _CVXcanon.DoubleVector_get_allocator(self)

    def begin(self):
        return _CVXcanon.DoubleVector_begin(self)

    def end(self):
        return _CVXcanon.DoubleVector_end(self)

    def rbegin(self):
        return _CVXcanon.DoubleVector_rbegin(self)

    def rend(self):
        return _CVXcanon.DoubleVector_rend(self)

    def pop_back(self):
        return _CVXcanon.DoubleVector_pop_back(self)

    def erase(self, *args):
        return _CVXcanon.DoubleVector_erase(self, *args)

    def __init__(self, *args):
        this = _CVXcanon.new_DoubleVector(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def push_back(self, *args):
        return _CVXcanon.DoubleVector_push_back(self, *args)

    def front(self):
        return _CVXcanon.DoubleVector_front(self)

    def back(self):
        return _CVXcanon.DoubleVector_back(self)

    def assign(self, *args):
        return _CVXcanon.DoubleVector_assign(self, *args)

    def resize(self, *args):
        return _CVXcanon.DoubleVector_resize(self, *args)

    def insert(self, *args):
        return _CVXcanon.DoubleVector_insert(self, *args)

    def reserve(self, *args):
        return _CVXcanon.DoubleVector_reserve(self, *args)

    def capacity(self):
        return _CVXcanon.DoubleVector_capacity(self)

    __swig_destroy__ = _CVXcanon.delete_DoubleVector
    __del__ = lambda self: None


DoubleVector_swigregister = _CVXcanon.DoubleVector_swigregister
DoubleVector_swigregister(DoubleVector)

class IntVector2D(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IntVector2D, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IntVector2D, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _CVXcanon.IntVector2D_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CVXcanon.IntVector2D___nonzero__(self)

    def __bool__(self):
        return _CVXcanon.IntVector2D___bool__(self)

    def __len__(self):
        return _CVXcanon.IntVector2D___len__(self)

    def pop(self):
        return _CVXcanon.IntVector2D_pop(self)

    def __getslice__(self, *args):
        return _CVXcanon.IntVector2D___getslice__(self, *args)

    def __setslice__(self, *args):
        return _CVXcanon.IntVector2D___setslice__(self, *args)

    def __delslice__(self, *args):
        return _CVXcanon.IntVector2D___delslice__(self, *args)

    def __delitem__(self, *args):
        return _CVXcanon.IntVector2D___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CVXcanon.IntVector2D___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CVXcanon.IntVector2D___setitem__(self, *args)

    def append(self, *args):
        return _CVXcanon.IntVector2D_append(self, *args)

    def empty(self):
        return _CVXcanon.IntVector2D_empty(self)

    def size(self):
        return _CVXcanon.IntVector2D_size(self)

    def clear(self):
        return _CVXcanon.IntVector2D_clear(self)

    def swap(self, *args):
        return _CVXcanon.IntVector2D_swap(self, *args)

    def get_allocator(self):
        return _CVXcanon.IntVector2D_get_allocator(self)

    def begin(self):
        return _CVXcanon.IntVector2D_begin(self)

    def end(self):
        return _CVXcanon.IntVector2D_end(self)

    def rbegin(self):
        return _CVXcanon.IntVector2D_rbegin(self)

    def rend(self):
        return _CVXcanon.IntVector2D_rend(self)

    def pop_back(self):
        return _CVXcanon.IntVector2D_pop_back(self)

    def erase(self, *args):
        return _CVXcanon.IntVector2D_erase(self, *args)

    def __init__(self, *args):
        this = _CVXcanon.new_IntVector2D(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def push_back(self, *args):
        return _CVXcanon.IntVector2D_push_back(self, *args)

    def front(self):
        return _CVXcanon.IntVector2D_front(self)

    def back(self):
        return _CVXcanon.IntVector2D_back(self)

    def assign(self, *args):
        return _CVXcanon.IntVector2D_assign(self, *args)

    def resize(self, *args):
        return _CVXcanon.IntVector2D_resize(self, *args)

    def insert(self, *args):
        return _CVXcanon.IntVector2D_insert(self, *args)

    def reserve(self, *args):
        return _CVXcanon.IntVector2D_reserve(self, *args)

    def capacity(self):
        return _CVXcanon.IntVector2D_capacity(self)

    __swig_destroy__ = _CVXcanon.delete_IntVector2D
    __del__ = lambda self: None


IntVector2D_swigregister = _CVXcanon.IntVector2D_swigregister
IntVector2D_swigregister(IntVector2D)

class DoubleVector2D(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DoubleVector2D, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DoubleVector2D, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _CVXcanon.DoubleVector2D_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CVXcanon.DoubleVector2D___nonzero__(self)

    def __bool__(self):
        return _CVXcanon.DoubleVector2D___bool__(self)

    def __len__(self):
        return _CVXcanon.DoubleVector2D___len__(self)

    def pop(self):
        return _CVXcanon.DoubleVector2D_pop(self)

    def __getslice__(self, *args):
        return _CVXcanon.DoubleVector2D___getslice__(self, *args)

    def __setslice__(self, *args):
        return _CVXcanon.DoubleVector2D___setslice__(self, *args)

    def __delslice__(self, *args):
        return _CVXcanon.DoubleVector2D___delslice__(self, *args)

    def __delitem__(self, *args):
        return _CVXcanon.DoubleVector2D___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CVXcanon.DoubleVector2D___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CVXcanon.DoubleVector2D___setitem__(self, *args)

    def append(self, *args):
        return _CVXcanon.DoubleVector2D_append(self, *args)

    def empty(self):
        return _CVXcanon.DoubleVector2D_empty(self)

    def size(self):
        return _CVXcanon.DoubleVector2D_size(self)

    def clear(self):
        return _CVXcanon.DoubleVector2D_clear(self)

    def swap(self, *args):
        return _CVXcanon.DoubleVector2D_swap(self, *args)

    def get_allocator(self):
        return _CVXcanon.DoubleVector2D_get_allocator(self)

    def begin(self):
        return _CVXcanon.DoubleVector2D_begin(self)

    def end(self):
        return _CVXcanon.DoubleVector2D_end(self)

    def rbegin(self):
        return _CVXcanon.DoubleVector2D_rbegin(self)

    def rend(self):
        return _CVXcanon.DoubleVector2D_rend(self)

    def pop_back(self):
        return _CVXcanon.DoubleVector2D_pop_back(self)

    def erase(self, *args):
        return _CVXcanon.DoubleVector2D_erase(self, *args)

    def __init__(self, *args):
        this = _CVXcanon.new_DoubleVector2D(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def push_back(self, *args):
        return _CVXcanon.DoubleVector2D_push_back(self, *args)

    def front(self):
        return _CVXcanon.DoubleVector2D_front(self)

    def back(self):
        return _CVXcanon.DoubleVector2D_back(self)

    def assign(self, *args):
        return _CVXcanon.DoubleVector2D_assign(self, *args)

    def resize(self, *args):
        return _CVXcanon.DoubleVector2D_resize(self, *args)

    def insert(self, *args):
        return _CVXcanon.DoubleVector2D_insert(self, *args)

    def reserve(self, *args):
        return _CVXcanon.DoubleVector2D_reserve(self, *args)

    def capacity(self):
        return _CVXcanon.DoubleVector2D_capacity(self)

    __swig_destroy__ = _CVXcanon.delete_DoubleVector2D
    __del__ = lambda self: None


DoubleVector2D_swigregister = _CVXcanon.DoubleVector2D_swigregister
DoubleVector2D_swigregister(DoubleVector2D)

class IntIntMap(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IntIntMap, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IntIntMap, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _CVXcanon.IntIntMap_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CVXcanon.IntIntMap___nonzero__(self)

    def __bool__(self):
        return _CVXcanon.IntIntMap___bool__(self)

    def __len__(self):
        return _CVXcanon.IntIntMap___len__(self)

    def __iter__(self):
        return self.key_iterator()

    def iterkeys(self):
        return self.key_iterator()

    def itervalues(self):
        return self.value_iterator()

    def iteritems(self):
        return self.iterator()

    def __getitem__(self, *args):
        return _CVXcanon.IntIntMap___getitem__(self, *args)

    def __delitem__(self, *args):
        return _CVXcanon.IntIntMap___delitem__(self, *args)

    def has_key(self, *args):
        return _CVXcanon.IntIntMap_has_key(self, *args)

    def keys(self):
        return _CVXcanon.IntIntMap_keys(self)

    def values(self):
        return _CVXcanon.IntIntMap_values(self)

    def items(self):
        return _CVXcanon.IntIntMap_items(self)

    def __contains__(self, *args):
        return _CVXcanon.IntIntMap___contains__(self, *args)

    def key_iterator(self):
        return _CVXcanon.IntIntMap_key_iterator(self)

    def value_iterator(self):
        return _CVXcanon.IntIntMap_value_iterator(self)

    def __setitem__(self, *args):
        return _CVXcanon.IntIntMap___setitem__(self, *args)

    def asdict(self):
        return _CVXcanon.IntIntMap_asdict(self)

    def __init__(self, *args):
        this = _CVXcanon.new_IntIntMap(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def empty(self):
        return _CVXcanon.IntIntMap_empty(self)

    def size(self):
        return _CVXcanon.IntIntMap_size(self)

    def clear(self):
        return _CVXcanon.IntIntMap_clear(self)

    def swap(self, *args):
        return _CVXcanon.IntIntMap_swap(self, *args)

    def get_allocator(self):
        return _CVXcanon.IntIntMap_get_allocator(self)

    def begin(self):
        return _CVXcanon.IntIntMap_begin(self)

    def end(self):
        return _CVXcanon.IntIntMap_end(self)

    def rbegin(self):
        return _CVXcanon.IntIntMap_rbegin(self)

    def rend(self):
        return _CVXcanon.IntIntMap_rend(self)

    def count(self, *args):
        return _CVXcanon.IntIntMap_count(self, *args)

    def erase(self, *args):
        return _CVXcanon.IntIntMap_erase(self, *args)

    def find(self, *args):
        return _CVXcanon.IntIntMap_find(self, *args)

    def lower_bound(self, *args):
        return _CVXcanon.IntIntMap_lower_bound(self, *args)

    def upper_bound(self, *args):
        return _CVXcanon.IntIntMap_upper_bound(self, *args)

    __swig_destroy__ = _CVXcanon.delete_IntIntMap
    __del__ = lambda self: None


IntIntMap_swigregister = _CVXcanon.IntIntMap_swigregister
IntIntMap_swigregister(IntIntMap)

class LinOpVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LinOpVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LinOpVector, name)
    __repr__ = _swig_repr

    def iterator(self):
        return _CVXcanon.LinOpVector_iterator(self)

    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CVXcanon.LinOpVector___nonzero__(self)

    def __bool__(self):
        return _CVXcanon.LinOpVector___bool__(self)

    def __len__(self):
        return _CVXcanon.LinOpVector___len__(self)

    def pop(self):
        return _CVXcanon.LinOpVector_pop(self)

    def __getslice__(self, *args):
        return _CVXcanon.LinOpVector___getslice__(self, *args)

    def __setslice__(self, *args):
        return _CVXcanon.LinOpVector___setslice__(self, *args)

    def __delslice__(self, *args):
        return _CVXcanon.LinOpVector___delslice__(self, *args)

    def __delitem__(self, *args):
        return _CVXcanon.LinOpVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CVXcanon.LinOpVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CVXcanon.LinOpVector___setitem__(self, *args)

    def append(self, *args):
        return _CVXcanon.LinOpVector_append(self, *args)

    def empty(self):
        return _CVXcanon.LinOpVector_empty(self)

    def size(self):
        return _CVXcanon.LinOpVector_size(self)

    def clear(self):
        return _CVXcanon.LinOpVector_clear(self)

    def swap(self, *args):
        return _CVXcanon.LinOpVector_swap(self, *args)

    def get_allocator(self):
        return _CVXcanon.LinOpVector_get_allocator(self)

    def begin(self):
        return _CVXcanon.LinOpVector_begin(self)

    def end(self):
        return _CVXcanon.LinOpVector_end(self)

    def rbegin(self):
        return _CVXcanon.LinOpVector_rbegin(self)

    def rend(self):
        return _CVXcanon.LinOpVector_rend(self)

    def pop_back(self):
        return _CVXcanon.LinOpVector_pop_back(self)

    def erase(self, *args):
        return _CVXcanon.LinOpVector_erase(self, *args)

    def __init__(self, *args):
        this = _CVXcanon.new_LinOpVector(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def push_back(self, *args):
        return _CVXcanon.LinOpVector_push_back(self, *args)

    def front(self):
        return _CVXcanon.LinOpVector_front(self)

    def back(self):
        return _CVXcanon.LinOpVector_back(self)

    def assign(self, *args):
        return _CVXcanon.LinOpVector_assign(self, *args)

    def resize(self, *args):
        return _CVXcanon.LinOpVector_resize(self, *args)

    def insert(self, *args):
        return _CVXcanon.LinOpVector_insert(self, *args)

    def reserve(self, *args):
        return _CVXcanon.LinOpVector_reserve(self, *args)

    def capacity(self):
        return _CVXcanon.LinOpVector_capacity(self)

    __swig_destroy__ = _CVXcanon.delete_LinOpVector
    __del__ = lambda self: None


LinOpVector_swigregister = _CVXcanon.LinOpVector_swigregister
LinOpVector_swigregister(LinOpVector)

def build_matrix(*args):
    return _CVXcanon.build_matrix(*args)


build_matrix = _CVXcanon.build_matrix