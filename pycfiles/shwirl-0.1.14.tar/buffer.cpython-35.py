# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/gloo/buffer.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 16293 bytes
import numpy as np
from os import path as op
from traceback import extract_stack, format_list
import weakref
from .globject import GLObject
from ..util import logger
from ..ext.six import string_types

class Buffer(GLObject):
    __doc__ = ' Generic GPU buffer.\n\n    A generic buffer is an interface used to upload data to a GPU array buffer\n    (ARRAY_BUFFER or ELEMENT_ARRAY_BUFFER). It keeps track of\n    buffer size but does not have any CPU storage. You can consider it as\n    write-only.\n\n    The `set_data` is a deferred operation: you can call it even if an OpenGL\n    context is not available. The `update` function is responsible to upload\n    pending data to GPU memory and requires an active GL context.\n\n    The Buffer class only deals with data in terms of bytes; it is not\n    aware of data type or element size.\n\n    Parameters\n    ----------\n    data : ndarray | None\n        Buffer data.\n    nbytes : int | None\n        Buffer byte size.\n    '

    def __init__(self, data=None, nbytes=None):
        GLObject.__init__(self)
        self._views = []
        self._valid = True
        self._nbytes = 0
        if data is not None:
            if nbytes is not None:
                raise ValueError('Cannot specify both data and nbytes.')
            self.set_data(data, copy=False)
        elif nbytes is not None:
            self.resize_bytes(nbytes)

    @property
    def nbytes(self):
        """ Buffer size in bytes """
        return self._nbytes

    def set_subdata(self, data, offset=0, copy=False):
        """ Set a sub-region of the buffer (deferred operation).

        Parameters
        ----------

        data : ndarray
            Data to be uploaded
        offset: int
            Offset in buffer where to start copying data (in bytes)
        copy: bool
            Since the operation is deferred, data may change before
            data is actually uploaded to GPU memory.
            Asking explicitly for a copy will prevent this behavior.
        """
        data = np.array(data, copy=copy)
        nbytes = data.nbytes
        if offset < 0:
            raise ValueError('Offset must be positive')
        elif offset + nbytes > self._nbytes:
            raise ValueError('Data does not fit into buffer')
        if nbytes == self._nbytes and offset == 0:
            self._glir.command('SIZE', self._id, nbytes)
        self._glir.command('DATA', self._id, offset, data)

    def set_data(self, data, copy=False):
        """ Set data in the buffer (deferred operation).

        This completely resets the size and contents of the buffer.

        Parameters
        ----------
        data : ndarray
            Data to be uploaded
        copy: bool
            Since the operation is deferred, data may change before
            data is actually uploaded to GPU memory.
            Asking explicitly for a copy will prevent this behavior.
        """
        data = np.array(data, copy=copy)
        nbytes = data.nbytes
        if nbytes != self._nbytes:
            self.resize_bytes(nbytes)
        else:
            self._glir.command('SIZE', self._id, nbytes)
        if nbytes:
            self._glir.command('DATA', self._id, 0, data)

    def resize_bytes(self, size):
        """ Resize this buffer (deferred operation). 
        
        Parameters
        ----------
        size : int
            New buffer size in bytes.
        """
        self._nbytes = size
        self._glir.command('SIZE', self._id, size)
        for view in self._views:
            if view() is not None:
                view()._valid = False

        self._views = []


