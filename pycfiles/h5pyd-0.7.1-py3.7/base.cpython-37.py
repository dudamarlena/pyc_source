# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/base.py
# Compiled at: 2020-01-02 22:48:40
# Size of source mod 2**32: 35225 bytes
from __future__ import absolute_import
import posixpath, os, json, base64, numpy as np, logging, logging.handlers
from collections import Mapping, MutableMapping, KeysView, ValuesView, ItemsView
from .objectid import GroupID
from .h5type import Reference, check_dtype
numpy_integer_types = (
 np.int8, np.uint8, np.int16, np.int16, np.int32, np.uint32, np.int64, np.uint64)
numpy_float_types = (np.float16, np.float32, np.float64)

class FakeLock:

    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, a, b, c):
        pass


_phil = FakeLock()
phil = _phil

def with_phil(func):
    """ Locking decorator """
    import functools

    def wrapper(*args, **kwds):
        with _phil:
            return func(*args, **kwds)

    functools.update_wrapper(wrapper, func, ('__name__', '__doc__'))
    return wrapper


def guess_dtype(data):
    """ Attempt to guess an appropriate dtype for the object, returning None
    if nothing is appropriate (or if it should be left up the the array
    constructor to figure out)
    """
    pass


def _decode(item, encoding='ascii'):
    """decode any byte items to python 3 strings
        """
    ret_val = None
    if type(item) is bytes:
        ret_val = item.decode(encoding)
    else:
        if type(item) is list:
            ret_val = []
            for x in item:
                ret_val.append(_decode(x, encoding))

        else:
            if type(item) is tuple:
                ret_val = []
                for x in item:
                    ret_val.append(_decode(x, encoding))

                ret_val = tuple(ret_val)
            else:
                if type(item) is dict:
                    ret_val = {}
                    for k in dict:
                        ret_val[k] = _decode(item[k], encoding)

                else:
                    if type(item) is np.ndarray:
                        x = item.tolist()
                        ret_val = []
                        for x in item:
                            ret_val.append(_decode(x, encoding))

                    else:
                        if type(item) in numpy_integer_types:
                            ret_val = int(item)
                        else:
                            if type(item) in numpy_float_types:
                                ret_val = float(item)
                            else:
                                ret_val = item
    return ret_val


def getHeaders(domain, username=None, password=None, headers=None):
    if headers is None:
        headers = {}
    headers['host'] = domain
    if username is not None:
        if password is not None:
            auth_string = username + ':' + password
            auth_string = auth_string.encode('utf-8')
            auth_string = base64.b64encode(auth_string)
            auth_string = b'Basic ' + auth_string
            headers['Authorization'] = auth_string
    return headers


def toTuple(rank, data):
    if type(data) in (list, tuple):
        if rank > 0:
            return list((toTuple(rank - 1, x) for x in data))
        return tuple((toTuple(rank - 1, x) for x in data))
    else:
        return data


def getNumElements(dims):
    num_elements = 0
    if isinstance(dims, int):
        num_elements = dims
    else:
        if isinstance(dims, (list, tuple)):
            num_elements = 1
            for dim in dims:
                num_elements *= dim

        else:
            raise ValueError('Unexpected argument')
    return num_elements


def copyToArray(arr, rank, index, data, vlen_base=None):
    nlen = arr.shape[rank]
    if len(data) != nlen:
        raise ValueError("Array len of {} at index: {} doesn't match data length: {}".format(nlen, index, len(data)))
    for i in range(nlen):
        index[rank] = i
        if rank < len(arr.shape) - 1:
            copyToArray(arr, (rank + 1), index, (data[i]), vlen_base=vlen_base)
        elif vlen_base:
            e = np.array((data[i]), dtype=vlen_base)
            if len(e.shape) > 1:
                e = e.squeeze()
            arr[tuple(index)] = e
        else:
            arr[tuple(index)] = data[i]

    index[rank] = 0


