# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/dataset.py
# Compiled at: 2019-12-23 20:19:35
# Size of source mod 2**32: 49410 bytes
from __future__ import absolute_import
import posixpath as pp
from copy import copy
import sys, time, base64, numpy
from .base import HLObject, jsonToArray, bytesToArray, arrayToBytes
from .h5type import Reference, RegionReference
from .base import _decode
from .objectid import DatasetID
from . import filters
from . import selections as sel
from .datatype import Datatype
from .h5type import getTypeItem, createDataType, check_dtype, special_dtype, getItemSize
_LEGACY_GZIP_COMPRESSION_VALS = frozenset(range(10))
VERBOSE_REFRESH_TIME = 1.0

def readtime_dtype(basetype, names):
    """ Make a NumPy dtype appropriate for reading """
    if basetype.names is not None:
        if basetype.names == ('r', 'i'):
            if all((dt.kind == 'f' for dt, off in basetype.fields.values())):
                if basetype.fields['r'][0] == basetype.fields['i'][0]:
                    itemsize = basetype.itemsize
                    if itemsize == 16:
                        return numpy.dtype(numpy.complex128)
                    if itemsize == 8:
                        return numpy.dtype(numpy.complex64)
                    TypeError('Unsupported dtype for complex numbers: %s' % basetype)
    if len(names) == 0:
        return basetype
    if basetype.names is None:
        raise ValueError('Field names only allowed for compound types')
    for name in names:
        if name not in basetype.names:
            raise ValueError('Field %s does not appear in this type.' % name)

    return numpy.dtype([(name, basetype.fields[name][0]) for name in names])


def setSliceQueryParam(params, dims, sel):
    """
    Helper method - set query parameter for given shape + selection

        Query arg should be in the form: [<dim1>, <dim2>, ... , <dimn>]
            brackets are optional for one dimensional arrays.
            Each dimension, valid formats are:
                single integer: n
                start and end: n:m
                start, end, and stride: n:m:s
    """
    rank = len(dims)
    start = list(sel.start)
    count = list(sel.count)
    step = list(sel.step)
    if rank > 0:
        sel_param = '['
        for i in range(rank):
            sel_param += str(start[i])
            sel_param += ':'
            sel_param += str(start[i] + count[i])
            if step[i] > 1:
                sel_param += ':'
                sel_param += str(step[i])
            if i < rank - 1:
                sel_param += ','

        sel_param += ']'
        params['select'] = sel_param


def make_new_dset(parent, shape=None, dtype=None, chunks=None, compression=None, shuffle=None, fletcher32=None, maxshape=None, compression_opts=None, fillvalue=None, scaleoffset=None, track_times=None):
    """ Return a new low-level dataset identifier

    Only creates anonymous datasets.
    """
    body = {}
    if shape is None:
        raise TypeError('shape must be specified')
    else:
        shape = tuple(shape)
    body['shape'] = shape
    if isinstance(chunks, bool):
        chunks = None
    elif chunks is not None:
        errmsg = isinstance(chunks, dict) or 'Chunk shape must not be greater than data shape in any dimension. {} is not compatible with {}'.format(chunks, shape)
        if len(chunks) != len(shape):
            raise ValueError('chunk is of wrong dimension')
        for i in range(len(shape)):
            if maxshape is not None:
                if maxshape[i] is not None:
                    if maxshape[i] < chunks[i]:
                        raise ValueError(errmsg)
                    elif shape[i] < chunks[i]:
                        raise ValueError(errmsg)

    layout = None
    if chunks is not None:
        if isinstance(chunks, dict):
            layout = chunks
            chunks = None
    if isinstance(dtype, Datatype):
        type_json = dtype.id.type_json
    else:
        if dtype is None:
            dtype = numpy.dtype('=f4')
        else:
            dtype = numpy.dtype(dtype)
        if dtype.kind == 'O':
            if 'ref' in dtype.metadata:
                type_json = {}
                type_json['class'] = 'H5T_REFERENCE'
                meta_type = dtype.metadata['ref']
                if meta_type is Reference:
                    type_json['base'] = 'H5T_STD_REF_OBJ'
                else:
                    if meta_type is RegionReference:
                        type_json['base'] = 'H5T_STD_REF_DSETREG'
                    else:
                        errmsg = 'Unexpected metadata type'
                        raise ValueError(errmsg)
            else:
                type_json = getTypeItem(dtype)
        else:
            body['type'] = type_json
            if compression is True:
                if compression_opts is None:
                    compression_opts = 4
                compression = 'gzip'
            if compression in _LEGACY_GZIP_COMPRESSION_VALS:
                if compression_opts is not None:
                    raise TypeError('Conflict in compression options')
                compression_opts = compression
                compression = 'gzip'
            dcpl = filters.generate_dcpl(shape, dtype, chunks, compression, compression_opts, shuffle, fletcher32, maxshape, scaleoffset, layout)
            if fillvalue is not None:
                fillvalue = numpy.asarray(fillvalue, dtype=dtype)
                if fillvalue:
                    fillvalue_list = fillvalue.tolist()
                    fillvalue_list = _decode(fillvalue_list)
                    dcpl['fillValue'] = fillvalue_list
            if chunks:
                if isinstance(chunks, dict):
                    dcpl['layout'] = chunks
            body['creationProperties'] = dcpl
            if maxshape is not None:
                if len(maxshape) > 0:
                    if shape is not None:
                        maxshape = tuple(((m if m is not None else 0) for m in maxshape))
                        body['maxdims'] = maxshape
                    else:
                        print('Warning: maxshape provided but no shape')
                req = '/datasets'
                body['shape'] = shape
                rsp = parent.POST(req, body=body)
                json_rep = {}
                json_rep['id'] = rsp['id']
                req = '/datasets/' + rsp['id']
                rsp = parent.GET(req)
                json_rep['shape'] = rsp['shape']
                json_rep['type'] = rsp['type']
                json_rep['lastModified'] = rsp['lastModified']
                if 'creationProperties' in rsp:
                    json_rep['creationProperties'] = rsp['creationProperties']
            else:
                json_rep['creationProperties'] = {}
        if 'layout' in rsp:
            json_rep['layout'] = rsp['layout']
        dset_id = DatasetID(parent, json_rep)
        return dset_id


class AstypeContext(object):

    def __init__(self, dset, dtype):
        self._dset = dset
        self._dtype = numpy.dtype(dtype)

    def __enter__(self):
        self._dset._local.astype = self._dtype

    def __exit__(self, *args):
        self._dset._local.astype = None


