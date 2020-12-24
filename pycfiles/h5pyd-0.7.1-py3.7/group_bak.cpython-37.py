# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/group_bak.py
# Compiled at: 2019-05-24 23:35:22
# Size of source mod 2**32: 40665 bytes
from __future__ import absolute_import
import six
import os.path as op
import numpy, collections, logging
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
        logging.debug('Group init')
        if not isinstance(bind, GroupID):
            raise ValueError('%s is not a GroupID' % bind)
        (HLObject.__init__)(self, bind, **kwargs)
        self._req_prefix = '/groups/' + self.id.uuid
        self._link_db = None
        self.log.debug('Group init complete')

    def _get_link_db(self):
        if self._link_db is None:
            if self.id.http_conn._objdb:
                self.log.debug('geting links from objdb')
                objdb = self.id.http_conn._objdb
                if self.id.uuid in objdb:
                    group_json = objdb[self.id.uuid]
                    links = group_json['links']
                    for link in links:
                        if link['class'] == 'H5L_TYPE_HARD':
                            objid = link['id']
                            if objid.startswith('g-'):
                                link['collection'] = 'groups'
                            elif objid.startswith('d-'):
                                link['collection'] = 'datasets'
                            elif objid.startswith('t-'):
                                link['collection'] = 'datatypes'
                            else:
                                self.log.warn('unexpected objid: {}'.format(objid))

                    self._link_db = group_json['links']
            if self._link_db is None:
                req = '/groups/' + self.id.uuid + '/links'
                rsp_json = self.GET(req)
                links_json = rsp_json['links']
                self._link_db = {}
                for link in links_json:
                    name = link['title']
                    self._link_db[name] = link

        return self._link_db

    def _isroot(self):
        if self.id.uuid == self.file.id.id:
            return True
        return False

    def _h5path_is_member(self, h5path):
        if h5path[0] == '/' and h5path[1:].find('/') == -1 and self._isroot():
            in_group = True
            h5path = h5path[1:]
        else:
            if h5path.find('/') == -1:
                in_group = True
            else:
                in_group = False
        return in_group

    def _get_link_json(self, h5path):
        """ Return parent_uuid and json description of link for given path """
        parent_uuid = self.id.uuid
        root_uuid = self.file.id.id
        tgt_json = None
        self.log.debug('_get_link_json({})'.format(h5path))
        if isinstance(h5path, bytes):
            h5path = h5path.decode('utf-8')
        if h5path[0] == '/':
            parent_uuid = root_uuid
            if h5path == '/':
                tgt_json = {'collection':'groups', 
                 'class':'H5L_TYPE_HARD',  'id':parent_uuid}
                return (parent_uuid, tgt_json)
        linkdb = self._get_link_db()
        if self._h5path_is_member(h5path):
            if h5path in linkdb:
                tgt_json = self._link_db[h5path]
                parent_uuid = self.id.id
                self.log.debug('found link in linkdb: {}'.format(tgt_json))
                return (parent_uuid, tgt_json)
        if self.id.http_conn._objdb:
            self.log.debug('searching objdb for {}'.format(h5path))
            objdb = self.id.http_conn._objdb
            group_uuid = parent_uuid
            path = h5path.split('/')
            for name in path:
                if not name:
                    continue
                if group_uuid not in objdb:
                    self.log.debug('objdb search: {} not found in objdb'.format(group_uuid))
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
                    self.log.debug('objdb search: non-hardlink')
                    tgt_json = None
                    break
                group_uuid = tgt_json['id']

            if tgt_json:
                return (
                 group_uuid, tgt_json)
        path = h5path.split('/')
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
            if tgt_json['class'] == 'H5L_TYPE_HARD':
                if tgt_json['collection'] == 'groups':
                    parent_uuid = tgt_json['id']
                else:
                    parent_uuid = None

        if tgt_json:
            if self._h5path_is_member(h5path):
                self._link_db[h5path] = tgt_json
        self.log.debug('get_link_json for {}: {}'.format(h5path, tgt_json))
        return (
         parent_uuid, tgt_json)

    def create_group(self, h5path):
        """ Create and return a new subgroup.

        Name may be absolute or relative.  Fails if the target name already
        exists.
        """
        if h5path[(-1)] == '/':
            raise ValueError('Invalid path for create_group')
        else:
            parent_uuid = self.id.id
            if h5path[0] == '/':
                parent_uuid = self.file.id.id
            parent_path = op.dirname(h5path)
            title = op.basename(h5path)
            if parent_path:
                parent_uuid, link_json = self._get_link_json(parent_path)
                if link_json['class'] != 'H5L_TYPE_HARD':
                    raise IOError('cannot create subgroup of softlink')
                parent_uuid = link_json['id']
            body = {'link': {'id':parent_uuid,  'name':title}}
            rsp = self.POST('/groups', body=body)
            group_json = rsp
            groupId = GroupID(self, group_json)
            if parent_uuid == self.id.id:
                self.log.debug('adding {} to linkdb'.format(title))
                link_db = self._get_link_db()
                link_db[title] = {'collection':'groups',  'class':'H5L_TYPE_HARD',  'id':group_json['id']}
                print('count:', len(link_db))
                for k in link_db:
                    print(k, ':', link_db[k])

            else:
                self.log.warn('linkdb may be out of synch')
            subGroup = Group(groupId)
            if self._name:
                if self._name[(-1)] == '/':
                    subGroup._name = self._name + title
                else:
                    subGroup._name = self._name + '/' + title
        return subGroup

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

        def getObjByUuid(uuid, collection_type=None):
            """ Utility method to get an obj based on collection type and uuid """
            if uuid.startswith('groups/'):
                uuid = uuid[len('groups/'):]
                if collection_type is None:
                    collection_type = 'groups'
            elif uuid.startswith('datasets/'):
                uuid = uuid[len('datasets/'):]
                if collection_type is None:
                    collection_type = 'datasets'
            elif uuid.startswith('datatypes/'):
                uuid = uuid[len('datatypes/'):]
                if collection_type is None:
                    collection_type = 'datasets'
            if collection_type == 'groups' or uuid.startswith('g-'):
                req = '/groups/' + uuid
                group_json = self.GET(req)
                tgt = Group(GroupID(self, group_json))
            else:
                if collection_type == 'datatypes' or uuid.startswith('t-'):
                    req = '/datatypes/' + uuid
                    datatype_json = self.GET(req)
                    tgt = Datatype(TypeID(self, datatype_json))
                else:
                    if collection_type == 'datasets' or uuid.startswith('d-'):
                        req = '/datasets/' + uuid
                        dataset_json = self.GET(req)
                        shape_json = dataset_json['shape']
                        dtype_json = dataset_json['type']
                        if 'dims' in shape_json and len(shape_json['dims']) == 1 and dtype_json['class'] == 'H5T_COMPOUND':
                            tgt = Table(DatasetID(self, dataset_json))
                        else:
                            tgt = Dataset(DatasetID(self, dataset_json))
                    else:
                        raise IOError('Unexpected Error - collection type: ' + link_json['collection'])
            return tgt

        def isUUID(name):
            if isinstance(name, six.string_types) and len(name) >= 38 and not name.startswith('groups/'):
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

    def __setitem__(self, name, obj):
        """ Add an object to the group.  The name must not already be in use.

        The action taken depends on the type of object assigned:

        Named HDF5 object (Dataset, Group, Datatype)
            A hard link is created at "name" which points to the
            given object.

        SoftLink or ExternalLink
            Create the corresponding link.

        Numpy ndarray
            The array is converted to a dataset object, with default
            settings (contiguous storage, etc.).

        Numpy dtype
            Commit a copy of the datatype as a named datatype in the file.

        Anything else
            Attempt to convert it to an ndarray and store it.  Scalar
            values are stored as scalar datasets. Raise ValueError if we
            can't understand the resulting array dtype.
        """
        link_json = {}
        if name.find('/') != -1:
            parent_path = op.dirname(name)
            basename = op.basename(name)
            if not basename:
                raise KeyError("Group path can not end with '/'")
            parent_uuid, link_json = self._get_link_json(parent_path)
            if parent_uuid is None:
                raise KeyError('group path: {} not found'.format(parent_path))
            if link_json['class'] != 'H5L_TYPE_HARD':
                raise IOError('cannot create subgroup of softlink')
            parent_uuid = link_json['id']
            req = '/groups/' + parent_uuid
            group_json = self.GET(req)
            tgt = Group(GroupID(self, group_json))
            tgt[basename] = obj
        else:
            if isinstance(obj, HLObject):
                body = {'id': obj.id.uuid}
                req = '/groups/' + self.id.uuid + '/links/' + name
                self.PUT(req, body=body)
                link_json['title'] = name
                link_json['class'] = 'H5L_TYPE_HARD'
                link_json['id'] = obj.id.uuid
            else:
                if isinstance(obj, SoftLink):
                    body = {'h5path': obj.path}
                    req = '/groups/' + self.id.uuid + '/links/' + name
                    self.PUT(req, body=body)
                    link_json['title'] = name
                    link_json['class'] = 'H5L_TYPE_SOFT'
                    link_json['h5path'] = obj._path
                else:
                    if isinstance(obj, ExternalLink):
                        body = {'h5path':obj.path, 
                         'h5domain':obj.filename}
                        req = '/groups/' + self.id.uuid + '/links/' + name
                        self.PUT(req, body=body)
                        link_json['title'] = name
                        link_json['class'] = 'H5L_TYPE_EXTERNAL'
                        link_json['h5path'] = obj._path
                        link_json['h5domain'] = obj._filename
                    else:
                        if isinstance(obj, numpy.dtype):
                            type_json = h5type.getTypeItem(obj)
                            req = '/datatypes'
                            body = {'type': type_json}
                            rsp = self.POST(req, body=body)
                            body['id'] = rsp['id']
                            body['lastModified'] = rsp['lastModified']
                            type_id = TypeID(self, body)
                            req = '/groups/' + self.id.uuid + '/links/' + name
                            body = {'id': type_id.uuid}
                            self.PUT(req, body=body)
                            link_json['title'] = name
                            link_json['class'] = 'H5L_TYPE_HARD'
                            link_json['id'] = rsp['id']
                        else:
                            if name.find('/') == -1:
                                if self._link_db is None:
                                    self._link_db = {}
                                self._link_db[name] = link_json

    def __delitem__(self, h5path):
        """ Delete (unlink) an item from this group. """
        self.log.debugI('__delitem__({})'.format(h5path))
        req = '/groups/' + self.id.uuid + '/links/' + h5path
        self.DELETE(req)
        if self._h5path_is_member(h5path):
            if h5path[0] == '/':
                name = h5path[1:]
            else:
                name = h5path
            link_db = self._get_link_db()
            if name in link_db:
                del link_db[name]

    def __len__(self):
        """ Number of members attached to this group """
        link_db = self._get_link_db()
        return len(link_db)

    def __iter__(self):
        """ Iterate over member names """
        link_db = self._get_link_db()
        for x in link_db:
            yield x

    def __contains__(self, name):
        """ Test if a member name exists """
        if name == '/':
            return True
        if name.startswith('/'):
            if self._isroot():
                name = name[1:]
        link_db = self._get_link_db()
        print('count:', len(link_db))
        print(link_db)
        return name in link_db

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
        if six.PY3:
            nargs = func.__code__.co_argcount
        else:
            nargs = func.func_code.co_argcount
        while len(tovisit) > 0:
            parent_uuid, parent = tovisit.popitem(last=True)
            if parent.name != '/':
                if nargs == 1:
                    retval = func(parent.name)
                else:
                    retval = func(parent.name, parent)
                if retval is not None:
                    break
            visited[self.id.uuid] = True
            if parent.id.__class__ is GroupID:
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
                        if nargs == 1:
                            retval = func(link_name)
                        else:
                            retval = func(link_name, obj)
                        if retval is not None:
                            break

        return retval

    def __repr__(self):
        if not self:
            r = six.u('<Closed HDF5 group>')
        else:
            namestr = six.u('"%s"') % self.name if self.name is not None else six.u('(anonymous)')
            r = six.u('<HDF5 group %s (%d members)>') % (namestr, len(self))
        if six.PY3:
            return r
        return r.encode('utf8')


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