# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swistakm/dev/graceful/build/lib/graceful/parameters.py
# Compiled at: 2015-07-14 08:35:08
# Size of source mod 2**32: 7175 bytes
import base64, decimal, binascii, inspect

class BaseParam:
    __doc__ = '\n    Base parameter class for subclassing. To create new parameter type\n    subclass ``BaseField`` and implement following methods:\n\n    To create new field type subclass ``BaseParam`` and implement ``.value()``\n    method handlers.\n\n\n    Args:\n\n        details (str): verbose description of parameter. Should contain all\n           information that may be important to your API user and will be used\n           for describing resource on ``OPTIONS`` requests and ``.describe()``\n           call.\n\n        label (str): human readable label for this parameter (it will be used\n           for describing resource on OPTIONS requests).\n\n           *Note that it is recomended to use parameter names that are\n           self-explanatory intead of relying on param labels.*\n\n        required (bool): if set to ``True`` then all GET, POST, PUT,\n           PATCH and DELETE requests will return ``400 Bad Request`` response\n           if query param is not provided. Defaults to ``False``.\n\n        default (str): set default value for param if it is not\n           provided in request as query parameter. This MUST be a raw string\n           value that will be then parsed by ``.value()`` handler.\n\n           If default is set and ``required`` is ``True`` it will raise\n           ``ValueError`` as having required parameters with default\n           value has no sense.\n\n        param (str): set to ``True`` if multiple occurences of this parameter\n           can be included in query string, as a result values for this\n           parameter will be always included as a list in params dict. Defaults\n           to ``False``.\n\n          .. note::\n             If ``many=False`` and client inlcudes multiple values for this\n             parameter in query string then only one of those values will be\n             returned, and it is undefined which one.\n\n    Example:\n\n    .. code-block:: python\n\n           class BoolParam(BaseParam):\n               def value(self, data):\n                   if data in {\'true\', \'True\', \'yes\', \'1\', \'Y\'}:\n                       return True:\n                   elif data in {\'false\', \'False\', \'no\', \'0\', \'N\'}:\n                       return False:\n                   else:\n                       raise ValueError(\n                           "{data} is not valid boolean field".format(\n                               data=data\n                           )\n                       )\n\n    '
    spec = None
    type = None

    def __init__(self, details, label=None, required=False, default=None, many=False):
        self.label = label
        self.details = details
        self.required = required
        self.many = many
        if default is not None:
            if not isinstance(default, str):
                raise TypeError("value for {cls} 'default' argument must be string instance".format(cls=self.__class__.__name__))
        if default is not None:
            if required:
                raise ValueError("{cls}(required={required}, default='{default}'): initialization with both required and default makes no sense".format(cls=self.__class__.__name__, default=default, required=required))
        self.default = default

    def value(self, raw_value):
        """
        Raw value deserializtion method handler

        Args:
            raw_value (str) - raw value from GET parameters

        """
        raise NotImplementedError('{cls}.value() method not implemented'.format(cls=self.__class__.__name__))

    def describe(self, **kwargs):
        """
        Describe this parameter instance for purpose of self-documentation.

        Args:
            kwargs (dict): dictionary of additional description items for
               extending default description

        Returns:
            dict: dictionary of description items

        Suggested way for overriding description fields or extending it with
        additional items is calling super class method with new/overriden
        fields passed as keyword arguments like following:

        .. code-block:: python

            class DummyParam(BaseParam):
               def description(self, **kwargs):
                   super().describe(is_dummy=True, **kwargs)

        """
        description = {'label': self.label, 
         'details': inspect.cleandoc(self.details), 
         'required': self.required, 
         'many': self.many, 
         'spec': self.spec, 
         'default': self.default, 
         'type': self.type or 'unspecified'}
        description.update(kwargs)
        return description


class StringParam(BaseParam):
    __doc__ = '\n    Describes parameter that will always be returned in same form as provided\n    in query string. Still additional validation can be added to param instance\n    e.g.:\n\n    .. code-block:: python\n\n        from graceful.parameters import StringParam\n        from graceful.validators import match_validator\n        from graceful.resources.generic import Resource\n\n        class ExampleResource(Resource):\n            word = StringParam(\n                \'one "word" parameter\',\n                validators=[match_validator(\'\\w+\')],\n            )\n\n    '
    type = 'string'

    def value(self, raw_value):
        """Returns value as-is (str)"""
        return raw_value


class Base64EncodedParam(BaseParam):
    __doc__ = '\n    Describes string parameter that has value encoded using Base64 encoding\n    '
    spec = ('RFC-4648 Section 4', 'https://tools.ietf.org/html/rfc4648#section-4')

    def value(self, raw_value):
        """Decodes param with Base64"""
        try:
            return base64.b64decode(bytes(raw_value, 'utf-8')).decode('utf-8')
        except binascii.Error as err:
            raise ValueError(str(err))


class IntParam(BaseParam):
    __doc__ = '\n    Describes parameter that has value expressed as integer number\n    '
    type = 'integer'

    def value(self, raw_value):
        """Decodes param as integer value"""
        return int(raw_value)


class FloatParam(BaseParam):
    __doc__ = '\n    Describes parameter that has value expressed as float number\n    '
    type = 'float'

    def value(self, raw_value):
        """Decodes param as float value"""
        return float(raw_value)


class DecimalParam(BaseParam):
    __doc__ = '\n    Describes parameter that has value expressed as decimal number\n    '
    type = 'decimal'

    def value(self, raw_value):
        """Decodes param as decimal value"""
        try:
            return decimal.Decimal(raw_value)
        except decimal.InvalidOperation:
            raise ValueError("Could not parse '{}' value as decimal".format(raw_value))