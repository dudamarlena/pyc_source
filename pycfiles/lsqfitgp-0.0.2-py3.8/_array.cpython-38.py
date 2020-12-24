# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/lsqfitgp/_array.py
# Compiled at: 2020-04-22 07:26:33
# Size of source mod 2**32: 4558 bytes
import builtins
from autograd import numpy as np
from autograd.builtins import isinstance
__all__ = [
 'StructuredArray']

def _readonlyview(x):
    if not builtins.isinstance(x, (StructuredArray, np.numpy_boxes.ArrayBox)):
        x = x.view()
        x.flags['WRITEABLE'] = False
    return x


def _wrapifstructured(x):
    if x.dtype.names is None:
        return x
    return StructuredArray(x)


def _broadcast_shapes_2(s1, s2):
    if not isinstance(s1, tuple):
        raise AssertionError
    else:
        assert isinstance(s2, tuple)
        if len(s1) < len(s2):
            s1 = (len(s2) - len(s1)) * (1, ) + s1
        else:
            if len(s2) < len(s1):
                s2 = (len(s1) - len(s2)) * (1, ) + s2
    out = ()
    for a, b in zip(s1, s2):
        if a == b:
            out += (a,)
        elif a == 1 or b == 1:
            out += (a * b,)
        else:
            raise ValueError('can not broadcast shape {} with {}'.format(s1, s2))
    else:
        return out


def broadcast_shapes(shapes):
    """
    Return the broadcasted shape from a list of shapes.
    """
    out = ()
    for shape in shapes:
        try:
            out = _broadcast_shapes_2(out, shape)
        except ValueError:
            msg = 'can not broadcast shapes '
            msg += ', '.join((str(s) for s in shapes))
            raise ValueError(msg)

    else:
        return out


class broadcast:
    __doc__ = '\n    Version of np.broadcast that works with StructuredArray.\n    '

    def __init__(self, *arrays):
        shapes = [a.shape for a in arrays]
        self.shape = broadcast_shapes(shapes)


def broadcast_to(x, shape, **kw):
    """
    Version of np.broadcast_to that works with StructuredArray.
    """
    if isinstance(x, StructuredArray):
        return (x.broadcast_to)(shape, **kw)
    return (np.broadcast_to)(x, shape, **kw)


def broadcast_arrays(*arrays, **kw):
    """
    Version of np.broadcast_arrays that works with StructuredArray.
    """
    shapes = [a.shape for a in arrays]
    shape = broadcast_shapes(shapes)
    return tuple((broadcast_to(a, shape, **kw) for a in arrays))