def jsonToArray(data_shape, data_dtype, data_json):
    """Return numpy array from the given json array."""
    if data_dtype.names is not None and data_dtype.names == ('r', 'i') and all((dt.kind == 'f' for dt, off in data_dtype.fields.values())):
        if data_dtype.fields['r'][0] == data_dtype.fields['i'][0]:
            itemsize = data_dtype.itemsize
            if itemsize == 16:
                cmplx_dtype = np.dtype(np.complex128)
            else:
                if itemsize == 8:
                    cmplx_dtype = np.dtype(np.complex64)
                else:
                    arr = np.empty(shape=data_shape, dtype=cmplx_dtype)
                    if data_shape == ():
                        tmp = np.array((tuple(data_json)), dtype=data_dtype)
                        arr.real = tmp['r']
                        arr.imag = tmp['i']
                    else:
                        data = np.array(data_json)
                        tmp = np.empty(shape=data_shape, dtype=data_dtype)
                        for i, n in enumerate(data_dtype.names):
                            tmp[n] = data[:, i]

                    arr.real = tmp['r']
                    arr.imag = tmp['i']
                return arr
        elif len(data_dtype) > 1:
            if not isinstance(data_json, (list, tuple)):
                raise TypeError('expected list data for compound data type')
            vlen_base = check_dtype(vlen=data_dtype)
            if vlen_base:
                arr = np.zeros(data_shape, dtype=data_dtype)
                index = []
                for i in range(len(data_shape)):
                    index.append(0)

                if data_shape is ():
                    arr[()] = data_json
        else:
            copyToArray(arr, 0, index, data_json, vlen_base=vlen_base)
    else:
        npoints = np.product(data_shape)
        if type(data_json) in (list, tuple):
            np_shape_rank = len(data_shape)
            converted_data = []
            if npoints == 1 and len(data_json) == len(data_dtype):
                converted_data.append(toTuple(0, data_json))
            else:
                converted_data = toTuple(np_shape_rank, data_json)
            data_json = converted_data
        arr = np.array(data_json, dtype=data_dtype)
        if arr.size != npoints:
            msg = "Input data doesn't match selection number of elements"
            msg += ' Expected {}, but received: {}'.format(npoints, arr.size)
            raise ValueError(msg)
        if arr.shape != data_shape:
            arr = arr.reshape(data_shape)
        return arr


def isVlen(dt):
    is_vlen = False
    if len(dt) > 1:
        names = dt.names
        for name in names:
            if isVlen(dt[name]):
                is_vlen = True
                break

    else:
        if dt.metadata and 'vlen' in dt.metadata:
            is_vlen = True
    return is_vlen


def getElementSize(e, dt):
    if len(dt) > 1:
        count = 0
        for name in dt.names:
            field_dt = dt[name]
            field_val = e[name]
            count += getElementSize(field_val, field_dt)

    else:
        if not dt.metadata or 'vlen' not in dt.metadata:
            count = dt.itemsize
        else:
            vlen = dt.metadata['vlen']
            if isinstance(e, int):
                if e == 0:
                    count = 4
                else:
                    raise ValueError('Unexpected value: {}'.format(e))
            else:
                if isinstance(e, bytes):
                    count = len(e) + 4
                else:
                    if isinstance(e, str):
                        count = len(e.encode('utf-8')) + 4
                    else:
                        if isinstance(e, np.ndarray):
                            nElements = np.prod(e.shape)
                            if e.dtype.kind != 'O':
                                count = e.dtype.itemsize * nElements
                            else:
                                arr1d = e.reshape((nElements,))
                                count = 0
                                for item in arr1d:
                                    count += getElementSize(item, dt)

                            count += 4
                        else:
                            if isinstance(e, list) or isinstance(e, tuple):
                                count = len(e) * vlen.itemsize + 4
                            else:
                                raise TypeError('unexpected type: {}'.format(type(e)))
    return count


def getByteArraySize(arr):
    if not isVlen(arr.dtype):
        return arr.itemsize * np.prod(arr.shape)
    nElements = np.prod(arr.shape)
    arr1d = arr.reshape((nElements,))
    dt = arr1d.dtype
    count = 0
    for e in arr1d:
        count += getElementSize(e, dt)

    return count


def copyBuffer(src, des, offset):
    for i in range(len(src)):
        des[i + offset] = src[i]

    return offset + len(src)


