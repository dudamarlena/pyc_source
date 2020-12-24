# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/util/serializable.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 3163 bytes
from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod
from enum import Enum
import json
from mautrix.api import JSON
T = TypeVar('T')

class Serializable:
    __doc__ = 'Serializable is the base class for types with custom JSON serializers.'

    def serialize(self) -> JSON:
        """Convert this object into objects directly serializable with `json`."""
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, raw: JSON) -> Any:
        """Convert the given data parsed from JSON into an object of this type."""
        raise NotImplementedError()


class SerializerError(Exception):
    __doc__ = '\n    SerializerErrors are raised if something goes wrong during serialization or deserialization.\n    '


class GenericSerializable(ABC, Generic[T], Serializable):
    __doc__ = '\n    An abstract Serializable that adds ``@abstractmethod`` decorators and a `Generic[T]` base class.\n    '

    @classmethod
    @abstractmethod
    def deserialize(cls, raw: JSON) -> T:
        pass

    @abstractmethod
    def serialize(self) -> JSON:
        pass

    def json(self) -> str:
        """Serialize this object and dump the output as JSON."""
        return json.dumps(self.serialize())

    @classmethod
    def parse_json(cls, data: str) -> T:
        """Parse the given string as JSON and deserialize the result into this type."""
        return cls.deserialize(json.loads(data))


SerializableEnumChild = TypeVar('SerializableEnumChild', bound='SerializableEnum')

class SerializableEnum(Serializable, Enum):
    __doc__ = '\n    A simple Serializable implementation for Enums.\n\n    Examples:\n        >>> class MyEnum(SerializableEnum):\n        ...     FOO = "foo value"\n        ...     BAR = "hmm"\n        >>> MyEnum.FOO.serialize()\n        "foo value"\n        >>> MyEnum.BAR.json()\n        \'"hmm"\'\n    '

    def __init__(self, _):
        """
        A fake ``__init__`` to stop the type checker from complaining.
        Enum's ``__new__`` overrides this.
        """
        super().__init__()

    def serialize(self) -> str:
        """
        Convert this object into objects directly serializable with `json`, i.e. return the value
        set to this enum value.
        """
        return self.value

    @classmethod
    def deserialize(cls, raw: str) -> SerializableEnumChild:
        """
        Convert the given data parsed from JSON into an object of this type, i.e. find the enum
        value for the given string using ``cls(raw)``.
        """
        try:
            return cls(raw)
        except ValueError as e:
            raise SerializerError() from e

    def json(self) -> str:
        return json.dumps(self.serialize())

    @classmethod
    def parse_json(cls, data: str) -> SerializableEnumChild:
        return cls.deserialize(json.loads(data))

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value