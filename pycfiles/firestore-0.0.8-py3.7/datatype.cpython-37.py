# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/datatype.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 909 bytes
from firestore.datatypes.base import Base
from firestore.datatypes import Array, Boolean, Byte, Float, Geopoint, Map, MapSchema, Null, Integer, Float, Reference, String

class Datatype(object):
    __doc__ = '\n    Lazy class for the firestore library\n    '

    def __new__(cls, *args, **kwargs):
        target = args[0]
        target = datatypes.get(args[0].lower())
        args = args[1:]
        return target(*args, **kwargs)


datatypes = {'array':Array, 
 'boolean':Boolean, 
 'byte':Byte, 
 'float':Float, 
 'geopoint':Geopoint, 
 'integer':Integer, 
 'map':Map, 
 'map_schema':MapSchema, 
 'null':Null, 
 'reference':Reference, 
 'string':String}