def copyElement(e, dt, buffer, offset):
    if len(dt) > 1:
        for name in dt.names:
            field_dt = dt[name]
            field_val = e[name]
            offset = copyElement(field_val, field_dt, buffer, offset)

    else:
        if not dt.metadata or 'vlen' not in dt.metadata:
            e_buf = e.tobytes()
            if len(e_buf) < dt.itemsize:
                e_buf_ex = bytearray(dt.itemsize)
                for i in range(len(e_buf)):
                    e_buf_ex[i] = e_buf[i]

                e_buf = bytes(e_buf_ex)
            offset = copyBuffer(e_buf, buffer, offset)
        else:
            vlen = dt.metadata['vlen']
            if isinstance(e, int):
                if e == 0:
                    offset = copyBuffer(b'\x00\x00\x00\x00', buffer, offset)
                else:
                    raise ValueError('Unexpected value: {}'.format(e))
            else:
                if isinstance(e, bytes):
                    count = np.int32(len(e))
                    offset = copyBuffer(count.tobytes(), buffer, offset)
                    offset = copyBuffer(e, buffer, offset)
                else:
                    if isinstance(e, str):
                        text = e.encode('utf-8')
                        count = np.int32(len(text))
                        offset = copyBuffer(count.tobytes(), buffer, offset)
                        offset = copyBuffer(text, buffer, offset)
                    else:
                        if isinstance(e, np.ndarray):
                            nElements = np.prod(e.shape)
                            if e.dtype.kind != 'O':
                                count = np.int32(e.dtype.itemsize * nElements)
                                offset = copyBuffer(count.tobytes(), buffer, offset)
                                offset = copyBuffer(e.tobytes(), buffer, offset)
                            else:
                                arr1d = e.reshape((nElements,))
                                for item in arr1d:
                                    offset = copyElement(item, dt, buffer, offset)

                        else:
                            if not False or isinstance(e, list) or isinstance(e, tuple):
                                count = np.int32(len(e) * vlen.itemsize)
                                offset = copyBuffer(count.tobytes(), buffer, offset)
                                if isinstance(e, np.ndarray):
                                    arr = e
                                else:
                                    arr = np.asarray(e, dtype=vlen)
                                offset = copyBuffer(arr.tobytes(), buffer, offset)
                            else:
                                raise TypeError('unexpected type: {}'.format(type(e)))
    return offset


def getElementCount(buffer, offset):
    count_bytes = bytes(buffer[offset:offset + 4])
    try:
        count = int(np.frombuffer(count_bytes, dtype='<i4'))
    except TypeError as e:
        try:
            msg = 'Unexpected error reading count value for variable length elemennt: {}'.format(e)
            raise TypeError(msg)
        finally:
            e = None
            del e

    if count < 0:
        raise ValueError('Unexpected count value for variable length element')
    if count > 1073741824:
        raise ValueError('Variable length element size expected to be less than 1MB')
    return count


def readElement(buffer, offset, arr, index, dt):
    if len(dt) > 1:
        e = arr[index]
        for name in dt.names:
            field_dt = dt[name]
            offset = readElement(buffer, offset, e, name, field_dt)

    else:
        if not dt.metadata or 'vlen' not in dt.metadata:
            count = dt.itemsize
            e_buffer = buffer[offset:offset + count]
            offset += count
            if dt.kind == 'S':
                arr[index] = e_buffer
            else:
                arr[index] = np.frombuffer((bytes(e_buffer)), dtype=dt)
        else:
            vlen = dt.metadata['vlen']
            e = arr[index]
            if isinstance(e, np.ndarray):
                nelements = np.prod(dt.shape)
                e.reshape((nelements,))
                for i in range(nelements):
                    offset = readElement(buffer, offset, e, i, dt)

                e.reshape(dt.shape)
            else:
                count = getElementCount(buffer, offset)
                offset += 4
                if count > 0:
                    e_buffer = buffer[offset:offset + count]
                    offset += count
                    if vlen is bytes:
                        arr[index] = bytes(e_buffer)
                    else:
                        if vlen is str:
                            s = e_buffer.decode('utf-8')
                            arr[index] = s
                        else:
                            e = np.frombuffer((bytes(e_buffer)), dtype=vlen)
                            arr[index] = e
                else:
                    arr[index] = vlen(0)
    return offset


def arrayToBytes(arr):
    if not isVlen(arr.dtype):
        return arr.tobytes()
    nSize = getByteArraySize(arr)
    buffer = bytearray(nSize)
    offset = 0
    nElements = np.prod(arr.shape)
    arr1d = arr.reshape((nElements,))
    for e in arr1d:
        offset = copyElement(e, arr1d.dtype, buffer, offset)

    return buffer


