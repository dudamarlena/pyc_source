# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/datatype.py
# Compiled at: 2019-12-23 12:32:01
# Size of source mod 2**32: 1863 bytes
"""
    Implements high-level access to committed datatypes in the file. """
from __future__ import absolute_import
import posixpath as pp
from .base import HLObject
from .objectid import TypeID
from .h5type import createDataType

class Datatype(HLObject):
    __doc__ = '\n        Represents an HDF5 named datatype stored in a file.\n\n        To store a datatype, simply assign it to a name in a group:\n\n        >>> MyGroup["name"] = numpy.dtype("f")\n        >>> named_type = MyGroup["name"]\n        >>> assert named_type.dtype == numpy.dtype("f")  '

    @property
    def dtype(self):
        """Numpy dtype equivalent for this datatype"""
        return self._dtype

    def __init__(self, bind):
        """ Create a new Datatype object by binding to a low-level TypeID.
        """
        if not isinstance(bind, TypeID):
            raise ValueError('%s is not a TypeID' % bind)
        HLObject.__init__(self, bind)
        self._dtype = createDataType(self.id.type_json)
        self._req_prefix = '/datatypes/' + self.id.uuid

    def __repr__(self):
        if not self.id:
            return '<Closed HDF5 named type>'
        if self.name is None:
            namestr = '("anonymous")'
        else:
            name = pp.basename(pp.normpath(self.name))
            namestr = '"%s"' % (name if name != '' else '/')
            if name:
                namestr = f'"{name}"'
            else:
                namestr = '"/"'
        return f"<HDF5 named type {namestr} (dtype {self.dtype.str})>"