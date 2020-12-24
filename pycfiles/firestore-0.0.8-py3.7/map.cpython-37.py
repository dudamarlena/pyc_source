# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/map.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 2603 bytes
from firestore.containers.collection import Collection
from firestore.datatypes.base import Base
from firestore.errors import ValidationError

class MapSchema(Collection):
    __doc__ = '\n    A map schema defines a helper by which maps can be populated\n    so there is no need to use default python dicts'

    def __init__(self, *args, **kwargs):
        self.py_type = dict
        (super(MapSchema, self).__init__)(*args, **kwargs)


class Map(Base):
    __doc__ = 'Maps as defined by firestore represent an object saved within a document.\n    In python speak - A map is akin to a dictionary.\n\n    Maps on Firestore cloud are an ordered collection of key value pairs\n    and the firestore library mimics this sorting at retrieval and traversal\n    which is sufficient for almost use cases encountered in the wild\n    '

    def __init__(self, *args, **kwargs):
        try:
            self.map_ref = args[0]
        except IndexError:
            self.map_ref = None

        (super(Map, self).__init__)(*args, **kwargs)

    def __set__(self, instance, value):
        self.validate(value)
        if self.map_ref:
            value = (self.map_ref)(**value) if isinstance(value, dict) else value
        self.value = value
        instance.add_field(self, value)
        instance.__mutated__ = True

    def validate(self, value, instance=None):
        if self.map_ref:
            if not isinstance(value, (MapSchema, dict)):
                raise ValueError()
            if isinstance(value, dict):
                _schema = self.map_ref.__autospector__()
                for k in _schema:
                    f = _schema.get(k)
                    v = value.get(k)
                    f.validate(v)

            else:
                value._presave()