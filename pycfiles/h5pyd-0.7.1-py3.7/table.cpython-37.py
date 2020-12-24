# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/table.py
# Compiled at: 2019-12-23 20:18:24
# Size of source mod 2**32: 14530 bytes
from __future__ import absolute_import
import numpy
from .base import _decode
from .dataset import Dataset
from .objectid import DatasetID
from . import selections as sel
from .h5type import Reference
from .h5type import check_dtype

class Cursor:
    __doc__ = '\n      Cursor for retreiving rows from a table\n    '

    def __init__(self, table, query=None, start=None, stop=None):
        self._table = table
        self._query = query
        if start is None:
            self._start = 0
        else:
            self._start = start
        if stop is None:
            self._stop = table.nrows
        else:
            self._stop = stop

    def __iter__(self):
        """ Iterate over the first axis.  TypeError if scalar.

        BEWARE: Modifications to the yielded data are *NOT* written to file.
        """
        nrows = self._table.nrows
        BUFFER_SIZE = 10000
        arr = None
        query_complete = False
        for indx in range(self._start, self._stop):
            if indx % BUFFER_SIZE == 0:
                read_count = BUFFER_SIZE
                if nrows - indx < read_count:
                    read_count = nrows - indx
                if self._query is None:
                    arr = self._table[indx:read_count + indx]
                else:
                    if query_complete:
                        arr = None
                    else:
                        arr = self._table.read_where((self._query), start=indx, limit=read_count)
                        if arr is not None:
                            if arr.shape[0] < read_count:
                                query_complete = True
            if arr is not None and indx % BUFFER_SIZE < arr.shape[0]:
                yield arr[(indx % BUFFER_SIZE)]


