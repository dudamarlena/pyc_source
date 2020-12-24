# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swistakm/dev/graceful/build/lib/graceful/fields.py
# Compiled at: 2015-07-14 08:35:08
# Size of source mod 2**32: 10061 bytes
import inspect
from graceful.validators import min_validator, max_validator

class BaseField:
    __doc__ = '\n    Base field class for subclassing. To create new field type\n    subclass `BaseField` and implement following methods:\n\n    - ``from_representation()``: converts representation (used in\n      request/response body) to internal value.\n\n    - ``to_representation()``: converts internal value to representation\n      that will be used in response body.\n\n\n    Args:\n\n        details (str): human readable description of field (it will be used\n           for describing resource on OPTIONS requests).\n\n        label (str): human readable label of a field (it will be used for\n           describing resource on OPTIONS requests).\n\n           *Note: it is recommended to use field names that are\n           self-explanatory intead of relying on field labels.*\n\n        source (str): name of internal object key/attribute that will be\n           passed to field on ``.to_representation()`` call. Special ``\'*\'``\n           value is allowed that will pass whole object to field when making\n           representation. If not set then default source will\n           be a field name used as a serializer\'s attribute.\n\n        validators (list): list of validator callables.\n\n        many (bool): set to True if field is in fact a list of given type\n          objects\n\n        read_only (bool): True if field is read only and cannot be set/modified\n           by POST and PUT requests\n\n    Example:\n\n    .. code-block:: python\n\n        class BoolField(BaseField):\n            def from_representation(self, data):\n                if data in {\'true\', \'True\', \'yes\', \'1\', \'Y\'}:\n                    return True:\n                elif data in {\'false\', \'False\', \'no\', \'0\', \'N\'}:\n                    return False:\n                else:\n                    raise ValueError(\n                        "{data} is not valid boolean field".format(\n                            data=data\n                        )\n                    )\n\n            def to_representation(self, value):\n                return ["True", "False"][value]\n\n    '
    spec = None
    type = None

    def __init__(self, details, label=None, source=None, validators=None, many=False, read_only=False):
        self.label = label
        self.source = source
        self.details = details
        self.validators = validators or []
        self.many = many
        self.read_only = read_only

    def from_representation(self, data):
        raise NotImplementedError('{cls}.from_representation() method not implemented'.format(cls=self.__class__.__name__))

    def to_representation(self, value):
        raise NotImplementedError('{cls}.to_representation() method not implemented'.format(cls=self.__class__.__name__))

    def describe(self, **kwargs):
        """
        Describe this field instance for purpose of self-documentation.

        Args:
            kwargs (dict): dictionary of additional description items for
               extending default description

        Returns:
            dict: dictionary of description items

        Suggested way for overriding description fields or extending it with
        additional items is calling super class method with new/overriden
        fields passed as keyword arguments like following:

        .. code-block:: python

            class DummyField(BaseField):
               def description(self, **kwargs):
                   super().describe(is_dummy=True, **kwargs)

        """
        description = {'label': self.label, 
         'details': inspect.cleandoc(self.details), 
         'type': 'list of {}'.format(self.type) if self.many else self.type, 
         'spec': self.spec, 
         'read_only': self.read_only}
        description.update(kwargs)
        return description

    def validate(self, value):
        """ Perform validation on value by running all field validators.
        Single validator is a callable that accepts one positional argument
        and raises "ValidationError" when validation fails.

        Error message included in exception will be included in http error
        response

        Args:
            value: internal value to validate

        Returns:
            None

        Note:
            Concept of validation for fields is understood here as a process
            of checking if data of valid type (successfully parsed/processed by
            ``.from_representation`` handler) does meet some other constraints
            (lenght, bounds, unique, etc). Becasue of that this method is
            always called with result of ``.from_representation()`` passed
            as value.

        """
        for validator in self.validators:
            validator(value)


