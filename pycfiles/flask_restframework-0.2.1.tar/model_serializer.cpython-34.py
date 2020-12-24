# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/serializer/model_serializer.py
# Compiled at: 2017-07-14 10:03:06
# Size of source mod 2**32: 3119 bytes
import six
from mongoengine.document import Document
from flask_restframework.model_wrapper import BaseModelWrapper, BaseFieldWrapper
from flask_restframework.queryset_wrapper import InstanceWrapper, MongoInstanceWrapper
from flask_restframework.serializer.base_serializer import BaseSerializer, _BaseSerializerMetaClass
from ..utils import mongoengine_model_meta as model_meta

class _ModelSerializerMetaclass(_BaseSerializerMetaClass):
    field_mapping = model_meta.FIELD_MAPPING

    @classmethod
    def _get_declared_fields(cls, name, bases, attrs):
        declared = _BaseSerializerMetaClass._get_declared_fields(name, bases, attrs)
        if name == 'ModelSerializer':
            return declared
        if 'Meta' in attrs:
            if hasattr(attrs['Meta'], 'fields'):
                attrs['Meta'].fields = tuple(set(attrs['Meta'].fields).union(declared.keys()))
        try:
            model = BaseModelWrapper.fromModel(attrs['Meta'].model)
        except AttributeError:
            raise TypeError('You should define Meta class with model attribute')

        fieldsFromModel = {}
        assert isinstance(model, BaseModelWrapper)
        for key, wrappedField in model.get_fields().items():
            assert isinstance(wrappedField, BaseFieldWrapper)
            fieldsFromModel[key] = wrappedField.get_serializer_field(key)

        fieldsFromModel.update(declared)
        return fieldsFromModel


@six.add_metaclass(_ModelSerializerMetaclass)
class ModelSerializer(BaseSerializer):
    __doc__ = '\n    Generic serializer for mongoengine models.\n    You can use it in this way:\n\n        >>> class Col(db.Document):\n        >>>     value = db.StringField()\n        >>>     created = db.DateTimeField(default=datetime.datetime.now)\n        >>>\n        >>> class S(BaseSerializer):\n        >>>     class Meta:\n        >>>         model = Col\n        >>>\n        >>> data = S(Col.objects.all()).serialize()\n\n    '

    def get_model(self):
        """
        Returns BaseModelWrapper for serializer-defined model.
        """
        try:
            return BaseModelWrapper.fromModel(self.Meta.model)
        except:
            raise ValueError('You should specify Meta class with model attribute')

    def create(self, validated_data):
        """Performs create instance. Returns wrapped model intance"""
        return InstanceWrapper.from_instance(self.get_model().create(**validated_data))

    def update(self, instance, validated_data):
        """Performs update for instance. Returns wrapped instance with updated fields"""
        assert isinstance(instance, InstanceWrapper)
        validated_data.pop('id', None)
        instance.update(validated_data)
        return instance