class Table(Dataset):
    __doc__ = '\n        Represents an HDF5 dataset\n    '

    def __init__(self, bind):
        """ Create a new Table object by binding to a low-level DatasetID.
        """
        if not isinstance(bind, DatasetID):
            raise ValueError('%s is not a DatasetID' % bind)
        Dataset.__init__(self, bind)
        if len(self._dtype) < 1:
            raise ValueError('Table type must be compound')
        if len(self._shape) > 1:
            raise ValueError('Table must be one-dimensional')

    @property
    def colnames(self):
        """Numpy-style attribute giving the number of dimensions"""
        names = []
        for field in self._dtype.descr:
            names.append(field[0])

        return names

    @property
    def nrows(self):
        return self._shape[0]

    def read(self, start=None, stop=None, step=None, field=None, out=None):
        if start is None:
            start = 0
        else:
            if stop is None:
                stop = self._shape[0]
            if step is None:
                step = 1
            arr = self[start:stop:step]
            if field is not None:
                tmp = arr[field]
                arr = tmp
            if out is not None:
                numpy.copyto(out, arr)
            else:
                return arr

    def read_where(self, condition, condvars=None, field=None, start=None, stop=None, step=None, limit=None):
        """Read rows from table using pytable-style condition
        """
        names = ()

        def readtime_dtype(basetype, names):
            """ Make a NumPy dtype appropriate for reading """
            if len(names) == 0:
                return basetype
            if basetype.names is None:
                raise ValueError('Field names only allowed for compound types')
            for name in names:
                if name not in basetype.names:
                    raise ValueError('Field %s does not appear in this type.' % name)

            return numpy.dtype([(name, basetype.fields[name][0]) for name in names])

        new_dtype = getattr(self._local, 'astype', None)
        if new_dtype is not None:
            new_dtype = readtime_dtype(new_dtype, names)
        else:
            new_dtype = readtime_dtype(self.dtype, names)
        mtype = new_dtype
        if start or stop:
            if not start:
                start = 0
            stop = stop or self._shape[0]
        else:
            start = 0
            stop = self._shape[0]
        selection_arg = slice(start, stop)
        selection = sel.select(self, selection_arg)
        if selection.nselect == 0:
            return numpy.ndarray((selection.mshape), dtype=new_dtype)
        data = []
        cursor = start
        page_size = stop - start
        while 1:
            req = '/datasets/' + self.id.uuid + '/value'
            params = {}
            params['query'] = condition
            self.log.info('req - cursor: {} page_size: {}'.format(cursor, page_size))
            end_row = cursor + page_size
            if end_row > stop:
                end_row = stop
            selection_arg = slice(cursor, end_row)
            selection = sel.select(self, selection_arg)
            sel_param = selection.getQueryParam()
            self.log.debug('query param: {}'.format(sel_param))
            if sel_param:
                params['select'] = sel_param
            try:
                self.log.debug('params: {}'.format(params))
                rsp = self.GET(req, params=params)
                values = rsp['value']
                count = len(values)
                self.log.info('got {} rows'.format(count))
                if count > 0:
                    if limit is None or count + len(data) <= limit:
                        data.extend(values)
                    else:
                        add_count = limit - len(data)
                        self.log.debug('adding {} from {} to rrows'.format(add_count, count))
                        data.extend(values[:add_count])
                cursor += page_size
            except IOError as ioe:
                try:
                    if ioe.errno == 413 and page_size > 1024:
                        page_size //= 2
                        page_size += 1
                        self.log.info('Got 413, reducing page_size to: {}'.format(page_size))
                    else:
                        self.log.info('Unexpected exception: {}'.format(ioe.errno))
                        raise ioe
                finally:
                    ioe = None
                    del ioe

            if not cursor >= stop:
                if not limit or len(data) == limit:
                    self.log.info('completed iteration, returning: {} rows'.format(len(data)))
                    break

        mshape = (
         len(data),)
        if len(mtype) > 1:
            if type(data) in (list, tuple):
                converted_data = []
                for i in range(len(data)):
                    converted_data.append(self.toTuple(data[i]))

                data = converted_data
        arr = numpy.empty(mshape, dtype=mtype)
        arr[...] = data
        if len(names) == 1:
            arr = arr[names[0]]
        if arr.shape == ():
            arr = numpy.asscalar(arr)
        return arr

    def update_where(self, condition, value, start=None, stop=None, step=None, limit=None):
        """Modify rows in table using pytable-style condition
        """
        if not isinstance(value, dict):
            raise ValueError('expected value to be a dict')
        else:
            if start or stop:
                if not start:
                    start = 0
                stop = stop or self._shape[0]
            else:
                start = 0
                stop = self._shape[0]
            selection_arg = slice(start, stop)
            selection = sel.select(self, selection_arg)
            sel_param = selection.getQueryParam()
            params = {}
            params['query'] = condition
            if limit:
                params['Limit'] = limit
            self.log.debug('query param: {}'.format(sel_param))
            if sel_param:
                params['select'] = sel_param
            req = '/datasets/' + self.id.uuid + '/value'
            rsp = self.PUT(req, body=value, format='json', params=params)
            indices = None
            arr = None
            if 'index' in rsp:
                indices = rsp['index']
                if indices:
                    arr = numpy.array(indices)
        return arr

    def create_cursor(self, condition=None, start=None, stop=None):
        """Return a cursor for iteration
        """
        return Cursor(self, query=condition, start=start, stop=stop)

    def append(self, rows):
        """ Append rows to end of table
        """
        self.log.info('Table append')
        if not self.id.uuid.startswith('d-'):
            raise ValueError('append not supported')
        else:
            if self._item_size != 'H5T_VARIABLE':
                use_base64 = True
            else:
                use_base64 = False
                self.log.debug('Using JSON since type is variable length')
            val = rows
            val_dtype = None
            try:
                val_dtype = val.dtype
            except AttributeError:
                pass

            if isinstance(val, Reference):
                val = val.tolist()
            else:
                vlen = check_dtype(vlen=(self.dtype))
                if vlen is not None and vlen not in (bytes, str):
                    self.log.debug('converting ndarray for vlen data')
                    try:
                        val = numpy.asarray(val, dtype=vlen)
                    except ValueError:
                        try:
                            val = numpy.array([numpy.array(x, dtype=vlen) for x in val],
                              dtype=(self.dtype))
                        except ValueError:
                            pass

                    if vlen == val_dtype:
                        if val.ndim > 1:
                            tmp = numpy.empty(shape=(val.shape[:-1]), dtype=object)
                            tmp.ravel()[:] = [i for i in val.reshape((
                             numpy.product(val.shape[:-1]), val.shape[(-1)]))]
                        else:
                            tmp = numpy.array([None], dtype=object)
                            tmp[0] = val
                        val = tmp
                elif isinstance(val, numpy.ndarray):
                    self.log.debug('got numpy array')
                    if val.dtype != self.dtype and val.dtype.shape == self.dtype.shape:
                        self.log.info('converting {} to {}'.format(val.dtype, self.dtype))
                        tmp = numpy.empty((val.shape), dtype=(self.dtype))
                        tmp[...] = val[...]
                        val = tmp
                else:
                    val = numpy.asarray(val, order='C', dtype=(self.dtype))
        self.log.debug('rows shape: {}'.format(val.shape))
        self.log.debug('data dtype: {}'.format(val.dtype))
        if len(val.shape) != 1:
            raise ValueError('rows must be one-dimensional')
        numrows = val.shape[0]
        req = '/datasets/' + self.id.uuid + '/value'
        params = {}
        body = {}
        format = 'json'
        if use_base64:
            format = 'binary'
            body = val.tobytes()
            self.log.debug('writing binary data, {} bytes'.format(len(body)))
            params['append'] = numrows
        else:
            if type(val) is not list:
                val = val.tolist()
            val = _decode(val)
            self.log.debug('writing json data, {} elements'.format(len(val)))
            self.log.debug('data: {}'.format(val))
            body['value'] = val
            body['append'] = numrows
        self.PUT(req, body=body, format=format, params=params)
        total_rows = self._shape[0] + numrows
        self._shape = (total_rows,)