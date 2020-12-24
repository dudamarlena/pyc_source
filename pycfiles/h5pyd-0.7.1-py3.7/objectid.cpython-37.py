# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/objectid.py
# Compiled at: 2019-12-23 14:00:28
# Size of source mod 2**32: 5858 bytes
from __future__ import absolute_import
from datetime import datetime
import pytz, time

def parse_lastmodified(datestr):
    """Turn last modified datetime string into a datetime object."""
    if isinstance(datestr, str):
        dt = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=(pytz.UTC))
    else:
        dt = datetime.fromtimestamp(time.time())
    return dt


class ObjectID:
    __doc__ = '\n        Uniquely identifies an h5serv resource\n    '

    @property
    def uuid(self):
        return self._uuid

    @property
    def id(self):
        return self.uuid

    def __hash__(self):
        return self.uuid

    @property
    def objtype_code(self):
        """ return one char code to denote what type of object
        g: group
        d: dataset
        t: committed datatype
        """
        return self._objtype_code

    @property
    def domain(self):
        """ domain for this obj """
        return self.http_conn.domain

    @property
    def obj_json(self):
        """json representation of the object"""
        return self._obj_json

    @property
    def modified(self):
        """last modified timestamp"""
        return self._modified

    @property
    def http_conn(self):
        """ http connector """
        return self._http_conn

    def __init__(self, parent, item, objtype_code=None, http_conn=None, **kwds):
        """Create a new objectId.
        """
        parent_id = None
        if parent is not None:
            if isinstance(parent, ObjectID):
                parent_id = parent
            else:
                parent_id = parent.id
        elif type(item) is not dict:
            raise IOError('Unexpected Error')
        else:
            if 'id' not in item:
                raise IOError('Unexpected Error')
            self._uuid = item['id']
            self._modified = parse_lastmodified(item['lastModified'])
            self._obj_json = item
            if http_conn is not None:
                self._http_conn = http_conn
            else:
                if parent_id is not None and parent_id.http_conn is not None:
                    self._http_conn = parent_id.http_conn
                else:
                    raise IOError('Expected parent to have http connector')
        self._objtype_code = objtype_code

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._uuid == other._uuid
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def close(self):
        """Remove handles to id.
        """
        self._old_uuid = self._uuid
        self._uuid = 0
        self._obj_json = None
        self._http_conn = None

    def __bool__(self):
        return bool(self._uuid)

    __nonzero__ = __bool__


class TypeID(ObjectID):

    @property
    def type_json(self):
        return self.obj_json['type']

    def __init__(self, parent, item, **kwds):
        """Create a new TypeID.
        """
        (ObjectID.__init__)(self, parent, item, objtype_code='t', **kwds)


class DatasetID(ObjectID):

    @property
    def type_json(self):
        return self._obj_json['type']

    @property
    def shape_json(self):
        return self._obj_json['shape']

    @property
    def dcpl_json(self):
        if 'creationProperties' in self._obj_json:
            dcpl = self._obj_json['creationProperties']
        else:
            dcpl = {}
        return dcpl

    @property
    def rank(self):
        rank = 0
        shape = self._obj_json['shape']
        if shape['class'] == 'H5S_SIMPLE':
            dims = shape['dims']
            rank = len(dims)
        return rank

    @property
    def chunks(self):
        chunks = None
        layout = None
        if 'layout' in self._obj_json:
            layout = self._obj_json['layout']
        else:
            dcpl = self._obj_json['creationProperties']
            if 'layout' in dcpl:
                layout = dcpl['layout']
            elif layout:
                if layout['class'] in ('H5D_CHUNKED', 'H5D_CHUNKED_REF', 'H5D_CHUNKED_REF_INDIRECT'):
                    if layout['class'] == 'H5D_CHUNKED':
                        chunks = layout['dims']
                    else:
                        chunks = layout
            return chunks

    def __init__(self, parent, item, **kwds):
        """Create a new DatasetID.
        """
        (ObjectID.__init__)(self, parent, item, objtype_code='d', **kwds)


class GroupID(ObjectID):

    def __init__(self, parent, item, http_conn=None, **kwds):
        """Create a new GroupID.
        """
        ObjectID.__init__(self, parent, item, http_conn=http_conn, objtype_code='g')