# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/group.py
# Compiled at: 2019-12-23 13:50:33
# Size of source mod 2**32: 41403 bytes
from __future__ import absolute_import
import os.path as op
import numpy, collections
from .base import HLObject, MutableMappingHDF5, guess_dtype
from .objectid import TypeID, GroupID, DatasetID
from . import dataset
from .dataset import Dataset
from . import table
from .table import Table
from .datatype import Datatype
from . import h5type

class Group(HLObject, MutableMappingHDF5):
    __doc__ = ' Represents an HDF5 group.\n    '

    def __init__(self, bind, **kwargs):
        """ Create a new Group object by binding to a low-level GroupID.
        """
        if not isinstance(bind, GroupID):
            raise ValueError('%s is not a GroupID' % bind)
        (HLObject.__init__)(self, bind, **kwargs)
        self._req_prefix = '/groups/' + self.id.uuid
        self._link_db = {}

    def _get_link_json(self, h5path):
        """ Return parent_uuid and json description of link for given path """
        self.log.debug('__get_link_json({})'.format(h5path))
        parent_uuid = self.id.uuid
        tgt_json = None
        if isinstance(h5path, bytes):
            h5path = h5path.decode('utf-8')
        else:
            if h5path.find('/') == -1:
                in_group = True
            else:
                in_group = False
            if h5path[0] == '/':
                parent_uuid = self.id.http_conn.root_uuid
                tgt_json = {'collection':'groups', 
                 'class':'H5L_TYPE_HARD',  'id':parent_uuid}
                if h5path == '/':
                    return (parent_uuid, tgt_json)
            elif in_group:
                if h5path in self._link_db:
                    tgt_json = self._link_db[h5path]
                    parent_uuid = self.id.id
                    return (
                     parent_uuid, tgt_json)
        path = h5path.split('/')
        objdb = self.id._http_conn.getObjDb()
        if objdb:
            self.log.debug('searching objdb for {}'.format(h5path))
            group_uuid = parent_uuid
            for name in path:
                if not name:
                    continue
                if group_uuid not in objdb:
                    self.log.warn('objdb search: {} not found in objdb'.format(group_uuid))
                    tgt_json = None
                    break
                group_json = objdb[group_uuid]
                group_links = group_json['links']
                if name not in group_links:
                    self.log.debug('objdb search: {} not found'.format(name))
                    tgt_json = None
                    break
                tgt_json = group_links[name]
                if tgt_json['class'] != 'H5L_TYPE_HARD':
                    group_uuid = None
                    self.log.debug('objdb search: non-hardlink')
                else:
                    group_uuid = tgt_json['id']

            if tgt_json:
                if group_uuid and group_uuid.startswith('g-'):
                    tgt_json['collection'] = 'groups'
                else:
                    if group_uuid and group_uuid.startswith('d-'):
                        tgt_json['collection'] = 'datasets'
                    else:
                        if group_uuid and group_uuid.startswith('t-'):
                            tgt_json['collection'] = 'datatypes'
                        else:
                            self.log.debug('no collection for non hardlink')
                return (
                 group_uuid, tgt_json)
            raise KeyError('Unable to open object (Component not found)')
        for name in path:
            if not name:
                continue
            else:
                if not parent_uuid:
                    raise KeyError('Unable to open object (Component not found)')
                req = '/groups/' + parent_uuid + '/links/' + name
                try:
                    rsp_json = self.GET(req)
                except IOError:
                    raise KeyError('Unable to open object (Component not found)')

            if 'link' not in rsp_json:
                raise IOError('Unexpected Error')
            tgt_json = rsp_json['link']
            if in_group:
                self._link_db[name] = tgt_json
            if tgt_json['class'] == 'H5L_TYPE_HARD':
                if tgt_json['collection'] == 'groups':
                    parent_uuid = tgt_json['id']
                else:
                    parent_uuid = None

        return (
         parent_uuid, tgt_json)

    def _get_objdb_links(self):
        """ Return the links json from the objdb if present.
        """
        objdb = self.id.http_conn.getObjDb()
        if not objdb:
            return
        if self.id.id not in objdb:
            self.log.warn('{} not found in objdb'.format(self.id.id))
            return
        group_json = objdb[self.id.id]
        return group_json['links']

    def create_group(self, h5path):
        """ Create and return a new subgroup.

        Name may be absolute or relative.  Fails if the target name already
        exists.
        """
        if h5path[(-1)] == '/':
            raise ValueError('Invalid path for create_group')
        elif h5path[0] == '/':
            parent_uuid = self.file.id.id
            parent_name = '/'
        else:
            parent_uuid = self.id.id
            parent_name = self._name
        self.log.info('create_group: {}'.format(h5path))
        links = h5path.split('/')
        sub_group = None
        for link in links:
            if not link:
                continue
            self.log.debug('create_group - iterate for link: {}'.format(link))
            create_group = False
            req = '/groups/' + parent_uuid + '/links/' + link
            try:
                rsp_json = self.GET(req)
            except IOError as ioe:
                try:
                    self.log.debug('Got ioe: {}'.format(ioe))
                    create_group = True
                finally:
                    ioe = None
                    del ioe

            if create_group:
                link_json = {'id':parent_uuid, 
                 'name':link}
                body = {'link': link_json}
                self.log.debug('create group with body: {}'.format(body))
                rsp = self.POST('/groups', body=body)
                group_json = rsp
                groupId = GroupID(self, group_json)
                sub_group = Group(groupId)
                if parent_name:
                    if parent_name[(-1)] == '/':
                        parent_name = parent_name + link
                    else:
                        parent_name = parent_name + '/' + link
                    self.log.debug('create group - parent name: {}'.format(parent_name))
                    sub_group._name = parent_name
                parent_uuid = sub_group.id.id
            else:
                self.log.debug('create group - found subgroup: {}'.format(link))
                if 'link' not in rsp_json:
                    raise IOError('Unexpected Error')
                link_json = rsp_json['link']
                if link_json['class'] != 'H5L_TYPE_HARD':
                    raise IOError('cannot create subgroup of softlink')
                parent_uuid = link_json['id']
            if parent_name:
                if parent_name[(-1)] == '/':
                    parent_name = parent_name + link_json['title']
                else:
                    parent_name = parent_name + '/' + link_json['title']
                self.log.debug('create group - parent name: {}'.format(parent_name))

        if sub_group is None:
            raise ValueError('name already exists')
        return sub_group

    def create_dataset(self, name, shape=None, dtype=None, data=None, **kwds):
        """ Create a new HDF5 dataset

        name
            Name of the dataset (absolute or relative).  Provide None to make
            an anonymous dataset.
        shape
            Dataset shape.  Use "()" for scalar datasets.  Required if "data"
            isn't provided.
        dtype
            Numpy dtype or string.  If omitted, dtype('f') will be used.
            Required if "data" isn't provided; otherwise, overrides data
            array's dtype.
        data
            Provide data to initialize the dataset.  If used, you can omit
            shape and dtype arguments.

        Keyword-only arguments:

        chunks
            (Tuple) Chunk shape, or True to enable auto-chunking.
        maxshape
            (Tuple) Make the dataset resizable up to this shape.  Use None for
            axes you want to be unlimited.
        compression
            (String or int) Compression strategy.  Legal values are 'gzip',
            'szip', 'lzf'.  If an integer in range(10), this indicates gzip
            compression level. Otherwise, an integer indicates the number of a
            dynamically loaded compression filter.
        compression_opts
            Compression settings.  This is an integer for gzip, 2-tuple for
            szip, etc. If specifying a dynamically loaded compression filter
            number, this must be a tuple of values.
        scaleoffset
            (Integer) Enable scale/offset filter for (usually) lossy
            compression of integer or floating-point data. For integer
            data, the value of scaleoffset is the number of bits to
            retain (pass 0 to let HDF5 determine the minimum number of
            bits necessary for lossless compression). For floating point
            data, scaleoffset is the number of digits after the decimal
            place to retain; stored values thus have absolute error
            less than 0.5*10**(-scaleoffset).
        shuffle
            (T/F) Enable shuffle filter.
        fletcher32
            (T/F) Enable fletcher32 error detection. Not permitted in
            conjunction with the scale/offset filter.
        fillvalue
            (Scalar) Use this value for uninitialized parts of the dataset.
        track_times
            (T/F) Enable dataset creation timestamps.
        """
        if self.id.http_conn.mode == 'r':
            raise ValueError('Unable to create dataset (No write intent on file)')
        else:
            if shape is None:
                if data is None:
                    raise TypeError('Either data or shape must be specified')
            else:
                if data is not None:
                    if dtype is None:
                        dtype = guess_dtype(data)
                    if not isinstance(data, numpy.ndarray) or dtype != data.dtype:
                        data = numpy.asarray(data, order='C', dtype=dtype)
                        dtype = data.dtype
                    self.log.info('data dtype: {}'.format(data.dtype))
                if shape is None:
                    if data is None:
                        raise TypeError('Either data or shape must be specified')
                    shape = data.shape
                else:
                    shape = tuple(shape)
            if data is not None and numpy.product(shape) != numpy.product(data.shape):
                raise ValueError('Shape tuple is incompatible with data')
        dsid = (dataset.make_new_dset)(self, shape=shape, dtype=dtype, **kwds)
        dset = dataset.Dataset(dsid)
        if data is not None:
            self.log.info('initialize data')
            dset[...] = data
        if name is not None:
            items = name.split('/')
            path = []
            for item in items:
                if len(item) > 0:
                    path.append(item)

            grp = self
            if len(path) == 0:
                return dset
            dset_link = path[(-1)]
            dset._name = self._name
            if dset._name[(-1)] != '/':
                dset._name += '/'
            if len(path) > 1:
                grp_path = path[:-1]
                for item in grp_path:
                    if item not in grp:
                        grp = grp.create_group(item)
                    else:
                        grp = grp[item]
                    dset._name = dset._name + item + '/'

            dset._name += dset_link
            grp[dset_link] = dset
        return dset

    def create_table(self, name, numrows=None, dtype=None, data=None, **kwds):
        """ Create a new Table - a one dimensional HDF5 Dataset with a compound type

        name
            Name of the dataset (absolute or relative).  Provide None to make
            an anonymous dataset.
        shape
            Dataset shape.  Use "()" for scalar datasets.  Required if "data"
            isn't provided.
        dtype
            Numpy dtype or string.  If omitted, dtype('f') will be used.
            Required if "data" isn't provided; otherwise, overrides data
            array's dtype.
        data
            Provide data to initialize the dataset.  If used, you can omit
            shape and dtype arguments.

        Keyword-only arguments:
        """
        shape = None
        if data is not None:
            if dtype is None:
                dtype = guess_dtype(data)
            else:
                if dtype is None:
                    dtype = numpy.float32
                if not isinstance(data, numpy.ndarray) or dtype != data.dtype:
                    data = numpy.asarray(data, order='C', dtype=dtype)
                self.log.info('data dtype: {}'.format(data.dtype))
                if len(data.shape) != 1:
                    ValueError('Table must be one-dimensional')
                if numrows and numrows != data.shape[0]:
                    ValueError('Data does not match numrows value')
            shape = data.shape
        else:
            if numrows:
                shape = [
                 numrows]
            else:
                shape = [
                 0]
        if dtype is None:
            ValueError('dtype must be specified or data provided')
        if len(dtype) < 1:
            ValueError('dtype must be compound')
        kwds['maxshape'] = (0, )
        dset = (self.create_dataset)(name, shape=shape, dtype=dtype, data=data, **kwds)
        obj = table.Table(dset.id)
        return obj

    def require_dataset(self, name, shape, dtype, exact=False, **kwds):
        """ Open a dataset, creating it if it doesn't exist.

        If keyword "exact" is False (default), an existing dataset must have
        the same shape and a conversion-compatible dtype to be returned.  If
        True, the shape and dtype must match exactly.

        Other dataset keywords (see create_dataset) may be provided, but are
        only used if a new dataset is to be created.

        Raises TypeError if an incompatible object already exists, or if the
        shape or dtype don't match according to the above rules.
        """
        if name not in self:
            return (self.create_dataset)(name, *(shape, dtype), **kwds)
        dset = self[name]
        if not isinstance(dset, Dataset):
            raise TypeError('Incompatible object (%s) already exists' % dset.__class__.__name__)
        if not shape == dset.shape:
            raise TypeError('Shapes do not match (existing %s vs new %s)' % (dset.shape, shape))
        elif exact and not dtype == dset.dtype:
            raise TypeError('Datatypes do not exactly match (existing %s vs new %s)' % (dset.dtype, dtype))
        else:
            if not numpy.can_cast(dtype, dset.dtype):
                raise TypeError('Datatypes cannot be safely cast (existing %s vs new %s)' % (dset.dtype, dtype))
        return dset

    def require_group(self, name):
        """ Return a group, creating it if it doesn't exist.

        TypeError is raised if something with that name already exists that
        isn't a group.
        """
        if name not in self:
            return self.create_group(name)
        grp = self[name]
        if not isinstance(grp, Group):
            raise TypeError('Incompatible object (%s) already exists' % grp.__class__.__name__)
        return grp

    def __getitem__(self, name):
        """ Open an object in the file """
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        self.log.debug('group.__getitem__({})'.format(name))

        def getObjByUuid(uuid, collection_type=None):
            """ Utility method to get an obj based on collection type and uuid """
            self.log.debug('getObjByUuid({})'.format(uuid))
            obj_json = None
            if uuid.startswith('groups/'):
                uuid = uuid[len('groups/'):]
                if collection_type is None:
                    collection_type = 'groups'
                else:
                    if uuid.startswith('datasets/'):
                        uuid = uuid[len('datasets/'):]
                        if collection_type is None:
                            collection_type = 'datasets'
                    elif uuid.startswith('datatypes/'):
                        uuid = uuid[len('datatypes/'):]
                        if collection_type is None:
                            collection_type = 'datatypes'
            elif collection_type is None:
                if uuid.startswith('g-'):
                    collection_type = 'groups'
                else:
                    if uuid.startswith('t-'):
                        collection_type = 'datatypes'
                    else:
                        if uuid.startswith('d-'):
                            collection_type = 'datasets'
                        else:
                            raise IOError('Unexpected uuid: {}'.format(uuid))
            objdb = self.id.http_conn.getObjDb()
            if objdb and uuid in objdb:
                obj_json = objdb[uuid]
            else:
                req = '/' + collection_type + '/' + uuid
                obj_json = self.GET(req)
            if collection_type == 'groups':
                tgt = Group(GroupID(self, obj_json))
            else:
                if collection_type == 'datatypes':
                    tgt = Datatype(TypeID(self, obj_json))
                else:
                    if collection_type == 'datasets':
                        shape_json = obj_json['shape']
                        dtype_json = obj_json['type']
                        if 'dims' in shape_json and len(shape_json['dims']) == 1 and dtype_json['class'] == 'H5T_COMPOUND':
                            tgt = Table(DatasetID(self, obj_json))
                        else:
                            tgt = Dataset(DatasetID(self, obj_json))
                    else:
                        raise IOError('Unexpecrted collection_type: {}'.format(collection_type))
            return tgt

        def isUUID(name):
            if isinstance(name, str) and len(name) >= 38 and not name.startswith('groups/'):
                if name.startswith('g-'):
                    return True
                if name.startswith('datatypes/') or name.startswith('t-'):
                    return True
                if name.startswith('datasets/') or name.startswith('d-'):
                    return True
                return False
            else:
                return False

        tgt = None
        if isinstance(name, h5type.Reference):
            tgt = name.objref()
            if tgt is not None:
                return tgt
            elif isinstance(name.id, GroupID):
                tgt = getObjByUuid((name.id.uuid), collection_type='groups')
            else:
                if isinstance(name.id, DatasetID):
                    tgt = getObjByUuid((name.id.uuid), collection_type='datasets')
                else:
                    if isinstance(name.id, TypeID):
                        tgt = getObjByUuid((name.id.uuid), collection_type='datasets')
                    else:
                        raise IOError('Unexpected Error - ObjectID type: ' + name.__class__.__name__)
            return tgt
        if isUUID(name):
            tgt = getObjByUuid(name)
            return tgt
        parent_uuid, link_json = self._get_link_json(name)
        link_class = link_json['class']
        if link_class == 'H5L_TYPE_HARD':
            tgt = getObjByUuid((link_json['id']), collection_type=(link_json['collection']))
        else:
            if link_class == 'H5L_TYPE_SOFT':
                h5path = link_json['h5path']
                soft_parent_uuid, soft_json = self._get_link_json(h5path)
                tgt = getObjByUuid((soft_json['id']), collection_type=(soft_json['collection']))
            else:
                if link_class == 'H5L_TYPE_EXTERNAL':
                    from .files import File
                    external_domain = link_json['h5domain']
                    if not op.isabs(external_domain):
                        current_domain = self._id.http_conn.domain
                        external_domain = op.join(op.dirname(current_domain), external_domain)
                        external_domain = op.normpath(external_domain)
                    else:
                        try:
                            f = File(external_domain, endpoint=(self.id.http_conn.endpoint), mode='r', use_session=False)
                        except IOError:
                            raise KeyError('Unable to open file: ' + link_json['h5domain'])

                        return f[link_json['h5path']]
                        if link_class == 'H5L_TYPE_USER_DEFINED':
                            raise IOError('Unable to fetch user-defined link')
                        else:
                            raise IOError('Unexpected error, invalid link class:' + link_json['class'])
                elif name[0] == '/':
                    tgt._name = name
                else:
                    if self.name:
                        if self.name[(-1)] == '/':
                            tgt._name = self.name + name
                        else:
                            tgt._name = self.name + '/' + name
                    else:
                        tgt._name = name
                return tgt

    def get(self, name, default=None, getclass=False, getlink=False):
        """ Retrieve an item or other information.

        "name" given only:
            Return the item, or "default" if it doesn't exist

        "getclass" is True:
            Return the class of object (Group, Dataset, etc.), or "default"
            if nothing with that name exists

        "getlink" is True:
            Return HardLink, SoftLink or ExternalLink instances.  Return
            "default" if nothing with that name exists.

        "getlink" and "getclass" are True:
            Return HardLink, SoftLink and ExternalLink classes.  Return
            "default" if nothing with that name exists.

        Example:

        >>> cls = group.get('foo', getclass=True)
        >>> if cls == SoftLink:
        ...     print '"foo" is a soft link!'
        """
        if not (getclass or getlink):
            try:
                return self[name]
            except KeyError:
                return default

            if name not in self:
                return default
            if getclass:
                obj = getlink or self.__getitem__(name)
                if obj is None:
                    return
                if obj.id.__class__ is GroupID:
                    return Group
                if obj.id.__class__ is DatasetID:
                    return Dataset
                if obj.id.__class__ is TypeID:
                    return Datatype
                raise TypeError('Unknown object type')
        elif getlink:
            parent_uuid, link_json = self._get_link_json(name)
            typecode = link_json['class']
            if typecode == 'H5L_TYPE_SOFT':
                if getclass:
                    return SoftLink
                return SoftLink(link_json['h5path'])
            if typecode == 'H5L_TYPE_EXTERNAL':
                if getclass:
                    return ExternalLink
                return ExternalLink(link_json['h5domain'], link_json['h5path'])
            if typecode == 'H5L_TYPE_HARD':
                if getclass:
                    return HardLink
                return HardLink()
            raise TypeError('Unknown link type')

    def __setitem__--- This code section failed: ---

 L. 700         0  LOAD_FAST                'name'
                2  LOAD_METHOD              find
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  LOAD_CONST               -1
               10  COMPARE_OP               !=
               12  POP_JUMP_IF_FALSE   154  'to 154'

 L. 701        14  LOAD_GLOBAL              op
               16  LOAD_METHOD              dirname
               18  LOAD_FAST                'name'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  STORE_FAST               'parent_path'

 L. 702        24  LOAD_GLOBAL              op
               26  LOAD_METHOD              basename
               28  LOAD_FAST                'name'
               30  CALL_METHOD_1         1  '1 positional argument'
               32  STORE_FAST               'basename'

 L. 703        34  LOAD_FAST                'basename'
               36  POP_JUMP_IF_TRUE     46  'to 46'

 L. 704        38  LOAD_GLOBAL              KeyError
               40  LOAD_STR                 "Group path can not end with '/'"
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L. 705        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _get_link_json
               50  LOAD_FAST                'parent_path'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'parent_uuid'
               58  STORE_FAST               'link_json'

 L. 706        60  LOAD_FAST                'parent_uuid'
               62  LOAD_CONST               None
               64  COMPARE_OP               is
               66  POP_JUMP_IF_FALSE    82  'to 82'

 L. 707        68  LOAD_GLOBAL              KeyError
               70  LOAD_STR                 'group path: {} not found'
               72  LOAD_METHOD              format
               74  LOAD_FAST                'parent_path'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  RAISE_VARARGS_1       1  'exception instance'
             82_0  COME_FROM            66  '66'

 L. 708        82  LOAD_FAST                'link_json'
               84  LOAD_STR                 'class'
               86  BINARY_SUBSCR    
               88  LOAD_STR                 'H5L_TYPE_HARD'
               90  COMPARE_OP               !=
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 709        94  LOAD_GLOBAL              IOError
               96  LOAD_STR                 'cannot create subgroup of softlink'
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            92  '92'

 L. 710       102  LOAD_FAST                'link_json'
              104  LOAD_STR                 'id'
              106  BINARY_SUBSCR    
              108  STORE_FAST               'parent_uuid'

 L. 711       110  LOAD_STR                 '/groups/'
              112  LOAD_FAST                'parent_uuid'
              114  BINARY_ADD       
              116  STORE_FAST               'req'

 L. 712       118  LOAD_FAST                'self'
              120  LOAD_METHOD              GET
              122  LOAD_FAST                'req'
              124  CALL_METHOD_1         1  '1 positional argument'
              126  STORE_FAST               'group_json'

 L. 713       128  LOAD_GLOBAL              Group
              130  LOAD_GLOBAL              GroupID
              132  LOAD_FAST                'self'
              134  LOAD_FAST                'group_json'
              136  CALL_FUNCTION_2       2  '2 positional arguments'
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  STORE_FAST               'tgt'

 L. 714       142  LOAD_FAST                'obj'
              144  LOAD_FAST                'tgt'
              146  LOAD_FAST                'basename'
              148  STORE_SUBSCR     
          150_152  JUMP_FORWARD        462  'to 462'
            154_0  COME_FROM            12  '12'

 L. 716       154  LOAD_GLOBAL              isinstance
              156  LOAD_FAST                'obj'
              158  LOAD_GLOBAL              HLObject
              160  CALL_FUNCTION_2       2  '2 positional arguments'
              162  POP_JUMP_IF_FALSE   212  'to 212'

 L. 717       164  LOAD_STR                 'id'
              166  LOAD_FAST                'obj'
              168  LOAD_ATTR                id
              170  LOAD_ATTR                uuid
              172  BUILD_MAP_1           1 
              174  STORE_FAST               'body'

 L. 718       176  LOAD_STR                 '/groups/'
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                id
              182  LOAD_ATTR                uuid
              184  BINARY_ADD       
              186  LOAD_STR                 '/links/'
              188  BINARY_ADD       
              190  LOAD_FAST                'name'
              192  BINARY_ADD       
              194  STORE_FAST               'req'

 L. 719       196  LOAD_FAST                'self'
              198  LOAD_ATTR                PUT
              200  LOAD_FAST                'req'
              202  LOAD_FAST                'body'
              204  LOAD_CONST               ('body',)
              206  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              208  POP_TOP          
              210  JUMP_FORWARD        462  'to 462'
            212_0  COME_FROM           162  '162'

 L. 721       212  LOAD_GLOBAL              isinstance
              214  LOAD_FAST                'obj'
              216  LOAD_GLOBAL              SoftLink
              218  CALL_FUNCTION_2       2  '2 positional arguments'
          220_222  POP_JUMP_IF_FALSE   270  'to 270'

 L. 722       224  LOAD_STR                 'h5path'
              226  LOAD_FAST                'obj'
              228  LOAD_ATTR                path
              230  BUILD_MAP_1           1 
              232  STORE_FAST               'body'

 L. 723       234  LOAD_STR                 '/groups/'
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                id
              240  LOAD_ATTR                uuid
              242  BINARY_ADD       
              244  LOAD_STR                 '/links/'
              246  BINARY_ADD       
              248  LOAD_FAST                'name'
              250  BINARY_ADD       
              252  STORE_FAST               'req'

 L. 724       254  LOAD_FAST                'self'
              256  LOAD_ATTR                PUT
              258  LOAD_FAST                'req'
              260  LOAD_FAST                'body'
              262  LOAD_CONST               ('body',)
              264  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              266  POP_TOP          
              268  JUMP_FORWARD        462  'to 462'
            270_0  COME_FROM           220  '220'

 L. 728       270  LOAD_GLOBAL              isinstance
              272  LOAD_FAST                'obj'
              274  LOAD_GLOBAL              ExternalLink
              276  CALL_FUNCTION_2       2  '2 positional arguments'
          278_280  POP_JUMP_IF_FALSE   332  'to 332'

 L. 729       282  LOAD_FAST                'obj'
              284  LOAD_ATTR                path

 L. 730       286  LOAD_FAST                'obj'
              288  LOAD_ATTR                filename
              290  LOAD_CONST               ('h5path', 'h5domain')
              292  BUILD_CONST_KEY_MAP_2     2 
              294  STORE_FAST               'body'

 L. 731       296  LOAD_STR                 '/groups/'
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                id
              302  LOAD_ATTR                uuid
              304  BINARY_ADD       
              306  LOAD_STR                 '/links/'
              308  BINARY_ADD       
              310  LOAD_FAST                'name'
              312  BINARY_ADD       
              314  STORE_FAST               'req'

 L. 732       316  LOAD_FAST                'self'
              318  LOAD_ATTR                PUT
              320  LOAD_FAST                'req'
              322  LOAD_FAST                'body'
              324  LOAD_CONST               ('body',)
              326  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              328  POP_TOP          
              330  JUMP_FORWARD        462  'to 462'
            332_0  COME_FROM           278  '278'

 L. 736       332  LOAD_GLOBAL              isinstance
              334  LOAD_FAST                'obj'
              336  LOAD_GLOBAL              numpy
              338  LOAD_ATTR                dtype
              340  CALL_FUNCTION_2       2  '2 positional arguments'
          342_344  POP_JUMP_IF_FALSE   462  'to 462'

 L. 739       346  LOAD_GLOBAL              h5type
              348  LOAD_METHOD              getTypeItem
              350  LOAD_FAST                'obj'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  STORE_FAST               'type_json'

 L. 740       356  LOAD_STR                 '/datatypes'
              358  STORE_FAST               'req'

 L. 742       360  LOAD_STR                 'type'
              362  LOAD_FAST                'type_json'
              364  BUILD_MAP_1           1 
              366  STORE_FAST               'body'

 L. 743       368  LOAD_FAST                'self'
              370  LOAD_ATTR                POST
              372  LOAD_FAST                'req'
              374  LOAD_FAST                'body'
              376  LOAD_CONST               ('body',)
              378  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              380  STORE_FAST               'rsp'

 L. 744       382  LOAD_FAST                'rsp'
              384  LOAD_STR                 'id'
              386  BINARY_SUBSCR    
              388  LOAD_FAST                'body'
              390  LOAD_STR                 'id'
              392  STORE_SUBSCR     

 L. 745       394  LOAD_FAST                'rsp'
              396  LOAD_STR                 'lastModified'
              398  BINARY_SUBSCR    
              400  LOAD_FAST                'body'
              402  LOAD_STR                 'lastModified'
              404  STORE_SUBSCR     

 L. 747       406  LOAD_GLOBAL              TypeID
              408  LOAD_FAST                'self'
              410  LOAD_FAST                'body'
              412  CALL_FUNCTION_2       2  '2 positional arguments'
              414  STORE_FAST               'type_id'

 L. 748       416  LOAD_STR                 '/groups/'
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                id
              422  LOAD_ATTR                uuid
              424  BINARY_ADD       
              426  LOAD_STR                 '/links/'
              428  BINARY_ADD       
              430  LOAD_FAST                'name'
              432  BINARY_ADD       
              434  STORE_FAST               'req'

 L. 749       436  LOAD_STR                 'id'
              438  LOAD_FAST                'type_id'
              440  LOAD_ATTR                uuid
              442  BUILD_MAP_1           1 
              444  STORE_FAST               'body'

 L. 750       446  LOAD_FAST                'self'
              448  LOAD_ATTR                PUT
              450  LOAD_FAST                'req'
              452  LOAD_FAST                'body'
              454  LOAD_CONST               ('body',)
              456  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              458  POP_TOP          
              460  JUMP_FORWARD        462  'to 462'
            462_0  COME_FROM           460  '460'
            462_1  COME_FROM           342  '342'
            462_2  COME_FROM           330  '330'
            462_3  COME_FROM           268  '268'
            462_4  COME_FROM           210  '210'
            462_5  COME_FROM           150  '150'