class DataBuffer(Buffer):
    __doc__ = ' GPU data buffer that is aware of data type and elements size\n\n    Parameters\n    ----------\n    data : ndarray | None\n        Buffer data.\n    '

    def __init__(self, data=None):
        self._size = 0
        self._dtype = None
        self._stride = 0
        self._itemsize = 0
        self._last_dim = None
        Buffer.__init__(self, data)

    def _prepare_data(self, data):
        if not isinstance(data, np.ndarray):
            raise TypeError('DataBuffer data must be numpy array.')
        return data

    def set_subdata(self, data, offset=0, copy=False, **kwargs):
        """ Set a sub-region of the buffer (deferred operation).

        Parameters
        ----------

        data : ndarray
            Data to be uploaded
        offset: int
            Offset in buffer where to start copying data (in bytes)
        copy: bool
            Since the operation is deferred, data may change before
            data is actually uploaded to GPU memory.
            Asking explicitly for a copy will prevent this behavior.
        **kwargs : dict
            Additional keyword arguments.
        """
        data = self._prepare_data(data, **kwargs)
        offset = offset * self.itemsize
        Buffer.set_subdata(self, data=data, offset=offset, copy=copy)

    def set_data(self, data, copy=False, **kwargs):
        """ Set data (deferred operation)

        Parameters
        ----------
        data : ndarray
            Data to be uploaded
        copy: bool
            Since the operation is deferred, data may change before
            data is actually uploaded to GPU memory.
            Asking explicitly for a copy will prevent this behavior.
        **kwargs : dict
            Additional arguments.
        """
        data = self._prepare_data(data, **kwargs)
        self._dtype = data.dtype
        self._stride = data.strides[(-1)]
        self._itemsize = self._dtype.itemsize
        Buffer.set_data(self, data=data, copy=copy)

    @property
    def dtype(self):
        """ Buffer dtype """
        return self._dtype

    @property
    def offset(self):
        """ Buffer offset (in bytes) relative to base """
        return 0

    @property
    def stride(self):
        """ Stride of data in memory """
        return self._stride

    @property
    def size(self):
        """ Number of elements in the buffer """
        return self._size

    @property
    def itemsize(self):
        """ The total number of bytes required to store the array data """
        return self._itemsize

    @property
    def glsl_type(self):
        """ GLSL declaration strings required for a variable to hold this data.
        """
        if self.dtype is None:
            return
        dtshape = self.dtype[0].shape
        n = dtshape[0] if dtshape else 1
        if n > 1:
            dtype = 'vec%d' % n
        else:
            dtype = 'float' if 'f' in self.dtype[0].base.kind else 'int'
        return (
         'attribute', dtype)

    def resize_bytes(self, size):
        """ Resize the buffer (in-place, deferred operation)

        Parameters
        ----------
        size : integer
            New buffer size in bytes

        Notes
        -----
        This clears any pending operations.
        """
        Buffer.resize_bytes(self, size)
        self._size = size // self.itemsize

    def __getitem__(self, key):
        """ Create a view on this buffer. """
        view = DataBufferView(self, key)
        self._views.append(weakref.ref(view))
        return view

    def __setitem__(self, key, data):
        """ Set data (deferred operation) """
        if isinstance(key, string_types):
            raise ValueError('Cannot set non-contiguous data on buffer')
        else:
            if isinstance(key, int):
                if key < 0:
                    key += self.size
                if key < 0 or key > self.size:
                    raise IndexError('Buffer assignment index out of range')
                start, stop, step = key, key + 1, 1
            else:
                if isinstance(key, slice):
                    start, stop, step = key.indices(self.size)
                    if stop < start:
                        start, stop = stop, start
                else:
                    if key == Ellipsis:
                        start, stop, step = 0, self.size, 1
                    else:
                        raise TypeError('Buffer indices must be integers or strings')
                if step != 1:
                    raise ValueError('Cannot set non-contiguous data on buffer')
                if not isinstance(data, np.ndarray):
                    data = np.array(data, dtype=self.dtype, copy=False)
                if data.size < stop - start:
                    data = np.resize(data, stop - start)
                elif data.size > stop - start:
                    raise ValueError('Data too big to fit GPU data.')
        offset = start
        self.set_subdata(data=data, offset=offset, copy=True)

    def __repr__(self):
        return '<%s size=%s last_dim=%s>' % (
         self.__class__.__name__, self.size, self._last_dim)