class RawField(BaseField):
    __doc__ = '\n    Represents raw field subtype. Any value from resource object\n    will be returned as is without any conversion and no control\n    over serialized value type is provided. Can be used only with\n    very simple data types like int, float, str etc. but can eventually\n    cause problems if value provided in representation has type\n    that is not accepted in application.\n\n    Effect of using this can differ between various content-types.\n\n    '
    type = 'raw'

    def from_representation(self, data):
        return data

    def to_representation(self, value):
        return value


class StringField(BaseField):
    __doc__ = '\n    Represents string field subtype without any extensive validation.\n    '
    type = 'string'

    def from_representation(self, data):
        return str(data)

    def to_representation(self, value):
        return str(value)


class BoolField(BaseField):
    __doc__ = "\n    Represents boolean type of field. By default accepts a wide range of\n    incoming True/False representations:\n\n    * False: ``[False', 'false', 'FALSE', 'F', 'f' '0', 0, 0.0, False``\n    * True: ``['True', 'true', 'TRUE', 'T', 't', '1', 1, True]``\n\n    By default by as representations of internal object's value it returns\n    python's False/True values that will be later serialized to form that\n    is native for content-type of use.\n\n    This behavior can be changed using ``representations`` field argument.\n\n    Args:\n\n        representations (tuple): two-tuple with representations for\n           (False, True) values, that will be used instead of default values\n\n    "
    type = 'bool'
    _TRUE_VALUES = {
     'True', 'true', 'TRUE', 'T', 't', '1', 1, True}
    _FALSE_VALUES = {'False', 'false', 'FALSE', 'F', 'f0', 0, 0.0, False}
    _DEFAULT_REPRESENTATIONS = (False, True)

    def __init__(self, details, representations=None, **kwargs):
        super().__init__(details, **kwargs)
        if representations:
            self._FALSE_VALUES = {representations[False]}
            self._TRUE_VALUES = {representations[True]}
        self.representations = representations or self._DEFAULT_REPRESENTATIONS

    def from_representation(self, data):
        if data in self._TRUE_VALUES:
            return True
        if data in self._FALSE_VALUES:
            return False
        raise ValueError('{type} type value must be one of {{values}}'.format(type=self.type, values=self._TRUE_VALUES.union(self._FALSE_VALUES)))

    def to_representation(self, value):
        return self.representations[value]


class IntField(BaseField):
    __doc__ = "\n    Represents integer type of field. Accepts both integers and strings\n    as an incoming integer representation and always returns int as a\n    representation of internal objects's value that will be later\n    serialized to form that is native for content-type of use.\n\n    This field accepts optional arguments that simply add new `max` and `min`\n    value validation.\n\n    Args:\n        max_value (int): optional max value for validation\n        min_value (int): optional min value for validation\n\n    "
    type = 'int'

    def __init__(self, details, max_value=None, min_value=None, **kwargs):
        super().__init__(details, **kwargs)
        self.max_value = max_value
        self.min_value = min_value
        if max_value is not None:
            self.validators.append(max_validator(max_value))
        if min_value is not None:
            self.validators.append(min_validator(min_value))
        return

    def to_representation(self, value):
        return int(value)

    def from_representation(self, data):
        return int(data)


class FloatField(BaseField):
    __doc__ = "\n    Represents float type of field. Accepts both floats and strings\n    as an incoming float number representation and always returns float as a\n    representation of internal objects's value that will be later\n    serialized to form that is native for content-type of use.\n\n    This field accepts optional arguments that simply add new `max` and `min`\n    value validation.\n\n    Args:\n        max_value (int): optional max value for validation\n        min_value (int): optional min value for validation\n\n    "
    type = 'float'

    def __init__(self, details, max_value=None, min_value=None, **kwargs):
        super().__init__(details, **kwargs)
        self.max_value = max_value
        self.min_value = min_value
        if max_value is not None:
            self.validators.append(max_validator(max_value))
        if min_value is not None:
            self.validators.append(min_validator(min_value))
        return

    def to_representation(self, value):
        return float(value)

    def from_representation(self, data):
        return float(data)