class Dataset(HLObject):
    __doc__ = '\n        Represents an HDF5 dataset\n    '

    def astype(self, dtype):
        """ Get a context manager allowing you to perform reads to a
        different destination type, e.g.:

        >>> with dataset.astype('f8'):
        ...     double_precision = dataset[0:100:2]
        """
        pass

    @property
    def dims(self):
        from .dims import DimensionManager
        return DimensionManager(self)

    @property
    def ndim(self):
        """Numpy-style attribute giving the number of dimensions"""
        return len(self._shape)

    @property
    def shape(self):
        """Numpy-style shape tuple giving dataset dimensions"""
        return self._shape

    def get_shape(self, check_server=False):
        shape_json = self.id.shape_json
        if shape_json['class'] in ('H5S_NULL', 'H5S_SCALAR'):
            return ()
            dims = 'maxdims' not in shape_json or check_server or shape_json['dims']
        else:
            req = '/datasets/' + self.id.uuid + '/shape'
            rsp = self.GET(req)
            shape_json = rsp['shape']
            dims = shape_json['dims']
        self._shape = tuple(dims)
        return self._shape

    @shape.setter
    def shape(self, shape):
        self.resize(shape)

    @property
    def size(self):
        """Numpy-style attribute giving the total dataset size"""
        if self._shape is None:
            return 0
        return numpy.prod(self._shape).item()

    @property
    def dtype(self):
        """Numpy dtype representing the datatype"""
        return self._dtype

    @property
    def value(self):
        """  Alias for dataset[()] """
        DeprecationWarning('dataset.value has been deprecated. Use dataset[()] instead.')
        return self[()]

    @property
    def chunks(self):
        """Dataset chunks (or None)"""
        ret = self.id.chunks
        if isinstance(ret, list):
            ret = tuple(ret)
        return ret

    @property
    def compression(self):
        """Compression strategy (or None)"""
        for x in ('gzip', 'lzf', 'szip'):
            if x in self._filters:
                return x

    @property
    def compression_opts(self):
        """ Compression setting.  Int(0-9) for gzip, 2-tuple for szip. """
        return self._filters.get(self.compression, None)

    @property
    def shuffle(self):
        """Shuffle filter present (T/F)"""
        return 'shuffle' in self._filters

    @property
    def fletcher32(self):
        """Fletcher32 filter is present (T/F)"""
        return 'fletcher32' in self._filters

    @property
    def scaleoffset(self):
        """Scale/offset filter settings. For integer data types, this is
        the number of bits stored, or 0 for auto-detected. For floating
        point data types, this is the number of decimal places retained.
        If the scale/offset filter is not in use, this is None."""
        try:
            return self._filters['scaleoffset'][1]
        except KeyError:
            return

    @property
    def maxshape(self):
        """Shape up to which this dataset can be resized.  Axes with value
        None have no resize limit. """
        shape_json = self.id.shape_json
        if self.id.shape_json['class'] == 'H5S_SCALAR':
            return ()
        elif 'maxdims' not in shape_json:
            dims = shape_json['dims']
        else:
            dims = shape_json['maxdims']
        return tuple((x if (x != 0 and x != 'H5S_UNLIMITED') else None for x in dims))

    @property
    def fillvalue(self):
        """Fill value for this dataset (0 by default)"""
        dcpl = self.id.dcpl_json
        arr = numpy.zeros((), dtype=(self._dtype))
        fill_value = None
        if 'fillValue' in dcpl:
            fill_value = dcpl['fillValue']
            arr[()] = fill_value
        return arr[()]

    @property
    def num_chunks(self):
        """ return number of allocated chunks"""
        self._getVerboseInfo()
        return self._num_chunks

    @property
    def allocated_size(self):
        """ return storage used by all allocated chunks """
        self._getVerboseInfo()
        return self._allocated_size

    def __init__(self, bind):
        """ Create a new Dataset object by binding to a low-level DatasetID.
        """
        if not isinstance(bind, DatasetID):
            raise ValueError('%s is not a DatasetID' % bind)
        HLObject.__init__(self, bind)
        self._dcpl = self.id.dcpl_json
        self._filters = filters.get_filters(self._dcpl)
        self._local = None
        self._dtype = createDataType(self.id.type_json)
        self._item_size = getItemSize(self.id.type_json)
        self._shape = self.get_shape()
        self._num_chunks = None
        self._allocated_size = None
        self._verboseUpdated = None

    def _getVerboseInfo(self):
        now = time.time()
        if self._verboseUpdated is None or now - self._verboseUpdated > VERBOSE_REFRESH_TIME:
            req = '/datasets/' + self.id.uuid + '?verbose=1'
            rsp_json = self.GET(req)
            if 'num_chunks' in rsp_json:
                self._num_chunks = rsp_json['num_chunks']
            else:
                self._num_chunks = 0
            if 'allocated_size' in rsp_json:
                self._allocated_size = rsp_json['allocated_size']
            else:
                self._allocated_size = 0
            self._verboseUpdated = now

    def resize(self, size, axis=None):
        """ Resize the dataset, or the specified axis.

        The dataset must be stored in chunked format; it can be resized up to
        the "maximum shape" (keyword maxshape) specified at creation time.
        The rank of the dataset cannot be changed.

        "Size" should be a shape tuple, or if an axis is specified, an integer.

        BEWARE: This functions differently than the NumPy resize() method!
        The data is not "reshuffled" to fit in the new shape; each axis is
        grown or shrunk independently.  The coordinates of existing data are
        fixed.
        """
        if self.chunks is None:
            raise TypeError('Only chunked datasets can be resized')
        if axis is not None:
            if not (axis >= 0 and axis < self.id.rank):
                raise ValueError('Invalid axis (0 to %s allowed)' % (self.id.rank - 1))
            try:
                newlen = int(size)
            except TypeError:
                raise TypeError('Argument must be a single int if axis is specified')

            size = list(self._shape)
            size[axis] = newlen
        size = tuple(size)
        body = {'shape': size}
        req = '/datasets/' + self.id.uuid + '/shape'
        self.PUT(req, body=body)
        self._shape = size

    def __len__(self):
        """ The size of the first axis.  TypeError if scalar.

        Limited to 2**32 on 32-bit systems; Dataset.len() is preferred.
        """
        size = self.len()
        if size > sys.maxsize:
            raise OverflowError("Value too big for Python's __len__; use Dataset.len() instead.")
        return size

    def len(self):
        """ The size of the first axis.  TypeError if scalar.

        Use of this method is preferred to len(dset), as Python's built-in
        len() cannot handle values greater then 2**32 on 32-bit systems.
        """
        shape = self._shape
        if shape is None or len(shape) == 0:
            raise TypeError('Attempt to take len() of scalar dataset')
        return shape[0]

    def __iter__(self):
        """ Iterate over the first axis.  TypeError if scalar.

        BEWARE: Modifications to the yielded data are *NOT* written to file.
        """
        shape = self._shape
        BUFFER_SIZE = 1000
        arr = None
        self.log.info('__iter__')
        if len(shape) == 0:
            raise TypeError("Can't iterate over a scalar dataset")
        for i in range(shape[0]):
            if i % BUFFER_SIZE == 0:
                numrows = BUFFER_SIZE
                if shape[0] - i < numrows:
                    numrows = shape[0] - i
                self.log.debug('get {} iter items'.format(numrows))
                arr = self[i:numrows + i]
            yield arr[(i % BUFFER_SIZE)]

    def _getQueryParam(self, start, stop, step=None):
        param = ''
        rank = len(self._shape)
        if rank == 0:
            return
        if step is None:
            step = (1, ) * rank
        param += '['
        for i in range(rank):
            field = '{}:{}:{}'.format(start[i], stop[i], step[i])
            param += field
            if i != rank - 1:
                param += ','

        param += ']'
        return param

    def __getitem__(self, args):
        """ Read a slice from the HDF5 dataset.

        Takes slices and recarray-style field names (more than one is
        allowed!) in any order.  Obeys basic NumPy rules, including
        broadcasting.

        Also supports:

        * Boolean "mask" array indexing
        """
        args = args if isinstance(args, tuple) else (args,)
        self.log.debug('dataset.__getitem__')
        for arg in args:
            arg_len = 0
            try:
                arg_len = len(arg)
            except TypeError:
                pass

            if arg_len < 3:
                self.log.debug('arg: {} type: {}'.format(arg, type(arg)))
            else:
                self.log.debug('arg: [{},...] type: {}'.format(arg[0], type(arg)))

        names = tuple((x for x in args if isinstance(x, str)))
        args = tuple((x for x in args if not isinstance(x, str)))
        new_dtype = getattr(self._local, 'astype', None)
        if new_dtype is not None:
            new_dtype = readtime_dtype(new_dtype, names)
        else:
            new_dtype = readtime_dtype(self.dtype, names)
            self.log.debug('new_dtype: {}'.format(new_dtype))
        if new_dtype.kind == 'S':
            if check_dtype(ref=(self.dtype)):
                new_dtype = special_dtype(ref=Reference)
        mtype = new_dtype
        if self._shape is None or numpy.product(self._shape) == 0:
            if not len(args) == 0:
                if len(args) == 1 and isinstance(args[0], tuple):
                    if args[0] == Ellipsis:
                        return numpy.empty((self._shape), dtype=new_dtype)
        if self._shape == ():
            selection = sel.select(self, args)
            self.log.info('selection.mshape: {}'.format(selection.mshape))
            req = '/datasets/' + self.id.uuid + '/value'
            rsp = self.GET(req, format='binary')
            if type(rsp) is bytes:
                self.log.info('got binary response for scalar selection')
                arr = numpy.frombuffer(rsp, dtype=new_dtype)
                self.dtype.shape or self.log.debug('reshape arr to: {}'.format(self._shape))
                arr = numpy.reshape(arr, self._shape)
            else:
                data = rsp['value']
                self.log.info('got json response for scalar selection')
                if len(mtype) > 1:
                    if type(data) in (list, tuple):
                        converted_data = []
                        for i in range(len(data)):
                            converted_data.append(self.toTuple(data[i]))

                        data = tuple(converted_data)
                    arr = numpy.empty((), dtype=new_dtype)
                    arr[()] = data
                else:
                    if selection.mshape is None:
                        self.log.info('return scalar selection of: {}, dtype: {}, shape: {}'.format(arr, arr.dtype, arr.shape))
                        return arr[()]
                    return arr
                    selection = sel.select(self, args)
                    self.log.debug('selection_constructor')
                    if selection.nselect == 0:
                        return numpy.ndarray((selection.mshape), dtype=new_dtype)
                        single_element = selection.mshape == ()
                        mshape = (1, ) if single_element else selection.mshape
                        rank = len(self._shape)
                        self.log.debug('dataset shape: {}'.format(self._shape))
                        self.log.debug('mshape: {}'.format(mshape))
                        self.log.debug('single_element: {}'.format(single_element))
                        rsp = None
                        req = '/datasets/' + self.id.uuid + '/value'
                        if isinstance(selection, sel.SimpleSelection):
                            chunk_layout = self.id.chunks
                            if chunk_layout is None:
                                chunk_layout = self._shape
                    elif isinstance(chunk_layout, dict):
                        if 'dims' not in chunk_layout:
                            self.log.error('Unexpected chunk_layout: {}'.format(chunk_layout))
                        else:
                            chunk_layout = tuple(chunk_layout['dims'])
                max_chunks = 1
                split_dim = -1
                sel_start = selection.start
                sel_step = selection.step
                sel_stop = []
                self.log.debug('selection._sel: {}'.format(selection._sel))
                scalar_selection = selection._sel[3]
                chunks_per_page = 1
                for i in range(rank):
                    stop = sel_start[i] + selection.count[i] * sel_step[i]
                    if stop > self._shape[i]:
                        stop = self._shape[i]
                    sel_stop.append(stop)
                    if scalar_selection[i]:
                        continue
                    count = sel_stop[i] - sel_start[i]
                    num_chunks = count // chunk_layout[i]
                    if count % chunk_layout[i] > 0:
                        num_chunks += 1
                    if not split_dim < 0:
                        if num_chunks > max_chunks:
                            max_chunks = num_chunks
                            split_dim = i
                        chunks_per_page = max_chunks

                self.log.info('selection: start {} stop {} step {}'.format(sel_start, sel_stop, sel_step))
                self.log.debug('split_dim: {}'.format(split_dim))
                self.log.debug('chunks_per_page: {}'.format(chunks_per_page))
                mshape_split_dim = 0
                for i in range(rank):
                    if scalar_selection[i]:
                        continue
                    if i == split_dim:
                        break
                    mshape_split_dim += 1

                self.log.debug('mshape_split_dim: {}'.format(split_dim))
                chunk_size = chunk_layout[split_dim]
                self.log.debug('chunk size for split_dim: {}'.format(chunk_size))
                arr = numpy.empty(mshape, dtype=mtype)
                params = {}
                done = False
                while not done:
                    num_rows = chunks_per_page * chunk_layout[split_dim]
                    self.log.debug('num_rows: {}'.format(num_rows))
                    page_start = list(copy(sel_start))
                    num_pages = max_chunks // chunks_per_page
                    if max_chunks % chunks_per_page > 0:
                        num_pages += 1
                    des_index = 0
                    self.log.debug('paged read, chunks_per_page: {} max_chunks: {}, num_pages: {}'.format(chunks_per_page, max_chunks, num_pages))
                    for page_number in range(num_pages):
                        self.log.debug('page_number: {}'.format(page_number))
                        self.log.debug('start: {}  stop: {}'.format(page_start, sel_stop))
                        page_stop = list(copy(sel_stop))
                        page_stop[split_dim] = page_start[split_dim] + num_rows
                        if sel_step[split_dim] > 1:
                            rem = page_stop[split_dim] % sel_step[split_dim]
                            if rem != 0:
                                page_stop[split_dim] += sel_step[split_dim] - rem
                        if page_stop[split_dim] > sel_stop[split_dim]:
                            page_stop[split_dim] = sel_stop[split_dim]
                        self.log.info('page_stop: {}'.format(page_stop[split_dim]))
                        page_mshape = list(copy(mshape))
                        page_mshape[mshape_split_dim] = 1 + (page_stop[split_dim] - page_start[split_dim] - 1) // sel_step[split_dim]
                        page_mshape = tuple(page_mshape)
                        self.log.info('page_mshape: {}'.format(page_mshape))
                        params['select'] = self._getQueryParam(page_start, page_stop, sel_step)
                        try:
                            rsp = self.GET(req, params=params, format='binary')
                        except IOError as ioe:
                            try:
                                self.log.info('got IOError: {}'.format(ioe.errno))
                                if ioe.errno == 413 and chunks_per_page > 1:
                                    chunks_per_page //= 2
                                    self.log.info('New chunks_per_page: {}'.format(chunks_per_page))
                                    break
                                else:
                                    raise IOError('Error retrieving data: {}'.format(ioe.errno))
                            finally:
                                ioe = None
                                del ioe

                        if type(rsp) is bytes:
                            self.log.info('binary response, {} bytes'.format(len(rsp)))
                            arr1d = bytesToArray(rsp, mtype, page_mshape)
                            page_arr = numpy.reshape(arr1d, page_mshape)
                        else:
                            self.log.info('json response')
                            data = rsp['value']
                            self.log.debug(data)
                            page_arr = jsonToArray(page_mshape, mtype, data)
                            self.log.debug('jsontoArray returned: {}'.format(page_arr))
                        slices = []
                        for i in range(len(mshape)):
                            if i == mshape_split_dim:
                                num_rows = page_arr.shape[mshape_split_dim]
                                slices.append(slice(des_index, des_index + num_rows))
                                des_index += num_rows
                            else:
                                slices.append(slice(0, mshape[i]))

                        self.log.debug('slices: {}'.format(slices))
                        arr[tuple(slices)] = page_arr
                        page_start[split_dim] = page_stop[split_dim]
                        self.log.debug('new page_start: {}'.format(page_start))
                        rows_remaining = sel_stop[split_dim] - page_start[split_dim]
                        if rows_remaining <= 0:
                            self.log.debug('done = True')
                            done = True
                            break
                        self.log.debug('{} rows left'.format(rows_remaining))

        else:
            if isinstance(selection, sel.FancySelection):
                raise ValueError('selection type not supported')
            else:
                if isinstance(selection, sel.PointSelection):
                    format = 'json'
                    body = {}
                    points = selection.points.tolist()
                    rank = len(self._shape)
                    last_point = -1
                    delistify = False
                    if len(points) == rank and isinstance(points[0], int) and rank > 1:
                        self.log.info('single point selection')
                        points = [points]
                    else:
                        for point in points:
                            if isinstance(point, (list, tuple)):
                                if not isinstance(point, (list, tuple)):
                                    raise ValueError('invalid point argument')
                                if len(point) != rank:
                                    raise ValueError('invalid point argument')
                                for i in range(rank):
                                    if not point[i] < 0:
                                        if point[i] >= self._shape[i]:
                                            pass
                                        raise ValueError('point out of range')

                                if rank == 1:
                                    delistify = True
                                    if point[0] <= last_point:
                                        raise TypeError('index points must be strictly increasing')
                                    last_point = point[0]
                                elif rank == 1:
                                    if isinstance(point, int) and not point < 0:
                                        if point > self._shape[0]:
                                            raise ValueError('point out of range')
                                        if point <= last_point:
                                            raise TypeError('index points must be strictly increasing')
                                        last_point = point
                            else:
                                raise ValueError('invalid point argument')

                    if self.id.id.startswith('d-'):
                        format = 'binary'
                        arr_points = numpy.asarray(points, dtype='u8')
                        body = arr_points.tobytes()
                        self.log.info('point select binary request, num bytes: {}'.format(len(body)))
                    else:
                        if delistify:
                            self.log.info('delistifying point selection')
                            body['points'] = []
                            for point in points:
                                if isinstance(point, (list, tuple)):
                                    body['points'].append(point[0])
                                else:
                                    body['points'] = point

                        else:
                            body['points'] = points
                        self.log.info('sending point selection request: {}'.format(body))
                    rsp = self.POST(req, format=format, body=body)
                    if type(rsp) is bytes:
                        if len(rsp) // mtype.itemsize != selection.mshape[0]:
                            raise IOError('Expected {} elements, but got {}'.format(selection.mshape[0], len(rsp) // mtype.itemsize))
                        arr = numpy.frombuffer(rsp, dtype=mtype)
                    else:
                        data = rsp['value']
                        if len(data) != selection.mshape[0]:
                            raise IOError('Expected {} elements, but got {}'.format(selection.mshape[0], len(data)))
                        arr = numpy.asarray(data, dtype=mtype, order='C')
                else:
                    raise ValueError('selection type not supported')
        self.log.info('got arr: {}, cleaning up shape'.format(arr.shape))
        if len(names) == 1:
            arr = arr[names[0]]
        if arr.shape == ():
            arr = numpy.asscalar(arr)
        else:
            if single_element:
                arr = arr[0]
            else:
                if len(arr.shape) > 1:
                    arr = numpy.squeeze(arr)
                return arr

    def __setitem__--- This code section failed: ---

 L. 934         0  LOAD_FAST                'self'
                2  LOAD_ATTR                log
                4  LOAD_METHOD              info
                6  LOAD_STR                 'Dataset __setitem__, args: {}'
                8  LOAD_METHOD              format
               10  LOAD_FAST                'args'
               12  CALL_METHOD_1         1  '1 positional argument'
               14  CALL_METHOD_1         1  '1 positional argument'
               16  POP_TOP          

 L. 936        18  LOAD_CONST               True
               20  STORE_FAST               'use_base64'

 L. 941        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'args'
               26  LOAD_GLOBAL              tuple
               28  CALL_FUNCTION_2       2  '2 positional arguments'
               30  POP_JUMP_IF_FALSE    36  'to 36'
               32  LOAD_FAST                'args'
               34  JUMP_FORWARD         40  'to 40'
             36_0  COME_FROM            30  '30'
               36  LOAD_FAST                'args'
               38  BUILD_TUPLE_1         1 
             40_0  COME_FROM            34  '34'
               40  STORE_FAST               'args'

 L. 944        42  LOAD_CONST               None
               44  STORE_FAST               'val_dtype'

 L. 945        46  SETUP_EXCEPT         58  'to 58'

 L. 946        48  LOAD_FAST                'val'
               50  LOAD_ATTR                dtype
               52  STORE_FAST               'val_dtype'
               54  POP_BLOCK        
               56  JUMP_FORWARD         78  'to 78'
             58_0  COME_FROM_EXCEPT     46  '46'

 L. 947        58  DUP_TOP          
               60  LOAD_GLOBAL              AttributeError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    76  'to 76'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 948        72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            64  '64'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            56  '56'

 L. 950        78  LOAD_GLOBAL              isinstance
               80  LOAD_FAST                'val'
               82  LOAD_GLOBAL              Reference
               84  CALL_FUNCTION_2       2  '2 positional arguments'
               86  POP_JUMP_IF_FALSE    96  'to 96'

 L. 952        88  LOAD_FAST                'val'
               90  LOAD_METHOD              tolist
               92  CALL_METHOD_0         0  '0 positional arguments'
               94  STORE_FAST               'val'
             96_0  COME_FROM            86  '86'

 L. 955        96  LOAD_GLOBAL              tuple
               98  LOAD_GENEXPR             '<code_object <genexpr>>'
              100  LOAD_STR                 'Dataset.__setitem__.<locals>.<genexpr>'
              102  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              104  LOAD_FAST                'args'
              106  GET_ITER         
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  STORE_FAST               'names'

 L. 956       114  LOAD_GLOBAL              tuple
              116  LOAD_GENEXPR             '<code_object <genexpr>>'
              118  LOAD_STR                 'Dataset.__setitem__.<locals>.<genexpr>'
              120  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              122  LOAD_FAST                'args'
              124  GET_ITER         
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  STORE_FAST               'args'

 L. 961       132  LOAD_GLOBAL              check_dtype
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                dtype
              138  LOAD_CONST               ('vlen',)
              140  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              142  STORE_DEREF              'vlen'

 L. 962       144  LOAD_DEREF               'vlen'
              146  LOAD_CONST               None
              148  COMPARE_OP               is-not
          150_152  POP_JUMP_IF_FALSE   418  'to 418'
              154  LOAD_DEREF               'vlen'
              156  LOAD_GLOBAL              bytes
              158  LOAD_GLOBAL              str
              160  BUILD_TUPLE_2         2 
              162  COMPARE_OP               not-in
          164_166  POP_JUMP_IF_FALSE   418  'to 418'

 L. 963       168  LOAD_FAST                'self'
              170  LOAD_ATTR                log
              172  LOAD_METHOD              debug
              174  LOAD_STR                 'converting ndarray for vlen data'
              176  CALL_METHOD_1         1  '1 positional argument'
              178  POP_TOP          

 L. 964       180  SETUP_EXCEPT        200  'to 200'

 L. 965       182  LOAD_GLOBAL              numpy
              184  LOAD_ATTR                asarray
              186  LOAD_FAST                'val'
              188  LOAD_DEREF               'vlen'
              190  LOAD_CONST               ('dtype',)
              192  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              194  STORE_FAST               'val'
              196  POP_BLOCK        
              198  JUMP_FORWARD        280  'to 280'
            200_0  COME_FROM_EXCEPT    180  '180'

 L. 966       200  DUP_TOP          
              202  LOAD_GLOBAL              ValueError
              204  COMPARE_OP               exception-match
          206_208  POP_JUMP_IF_FALSE   278  'to 278'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L. 967       216  SETUP_EXCEPT        252  'to 252'

 L. 968       218  LOAD_GLOBAL              numpy
              220  LOAD_ATTR                array
              222  LOAD_CLOSURE             'vlen'
              224  BUILD_TUPLE_1         1 
              226  LOAD_LISTCOMP            '<code_object <listcomp>>'
              228  LOAD_STR                 'Dataset.__setitem__.<locals>.<listcomp>'
              230  MAKE_FUNCTION_8          'closure'

 L. 969       232  LOAD_FAST                'val'
              234  GET_ITER         
              236  CALL_FUNCTION_1       1  '1 positional argument'
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                dtype
              242  LOAD_CONST               ('dtype',)
              244  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              246  STORE_FAST               'val'
              248  POP_BLOCK        
              250  JUMP_FORWARD        274  'to 274'
            252_0  COME_FROM_EXCEPT    216  '216'

 L. 970       252  DUP_TOP          
              254  LOAD_GLOBAL              ValueError
              256  COMPARE_OP               exception-match
          258_260  POP_JUMP_IF_FALSE   272  'to 272'
              262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          

 L. 971       268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
            272_0  COME_FROM           258  '258'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           250  '250'
              274  POP_EXCEPT       
              276  JUMP_FORWARD        280  'to 280'
            278_0  COME_FROM           206  '206'
              278  END_FINALLY      
            280_0  COME_FROM           276  '276'
            280_1  COME_FROM           198  '198'

 L. 972       280  LOAD_DEREF               'vlen'
              282  LOAD_FAST                'val_dtype'
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   930  'to 930'

 L. 973       290  LOAD_FAST                'val'
              292  LOAD_ATTR                ndim
              294  LOAD_CONST               1
              296  COMPARE_OP               >
          298_300  POP_JUMP_IF_FALSE   386  'to 386'

 L. 974       302  LOAD_GLOBAL              numpy
              304  LOAD_ATTR                empty
              306  LOAD_FAST                'val'
              308  LOAD_ATTR                shape
              310  LOAD_CONST               None
              312  LOAD_CONST               -1
              314  BUILD_SLICE_2         2 
              316  BINARY_SUBSCR    
              318  LOAD_GLOBAL              object
              320  LOAD_CONST               ('shape', 'dtype')
              322  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              324  STORE_FAST               'tmp'

 L. 975       326  LOAD_LISTCOMP            '<code_object <listcomp>>'
              328  LOAD_STR                 'Dataset.__setitem__.<locals>.<listcomp>'
              330  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              332  LOAD_FAST                'val'
              334  LOAD_METHOD              reshape

 L. 976       336  LOAD_GLOBAL              numpy
              338  LOAD_METHOD              product
              340  LOAD_FAST                'val'
              342  LOAD_ATTR                shape
              344  LOAD_CONST               None
              346  LOAD_CONST               -1
              348  BUILD_SLICE_2         2 
              350  BINARY_SUBSCR    
              352  CALL_METHOD_1         1  '1 positional argument'
              354  LOAD_FAST                'val'
              356  LOAD_ATTR                shape
              358  LOAD_CONST               -1
              360  BINARY_SUBSCR    
              362  BUILD_TUPLE_2         2 
              364  CALL_METHOD_1         1  '1 positional argument'
              366  GET_ITER         
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  LOAD_FAST                'tmp'
              372  LOAD_METHOD              ravel
              374  CALL_METHOD_0         0  '0 positional arguments'
              376  LOAD_CONST               None
              378  LOAD_CONST               None
              380  BUILD_SLICE_2         2 
              382  STORE_SUBSCR     
              384  JUMP_FORWARD        410  'to 410'
            386_0  COME_FROM           298  '298'

 L. 978       386  LOAD_GLOBAL              numpy
              388  LOAD_ATTR                array
              390  LOAD_CONST               None
              392  BUILD_LIST_1          1 
              394  LOAD_GLOBAL              object
              396  LOAD_CONST               ('dtype',)
              398  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              400  STORE_FAST               'tmp'

 L. 979       402  LOAD_FAST                'val'
              404  LOAD_FAST                'tmp'
              406  LOAD_CONST               0
              408  STORE_SUBSCR     
            410_0  COME_FROM           384  '384'

 L. 980       410  LOAD_FAST                'tmp'
              412  STORE_FAST               'val'
          414_416  JUMP_FORWARD        930  'to 930'
            418_0  COME_FROM           164  '164'
            418_1  COME_FROM           150  '150'

 L. 982       418  LOAD_GLOBAL              isinstance
              420  LOAD_FAST                'val'
              422  LOAD_GLOBAL              complex
              424  CALL_FUNCTION_2       2  '2 positional arguments'
          426_428  POP_JUMP_IF_TRUE    456  'to 456'

 L. 983       430  LOAD_GLOBAL              getattr
              432  LOAD_GLOBAL              getattr
              434  LOAD_FAST                'val'
              436  LOAD_STR                 'dtype'
              438  LOAD_CONST               None
              440  CALL_FUNCTION_3       3  '3 positional arguments'
              442  LOAD_STR                 'kind'
              444  LOAD_CONST               None
              446  CALL_FUNCTION_3       3  '3 positional arguments'
              448  LOAD_STR                 'c'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   576  'to 576'
            456_0  COME_FROM           426  '426'

 L. 984       456  LOAD_FAST                'self'
              458  LOAD_ATTR                dtype
              460  LOAD_ATTR                kind
              462  LOAD_STR                 'V'
              464  COMPARE_OP               !=
          466_468  POP_JUMP_IF_TRUE    484  'to 484'
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                dtype
              474  LOAD_ATTR                names
              476  LOAD_CONST               ('r', 'i')
              478  COMPARE_OP               !=
          480_482  POP_JUMP_IF_FALSE   500  'to 500'
            484_0  COME_FROM           466  '466'

 L. 985       484  LOAD_GLOBAL              TypeError

 L. 986       486  LOAD_STR                 'Wrong dataset dtype for complex number values: %s'

 L. 987       488  LOAD_FAST                'self'
              490  LOAD_ATTR                dtype
              492  LOAD_ATTR                fields
              494  BINARY_MODULO    
              496  CALL_FUNCTION_1       1  '1 positional argument'
              498  RAISE_VARARGS_1       1  'exception instance'
            500_0  COME_FROM           480  '480'

 L. 988       500  LOAD_GLOBAL              isinstance
              502  LOAD_FAST                'val'
              504  LOAD_GLOBAL              complex
              506  CALL_FUNCTION_2       2  '2 positional arguments'
          508_510  POP_JUMP_IF_FALSE   530  'to 530'

 L. 989       512  LOAD_GLOBAL              numpy
              514  LOAD_ATTR                asarray
              516  LOAD_FAST                'val'
              518  LOAD_GLOBAL              type
              520  LOAD_FAST                'val'
              522  CALL_FUNCTION_1       1  '1 positional argument'
              524  LOAD_CONST               ('dtype',)
              526  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              528  STORE_FAST               'val'
            530_0  COME_FROM           508  '508'

 L. 990       530  LOAD_GLOBAL              numpy
              532  LOAD_ATTR                empty
              534  LOAD_FAST                'val'
              536  LOAD_ATTR                shape
              538  LOAD_FAST                'self'
              540  LOAD_ATTR                dtype
              542  LOAD_CONST               ('shape', 'dtype')
              544  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              546  STORE_FAST               'tmp'

 L. 991       548  LOAD_FAST                'val'
              550  LOAD_ATTR                real
              552  LOAD_FAST                'tmp'
              554  LOAD_STR                 'r'
              556  STORE_SUBSCR     

 L. 992       558  LOAD_FAST                'val'
              560  LOAD_ATTR                imag
              562  LOAD_FAST                'tmp'
              564  LOAD_STR                 'i'
              566  STORE_SUBSCR     

 L. 993       568  LOAD_FAST                'tmp'
              570  STORE_FAST               'val'
          572_574  JUMP_FORWARD        930  'to 930'
            576_0  COME_FROM           452  '452'

 L. 995       576  LOAD_FAST                'self'
              578  LOAD_ATTR                dtype
              580  LOAD_ATTR                kind
              582  LOAD_STR                 'O'
              584  COMPARE_OP               ==
          586_588  POP_JUMP_IF_TRUE    646  'to 646'

 L. 996       590  LOAD_FAST                'self'
              592  LOAD_ATTR                dtype
              594  LOAD_ATTR                kind
              596  LOAD_STR                 'V'
              598  COMPARE_OP               ==
          600_602  POP_JUMP_IF_FALSE   794  'to 794'

 L. 997       604  LOAD_GLOBAL              isinstance
              606  LOAD_FAST                'val'
              608  LOAD_GLOBAL              numpy
              610  LOAD_ATTR                ndarray
              612  CALL_FUNCTION_2       2  '2 positional arguments'
          614_616  POP_JUMP_IF_FALSE   632  'to 632'
              618  LOAD_FAST                'val'
              620  LOAD_ATTR                dtype
              622  LOAD_ATTR                kind
              624  LOAD_STR                 'V'
              626  COMPARE_OP               !=
          628_630  POP_JUMP_IF_FALSE   794  'to 794'
            632_0  COME_FROM           614  '614'

 L. 998       632  LOAD_FAST                'self'
              634  LOAD_ATTR                dtype
              636  LOAD_ATTR                subdtype
              638  LOAD_CONST               None
              640  COMPARE_OP               ==
          642_644  POP_JUMP_IF_FALSE   794  'to 794'
            646_0  COME_FROM           586  '586'

 L.1002       646  LOAD_GLOBAL              len
              648  LOAD_FAST                'names'
              650  CALL_FUNCTION_1       1  '1 positional argument'
              652  LOAD_CONST               1
              654  COMPARE_OP               ==
          656_658  POP_JUMP_IF_FALSE   734  'to 734'
              660  LOAD_FAST                'self'
              662  LOAD_ATTR                dtype
              664  LOAD_ATTR                fields
              666  LOAD_CONST               None
              668  COMPARE_OP               is-not
          670_672  POP_JUMP_IF_FALSE   734  'to 734'

 L.1004       674  LOAD_FAST                'names'
              676  LOAD_CONST               0
              678  BINARY_SUBSCR    
              680  LOAD_FAST                'self'
              682  LOAD_ATTR                dtype
              684  LOAD_ATTR                fields
              686  COMPARE_OP               not-in
          688_690  POP_JUMP_IF_FALSE   708  'to 708'

 L.1005       692  LOAD_GLOBAL              ValueError
              694  LOAD_STR                 'No such field for indexing: %s'
              696  LOAD_FAST                'names'
              698  LOAD_CONST               0
              700  BINARY_SUBSCR    
              702  BINARY_MODULO    
              704  CALL_FUNCTION_1       1  '1 positional argument'
              706  RAISE_VARARGS_1       1  'exception instance'
            708_0  COME_FROM           688  '688'

 L.1006       708  LOAD_FAST                'self'
              710  LOAD_ATTR                dtype
              712  LOAD_ATTR                fields
              714  LOAD_FAST                'names'
              716  LOAD_CONST               0
              718  BINARY_SUBSCR    
              720  BINARY_SUBSCR    
              722  LOAD_CONST               0
              724  BINARY_SUBSCR    
              726  STORE_FAST               'dtype'

 L.1007       728  LOAD_CONST               True
              730  STORE_FAST               'cast_compound'
              732  JUMP_FORWARD        744  'to 744'
            734_0  COME_FROM           670  '670'
            734_1  COME_FROM           656  '656'

 L.1009       734  LOAD_FAST                'self'
              736  LOAD_ATTR                dtype
              738  STORE_FAST               'dtype'

 L.1010       740  LOAD_CONST               False
              742  STORE_FAST               'cast_compound'
            744_0  COME_FROM           732  '732'

 L.1011       744  LOAD_GLOBAL              numpy
              746  LOAD_ATTR                asarray
              748  LOAD_FAST                'val'
              750  LOAD_FAST                'dtype'
              752  LOAD_STR                 'C'
              754  LOAD_CONST               ('dtype', 'order')
              756  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              758  STORE_FAST               'val'

 L.1012       760  LOAD_FAST                'cast_compound'
          762_764  POP_JUMP_IF_FALSE   930  'to 930'

 L.1013       766  LOAD_FAST                'val'
              768  LOAD_METHOD              astype
              770  LOAD_GLOBAL              numpy
              772  LOAD_METHOD              dtype
              774  LOAD_FAST                'names'
              776  LOAD_CONST               0
              778  BINARY_SUBSCR    
              780  LOAD_FAST                'dtype'
              782  BUILD_TUPLE_2         2 
              784  BUILD_LIST_1          1 
              786  CALL_METHOD_1         1  '1 positional argument'
              788  CALL_METHOD_1         1  '1 positional argument'
              790  STORE_FAST               'val'
              792  JUMP_FORWARD        930  'to 930'
            794_0  COME_FROM           642  '642'
            794_1  COME_FROM           628  '628'
            794_2  COME_FROM           600  '600'

 L.1016       794  LOAD_GLOBAL              isinstance
              796  LOAD_FAST                'val'
              798  LOAD_GLOBAL              numpy
              800  LOAD_ATTR                ndarray
              802  CALL_FUNCTION_2       2  '2 positional arguments'
          804_806  POP_JUMP_IF_FALSE   912  'to 912'

 L.1019       808  LOAD_FAST                'self'
              810  LOAD_ATTR                log
              812  LOAD_METHOD              debug
              814  LOAD_STR                 'got numpy array'
              816  CALL_METHOD_1         1  '1 positional argument'
              818  POP_TOP          

 L.1020       820  LOAD_FAST                'val'
              822  LOAD_ATTR                dtype
              824  LOAD_FAST                'self'
              826  LOAD_ATTR                dtype
              828  COMPARE_OP               !=
          830_832  POP_JUMP_IF_FALSE   930  'to 930'
              834  LOAD_FAST                'val'
              836  LOAD_ATTR                dtype
              838  LOAD_ATTR                shape
              840  LOAD_FAST                'self'
              842  LOAD_ATTR                dtype
              844  LOAD_ATTR                shape
              846  COMPARE_OP               ==
          848_850  POP_JUMP_IF_FALSE   930  'to 930'

 L.1021       852  LOAD_FAST                'self'
              854  LOAD_ATTR                log
              856  LOAD_METHOD              info
              858  LOAD_STR                 'converting {} to {}'
              860  LOAD_METHOD              format
              862  LOAD_FAST                'val'
              864  LOAD_ATTR                dtype
              866  LOAD_FAST                'self'
              868  LOAD_ATTR                dtype
              870  CALL_METHOD_2         2  '2 positional arguments'
              872  CALL_METHOD_1         1  '1 positional argument'
              874  POP_TOP          

 L.1023       876  LOAD_GLOBAL              numpy
              878  LOAD_ATTR                empty
              880  LOAD_FAST                'val'
              882  LOAD_ATTR                shape
              884  LOAD_FAST                'self'
              886  LOAD_ATTR                dtype
              888  LOAD_CONST               ('dtype',)
              890  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              892  STORE_FAST               'tmp'

 L.1024       894  LOAD_FAST                'val'
              896  LOAD_CONST               Ellipsis
              898  BINARY_SUBSCR    
              900  LOAD_FAST                'tmp'
              902  LOAD_CONST               Ellipsis
              904  STORE_SUBSCR     

 L.1025       906  LOAD_FAST                'tmp'
              908  STORE_FAST               'val'
              910  JUMP_FORWARD        930  'to 930'
            912_0  COME_FROM           804  '804'

 L.1027       912  LOAD_GLOBAL              numpy
              914  LOAD_ATTR                asarray
              916  LOAD_FAST                'val'
              918  LOAD_STR                 'C'
              920  LOAD_FAST                'self'
              922  LOAD_ATTR                dtype
              924  LOAD_CONST               ('order', 'dtype')
              926  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              928  STORE_FAST               'val'
            930_0  COME_FROM           910  '910'
            930_1  COME_FROM           848  '848'
            930_2  COME_FROM           830  '830'
            930_3  COME_FROM           792  '792'
            930_4  COME_FROM           762  '762'
            930_5  COME_FROM           572  '572'
            930_6  COME_FROM           414  '414'
            930_7  COME_FROM           286  '286'

 L.1030       930  LOAD_CONST               None
              932  STORE_FAST               'mshape'

 L.1075       934  LOAD_FAST                'val'
              936  LOAD_ATTR                shape
              938  STORE_FAST               'mshape'

 L.1076       940  LOAD_FAST                'self'
              942  LOAD_ATTR                log
              944  LOAD_METHOD              debug
              946  LOAD_STR                 'mshape: {}'
              948  LOAD_METHOD              format
              950  LOAD_FAST                'mshape'
              952  CALL_METHOD_1         1  '1 positional argument'
              954  CALL_METHOD_1         1  '1 positional argument'
              956  POP_TOP          

 L.1077       958  LOAD_FAST                'self'
              960  LOAD_ATTR                log
              962  LOAD_METHOD              debug
              964  LOAD_STR                 'data dtype: {}'
              966  LOAD_METHOD              format
              968  LOAD_FAST                'val'
              970  LOAD_ATTR                dtype
              972  CALL_METHOD_1         1  '1 positional argument'
              974  CALL_METHOD_1         1  '1 positional argument'
              976  POP_TOP          

 L.1080       978  LOAD_GLOBAL              sel
              980  LOAD_METHOD              select
              982  LOAD_FAST                'self'
              984  LOAD_FAST                'args'
              986  CALL_METHOD_2         2  '2 positional arguments'
              988  STORE_FAST               'selection'

 L.1081       990  LOAD_FAST                'self'
              992  LOAD_ATTR                log
              994  LOAD_METHOD              debug
              996  LOAD_STR                 'selection.mshape: {}'
              998  LOAD_METHOD              format
             1000  LOAD_FAST                'selection'
             1002  LOAD_ATTR                mshape
             1004  CALL_METHOD_1         1  '1 positional argument'
             1006  CALL_METHOD_1         1  '1 positional argument'
             1008  POP_TOP          

 L.1082      1010  LOAD_FAST                'selection'
             1012  LOAD_ATTR                nselect
             1014  LOAD_CONST               0
             1016  COMPARE_OP               ==
         1018_1020  POP_JUMP_IF_FALSE  1026  'to 1026'

 L.1083      1022  LOAD_CONST               None
             1024  RETURN_VALUE     
           1026_0  COME_FROM          1018  '1018'

 L.1086      1026  LOAD_FAST                'mshape'
             1028  LOAD_CONST               ()
             1030  COMPARE_OP               ==
         1032_1034  POP_JUMP_IF_FALSE  1150  'to 1150'
             1036  LOAD_FAST                'selection'
             1038  LOAD_ATTR                mshape
             1040  LOAD_CONST               None
             1042  COMPARE_OP               !=
         1044_1046  POP_JUMP_IF_FALSE  1150  'to 1150'
             1048  LOAD_FAST                'selection'
             1050  LOAD_ATTR                mshape
             1052  LOAD_CONST               ()
             1054  COMPARE_OP               !=
         1056_1058  POP_JUMP_IF_FALSE  1150  'to 1150'

 L.1087      1060  LOAD_FAST                'self'
             1062  LOAD_ATTR                log
             1064  LOAD_METHOD              debug
             1066  LOAD_STR                 'broadcast scalar'
             1068  CALL_METHOD_1         1  '1 positional argument'
             1070  POP_TOP          

 L.1088      1072  LOAD_FAST                'self'
             1074  LOAD_ATTR                log
             1076  LOAD_METHOD              debug
             1078  LOAD_STR                 'selection.mshape: {}'
             1080  LOAD_METHOD              format
             1082  LOAD_FAST                'selection'
             1084  LOAD_ATTR                mshape
             1086  CALL_METHOD_1         1  '1 positional argument'
             1088  CALL_METHOD_1         1  '1 positional argument'
             1090  POP_TOP          

 L.1089      1092  LOAD_FAST                'self'
             1094  LOAD_ATTR                dtype
             1096  LOAD_ATTR                subdtype
             1098  LOAD_CONST               None
             1100  COMPARE_OP               is-not
         1102_1104  POP_JUMP_IF_FALSE  1114  'to 1114'

 L.1090      1106  LOAD_GLOBAL              TypeError
             1108  LOAD_STR                 'Scalar broadcasting is not supported for array dtypes'
             1110  CALL_FUNCTION_1       1  '1 positional argument'
             1112  RAISE_VARARGS_1       1  'exception instance'
           1114_0  COME_FROM          1102  '1102'

 L.1091      1114  LOAD_GLOBAL              numpy
             1116  LOAD_ATTR                empty
             1118  LOAD_FAST                'selection'
             1120  LOAD_ATTR                mshape
             1122  LOAD_FAST                'val'
             1124  LOAD_ATTR                dtype
             1126  LOAD_CONST               ('dtype',)
             1128  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1130  STORE_FAST               'val2'

 L.1092      1132  LOAD_FAST                'val'
             1134  LOAD_FAST                'val2'
             1136  LOAD_CONST               Ellipsis
             1138  STORE_SUBSCR     

 L.1093      1140  LOAD_FAST                'val2'
             1142  STORE_FAST               'val'

 L.1094      1144  LOAD_FAST                'val'
             1146  LOAD_ATTR                shape
             1148  STORE_FAST               'mshape'
           1150_0  COME_FROM          1056  '1056'
           1150_1  COME_FROM          1044  '1044'
           1150_2  COME_FROM          1032  '1032'

 L.1106      1150  LOAD_STR                 '/datasets/'
             1152  LOAD_FAST                'self'
             1154  LOAD_ATTR                id
             1156  LOAD_ATTR                uuid
             1158  BINARY_ADD       
             1160  LOAD_STR                 '/value'
             1162  BINARY_ADD       
             1164  STORE_FAST               'req'

 L.1108      1166  BUILD_MAP_0           0 
             1168  STORE_FAST               'params'

 L.1109      1170  BUILD_MAP_0           0 
             1172  STORE_FAST               'body'

 L.1112      1174  LOAD_STR                 'json'
             1176  STORE_FAST               'format'

 L.1114      1178  LOAD_FAST                'use_base64'
         1180_1182  POP_JUMP_IF_FALSE  1314  'to 1314'

 L.1116      1184  LOAD_FAST                'self'
             1186  LOAD_ATTR                id
             1188  LOAD_ATTR                uuid
             1190  LOAD_METHOD              startswith
             1192  LOAD_STR                 'd-'
             1194  CALL_METHOD_1         1  '1 positional argument'
         1196_1198  POP_JUMP_IF_FALSE  1236  'to 1236'

 L.1118      1200  LOAD_STR                 'binary'
             1202  STORE_FAST               'format'

 L.1120      1204  LOAD_GLOBAL              arrayToBytes
             1206  LOAD_FAST                'val'
             1208  CALL_FUNCTION_1       1  '1 positional argument'
             1210  STORE_FAST               'body'

 L.1121      1212  LOAD_FAST                'self'
             1214  LOAD_ATTR                log
             1216  LOAD_METHOD              debug
             1218  LOAD_STR                 'writing binary data, {} bytes'
             1220  LOAD_METHOD              format
             1222  LOAD_GLOBAL              len
             1224  LOAD_FAST                'body'
             1226  CALL_FUNCTION_1       1  '1 positional argument'
             1228  CALL_METHOD_1         1  '1 positional argument'
             1230  CALL_METHOD_1         1  '1 positional argument'
             1232  POP_TOP          
             1234  JUMP_FORWARD       1312  'to 1312'
           1236_0  COME_FROM          1196  '1196'

 L.1125      1236  LOAD_FAST                'val'
             1238  LOAD_METHOD              tobytes
             1240  CALL_METHOD_0         0  '0 positional arguments'
             1242  STORE_FAST               'data'

 L.1126      1244  LOAD_GLOBAL              base64
             1246  LOAD_METHOD              b64encode
             1248  LOAD_FAST                'data'
             1250  CALL_METHOD_1         1  '1 positional argument'
             1252  STORE_FAST               'data'

 L.1127      1254  LOAD_FAST                'data'
             1256  LOAD_METHOD              decode
             1258  LOAD_STR                 'ascii'
             1260  CALL_METHOD_1         1  '1 positional argument'
             1262  STORE_FAST               'data'

 L.1128      1264  LOAD_FAST                'self'
             1266  LOAD_ATTR                log
             1268  LOAD_METHOD              debug
             1270  LOAD_STR                 'data: {}'
             1272  LOAD_METHOD              format
             1274  LOAD_FAST                'data'
             1276  CALL_METHOD_1         1  '1 positional argument'
             1278  CALL_METHOD_1         1  '1 positional argument'
             1280  POP_TOP          

 L.1129      1282  LOAD_FAST                'data'
             1284  LOAD_FAST                'body'
             1286  LOAD_STR                 'value_base64'
             1288  STORE_SUBSCR     

 L.1130      1290  LOAD_FAST                'self'
             1292  LOAD_ATTR                log
             1294  LOAD_METHOD              debug
             1296  LOAD_STR                 'writing base64 data, {} bytes'
             1298  LOAD_METHOD              format
             1300  LOAD_GLOBAL              len
             1302  LOAD_FAST                'data'
             1304  CALL_FUNCTION_1       1  '1 positional argument'
             1306  CALL_METHOD_1         1  '1 positional argument'
             1308  CALL_METHOD_1         1  '1 positional argument'
             1310  POP_TOP          
           1312_0  COME_FROM          1234  '1234'
             1312  JUMP_FORWARD       1392  'to 1392'
           1314_0  COME_FROM          1180  '1180'

 L.1132      1314  LOAD_GLOBAL              type
             1316  LOAD_FAST                'val'
             1318  CALL_FUNCTION_1       1  '1 positional argument'
             1320  LOAD_GLOBAL              list
             1322  COMPARE_OP               is-not
         1324_1326  POP_JUMP_IF_FALSE  1336  'to 1336'

 L.1133      1328  LOAD_FAST                'val'
             1330  LOAD_METHOD              tolist
             1332  CALL_METHOD_0         0  '0 positional arguments'
             1334  STORE_FAST               'val'
           1336_0  COME_FROM          1324  '1324'

 L.1134      1336  LOAD_GLOBAL              _decode
             1338  LOAD_FAST                'val'
             1340  CALL_FUNCTION_1       1  '1 positional argument'
             1342  STORE_FAST               'val'

 L.1135      1344  LOAD_FAST                'self'
             1346  LOAD_ATTR                log
             1348  LOAD_METHOD              debug
             1350  LOAD_STR                 'writing json data, {} elements'
             1352  LOAD_METHOD              format
             1354  LOAD_GLOBAL              len
             1356  LOAD_FAST                'val'
             1358  CALL_FUNCTION_1       1  '1 positional argument'
             1360  CALL_METHOD_1         1  '1 positional argument'
             1362  CALL_METHOD_1         1  '1 positional argument'
             1364  POP_TOP          

 L.1136      1366  LOAD_FAST                'self'
             1368  LOAD_ATTR                log
             1370  LOAD_METHOD              debug
             1372  LOAD_STR                 'data: {}'
             1374  LOAD_METHOD              format
             1376  LOAD_FAST                'val'
             1378  CALL_METHOD_1         1  '1 positional argument'
             1380  CALL_METHOD_1         1  '1 positional argument'
             1382  POP_TOP          

 L.1137      1384  LOAD_FAST                'val'
             1386  LOAD_FAST                'body'
             1388  LOAD_STR                 'value'
             1390  STORE_SUBSCR     
           1392_0  COME_FROM          1312  '1312'

 L.1139      1392  LOAD_FAST                'selection'
             1394  LOAD_ATTR                select_type
             1396  LOAD_GLOBAL              sel
             1398  LOAD_ATTR                H5S_SELECT_ALL
             1400  COMPARE_OP               !=
         1402_1404  POP_JUMP_IF_FALSE  1532  'to 1532'

 L.1140      1406  LOAD_FAST                'format'
             1408  LOAD_STR                 'binary'
             1410  COMPARE_OP               ==
         1412_1414  POP_JUMP_IF_FALSE  1432  'to 1432'

 L.1142      1416  LOAD_GLOBAL              setSliceQueryParam
             1418  LOAD_FAST                'params'
             1420  LOAD_FAST                'self'
             1422  LOAD_ATTR                _shape
             1424  LOAD_FAST                'selection'
             1426  CALL_FUNCTION_3       3  '3 positional arguments'
             1428  POP_TOP          
             1430  JUMP_FORWARD       1532  'to 1532'
           1432_0  COME_FROM          1412  '1412'

 L.1145      1432  LOAD_GLOBAL              list
             1434  LOAD_FAST                'selection'
             1436  LOAD_ATTR                start
             1438  CALL_FUNCTION_1       1  '1 positional argument'
             1440  LOAD_FAST                'body'
             1442  LOAD_STR                 'start'
             1444  STORE_SUBSCR     

 L.1146      1446  LOAD_GLOBAL              list
             1448  LOAD_FAST                'selection'
             1450  LOAD_ATTR                start
             1452  CALL_FUNCTION_1       1  '1 positional argument'
             1454  STORE_FAST               'stop'

 L.1147      1456  SETUP_LOOP         1502  'to 1502'
             1458  LOAD_GLOBAL              range
             1460  LOAD_GLOBAL              len
             1462  LOAD_FAST                'stop'
             1464  CALL_FUNCTION_1       1  '1 positional argument'
             1466  CALL_FUNCTION_1       1  '1 positional argument'
             1468  GET_ITER         
             1470  FOR_ITER           1500  'to 1500'
             1472  STORE_FAST               'i'

 L.1148      1474  LOAD_FAST                'stop'
             1476  LOAD_FAST                'i'
             1478  DUP_TOP_TWO      
             1480  BINARY_SUBSCR    
             1482  LOAD_FAST                'selection'
             1484  LOAD_ATTR                count
             1486  LOAD_FAST                'i'
             1488  BINARY_SUBSCR    
             1490  INPLACE_ADD      
             1492  ROT_THREE        
             1494  STORE_SUBSCR     
         1496_1498  JUMP_BACK          1470  'to 1470'
             1500  POP_BLOCK        
           1502_0  COME_FROM_LOOP     1456  '1456'

 L.1149      1502  LOAD_FAST                'stop'
             1504  LOAD_FAST                'body'
             1506  LOAD_STR                 'stop'
             1508  STORE_SUBSCR     

 L.1150      1510  LOAD_FAST                'selection'
             1512  LOAD_ATTR                step
         1514_1516  POP_JUMP_IF_FALSE  1532  'to 1532'

 L.1151      1518  LOAD_GLOBAL              list
             1520  LOAD_FAST                'selection'
             1522  LOAD_ATTR                step
             1524  CALL_FUNCTION_1       1  '1 positional argument'
             1526  LOAD_FAST                'body'
             1528  LOAD_STR                 'step'
             1530  STORE_SUBSCR     
           1532_0  COME_FROM          1514  '1514'
           1532_1  COME_FROM          1430  '1430'
           1532_2  COME_FROM          1402  '1402'

 L.1153      1532  LOAD_FAST                'self'
             1534  LOAD_ATTR                PUT
             1536  LOAD_FAST                'req'
             1538  LOAD_FAST                'body'
             1540  LOAD_FAST                'format'
             1542  LOAD_FAST                'params'
             1544  LOAD_CONST               ('body', 'format', 'params')
             1546  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1548  POP_TOP          

Parse error at or near `CALL_FUNCTION_KW_4' instruction at offset 1546

    def read_direct(self, dest, source_sel=None, dest_sel=None):
        """ Read data directly from HDF5 into an existing NumPy array.

        The destination array must be C-contiguous and writable.
        Selections must be the output of numpy.s_[<args>].

        Broadcasting is supported for simple indexing.
        """
        pass

    def write_direct(self, source, source_sel=None, dest_sel=None):
        """ Write data directly to HDF5 from a NumPy array.

        The source array must be C-contiguous.  Selections must be
        the output of numpy.s_[<args>].

        Broadcasting is supported for simple indexing.
        """
        pass

    def __array__(self, dtype=None):
        """ Create a Numpy array containing the whole dataset.  DON'T THINK
        THIS MEANS DATASETS ARE INTERCHANGABLE WITH ARRAYS.  For one thing,
        you have to read the whole dataset everytime this method is called.
        """
        arr = numpy.empty((self._shape), dtype=(self.dtype if dtype is None else dtype))
        if self._shape is None or numpy.product(self._shape) == 0:
            return arr
        return arr

    def __repr__(self):
        if not self:
            r = '<Closed HDF5 dataset>'
        else:
            if self.name is None:
                namestr = '("anonymous")'
            else:
                name = pp.basename(pp.normpath(self.name))
                if name:
                    namestr = f'"{name}"'
                else:
                    namestr = '/'
            r = f'<HDF5 dataset {namestr}: shape {self._shape}, type "{self.dtype.str}">'
        return r

    def refresh(self):
        """ Refresh the dataset metadata by reloading from the file.

        This is part of the SWMR features and only exist when the HDF5
        librarary version >=1.9.178
        """
        pass

    def flush(self):
        """ Flush the dataset data and metadata to the file.
       If the dataset is chunked, raw data chunks are written to the file.

       This is part of the SWMR features and only exist when the HDF5
       librarary version >=1.9.178
       """
        pass

    def toTuple(self, data):
        if type(data) in (list, tuple):
            return tuple((self.toTuple(x) for x in data))
        return data