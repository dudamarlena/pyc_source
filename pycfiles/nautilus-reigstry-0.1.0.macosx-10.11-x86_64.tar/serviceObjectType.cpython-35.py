# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/nautilus-registry/objectTypes/serviceObjectType.py
# Compiled at: 2016-06-20 02:07:59
# Size of source mod 2**32: 4000 bytes
from graphene import String, ObjectType
from graphene.core.classtypes.objecttype import ObjectTypeOptions
from nautilus.api import fields_for_model
from nautilus.network import query_service
serivce_objects = {}

class ServiceObjectTypeOptions(ObjectTypeOptions):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.valid_attrs += ('service', )
        self.service = None

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        cls.service = self.service


class ServiceObjectTypeMeta(type(ObjectType)):
    options_class = ServiceObjectTypeOptions

    def construct(self, *args, **kwds):
        self.service = self._meta.service() if self._meta.service else None
        return super().construct(*args, **kwds)

    def __new__(cls, name, bases, attributes, **kwds):
        if 'Meta' in attributes:
            service = attributes['Meta'].service
            if hasattr(service, 'model'):
                attributes.update(fields_for_model(service.model))
            return super().__new__(cls, name, bases, attributes, **kwds)

    def __init__(self, name, bases, dict):
        super().__init__(name, bases, dict)
        serivce_objects[name] = self


class ServiceObjectType(ObjectType, metaclass=ServiceObjectTypeMeta):
    __doc__ = '\n        This object type represents data maintained by a remote service.\n        `Connection`s to and from other `ServiceObjectType`s are resolved\n        through a specified a connection service assuming nautilus naming\n        conventions.\n    '
    pk = String()

    def __getattr__(self, attr):
        """
            This is overwritten to check for connection fields which don't
            make it to the class record.
        """
        try:
            connection = [connection for connection in type(self).connections() if connection.attname == attr][0]
            return connection.resolver(self, {}, {})
        except KeyError:
            raise AttributeError

    @classmethod
    def true_fields(cls):
        """
            Returns the list of fields that are not connections.

            Returns:
                (list of fields): The list of fields of this object that are
                    not connections to other objects.
        """
        from nautilus.api.fields import Connection
        fields = cls._meta.fields
        return [field for field in fields if not isinstance(field.type, Connection)]

    @classmethod
    def connections(cls):
        """
            Returns the list of fields that are connections.

            Returns:
                (list of fields): The list of fields of this object that are
                    connections to other objects.
        """
        from nautilus.api.fields import Connection
        fields = cls._meta.fields
        return [field for field in fields if isinstance(field, Connection)]