class StructuredArray:
    __doc__ = "\n    Autograd-friendly imitation of a numpy structured array. It behaves like\n    a read-only numpy array, with the exception that you can set a whole field.\n    Example:\n    \n    >>> a = np.empty(3, dtype=[('f', float), ('g', float)])\n    >>> a = StructuredArray(a)\n    >>> a['f'] = np.arange(3) # this is allowed\n    >>> a[1] = (0.3, 0.4) # this raises an error\n    "

    @classmethod
    def _fromarrayanddict(cls, x, d):
        out = super().__new__(cls)
        out.dtype = x.dtype
        out._dict = d
        f0 = x.dtype.names[0]
        a0 = d[f0]
        subshape = x.dtype.fields[f0][0].shape
        out.shape = a0.shape[:len(a0.shape) - len(subshape)]
        out.size = np.prod(out.shape)
        return out

    def __new__--- This code section failed: ---

 L. 104         0  LOAD_GLOBAL              isinstance
                2  LOAD_DEREF               'array'
                4  LOAD_GLOBAL              np
                6  LOAD_ATTR                ndarray
                8  LOAD_FAST                'cls'
               10  BUILD_TUPLE_2         2 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  LOAD_ASSERT              AssertionError
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 105        20  LOAD_DEREF               'array'
               22  LOAD_ATTR                dtype
               24  LOAD_ATTR                names
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  LOAD_ASSERT              AssertionError
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L. 106        36  LOAD_CLOSURE             'array'
               38  BUILD_TUPLE_1         1 
               40  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               42  LOAD_STR                 'StructuredArray.__new__.<locals>.<dictcomp>'
               44  MAKE_FUNCTION_8          'closure'

 L. 108        46  LOAD_DEREF               'array'
               48  LOAD_ATTR                dtype
               50  LOAD_ATTR                names

 L. 106        52  GET_ITER         
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'd'

 L. 110        58  LOAD_FAST                'cls'
               60  LOAD_METHOD              _fromarrayanddict
               62  LOAD_DEREF               'array'
               64  LOAD_FAST                'd'
               66  CALL_METHOD_2         2  ''
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 40

    def __getitem__--- This code section failed: ---

 L. 113         0  LOAD_GLOBAL              isinstance
                2  LOAD_DEREF               'key'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 114        10  LOAD_DEREF               'self'
               12  LOAD_ATTR                _dict
               14  LOAD_DEREF               'key'
               16  BINARY_SUBSCR    
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L. 115        20  LOAD_GLOBAL              isinstance
               22  LOAD_DEREF               'key'
               24  LOAD_GLOBAL              list
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    68  'to 68'
               30  LOAD_GLOBAL              all
               32  LOAD_GENEXPR             '<code_object <genexpr>>'
               34  LOAD_STR                 'StructuredArray.__getitem__.<locals>.<genexpr>'
               36  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               38  LOAD_DEREF               'key'
               40  GET_ITER         
               42  CALL_FUNCTION_1       1  ''
               44  CALL_FUNCTION_1       1  ''
               46  POP_JUMP_IF_FALSE    68  'to 68'

 L. 116        48  LOAD_CLOSURE             'self'
               50  BUILD_TUPLE_1         1 
               52  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               54  LOAD_STR                 'StructuredArray.__getitem__.<locals>.<dictcomp>'
               56  MAKE_FUNCTION_8          'closure'

 L. 118        58  LOAD_DEREF               'key'

 L. 116        60  GET_ITER         
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'd'
               66  JUMP_FORWARD         92  'to 92'
             68_0  COME_FROM            46  '46'
             68_1  COME_FROM            28  '28'

 L. 121        68  LOAD_CLOSURE             'key'
               70  BUILD_TUPLE_1         1 
               72  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               74  LOAD_STR                 'StructuredArray.__getitem__.<locals>.<dictcomp>'
               76  MAKE_FUNCTION_8          'closure'

 L. 123        78  LOAD_DEREF               'self'
               80  LOAD_ATTR                _dict
               82  LOAD_METHOD              items
               84  CALL_METHOD_0         0  ''

 L. 121        86  GET_ITER         
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'd'
             92_0  COME_FROM            66  '66'

 L. 125        92  LOAD_GLOBAL              type
               94  LOAD_DEREF               'self'
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_METHOD              _fromarrayanddict
              100  LOAD_DEREF               'self'
              102  LOAD_FAST                'd'
              104  CALL_METHOD_2         2  ''
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 52

    def __setitem__(self, key, val):
        assert key in self.dtype.names
        assert isinstance(val, (np.ndarray, StructuredArray))
        prev = self._dict[key]
        assert prev.dtype == val.dtype
        assert prev.shape == val.shape
        self._dict[key] = _readonlyview(val)

    def reshape--- This code section failed: ---

 L. 137         0  LOAD_GLOBAL              len
                2  LOAD_DEREF               'shape'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               1
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    34  'to 34'
               12  LOAD_GLOBAL              isinstance
               14  LOAD_DEREF               'shape'
               16  LOAD_CONST               0
               18  BINARY_SUBSCR    
               20  LOAD_GLOBAL              tuple
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 138        26  LOAD_DEREF               'shape'
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  STORE_DEREF              'shape'
             34_0  COME_FROM            24  '24'
             34_1  COME_FROM            10  '10'

 L. 139        34  LOAD_CLOSURE             'self'
               36  LOAD_CLOSURE             'shape'
               38  BUILD_TUPLE_2         2 
               40  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               42  LOAD_STR                 'StructuredArray.reshape.<locals>.<dictcomp>'
               44  MAKE_FUNCTION_8          'closure'

 L. 141        46  LOAD_DEREF               'self'
               48  LOAD_ATTR                _dict
               50  LOAD_METHOD              items
               52  CALL_METHOD_0         0  ''

 L. 139        54  GET_ITER         
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'd'

 L. 143        60  LOAD_GLOBAL              type
               62  LOAD_DEREF               'self'
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_METHOD              _fromarrayanddict
               68  LOAD_DEREF               'self'
               70  LOAD_FAST                'd'
               72  CALL_METHOD_2         2  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 40

    def broadcast_to--- This code section failed: ---

 L. 146         0  LOAD_GLOBAL              _broadcast_shapes_2
                2  LOAD_DEREF               'self'
                4  LOAD_ATTR                shape
                6  LOAD_DEREF               'shape'
                8  CALL_FUNCTION_2       2  ''
               10  POP_TOP          

 L. 147        12  LOAD_CLOSURE             'kw'
               14  LOAD_CLOSURE             'self'
               16  LOAD_CLOSURE             'shape'
               18  BUILD_TUPLE_3         3 
               20  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               22  LOAD_STR                 'StructuredArray.broadcast_to.<locals>.<dictcomp>'
               24  MAKE_FUNCTION_8          'closure'

 L. 149        26  LOAD_DEREF               'self'
               28  LOAD_ATTR                _dict
               30  LOAD_METHOD              items
               32  CALL_METHOD_0         0  ''

 L. 147        34  GET_ITER         
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'd'

 L. 151        40  LOAD_GLOBAL              type
               42  LOAD_DEREF               'self'
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_METHOD              _fromarrayanddict
               48  LOAD_DEREF               'self'
               50  LOAD_FAST                'd'
               52  CALL_METHOD_2         2  ''
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 20