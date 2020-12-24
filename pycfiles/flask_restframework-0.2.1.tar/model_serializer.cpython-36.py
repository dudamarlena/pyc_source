# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/logviewer/flask_validator/serializer/model_serializer.py
# Compiled at: 2017-01-12 12:17:35
# Size of source mod 2**32: 1680 bytes
import six
from flask_validator.serializer.base_serializer import BaseSerializer, _BaseSerializerMetaClass
from ..utils import mongoengine_model_meta as model_meta

class ModelSerializer(BaseSerializer):
    __doc__ = '\n    Generic serializer for mongoengine models.\n    You can use it in this way:\n\n        >>> class Col(db.Document):\n        >>>     value = db.StringField()\n        >>>     created = db.DateTimeField(default=datetime.datetime.now)\n        >>>\n        >>> class S(BaseSerializer):\n        >>>     class Meta:\n        >>>         model = Col\n        >>>\n        >>> data = S(Col.objects.all()).to_python()\n\n    '
    field_mapping = model_meta.FIELD_MAPPING

    def get_model(self):
        try:
            return self.Meta.model
        except:
            raise ValueError('You should specify Meta class with model attribute')

    def get_fields(self):
        model = self.get_model()
        fieldsFromModel = {}
        for key, fieldCls in six.iteritems(model_meta.get_fields(model)):
            if fieldCls not in self.field_mapping:
                raise ValueError('No mapping for field {}'.format(fieldCls))
            fieldsFromModel[key] = self.field_mapping[fieldCls].from_mongoengine_field(model_meta.get_field(model, key))

        fieldsFromModel.update(super(ModelSerializer, self).get_fields())
        return fieldsFromModel

    def update(self, instance, validated_data):
        """Performs update for instance. Returns instance with updated fields"""
        for key, value in six.iteritems(validated_data):
            setattr(instance, key, value)

        instance.save()
        return instance