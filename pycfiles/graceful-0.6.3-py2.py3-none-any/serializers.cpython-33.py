# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swistakm/dev/graceful/build/lib/graceful/serializers.py
# Compiled at: 2015-07-14 08:35:08
# Size of source mod 2**32: 9940 bytes
from collections import OrderedDict
from collections.abc import Mapping, MutableMapping
from graceful.errors import DeserializationError, ValidationError
from graceful.fields import BaseField

class MetaSerializer(type):
    __doc__ = ' Metaclass for handling serialization with field objects\n    '
    _fields_storage_key = '_fields'

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        """
        Prepare class namespace in a way that ensures order of attributes.
        This needs to be an `OrderedDict` so `_get_params()` method can
        construct fields storage that preserves the same order of fields as
        defined in code.

        Note: this is python3 thing and support for ordering of params in
        descriptions will not be backported to python2 even if this framework
        will get python2 support.

        """
        return OrderedDict()

    @classmethod
    def _get_fields(mcs, bases, namespace):
        """ Pop all field objects from attributes dict (namespace)
        and store them under _field_storage_key atrribute.
        Also collect all fields from base classes in order that ensures
        fields can be overriden.

        Args:
            bases: all base classes of created serializer class
            namespace (dict): namespace as dictionary of attributes

        """
        fields = [(name, namespace.pop(name)) for name, attribute in list(namespace.items()) if isinstance(attribute, BaseField)]
        for base in reversed(bases):
            if hasattr(base, mcs._fields_storage_key):
                fields = list(getattr(base, mcs._fields_storage_key).items()) + fields
                continue

        return OrderedDict(fields)

    def __new__(mcs, name, bases, namespace):
        namespace[mcs._fields_storage_key] = mcs._get_fields(bases, namespace)
        return super().__new__(mcs, name, bases, dict(namespace))


class BaseSerializer(metaclass=MetaSerializer):
    __doc__ = '\n    Base serializer class for describing internal object serialization\n\n    Example:\n\n    .. code-block:: python\n\n        from graceful.serializers import BaseSerializer\n        from graceful.fields import RawField, IntField, FloatField\n\n\n        class CatSerializer(BaseSerializer):\n            species = RawField("non normalized cat species")\n            age = IntField("cat age in years")\n            height = FloatField("cat height in cm")\n\n    '

    @property
    def fields(self):
        """
        Dictionary of field objects defined for this resource serialization
        """
        return getattr(self, self.__class__._fields_storage_key)

    def to_representation(self, obj):
        """
        Convert given internal object instance into defined representation
        that will be later serialized to content-type of use in resource
        http method handler.

        This loops over all fields and retrieves source keys/attributes as
        field values with respect to optional field sources and converts each
        one using ``field.to_representation()`` method.

        Args:
            obj (object): internal object that needs to be represented

        Returns:
            dict: representation dictionary

        """
        representation = {}
        for name, field in self.fields.items():
            attribute = self.get_attribute(obj, field.source or name)
            if attribute is None:
                representation[name] = [] if field.many else None
            elif field.many:
                representation[name] = [field.to_representation(item) for item in attribute]
            else:
                representation[name] = field.to_representation(attribute)

        return representation

    def from_representation(self, representation):
        """
        Convert given representation dict into dictionary of internal object
        values with respect to field sources.

        This does not check if all required fields exist or values are
        valid in terms of value validation
        (see: :meth:`BaseField.validate()`) but still requires all of passed
        representation values to be well formed representation (success call
        to ``field.from_representation``).

        In case of malformed representation it will run additional validation
        only to provide a full detailed exception about all that might be
        wrong with provided representation.

        Args:
           representation (dict): dictionary with field representation values

        Raises:
            DeserializationError: when at least one representation field
               is not formed as expected by field object. Information
               about additional forbidden/missing/invalid fields is provided
               as well.

        """
        object_dict = {}
        failed = {}
        for name, field in self.fields.items():
            if name not in representation:
                continue
            try:
                object_dict[field.source or name] = field.from_representation(representation[name])
            except ValueError as err:
                failed[name] = str(err)

        if failed:
            try:
                self.validate(object_dict)
                raise DeserializationError()
            except DeserializationError as err:
                err.failed = failed
                raise

        return object_dict

    def validate(self, object_dict, partial=False):
        """
        Validate given internal object agains missing/forbidden/invalid
        fields values using fields definitions defined in serializer.

        Args:
            object_dict (dict): internal object dictionart to perform
              to validate
            partial (bool): if set to True then incomplete object_dict
              is accepter and will not raise any exceptions when one
              of fields is missing

        Raises:
            DeserializationError:

        """
        sources = {field.source or name if field.source != '*' else name:field for name, field in self.fields.items()}
        missing = [name for name, field in sources.items() if all((not partial, name not in object_dict, not field.read_only))]
        forbidden = [name for name in object_dict if any((name not in sources, sources[name].read_only))]
        invalid = {}
        for name, value in object_dict.items():
            try:
                sources[name].validate(value)
            except ValidationError as err:
                invalid[name] = str(err)

        if any([missing, forbidden, invalid]):
            raise DeserializationError(missing, forbidden, invalid)

    def get_attribute(self, obj, attr):
        """
        Get attribute from given object instance where 'attribute' can
        be also a key from object if is a dict or any kind of mapping

        Note: it will return None if attribute key does not exist

        Args:
            obj (object): internal object to retrieve data from

        Returns:
            internal object's key value or attribute

        """
        if attr == '*':
            return obj
        else:
            if isinstance(obj, Mapping):
                return obj.get(attr, None)
            return getattr(obj, attr, None)

    def set_attribute(self, obj, attr, value):
        """
        Set attribute in given object instance where 'attribute' can
        be also a key from object if it is a dict or any kind of mapping

        Args:
            obj (object): object instance to modify
            attr (str): attribute (or key) to change
            value: value to set

        """
        if isinstance(obj, MutableMapping):
            obj[attr] = value
        else:
            setattr(obj, attr, value)

    def describe(self):
        """
        Describe whole all fields defined for this serializer using their own
        descriptions with respect to order in which they are defined as class
        attributes.

        Returns:
            OrderedDict: serializer description

        """
        return OrderedDict([(name, field.describe()) for name, field in self.fields.items()])