def bytesToArray(data, dt, shape):
    nelements = getNumElements(shape)
    if not isVlen(dt):
        arr = np.frombuffer(data, dtype=dt)
    else:
        arr = np.zeros((nelements,), dtype=dt)
        offset = 0
        for index in range(nelements):
            offset = readElement(data, offset, arr, index, dt)

    arr = arr.reshape(shape)
    return arr


class LinkCreationPropertyList(object):
    __doc__ = '\n        Represents a LinkCreationPropertyList\n    '

    @with_phil
    def __init__(self, char_encoding=None):
        if char_encoding:
            if char_encoding not in ('CSET_ASCII', 'CSET_UTF8'):
                raise ValueError('Unknown encoding')
            self._char_encoding = char_encoding
        else:
            self._char_encoding = 'CSET_ASCII'

    @with_phil
    def __repr__(self):
        return '<HDF5 LinkCreationPropertyList>'

    @property
    def char_encoding(self):
        return self._char_encoding


class LinkAccessPropertyList(object):
    __doc__ = '\n        Represents a LinkAccessPropertyList\n    '

    @with_phil
    def __repr__(self):
        return '<HDF5 LinkAccessPropertyList>'


def default_lcpl():
    """ Default link creation property list """
    lcpl = LinkCreationPropertyList()
    return lcpl


def default_lapl():
    """ Default link access property list """
    lapl = LinkAccessPropertyList()
    return lapl


dlapl = default_lapl()
dlcpl = default_lcpl()

class CommonStateObject(object):
    __doc__ = '\n        Mixin class that allows sharing information between objects which\n        reside in the same HDF5 file.  Requires that the host class have\n        a ".id" attribute which returns a low-level ObjectID subclass.\n\n        Also implements Unicode operations.\n    '

    @property
    def _lapl(self):
        """ Fetch the link access property list appropriate for this object
        """
        return dlapl

    @property
    def _lcpl(self):
        """ Fetch the link creation property list appropriate for this object
        """
        return dlcpl

    def _e(self, name, lcpl=None):
        """ Encode a name according to the current file settings.

        Returns name, or 2-tuple (name, lcpl) if lcpl is True

        - Binary strings are always passed as-is, h5t.CSET_ASCII
        - Unicode strings are encoded utf8, h5t.CSET_UTF8

        If name is None, returns either None or (None, None) appropriately.
        """

        def get_lcpl(coding):
            lcpl = self._lcpl.copy()
            lcpl.set_char_encoding(coding)
            return lcpl

        if name is None:
            if lcpl:
                return (None, None)
            return
        if isinstance(name, bytes):
            coding = 'CSET_ASCII'
        else:
            try:
                name = name.encode('ascii')
                coding = 'CSET_ASCII'
            except UnicodeEncodeError:
                name = name.encode('utf8')
                coding = 'CSET_UTF8'

            if lcpl:
                return (
                 name, get_lcpl(coding))
            return name

    def _d(self, name):
        """ Decode a name according to the current file settings.

        - Try to decode utf8
        - Failing that, return the byte string

        If name is None, returns None.
        """
        if name is None:
            return
        try:
            return name.decode('utf8')
        except UnicodeDecodeError:
            pass

        return name


class _RegionProxy(object):
    __doc__ = '\n        Proxy object which handles region references.\n\n        To create a new region reference (datasets only), use slicing syntax:\n\n            >>> newref = obj.regionref[0:10:2]\n\n        To determine the target dataset shape from an existing reference:\n\n            >>> shape = obj.regionref.shape(existingref)\n\n        where <obj> may be any object in the file. To determine the shape of\n        the selection in use on the target dataset:\n\n            >>> selection_shape = obj.regionref.selection(existingref)\n    '

    def __init__(self, obj):
        self.id = obj.id
        self._name = None

    def __getitem__(self, args):
        pass

    def shape(self, ref):
        pass

    def selection(self, ref):
        """ Get the shape of the target dataspace selection referred to by *ref*
        """
        pass


