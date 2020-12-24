# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\jep_py\serializer.py
# Compiled at: 2015-04-25 10:31:58
# Size of source mod 2**32: 4723 bytes
"""Reflective serialization of messages based on mapping classes to built-in types."""
import enum, inspect

class SerializedAttribute:
    __doc__ = 'Description of constructor attribute to be serialized as member of object.'

    def __init__(self, name, annotation, default):
        self.name = name
        self.default = default
        self.annotation = annotation
        if isinstance(annotation, list):
            assert len(annotation) == 1, 'Type annotation for list must contain a single item type, e.g. [int].'
            self.datatype = list
            self.itemtype = annotation[0]
        else:
            if isinstance(annotation, dict):
                assert len(annotation) == 1, 'Type annotation for dict must contain a single map to item type, e.g. {int: str}.'
                self.datatype = dict
                self.itemtype = list(annotation.values())[0]
            else:
                self.datatype = annotation
                self.itemtype = None


class SerializableMeta(type):
    __doc__ = 'Metaclass remembering the types and default values passed to class constructors.'

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        ctor = inspect.signature(cls.__init__)
        cls.serialized_attribs = {p.name:SerializedAttribute(p.name, p.annotation, p.default) for p in ctor.parameters.values() if p.name is not 'self' if p.name is not 'self'}


class Serializable(metaclass=SerializableMeta):
    __doc__ = 'Base class for classes to be serialized to and from built-in types.'
    serialized_attribs = None

    def __init__(self):
        super().__init__()

    @classmethod
    def is_serialized_and_not_default(cls, name, value):
        """Checks if attribute with given name has a value different from its optional default."""
        if not cls.serialized_attribs:
            return False
        attrib = cls.serialized_attribs.get(name, None)
        return attrib and (attrib.default is inspect._empty or attrib.default != value)


def serialize_to_builtins(o):
    """Serialization of arbitrary object to built-in data types."""
    if isinstance(o, enum.Enum):
        serialized = o.name
    else:
        if isinstance(o, Serializable):
            serialized = serialize_to_builtins({key:value for key, value in o.__dict__.items() if o.is_serialized_and_not_default(key, value)})
        else:
            if hasattr(o, '__dict__'):
                serialized = serialize_to_builtins(o.__dict__)
            else:
                if isinstance(o, list):
                    serialized = [serialize_to_builtins(item) for item in o]
                else:
                    if isinstance(o, dict):
                        serialized = {key:serialize_to_builtins(value) for key, value in o.items()}
                    else:
                        serialized = o
    return serialized


def deserialize_from_builtins(serialized, datatype, itemtype=None, name=None):
    """Instantiation of data type from built-in serialized form."""
    if datatype is str and isinstance(serialized, bytes) or datatype is bytes and isinstance(serialized, str):
        raise TypeError('Cannot deserialize attribute %s of type %s from object "%s" of type %s.' % (name, datatype.__name__, serialized, type(serialized).__name__))
    if serialized is None:
        instantiated = None
    else:
        if serialized is inspect._empty:
            raise TypeError('While trying to deserialize type %s, required attribute %s was not in stream.' % (datatype, name))
        else:
            if isinstance(datatype, SerializableMeta):
                ctor_arguments = {attrib.name:deserialize_from_builtins(serialized.get(attrib.name, attrib.default), attrib.datatype, attrib.itemtype, attrib.name) for attrib in datatype.serialized_attribs.values()}
                instantiated = datatype(**ctor_arguments)
            else:
                if datatype is list and itemtype:
                    instantiated = [deserialize_from_builtins(item, itemtype) for item in serialized]
                else:
                    if datatype is dict and itemtype:
                        instantiated = {key:deserialize_from_builtins(value, itemtype) for key, value in serialized.items()}
                    else:
                        if issubclass(datatype, enum.Enum):
                            instantiated = datatype[serialized]
                        else:
                            if not itemtype:
                                instantiated = datatype(serialized)
                            else:
                                raise TypeError('Cannot deserialize type %s with item type %s.' % (datatype, itemtype))
    return instantiated