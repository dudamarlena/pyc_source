# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/io/json_codec.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 5486 bytes
import logging
logger = logging.getLogger(__name__)
import json, numpy as np

class PyXRDEncoder(json.JSONEncoder):
    __doc__ = "\n        A custom JSON encoder that checks if:\n            - the object has a to_json callable method, if so it is called to\n              convert the object to a JSON encodable object.\n              E.g. the default implementation from the Storable class is a dict object\n              containing:\n               - a 'type' key mapped to the storage type id of the storable class\n               - a 'properties' key mapped to a dict of name-values for each\n                 property that needs to be stored in order to be able to \n                 recreate the object.\n              If the user registered this class as a storable\n              (see the 'registes_storable' method or the Storable class)\n              then the JSON object is transformed back into the actual Python\n              object using its from_json(...) method. Default implementation\n              finds the registered class using the 'type' value and passes the\n              'properties' value to its constructor as keyword arguments.  \n            - if the object is a numpy array, it is converted to a list\n            - if the object is a wrapped list, dictionary, ... (ObsWrapper \n              subclass) then the wrapped object is returned, as these are\n              directly JSON encodable.\n            - fall back to the default JSONEncoder methods\n    "

    @classmethod
    def dump_object(cls, obj):
        """ Serialize an object using this encoder and return it as a string """
        return json.dumps(obj, indent=4, cls=cls)

    @classmethod
    def dump_object_to_file(cls, obj, f):
        """ Serialize an object using this encoder and dump it into a file"""
        return json.dump(obj, f, indent=4, cls=cls)

    def default(self, obj):
        from mvc.support.observables import ObsWrapper
        if hasattr(obj, 'to_json'):
            if callable(getattr(obj, 'to_json')):
                return obj.to_json()
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            if isinstance(obj, ObsWrapper):
                return obj._obj
            return json.JSONEncoder(self).default(obj)


class PyXRDDecoder(json.JSONDecoder):
    __doc__ = "\n        A custom JSON decoder that can decode objects, following these steps:\n            - decode the JSON object at once using the default decoder\n            - the resulting dict is then parsed:\n               - if a valid 'type' and a 'properties' key is given,\n                 the object is translated using the mapped class type's \n                 'from_json' method. This mapping is done using a dict mapping\n                 the json class name to an actual class type (`mapper` __init__ keyword)\n               - parent keyword arguments are passed on (e.g. a project) to\n                 the from_json method as well\n    "

    def __init__(self, mapper=None, parent=None, **kwargs):
        (super(PyXRDDecoder, self).__init__)(**kwargs)
        self.mapper = mapper
        self.parent = parent

    @classmethod
    def decode_file(cls, f, mapper, parent=None):
        data = f.read()
        data = data.decode('utf-8') if isinstance(data, bytes) else data
        return json.loads(data, cls=PyXRDDecoder, mapper=mapper, parent=parent)

    @classmethod
    def decode_string(cls, string, mapper, parent=None):
        return json.loads(string, cls=PyXRDDecoder, mapper=mapper, parent=parent)

    def decode(self, string):
        obj = super(PyXRDDecoder, self).decode(string)
        return self.__pyxrd_decode__(obj) or obj

    def __pyxrd_decode__(self, obj, **kwargs):
        """ Decodes the PyXRD JSON object serialization """
        if isinstance(obj, list):
            for index, subobj in enumerate(obj):
                obj[index] = self.__pyxrd_decode__(subobj) or subobj

            return obj
        if 'type' in obj:
            objtype = self.mapper[obj['type']]
            if 'properties' in obj:
                if hasattr(objtype, 'from_json'):
                    if self.parent is not None:
                        if 'parent' not in kwargs:
                            kwargs['parent'] = self.parent
                    return (objtype.from_json)(**)
        logger.warn('__pyxrd_decode__ will return None for %s!' % str(obj)[:30] + '...' + str(obj)[:-30])