class ACL(object):

    @property
    def username(self):
        return self._username

    @property
    def create(self):
        return self._create

    @property
    def delete(self):
        return self._delete

    @property
    def read(self):
        return self._read

    @property
    def update(self):
        return self._update

    @property
    def readACL(self):
        return self._readACL

    @property
    def updateACL(self):
        return self._updateACL

    def __init__(self):
        self._username = None
        self._create = True
        self._delete = True
        self._read = True
        self._update = True
        self._readACL = True
        self._updateACL = True


class HLObject(CommonStateObject):

    @property
    def file(self):
        """ Return a File instance associated with this object """
        from .files import File
        http_conn = self._id.http_conn
        root_uuid = http_conn.root_uuid
        group_json = {}
        group_json['root'] = root_uuid
        group_json['id'] = root_uuid
        group_json['domain'] = http_conn.domain
        group_json['created'] = http_conn.created
        group_json['lastModified'] = http_conn.modified
        groupid = GroupID(None, group_json, http_conn=http_conn)
        return File(groupid)

    def _getNameFromObjDb(self):
        objdb = self._id._http_conn.getObjDb()
        if not objdb:
            return
        root_uuid = self._id.http_conn.root_uuid
        objid = self._id.uuid
        self.log.debug('_getNameFromObjDb: find name for: {}'.format(objid))
        objids = set()
        objids.add(objid)
        h5path = ''
        while not h5path.startswith('/'):
            found_link = False
            for id in objdb:
                if id == objid:
                    self.log.debug('_getNameFromObjDb - skipping id {} - obj cannot link to itself'.format(id))
                    continue
                self.log.debug('_getNameFromObjDb - searching id: {}'.format(id))
                if not id.startswith('g-'):
                    continue
                if id in objids:
                    continue
                obj = objdb[id]
                links = obj['links']
                for title in links:
                    self.log.debug('_getNameFromObjDb - looking at linK: {}'.format(title))
                    link = links[title]
                    if link['class'] != 'H5L_TYPE_HARD':
                        self.log.debug('_getNameFromObjDb - skipping link type: {}'.format(link['class']))
                        continue
                    if link['id'] == objid:
                        found_link = True
                        if not h5path:
                            h5path = title
                        else:
                            h5path = title + '/' + h5path
                        self.log.debug('_getNameFromObjDb - update h5path: {}'.format(h5path))
                        objids.add(id)
                        if id == root_uuid:
                            h5path = '/' + h5path
                            self.log.debug('_getNameFromObjDb - found root')
                        else:
                            objid = id
                            self.log.debug('_getNameFromObjDb - now looking for link to: {}'.format(objid))
                        break

            found_link or self.log.info('_getNameFromObjDb - could not find link')
            break

        if h5path.startswith('/'):
            self.log.debug('_getNameFromObjDb - returning: {}'.format(h5path))
            return h5path
        self.log.debug('_getNameFromObjDb - could not find path')
        return

    @property
    def name(self):
        """ Return the full name of this object.  None if anonymous. """
        try:
            obj_name = self._name
        except AttributeError:
            obj_name = self._getNameFromObjDb()
            if obj_name:
                self._name = obj_name
            if not obj_name:
                self.log.debug('querying server for name to: {}'.format(self._id.id))
                req = None
                if self._id.id.startswith('g-'):
                    req = '/groups/' + self._id.id
                else:
                    if self._id.id.startswith('d-'):
                        req = '/datasets/' + self._id.id
                    else:
                        if self._id.id.startswith('t-'):
                            req = '/datatypes/' + self._id
                        elif req:
                            params = params = {'getalias': 1}
                            self.log.info('sending get alias request for id: {}'.format(self._id.id))
                            obj_json = self.GET(req, params, use_cache=False)
                            if 'alias' in obj_json:
                                alias = obj_json['alias']
                                if len(alias) > 0:
                                    obj_name = alias[0]
                                    self._name = obj_name

        return obj_name

    @property
    def parent(self):
        """Return the parent group of this object.

        This is always equivalent to obj.file[posixpath.dirname(obj.name)].
        ValueError if this object is anonymous.
        """
        if self.name is None:
            raise ValueError('Parent of an anonymous object is undefined')
        return self.file[posixpath.dirname(self.name)]

    @property
    def id(self):
        """ Low-level identifier appropriate for this object """
        return self._id

    @property
    def ref(self):
        """ An (opaque) HDF5 reference to this object """
        return Reference(self)

    @property
    def regionref(self):
        """Create a region reference (Datasets only).

        The syntax is regionref[<slices>]. For example, dset.regionref[...]
        creates a region reference in which the whole dataset is selected.

        Can also be used to determine the shape of the referenced dataset
        (via .shape property), or the shape of the selection (via the
        .selection property).
        """
        return 'todo'

    @property
    def attrs(self):
        """ Attributes attached to this object """
        from . import attrs
        return attrs.AttributeManager(self)

    @property
    def modified(self):
        """Last modified time as a datetime object"""
        return self.id._modified

    def verifyCert(self):
        if 'H5PYD_VERIFY_CERT' in os.environ:
            verify_cert = os.environ['H5PYD_VERIFY_CERT'].upper()
            if verify_cert.startswith('F'):
                return False
        return True

    def GET(self, req, params=None, use_cache=True, format='json'):
        if self.id.http_conn is None:
            raise IOError('object not initialized')
        rsp = self.id._http_conn.GET(req, params=params, format=format, use_cache=use_cache)
        if rsp.status_code != 200:
            self.log.info('Got response: {}'.format(rsp.status_code))
            raise IOError(rsp.status_code, rsp.reason)
        if rsp.headers['Content-Type'] == 'application/octet-stream':
            self.log.info('returning binary content, length: ' + rsp.headers['Content-Length'])
            return rsp.content
        rsp_json = json.loads(rsp.text)
        self.log.debug('rsp_json: {}'.format(rsp_json))
        return rsp_json

    def PUT(self, req, body=None, params=None, format='json', replace=False):
        if self.id.http_conn is None:
            raise IOError('object not initialized')
        else:
            rsp = self._id._http_conn.PUT(req, body=body, params=params, format=format)
            if rsp.status_code not in (200, 201, 204):
                if rsp.status_code == 409:
                    if replace:
                        self.log.info('replacing resource: {}'.format(req))
                        rsp = self.id._http_conn.DELETE(req)
                        if rsp.status_code != 200:
                            raise IOError(rsp.reason)
                        rsp = self._id._http_conn.PUT(req, body=body, params=params, format=format)
                        if rsp.status_code not in (200, 201):
                            raise IOError(rsp.reason)
                    else:
                        raise RuntimeError(rsp.reason)
                else:
                    raise IOError(rsp.reason)
        if rsp.text:
            rsp_json = json.loads(rsp.text)
            return rsp_json

    def POST(self, req, body=None, format='json'):
        if self.id.http_conn is None:
            raise IOError('object not initialized')
        self.log.info('POST: {} [{}]'.format(req, self.id.domain))
        rsp = self.id._http_conn.POST(req, body=body, format=format)
        if rsp.status_code == 409:
            raise ValueError('name already exists')
        if rsp.status_code not in (200, 201):
            raise IOError(rsp.reason)
        if rsp.headers['Content-Type'] == 'application/octet-stream':
            self.log.info('returning binary content, length: ' + rsp.headers['Content-Length'])
            return rsp.content
        rsp_json = json.loads(rsp.text)
        return rsp_json

    def DELETE(self, req):
        if self.id.http_conn is None:
            raise IOError('object not initialized')
        self.log.info('DEL: {} [{}]'.format(req, self.id.domain))
        rsp = self.id._http_conn.DELETE(req)
        if rsp.status_code != 200:
            raise IOError(rsp.reason)

    def __init__--- This code section failed: ---

 L. 972         0  LOAD_FAST                'oid'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _id

 L. 973         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _id
               10  LOAD_ATTR                http_conn
               12  LOAD_ATTR                logging
               14  LOAD_FAST                'self'
               16  STORE_ATTR               log

 L. 974        18  LOAD_CONST               None
               20  LOAD_FAST                'self'
               22  STORE_ATTR               req_prefix

 L. 975        24  LOAD_FAST                'file'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _file

 L. 978        30  LOAD_FAST                'self'
               32  LOAD_ATTR                log
               34  LOAD_ATTR                handlers
               36  POP_JUMP_IF_TRUE    116  'to 116'

 L. 980        38  LOAD_GLOBAL              os
               40  LOAD_METHOD              getcwd
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  STORE_FAST               'log_path'

 L. 981        46  LOAD_GLOBAL              os
               48  LOAD_METHOD              access
               50  LOAD_FAST                'log_path'
               52  LOAD_GLOBAL              os
               54  LOAD_ATTR                W_OK
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  POP_JUMP_IF_TRUE     64  'to 64'

 L. 982        60  LOAD_STR                 '/tmp'
               62  STORE_FAST               'log_path'
             64_0  COME_FROM            58  '58'

 L. 983        64  LOAD_GLOBAL              os
               66  LOAD_ATTR                path
               68  LOAD_METHOD              join
               70  LOAD_FAST                'log_path'
               72  LOAD_STR                 'h5pyd.log'
               74  CALL_METHOD_2         2  '2 positional arguments'
               76  STORE_FAST               'log_file'

 L. 984        78  LOAD_FAST                'self'
               80  LOAD_ATTR                log
               82  LOAD_METHOD              setLevel
               84  LOAD_GLOBAL              logging
               86  LOAD_ATTR                INFO
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_TOP          

 L. 985        92  LOAD_GLOBAL              logging
               94  LOAD_METHOD              FileHandler
               96  LOAD_FAST                'log_file'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  STORE_FAST               'fh'

 L. 986       102  LOAD_FAST                'self'
              104  LOAD_ATTR                log
              106  LOAD_METHOD              addHandler
              108  LOAD_FAST                'fh'
              110  CALL_METHOD_1         1  '1 positional argument'
              112  POP_TOP          
              114  JUMP_FORWARD        116  'to 116'
            116_0  COME_FROM           114  '114'
            116_1  COME_FROM            36  '36'

