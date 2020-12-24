# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/transdb/xml_serializer.py
# Compiled at: 2010-11-15 07:25:19
from django.core.serializers import base, xml_serializer
from django.db import models
from django.utils.encoding import smart_unicode
from fields import TransField

class Serializer(xml_serializer.Serializer):

    def get_string_value(self, obj, field):
        if isinstance(field, TransField):
            return smart_unicode(getattr(obj, field.name).raw_data)
        else:
            return super(Serializer, self).get_string_value(obj, field)


class Deserializer(xml_serializer.Deserializer):

    def _handle_object(self, node):
        """
        Convert an <object> node to a DeserializedObject.
        """
        Model = self._get_model_from_node(node, 'model')
        pk = node.getAttribute('pk')
        if not pk:
            raise base.DeserializationError("<object> node is missing the 'pk' attribute")
        data = {Model._meta.pk.attname: Model._meta.pk.to_python(pk)}
        m2m_data = {}
        for field_node in node.getElementsByTagName('field'):
            field_name = field_node.getAttribute('name')
            if not field_name:
                raise base.DeserializationError("<field> node is missing the 'name' attribute")
            field = Model._meta.get_field(field_name)
            if field.rel and isinstance(field.rel, models.ManyToManyRel):
                m2m_data[field.name] = self._handle_m2m_field_node(field_node, field)
            elif field.rel and isinstance(field.rel, models.ManyToOneRel):
                data[field.attname] = self._handle_fk_field_node(field_node, field)
            else:
                if field_node.getElementsByTagName('None'):
                    value = None
                elif isinstance(field, TransField):
                    value = field.to_python(xml_serializer.getInnerText(field_node).strip()).raw_data
                else:
                    value = field.to_python(xml_serializer.getInnerText(field_node).strip())
                data[field.name] = value

        return base.DeserializedObject(Model(**data), m2m_data)