Parse error at or near `COME_FROM' instruction at offset 462_4

    def __delitem__(self, name):
        """ Delete (unlink) an item from this group. """
        req = '/groups/' + self.id.uuid + '/links/' + name
        self.DELETE(req)
        if name.find('/') == -1:
            if name in self._link_db:
                del self._link_db[name]

    def __len__(self):
        """ Number of members attached to this group """
        links_json = self._get_objdb_links()
        if links_json:
            return len(links_json)
        req = '/groups/' + self.id.uuid
        rsp_json = self.GET(req)
        return rsp_json['linkCount']

    def __iter__(self):
        """ Iterate over member names """
        links = self._get_objdb_links()
        if links is None:
            req = '/groups/' + self.id.uuid + '/links'
            rsp_json = self.GET(req)
            links = rsp_json['links']
            self._link_db = {}
            for link in links:
                name = link['title']
                self._link_db[name] = link

            for x in links:
                yield x['title']

        else:
            for name in links:
                yield name

    def __contains__(self, name):
        """ Test if a member name exists """
        found = False
        try:
            link_json = self._get_link_json(name)
            found = True
        except KeyError:
            pass

        return found

    def copy(self, source, dest, name=None, shallow=False, expand_soft=False, expand_external=False, expand_refs=False, without_attrs=False):
        """Copy an object or group.

        The source can be a path, Group, Dataset, or Datatype object.  The
        destination can be either a path or a Group object.  The source and
        destinations need not be in the same file.

        If the source is a Group object, all objects contained in that group
        will be copied recursively.

        When the destination is a Group object, by default the target will
        be created in that group with its current name (basename of obj.name).
        You can override that by setting "name" to a string.

        There are various options which all default to "False":

         - shallow: copy only immediate members of a group.

         - expand_soft: expand soft links into new objects.

         - expand_external: expand external links into new objects.

         - expand_refs: copy objects that are pointed to by references.

         - without_attrs: copy object without copying attributes.

       Example:

        >>> f = File('myfile.hdf5')
        >>> f.listnames()
        ['MyGroup']
        >>> f.copy('MyGroup', 'MyCopy')
        >>> f.listnames()
        ['MyGroup', 'MyCopy']

        """
        pass

    def move(self, source, dest):
        """ Move a link to a new location in the file.

        If "source" is a hard link, this effectively renames the object.  If
        "source" is a soft or external link, the link itself is moved, with its
        value unmodified.
        """
        pass

    def visit(self, func):
        """ Recursively visit all names in this group and subgroups (HDF5 1.8).

        You supply a callable (function, method or callable object); it
        will be called exactly once for each link in this group and every
        group below it. Your callable must conform to the signature:

            func(<member name>) => <None or return value>

        Returning None continues iteration, returning anything else stops
        and immediately returns that value from the visit method.  No
        particular order of iteration within groups is guranteed.

        Example:

        >>> # List the entire contents of the file
        >>> f = File("foo.hdf5")
        >>> list_of_names = []
        >>> f.visit(list_of_names.append)
        """
        return self.visititems(func)

    def visititems(self, func):
        """ Recursively visit names and objects in this group (HDF5 1.8).

        You supply a callable (function, method or callable object); it
        will be called exactly once for each link in this group and every
        group below it. Your callable must conform to the signature:

            func(<member name>, <object>) => <None or return value>

        Returning None continues iteration, returning anything else stops
        and immediately returns that value from the visit method.  No
        particular order of iteration within groups is guranteed.

        Example:

        # Get a list of all datasets in the file
        >>> mylist = []
        >>> def func(name, obj):
        ...     if isinstance(obj, Dataset):
        ...         mylist.append(name)
        ...
        >>> f = File('foo.hdf5')
        >>> f.visititems(func)
        """
        visited = collections.OrderedDict()
        visited[self.id.uuid] = True
        tovisit = collections.OrderedDict()
        tovisit[self.id.uuid] = self
        retval = None
        nargs = func.__code__.co_argcount
        while len(tovisit) > 0:
            parent_uuid, parent = tovisit.popitem(last=True)
            if parent.name != '/':
                h5path = parent.name
                if h5path[0] == '/':
                    h5path = h5path[1:]
                elif nargs == 1:
                    retval = func(h5path)
                else:
                    retval = func(h5path, parent)
                if retval is not None:
                    break
            visited[parent.id.uuid] = True
            if parent.id.__class__ is GroupID:
                objdb = self.id._http_conn.getObjDb()
                if objdb:
                    if parent.id.uuid not in objdb:
                        raise IOError('expected to find id {} in objdb'.format(parent.id.uuid))
                    group_json = objdb[parent.id.uuid]
                    links_json = group_json['links']
                    links = []
                    for k in links_json:
                        item = links_json[k]
                        item['title'] = k
                        links.append(item)

                else:
                    req = '/groups/' + parent.id.uuid + '/links'
                    rsp_json = self.GET(req)
                    links = rsp_json['links']
                for link in links:
                    obj = None
                    if link['class'] == 'H5L_TYPE_SOFT':
                        pass
                    elif link['class'] == 'H5L_TYPE_EXTERNAL':
                        pass
                    elif link['class'] == 'H5L_TYPE_UDLINK':
                        obj = UserDefinedLink()
                    else:
                        if link['class'] == 'H5L_TYPE_HARD':
                            if link['id'] in visited:
                                continue
                            obj = parent.__getitem__(link['title'])
                            tovisit[obj.id.uuid] = obj
                            obj = None
                    if obj is not None:
                        link_name = parent.name + '/' + link['title']
                        if link_name[0] == '/':
                            link_name = link_name[1:]
                        elif nargs == 1:
                            retval = func(link_name)
                        else:
                            retval = func(link_name, obj)
                        if retval is not None:
                            break

        return retval

    def __repr__(self):
        if not self:
            r = '<Closed HDF5 group>'
        else:
            if self.name is None:
                namestr = '(anonymous)'
            else:
                namestr = f'"{self.name}"'
            r = f"<HDF5 group {namestr} ({len(self)} members)>"
        return r


class HardLink(object):
    __doc__ = '\n        Represents a hard link in an HDF5 file.  Provided only so that\n        Group.get works in a sensible way.  Has no other function.\n    '


class SoftLink(object):
    __doc__ = '\n        Represents a symbolic ("soft") link in an HDF5 file.  The path\n        may be absolute or relative.  No checking is performed to ensure\n        that the target actually exists.\n    '

    @property
    def path(self):
        return self._path

    def __init__(self, path):
        self._path = str(path)

    def __repr__(self):
        return '<SoftLink to "%s">' % self.path


class ExternalLink(object):
    __doc__ = '\n        Represents an HDF5 external link.  Paths may be absolute or relative.\n        No checking is performed to ensure either the target or file exists.\n    '

    @property
    def path(self):
        return self._path

    @property
    def filename(self):
        return self._filename

    def __init__(self, filename, path):
        self._filename = str(filename)
        self._path = str(path)

    def __repr__(self):
        return '<ExternalLink to "%s" in file "%s">' % (self.path, self.filename)


class UserDefinedLink(object):
    __doc__ = '\n        Represents a user-defined link\n    '

    def __init__(self):
        pass

    def __repr__(self):
        return '<UDLink >'