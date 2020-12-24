# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/serializer/base_serializer.py
# Compiled at: 2017-11-03 05:35:30
# Size of source mod 2**32: 12818 bytes
from collections import OrderedDict
import six
from werkzeug.exceptions import BadRequest
from flask_restframework.fields import BaseRelatedField
from flask_restframework.fields import ForeignKeyField
from flask_restframework.fields import BaseField
from ..exceptions import ValidationError
__author__ = 'stas'

class _BaseSerializerMetaClass(type):
    __doc__ = '\n    This metaclass sets a dictionary named `_declared_fields` on the class.\n    Any instances of `Field` included as attributes on either the class\n    or on any of its superclasses will be include in the\n    `_declared_fields` dictionary.\n    '

    @classmethod
    def _get_declared_fields(cls, name, bases, attrs):
        fields = [(field_name, attrs.pop(field_name)) for field_name, obj in list(attrs.items()) if isinstance(obj, BaseField)]
        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                fields = list(base._declared_fields.items()) + fields

        return OrderedDict(fields)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls._get_declared_fields(name, bases, attrs)
        return super(_BaseSerializerMetaClass, cls).__new__(cls, name, bases, attrs)


@six.add_metaclass(_BaseSerializerMetaClass)
class BaseSerializer:
    __doc__ = '\n    Base class for all validators.\n    Each validator represents rules for validating request\n    Each view can have multiple validators, base on Content-Type header\n    Validator can validate next fields:\n\n        * request.form - Ordinal POST queries\n        * request.json - POST JSON body\n        * request.args - GET params\n        * request.files - passed files\n\n    After validation, validator has next properties:\n\n        * self.errors - error dict in next format::\n\n            {\n                <field>: [list of errors]\n                __non_field_errors__: [list of common (not field) errors]\n            }\n\n        * self.data - validated data constructed from request.form/request.json\n        * self.query_data - validated data constructed from request.args\n        * self.files - validated files\n\n    Usage example::\n\n        class TestValidation(BaseValidator):\n\n            choices = fields.StringField(choices=["1", "2", "3"], required=True)\n            not_req = fields.StringField()\n            boolean = fields.BooleanField(required=True)\n            boolean_not_req = fields.BooleanField()\n\n    Meta subclass atributes::\n\n        class Meta:\n\n            allow_additional_fields = False     #if True - all not registered fields also will be passed in cleaned_data\n            excluded = ("field1", )             # array of fields need to be excluded from serialization\n            fields = ("field1", )               # array of fields need to be serialized. You can\'t use fields and excluded in\n                                                  same serializer\n            fk_fields = ("related__field", )    # array of related (or embeddedDocument) fields need to be serialized\n            read_only = (<read only field name>, )  #array of read only fields of serializer\n\n\n    '
    _declared_fields = None

    def __init__(self, data, context=None):
        self._data = data
        self._cleaned_data = {}
        self.context = context or {}
        self._bind_self_to_fields()

    def get_fields(self):
        """
        returns mapping: <fieldName>: <Field>

        Returns:

            * Only fields declared in Meta.fields if present (+ class-defined fields)
            * All fields, except Meta.excluded if present
        """
        output = {}
        if hasattr(self, 'Meta'):
            meta = self.Meta
            if hasattr(meta, 'fields'):
                return {key:value for key, value in self._declared_fields.items() if key in meta.fields}
            if hasattr(meta, 'excluded'):
                pass
            return {key:value for key, value in self._declared_fields.items() if key not in meta.excluded}
        return self._declared_fields

    def to_python(self):
        """
        Returns python representation of queryset data.
        This data will be used in serializer.cleaned_data
        """
        from mongoengine.queryset.queryset import QuerySet
        if isinstance(self._data, (QuerySet, list)):
            output = []
            for item in self._data:
                output.append(self._item_to_python(item))

        else:
            output = self._item_to_python(self._data)
        return output

    def serialize(self):
        """
        This method takes python representation .to_python of data
        and perform serialization to json-compatible array
        """
        data = self._data
        if hasattr(data, '__iter__') and not isinstance(data, dict):
            out = []
            for item in data:
                out.append(self._serialize_item(item))

            return out
        else:
            return self._serialize_item(data)

    def serialize_one(self):
        return self._serialize_item(self._data)

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

    def validate(self, part=False, throw=False):
        """
        Runs validation on passed data

        Usage example::

            >>> s = serializerCls(request.json)
            >>> if not s.validate():
            >>>     out = jsonify(s.errors)
            >>>     out.status_code = 400
            >>>     return out

        You can preform part validation, i.e. to validate only presented in data fields.
        It can be useful for validating PATCH request, when we need to validate only subset of fields.

        :return: True if validation succeeded, False else
        """
        from flask_restframework import fields
        errors = {}
        if self._data is None:
            raise BadRequest('No data passed')
        if self._allow_additional_fields():
            self._cleaned_data = self._data.copy()
        for key, field in self._get_writable_fields().items():
            if part and key not in self._data.keys():
                pass
            else:
                assert isinstance(field, fields.BaseField)
                value = self._data.get(key)
                try:
                    validated_value = field.run_validate(serializer=self, value=value)
                    self._cleaned_data[key] = validated_value
                except ValidationError as e:
                    self.process_validation_exception(e, errors, key)

        try:
            post_validate_value = self.post_validate(self._cleaned_data)
            if post_validate_value is not None:
                self._cleaned_data = post_validate_value
        except ValidationError as e:
            self.process_validation_exception(e, errors, 'non_field_errors')

        self.errors = errors
        if throw and errors:
            raise ValidationError(errors)
        if errors:
            return False
        post_validate_value = self.post_validate(self._cleaned_data)
        if post_validate_value is not None:
            self._cleaned_data = post_validate_value
        return True

    def post_validate(self, cleaned_data):
        """
        This method can be used for custom validation of whole serializer.
        Also you can owerwrite cleaned data in this method.
        Should raise ValidationError on validation error.

        :param cleaned_data:
        :return: new cleaned data
        """
        return cleaned_data

    def process_validation_exception(self, exception, errors_dict, key):
        if isinstance(exception.data, dict):
            for key, message in six.iteritems(exception.data):
                errors_dict.setdefault(key, []).append(message)

        elif isinstance(exception.data, six.string_types):
            errors_dict.setdefault(key, []).append(exception.data)

    def get_serialisable_fields(self):
        """returns set of fields need to be serialized"""
        output = set(self.get_fields().keys())
        if hasattr(self, 'Meta'):
            meta = self.Meta
            if hasattr(meta, 'fields'):
                pass
            output = set(meta.fields)
            if hasattr(meta, 'excluded'):
                raise ValueError("You can't use fields and excluded attribute together!")
        elif hasattr(meta, 'excluded'):
            output = set(self.get_fields().keys()).difference(meta.excluded)
        fields = self.get_fields()
        bad_fields = [f for f in output if f not in fields]
        if bad_fields:
            raise TypeError('Fields in Meta.fields are not declared in serializer: {}'.format(', '.join(bad_fields)))
        return output

    def get_declared_only_fields(self):
        """Returns only declared fields"""
        return self._declared_fields

    def get_fk_fields(self):
        """
        Returns dictionary with ForeignKey fields
        This is fields which ONLY readable. You can use it only for representing nested/related data.
        For use it in validation, use PrimaryKeyField
        <key in serializer>: <field instance>
        """
        out = {}
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'fk_fields'):
            for key in self.Meta.fk_fields:
                if '__' not in key:
                    raise ValueError('You should use Django __ notation for FK fields!')
                mainFkField = key.split('__')[0]
                if mainFkField not in self._declared_fields:
                    raise ValueError('Incorrect field: {}'.format(mainFkField))
                out[key] = self._declared_fields[mainFkField]

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
            assert isinstance(field, BaseRelatedField)
            value = field.get_value_from_model_object(item, key)
            out[key] = value

        return out

    def _serialize_item(self, item):
        """
        Performs serialization for python representation of item.
        Uses Field.
        """
        out = {}
        for key, field in self.get_fields().items():
            assert isinstance(field, BaseField)
            value = field.get_value_from_model_object(item, key)
            out[key] = field.to_json(value)

        for key, field in self.get_fk_fields().items():
            value = field.get_value_from_model_object(item, key)
            out[key] = field.to_json(value)

        return out

    def _get_writable_fields(self):
        """
        Returns subdict from self.get_fields() with writable fields only

        :rtype dict:
        """
        out = {}
        read_only_from_meta = []
        if hasattr(self, 'Meta'):
            read_only_from_meta = getattr(self.Meta, 'read_only', [])
        for key, field in self.get_fields().items():
            assert isinstance(field, BaseField)
            if not field._read_only and key not in read_only_from_meta:
                out[key] = field

        return out

    def _bind_self_to_fields(self):
        """For each field sets <field>.serializer to self"""
        for fieldname, field in six.iteritems(self.get_fields()):
            field.serializer = self
            field.fieldname = fieldname