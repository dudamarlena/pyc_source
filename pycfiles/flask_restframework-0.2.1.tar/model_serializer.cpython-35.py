# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/serializer/model_serializer.py
# Compiled at: 2017-11-03 05:35:30
# Size of source mod 2**32: 2797 bytes
import six
from flask_restframework.fields import BaseField
from flask_restframework.serializer.base_serializer import BaseSerializer, _BaseSerializerMetaClass
from ..utils import mongoengine_model_meta as model_meta

class _ModelSerializerMetaclass(_BaseSerializerMetaClass):
    field_mapping = model_meta.FIELD_MAPPING

    @classmethod
    def _get_declared_fields(cls, name, bases, attrs):
        declared = _BaseSerializerMetaClass._get_declared_fields(name, bases, attrs)
        if name == 'ModelSerializer':
            return declared
        if 'Meta' in attrs and hasattr(attrs['Meta'], 'fields'):
            attrs['Meta'].fields = tuple(set(attrs['Meta'].fields).union(declared.keys()))
        try:
            model = attrs['Meta'].model
        except:
            raise TypeError('You should define Meta class with model attribute')

        fieldsFromModel = {}
        for key, fieldCls in six.iteritems(model_meta.get_fields(model)):
            if fieldCls not in cls.field_mapping:
                raise ValueError('No mapping for field {}'.format(fieldCls))
            fieldsFromModel[key] = cls.field_mapping[fieldCls].from_mongoengine_field(model_meta.get_field(model, key))

        fieldsFromModel.update(declared)
        return fieldsFromModel


@six.add_metaclass(_ModelSerializerMetaclass)
class ModelSerializer(BaseSerializer):
    __doc__ = '\n    Generic serializer for mongoengine models.\n    You can use it in this way:\n\n        >>> class Col(db.Document):\n        >>>     value = db.StringField()\n        >>>     created = db.DateTimeField(default=datetime.datetime.now)\n        >>>\n        >>> class S(BaseSerializer):\n        >>>     class Meta:\n        >>>         model = Col\n        >>>\n        >>> data = S(Col.objects.all()).serialize()\n\n    '
    field_mapping = model_meta.FIELD_MAPPING

    def get_model(self):
        """
        Returns model ORM class.
        """
        try:
            return self.Meta.model
        except:
            raise ValueError('You should specify Meta class with model attribute')

    def create(self, validated_data):
        """Performs create instance. Returns model intance"""
        return self.get_model().objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Performs update for instance. Returns instance with updated fields"""
        validated_data.pop('id', None)
        for key, value in six.iteritems(validated_data):
            try:
                setattr(instance, key, value)
            except Exception as e:
                print(key, value)

        instance.save()
        return instance