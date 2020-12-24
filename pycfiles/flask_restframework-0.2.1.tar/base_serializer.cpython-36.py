# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/logviewer/flask_validator/serializer/base_serializer.py
# Compiled at: 2017-01-12 12:04:40
# Size of source mod 2**32: 9059 bytes
from collections import OrderedDict
import six
from mongoengine.queryset.queryset import QuerySet
from werkzeug.exceptions import BadRequest
from flask_validator.fields import ForeignKeyField
from flask_validator.fields import BaseField
from ..exceptions import ValidationError
__author__ = 'stas'

class _BaseSerializerMetaClass(type):
    __doc__ = '\n    This metaclass sets a dictionary named `_declared_fields` on the class.\n    Any instances of `Field` included as attributes on either the class\n    or on any of its superclasses will be include in the\n    `_declared_fields` dictionary.\n    '

    @classmethod
    def _get_declared_fields(cls, bases, attrs):
        fields = [(field_name, attrs.pop(field_name)) for field_name, obj in list(attrs.items()) if isinstance(obj, BaseField)]
        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                fields = list(base._declared_fields.items()) + fields

        return OrderedDict(fields)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls._get_declared_fields(bases, attrs)
        return super(_BaseSerializerMetaClass, cls).__new__(cls, name, bases, attrs)


@six.add_metaclass(_BaseSerializerMetaClass)
class BaseSerializer:
    __doc__ = '\n    Base class for all validators.\n    Each validator represents rules for validating request\n    Each view can have multiple validators, base on Content-Type header\n    Validator can validate next fields:\n\n        * request.form - Ordinal POST queries\n        * request.json - POST JSON body\n        * request.args - GET params\n        * request.files - passed files\n\n    After validation, validator has next properties:\n\n        * self.errors - error dict in next format::\n\n            {\n                <field>: [list of errors]\n                __non_field_errors__: [list of common (not field) errors]\n            }\n\n        * self.data - validated data constructed from request.form/request.json\n        * self.query_data - validated data constructed from request.args\n        * self.files - validated files\n\n    Usage example::\n\n        class TestValidation(BaseValidator):\n\n            choices = fields.StringField(choices=["1", "2", "3"], required=True)\n            not_req = fields.StringField()\n            boolean = fields.BooleanField(required=True)\n            boolean_not_req = fields.BooleanField()\n\n    Meta subclass atributes::\n\n        class Meta:\n\n            allow_additional_fields = False     #if True - all not registered fields also will be passed in cleaned_data\n            excluded = ("field1", )             # array of fields need to be excluded from serialization\n            fields = ("field1", )               # array of fields need to be serialized. You can\'t use fields and excluded in\n                                                  same serializer\n            fk_fields = ("related__field", )    # array of related (or embeddedDocument) fields need to be serialized\n\n\n    '
    _declared_fields = None

    def __init__(self, data, context=None):
        self._data = data
        self._cleaned_data = {}
        self.context = context or {}
        self._bind_self_to_fields()

    def get_fields(self):
        """returns mapping: <fieldName>: <Field>"""
        return self._declared_fields

    def to_python(self):
        """Returns python representation of queryset data"""
        if isinstance(self._data, QuerySet):
            output = []
            for item in self._data:
                output.append(self._item_to_python(item))

        else:
            output = self._item_to_python(self._data)
        output = self.serialize(output)
        return output

    def serialize(self, serializedData):
        """This method allows to add custom serialization"""
        return serializedData

    @property
    def cleaned_data(self):
        return self._cleaned_data

    def create(self, validated_data):
        """
        Perform create operation
        :param validated_data: data after validation
        :return: created instance
        """
        pass

    def update(self, instance, validated_data):
        """
        Perform update opertaion
        :param instance: instance for update
        :param validated_data: data after validation
        :return: updated instance
        """
        pass

    def validate(self):
        """
        Runs validation on passed data

        Usage example::

            >>> s = serializerCls(request.json)
            >>> if not s.validate():
            >>>     out = jsonify(s.errors)
            >>>     out.status_code = 400
            >>>     return out

        :return: True if validation succeeded, False else
        """
        from flask_validator import fields
        errors = {}
        if self._data is None:
            raise BadRequest('No data passed')
        if self._allow_additional_fields():
            self._cleaned_data = self._data.copy()
        for key, field in self._get_writable_fields().items():
            assert isinstance(field, fields.BaseField)
            value = self._data.get(key)
            try:
                validated_value = field.run_validate(validator=self,
                  value=value)
                self._cleaned_data[key] = validated_value
            except ValidationError as e:
                if isinstance(e.data, dict):
                    for key, message in six.iteritems(e.data):
                        errors.setdefault(e.data.key, []).append(message)

                else:
                    if isinstance(e.data, six.string_types):
                        errors.setdefault(key, []).append(e.data)

        self.errors = errors
        if errors:
            return False
        else:
            return True

    def get_serialisable_fields(self):
        """returns set of fields need to be serialized"""
        output = set(self.get_fields().keys())
        if hasattr(self, 'Meta'):
            meta = self.Meta
            if hasattr(meta, 'fields'):
                output = set(meta.fields)
                if hasattr(meta, 'excluded'):
                    raise ValueError("You can't use fields and excluded attribute together!")
            elif hasattr(meta, 'excluded'):
                output = set(self.get_fields().keys()).difference(meta.excluded)
        return output

    def get_declared_only_fields(self):
        """Returns only declared fields"""
        return self._declared_fields

    def get_fk_fields(self):
        """
        Returns dictionary with ForeignKey fields
        <key in serializer>: <field instance>
        """
        out = {}
        if hasattr(self, 'Meta'):
            if hasattr(self.Meta, 'fk_fields'):
                for key in self.Meta.fk_fields:
                    if '__' not in key:
                        raise ValueError('You should use Django __ notation for FK fields!')
                    mainFkField = key.split('__')[0]
                    fields = self.get_fields()
                    if mainFkField not in self.get_fields():
                        raise ValueError('Incorrect field: {}'.format(mainFkField))
                    out[key] = fields[mainFkField]

        for key, value in six.iteritems(self.get_declared_only_fields()):
            if isinstance(value, ForeignKeyField):
                out[key] = value

        return out

    def _allow_additional_fields(self):
        meta = getattr(self, 'Meta', None)
        return getattr(meta, 'allow_additional_fields', False)

    def _item_to_python(self, item):
        """Return python representation for one item, base on fields"""
        out = {}
        serializable_fields = self.get_serialisable_fields()
        for key, field in self.get_fields().items():
            if key not in serializable_fields:
                pass
            else:
                assert isinstance(field, BaseField), field
                value = field.get_value_from_model_object(item, key)
                out[key] = field.to_python(value)

        for key, field in six.iteritems(self.get_fk_fields()):
            assert isinstance(field, ForeignKeyField)
            value = field.get_value_from_model_object(item, key)
            out[key] = field.to_python(value)

        return out

    def _get_writable_fields(self):
        """
        Returns subdict from self.get_fields() with writable fields only

        :rtype dict:
        """
        out = {}
        for key, field in self.get_fields().items():
            assert isinstance(field, BaseField)
            if not field._read_only:
                out[key] = field

        return out

    def _bind_self_to_fields(self):
        """For each field sets <field>.serializer to self"""
        for field in six.itervalues(self.get_fields()):
            field.serializer = self