Parse error at or near `COME_FROM' instruction at offset 116_0

    def __eq__(self, other):
        if hasattr(other, 'id'):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        with phil:
            return bool(self.id)

    __nonzero__ = __bool__

    def getACL(self, username):
        req = self._req_prefix + '/acls/' + username
        rsp_json = self.GET(req)
        acl_json = rsp_json['acl']
        return acl_json

    def getACLs(self):
        req = self._req_prefix + '/acls'
        rsp_json = self.GET(req)
        acls_json = rsp_json['acls']
        return acls_json

    def putACL(self, acl):
        if 'userName' not in acl:
            raise IOError("ACL has no 'userName' key")
        perm = {}
        for k in ('create', 'read', 'update', 'delete', 'readACL', 'updateACL'):
            perm[k] = acl[k]

        req = self._req_prefix + '/acls/' + acl['userName']
        self.PUT(req, body=perm)


class ValuesViewHDF5(ValuesView):
    __doc__ = '\n        Wraps e.g. a Group or AttributeManager to provide a value view.\n\n        Note that __contains__ will have poor performance as it has\n        to scan all the links or attributes.\n    '

    def __contains__(self, value):
        with phil:
            for key in self._mapping:
                if value == self._mapping.get(key):
                    return True

            return False

    def __iter__(self):
        with phil:
            for key in self._mapping:
                yield self._mapping.get(key)


class ItemsViewHDF5(ItemsView):
    __doc__ = '\n        Wraps e.g. a Group or AttributeManager to provide an items view.\n    '

    def __contains__(self, item):
        with phil:
            key, val = item
            if key in self._mapping:
                return val == self._mapping.get(key)
            return False

    def __iter__(self):
        with phil:
            for key in self._mapping:
                yield (
                 key, self._mapping.get(key))


class MappingHDF5(Mapping):
    __doc__ = "\n        Wraps a Group, AttributeManager or DimensionManager object to provide\n        an immutable mapping interface.\n\n        We don't inherit directly from MutableMapping because certain\n        subclasses, for example DimensionManager, are read-only.\n    "

    def keys(self):
        """ Get a view object on member names """
        return KeysView(self)

    def values(self):
        """ Get a view object on member objects """
        return ValuesViewHDF5(self)

    def items(self):
        """ Get a view object on member items """
        return ItemsViewHDF5(self)


class MutableMappingHDF5(MappingHDF5, MutableMapping):
    __doc__ = '\n        Wraps a Group or AttributeManager object to provide a mutable\n        mapping interface, in contrast to the read-only mapping of\n        MappingHDF5.\n    '