class DataBufferView(DataBuffer):
    __doc__ = ' View on a sub-region of a DataBuffer.\n\n    Parameters\n    ----------\n    base : DataBuffer\n        The buffer accessed by this view.\n    key : str, int, slice, or Ellpsis\n        The index into the base buffer that defines a sub-region of the buffer\n        to view. String arguments select a single field from multi-field \n        dtypes, and other allowed types select a subset of rows. \n        \n    Notes\n    -----\n    \n    It is generally not necessary to instantiate this class manually; use \n    ``base_buffer[key]`` instead.\n    '

    def __init__(self, base, key):
        self._base = base
        self._key = key
        self._stride = base.stride
        if isinstance(key, string_types):
            self._dtype = base.dtype[key]
            self._offset = base.dtype.fields[key][1]
            self._nbytes = base.size * self._dtype.itemsize
            self._size = base.size
            self._itemsize = self._dtype.itemsize
            return
        if isinstance(key, int):
            if key < 0:
                key += base.size
            if key < 0 or key > base.size:
                raise IndexError('Buffer assignment index out of range')
            start, stop, step = key, key + 1, 1
        else:
            if isinstance(key, slice):
                start, stop, step = key.indices(base.size)
                if stop < start:
                    start, stop = stop, start
            else:
                if key == Ellipsis:
                    start, stop, step = 0, base.size, 1
                else:
                    raise TypeError('Buffer indices must be integers or strings')
        if step != 1:
            raise ValueError('Cannot access non-contiguous data')
        self._itemsize = base.itemsize
        self._offset = start * self.itemsize
        self._size = stop - start
        self._dtype = base.dtype
        self._nbytes = self.size * self.itemsize

    @property
    def glir(self):
        return self._base.glir

    @property
    def id(self):
        return self._base.id

    @property
    def _last_dim(self):
        return self._base._last_dim

    def set_subdata(self, data, offset=0, copy=False, **kwargs):
        raise RuntimeError('Cannot set data on buffer view.')

    def set_data(self, data, copy=False, **kwargs):
        raise RuntimeError('Cannot set data on buffer view.')

    @property
    def offset(self):
        """ Buffer offset (in bytes) relative to base """
        return self._offset

    @property
    def base(self):
        """Buffer base if this buffer is a view on another buffer. """
        return self._base

    def resize_bytes(self, size):
        raise RuntimeError('Cannot resize buffer view.')

    def __getitem__(self, key):
        raise RuntimeError('Can only access data from a base buffer')

    def __setitem__(self, key, data):
        raise RuntimeError('Cannot set data on Buffer view')

    def __repr__(self):
        return '<DataBufferView on %r at offset=%d size=%d>' % (
         self.base, self.offset, self.size)


class VertexBuffer(DataBuffer):
    __doc__ = ' Buffer for vertex attribute data\n\n    Parameters\n    ----------\n    data : ndarray\n        Buffer data (optional)\n    '
    _GLIR_TYPE = 'VertexBuffer'

    def _prepare_data(self, data, convert=False):
        if isinstance(data, list):
            data = np.array(data, dtype=np.float32)
        if not isinstance(data, np.ndarray):
            raise ValueError('Data must be a ndarray (got %s)' % type(data))
        if data.dtype.isbuiltin:
            if convert is True:
                data = data.astype(np.float32)
            if data.dtype in (np.float64, np.int64):
                raise TypeError('data must be 32-bit not %s' % data.dtype)
            c = data.shape[(-1)] if data.ndim > 1 else 1
            if c in (2, 3, 4):
                if not data.flags['C_CONTIGUOUS']:
                    logger.warning('Copying discontiguous data for struct dtype:\n%s' % _last_stack_str())
                    data = data.copy()
            else:
                c = 1
            if self._last_dim and c != self._last_dim:
                raise ValueError('Last dimension should be %s not %s' % (
                 self._last_dim, c))
            data = data.view(dtype=[('f0', data.dtype.base, c)])
            self._last_dim = c
        return data


def _last_stack_str():
    """Print stack trace from call that didn't originate from here"""
    stack = extract_stack()
    for s in stack[::-1]:
        if op.join('vispy', 'gloo', 'buffer.py') not in __file__:
            break

    return format_list([s])[0]


class IndexBuffer(DataBuffer):
    __doc__ = ' Buffer for index data\n\n    Parameters\n    ----------\n\n    data : ndarray | None\n        Buffer data.\n    '
    _GLIR_TYPE = 'IndexBuffer'

    def __init__(self, data=None):
        DataBuffer.__init__(self, data)
        self._last_dim = 1

    def _prepare_data(self, data, convert=False):
        if isinstance(data, list):
            data = np.array(data, dtype=np.uint32)
        if not isinstance(data, np.ndarray):
            raise ValueError('Data must be a ndarray (got %s)' % type(data))
        if not data.dtype.isbuiltin:
            raise TypeError('Element buffer dtype cannot be structured')
        else:
            if convert:
                if data.dtype is not np.uint32:
                    data = data.astype(np.uint32)
            elif data.dtype not in [np.uint32, np.uint16, np.uint8]:
                raise TypeError('Invalid dtype for IndexBuffer: %r' % data.dtype)
        return data