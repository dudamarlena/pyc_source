# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sao/src/github/django-json-api/django-rest-framework-json-api/rest_framework_json_api/renderers.py
# Compiled at: 2019-12-13 14:53:50
# Size of source mod 2**32: 26673 bytes
"""
Renderers
"""
import copy
from collections import OrderedDict, defaultdict
from collections.abc import Iterable
import inflection
from django.db.models import Manager
from django.utils import encoding
from rest_framework import relations, renderers
from rest_framework.fields import SkipField, get_attribute
from rest_framework.relations import PKOnlyObject
from rest_framework.serializers import BaseSerializer, ListSerializer, Serializer
from rest_framework.settings import api_settings
import rest_framework_json_api
from rest_framework_json_api import utils
from rest_framework_json_api.relations import HyperlinkedMixin, ResourceRelatedField, SkipDataMixin

class JSONRenderer(renderers.JSONRenderer):
    __doc__ = '\n    The `JSONRenderer` exposes a number of methods that you may override if you need highly\n    custom rendering control.\n\n    Render a JSON response per the JSON API spec:\n\n    .. code-block:: json\n\n        {\n          "data": [\n            {\n              "type": "companies",\n              "id": 1,\n              "attributes": {\n                "name": "Mozilla",\n                "slug": "mozilla",\n                "date-created": "2014-03-13 16:33:37"\n              }\n            }\n          ]\n        }\n    '
    media_type = 'application/vnd.api+json'
    format = 'vnd.api+json'

    @classmethod
    def extract_attributes(cls, fields, resource):
        """
        Builds the `attributes` object of the JSON API resource object.
        """
        data = OrderedDict()
        for field_name, field in iter(fields.items()):
            if field_name == 'id':
                pass
            else:
                if fields[field_name].write_only:
                    pass
                else:
                    if isinstance(field, (relations.RelatedField, relations.ManyRelatedField, BaseSerializer)):
                        pass
                    else:
                        try:
                            resource[field_name]
                        except KeyError:
                            if fields[field_name].read_only:
                                continue

                        data.update({field_name: resource.get(field_name)})

        return utils.format_field_names(data)

    @classmethod
    def extract_relationships(cls, fields, resource, resource_instance):
        """
        Builds the relationships top level object based on related serializers.
        """
        from rest_framework_json_api.relations import ResourceRelatedField
        data = OrderedDict()
        if resource_instance is None:
            return
        for field_name, field in iter(fields.items()):
            if field_name == api_settings.URL_FIELD_NAME:
                pass
            else:
                if fields[field_name].write_only:
                    pass
                else:
                    if not isinstance(field, (relations.RelatedField, relations.ManyRelatedField, BaseSerializer)):
                        pass
                    else:
                        source = field.source
                        relation_type = utils.get_related_resource_type(field)
                        if isinstance(field, relations.HyperlinkedIdentityField):
                            pass
                        resolved, relation_instance = utils.get_relation_instance(resource_instance, source, field.parent)
                        if not resolved:
                            pass
                        else:
                            relation_data = list()
                            relation_queryset = relation_instance if relation_instance is not None else list()
                            for related_object in relation_queryset:
                                relation_data.append(OrderedDict([
                                 (
                                  'type', relation_type),
                                 (
                                  'id', encoding.force_str(related_object.pk))]))

                            data.update({field_name: {'links': {'related': resource.get(field_name)}, 
                                          
                                          'data': relation_data, 
                                          'meta': {'count': len(relation_data)}}})
                            continue
                            relation_data = {}
                            if isinstance(field, HyperlinkedMixin):
                                field_links = field.get_links(resource_instance, field.related_link_lookup_field)
                                relation_data.update({'links': field_links} if field_links else dict())
                                data.update({field_name: relation_data})
                            if isinstance(field, (ResourceRelatedField,)):
                                if not isinstance(field, SkipDataMixin):
                                    relation_data.update({'data': resource.get(field_name)})
                                data.update({field_name: relation_data})
                                continue
                                if isinstance(field, (relations.PrimaryKeyRelatedField, relations.HyperlinkedRelatedField)):
                                    pass
                            resolved, relation = utils.get_relation_instance(resource_instance, '%s_id' % source, field.parent)
                            if not resolved:
                                pass
                            else:
                                relation_id = relation if resource.get(field_name) else None
                                relation_data = {'data': OrderedDict([('type', relation_type), ('id', encoding.force_str(relation_id))]) if relation_id is not None else None}
                                if isinstance(field, relations.HyperlinkedRelatedField) and resource.get(field_name):
                                    relation_data.update({'links': {'related': resource.get(field_name)}})
                                data.update({field_name: relation_data})
                                continue
                                if isinstance(field, relations.ManyRelatedField):
                                    pass
                                resolved, relation_instance = utils.get_relation_instance(resource_instance, source, field.parent)
                                if not resolved:
                                    pass
                                else:
                                    relation_data = {}
                                    if isinstance(resource.get(field_name), Iterable):
                                        relation_data.update({'meta': {'count': len(resource.get(field_name))}})
                                    if isinstance(field.child_relation, ResourceRelatedField):
                                        relation_data.update({'data': resource.get(field_name)})
                        if isinstance(field.child_relation, HyperlinkedMixin):
                            field_links = field.child_relation.get_links(resource_instance, field.child_relation.related_link_lookup_field)
                            relation_data.update({'links': field_links} if field_links else dict())
                            data.update({field_name: relation_data})
                            continue
                            relation_data = list()
                            for nested_resource_instance in relation_instance:
                                nested_resource_instance_type = relation_type or utils.get_resource_type_from_instance(nested_resource_instance)
                                relation_data.append(OrderedDict([
                                 (
                                  'type', nested_resource_instance_type),
                                 (
                                  'id', encoding.force_str(nested_resource_instance.pk))]))

                            data.update({field_name: {'data': relation_data, 
                                          'meta': {'count': len(relation_data)}}})
                            continue
                            if isinstance(field, ListSerializer):
                                resolved, relation_instance = utils.get_relation_instance(resource_instance, source, field.parent)
                                if not resolved:
                                    pass
                        else:
                            relation_data = list()
                            serializer_data = resource.get(field_name)
                            resource_instance_queryset = list(relation_instance)
                            if isinstance(serializer_data, list):
                                for position in range(len(serializer_data)):
                                    nested_resource_instance = resource_instance_queryset[position]
                                    nested_resource_instance_type = relation_type or utils.get_resource_type_from_instance(nested_resource_instance)
                                    relation_data.append(OrderedDict([
                                     (
                                      'type', nested_resource_instance_type),
                                     (
                                      'id', encoding.force_str(nested_resource_instance.pk))]))

                                data.update({field_name: {'data': relation_data}})
                            continue
                            if isinstance(field, Serializer):
                                relation_instance_id = getattr(resource_instance, source + '_id', None)
                                if not relation_instance_id:
                                    resolved, relation_instance = utils.get_relation_instance(resource_instance, source, field.parent)
                                    if not resolved:
                                        pass
                                    else:
                                        if relation_instance is not None:
                                            relation_instance_id = relation_instance.pk
                                        data.update({field_name: {'data': OrderedDict([('type', relation_type), ('id', encoding.force_str(relation_instance_id))]) if resource.get(field_name) else None}})
                                        continue

        return utils.format_field_names(data)

    @classmethod
    def extract_relation_instance(cls, field, resource_instance):
        """
        Determines what instance represents given relation and extracts it.

        Relation instance is determined exactly same way as it determined
        in parent serializer
        """
        try:
            res = field.get_attribute(resource_instance)
            if isinstance(res, PKOnlyObject):
                return get_attribute(resource_instance, field.source_attrs)
            else:
                return res
        except SkipField:
            return

    @classmethod
    def extract_included(cls, fields, resource, resource_instance, included_resources, included_cache):
        """
        Adds related data to the top level included key when the request includes
        ?include=example,example_field2
        """
        if not resource_instance:
            return
        current_serializer = fields.serializer
        context = current_serializer.context
        included_serializers = utils.get_included_serializers(current_serializer)
        included_resources = copy.copy(included_resources)
        included_resources = [inflection.underscore(value) for value in included_resources]
        for field_name, field in iter(fields.items()):
            if field_name == api_settings.URL_FIELD_NAME:
                pass
            else:
                if not isinstance(field, (relations.RelatedField, relations.ManyRelatedField, BaseSerializer)):
                    pass
                else:
                    try:
                        included_resources.remove(field_name)
                    except ValueError:
                        if field_name not in [node.split('.')[0] for node in included_resources]:
                            continue

                    relation_instance = cls.extract_relation_instance(field, resource_instance)
                    if isinstance(relation_instance, Manager):
                        relation_instance = relation_instance.all()
                    serializer_data = resource.get(field_name)
                    if isinstance(field, relations.ManyRelatedField):
                        serializer_class = included_serializers[field_name]
                        field = serializer_class(relation_instance, many=True, context=context)
                        serializer_data = field.data
                    if isinstance(field, relations.RelatedField):
                        if not relation_instance is None:
                            if not serializer_data:
                                pass
                    else:
                        many = field._kwargs.get('child_relation', None) is not None
                        if isinstance(field, ResourceRelatedField) and not many:
                            already_included = serializer_data['type'] in included_cache and serializer_data['id'] in included_cache[serializer_data['type']]
                            if already_included:
                                pass
                            continue
                            serializer_class = included_serializers[field_name]
                            field = serializer_class(relation_instance, many=many, context=context)
                            serializer_data = field.data
                        new_included_resources = [key.replace('%s.' % field_name, '', 1) for key in included_resources if field_name == key.split('.')[0]]
                        if isinstance(field, ListSerializer):
                            serializer = field.child
                            relation_type = utils.get_resource_type_from_serializer(serializer)
                            relation_queryset = list(relation_instance)
                            if serializer_data:
                                for position in range(len(serializer_data)):
                                    serializer_resource = serializer_data[position]
                                    nested_resource_instance = relation_queryset[position]
                                    resource_type = relation_type or utils.get_resource_type_from_instance(nested_resource_instance)
                                    serializer_fields = utils.get_serializer_fields(serializer.__class__(nested_resource_instance, context=serializer.context))
                                    new_item = cls.build_json_resource_obj(serializer_fields, serializer_resource, nested_resource_instance, resource_type, getattr(serializer, '_poly_force_type_resolution', False))
                                    included_cache[new_item['type']][new_item['id']] = utils.format_field_names(new_item)
                                    cls.extract_included(serializer_fields, serializer_resource, nested_resource_instance, new_included_resources, included_cache)

                            if isinstance(field, Serializer):
                                relation_type = utils.get_resource_type_from_serializer(field)
                                serializer_fields = utils.get_serializer_fields(field)
                                if serializer_data:
                                    new_item = cls.build_json_resource_obj(serializer_fields, serializer_data, relation_instance, relation_type, getattr(field, '_poly_force_type_resolution', False))
                                    included_cache[new_item['type']][new_item['id']] = utils.format_field_names(new_item)
                                    cls.extract_included(serializer_fields, serializer_data, relation_instance, new_included_resources, included_cache)

    @classmethod
    def extract_meta(cls, serializer, resource):
        """
        Gathers the data from serializer fields specified in meta_fields and adds it to
        the meta object.
        """
        if hasattr(serializer, 'child'):
            meta = getattr(serializer.child, 'Meta', None)
        else:
            meta = getattr(serializer, 'Meta', None)
        meta_fields = getattr(meta, 'meta_fields', [])
        data = OrderedDict()
        for field_name in meta_fields:
            data.update({field_name: resource.get(field_name)})

        return data

    @classmethod
    def extract_root_meta(cls, serializer, resource):
        """
        Calls a `get_root_meta` function on a serializer, if it exists.
        """
        many = False
        if hasattr(serializer, 'child'):
            many = True
            serializer = serializer.child
        data = {}
        if getattr(serializer, 'get_root_meta', None):
            json_api_meta = serializer.get_root_meta(resource, many)
            assert isinstance(json_api_meta, dict), 'get_root_meta must return a dict'
            data.update(json_api_meta)
        return data

    @classmethod
    def build_json_resource_obj(cls, fields, resource, resource_instance, resource_name, force_type_resolution=False):
        """
        Builds the resource object (type, id, attributes) and extracts relationships.
        """
        if force_type_resolution:
            resource_name = utils.get_resource_type_from_instance(resource_instance)
        resource_data = [('type', resource_name),
         (
          'id', encoding.force_str(resource_instance.pk) if resource_instance else None),
         (
          'attributes', cls.extract_attributes(fields, resource))]
        relationships = cls.extract_relationships(fields, resource, resource_instance)
        if relationships:
            resource_data.append(('relationships', relationships))
        if api_settings.URL_FIELD_NAME in resource and isinstance(fields[api_settings.URL_FIELD_NAME], relations.RelatedField):
            resource_data.append(('links', {'self': resource[api_settings.URL_FIELD_NAME]}))
        return OrderedDict(resource_data)

    def render_relationship_view(self, data, accepted_media_type=None, renderer_context=None):
        view = renderer_context.get('view', None)
        render_data = OrderedDict([
         (
          'data', data)])
        links = view.get_links()
        if links:
            (
             render_data.update({'links': links}),)
        return super(JSONRenderer, self).render(render_data, accepted_media_type, renderer_context)

    def render_errors(self, data, accepted_media_type=None, renderer_context=None):
        return super(JSONRenderer, self).render(utils.format_errors(data), accepted_media_type, renderer_context)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        view = renderer_context.get('view', None)
        request = renderer_context.get('request', None)
        resource_name = utils.get_resource_name(renderer_context)
        if resource_name == 'errors':
            return self.render_errors(data, accepted_media_type, renderer_context)
        response = renderer_context.get('response', None)
        if response is not None and response.status_code == 204:
            return super(JSONRenderer, self).render(None, accepted_media_type, renderer_context)
        from rest_framework_json_api.views import RelationshipView
        if isinstance(view, RelationshipView):
            return self.render_relationship_view(data, accepted_media_type, renderer_context)
        if resource_name is None or resource_name is False:
            return super(JSONRenderer, self).render(data, accepted_media_type, renderer_context)
        json_api_data = data
        json_api_meta = data.get('meta', {}) if isinstance(data, dict) else {}
        included_cache = defaultdict(dict)
        if data and 'results' in data:
            serializer_data = data['results']
        else:
            serializer_data = data
        serializer = getattr(serializer_data, 'serializer', None)
        included_resources = utils.get_included_resources(request, serializer)
        if serializer is not None:
            json_api_meta.update(self.extract_root_meta(serializer, serializer_data))
            if getattr(serializer, 'many', False):
                json_api_data = list()
                for position in range(len(serializer_data)):
                    resource = serializer_data[position]
                    resource_instance = serializer.instance[position]
                    if isinstance(serializer.child, rest_framework_json_api.serializers.PolymorphicModelSerializer):
                        resource_serializer_class = serializer.child.get_polymorphic_serializer_for_instance(resource_instance)(context=serializer.child.context)
                    else:
                        resource_serializer_class = serializer.child
                    fields = utils.get_serializer_fields(resource_serializer_class)
                    force_type_resolution = getattr(resource_serializer_class, '_poly_force_type_resolution', False)
                    json_resource_obj = self.build_json_resource_obj(fields, resource, resource_instance, resource_name, force_type_resolution)
                    meta = self.extract_meta(serializer, resource)
                    if meta:
                        json_resource_obj.update({'meta': utils.format_field_names(meta)})
                    json_api_data.append(json_resource_obj)
                    self.extract_included(fields, resource, resource_instance, included_resources, included_cache)

            else:
                fields = utils.get_serializer_fields(serializer)
                force_type_resolution = getattr(serializer, '_poly_force_type_resolution', False)
                resource_instance = serializer.instance
                json_api_data = self.build_json_resource_obj(fields, serializer_data, resource_instance, resource_name, force_type_resolution)
                meta = self.extract_meta(serializer, serializer_data)
                if meta:
                    json_api_data.update({'meta': utils.format_field_names(meta)})
                self.extract_included(fields, serializer_data, resource_instance, included_resources, included_cache)
            render_data = OrderedDict()
            if isinstance(data, dict) and data.get('links'):
                render_data['links'] = data.get('links')
            if view.__class__ and view.__class__.__name__ == 'APIRoot':
                render_data['data'] = None
                render_data['links'] = json_api_data
        else:
            render_data['data'] = json_api_data
        if included_cache:
            if isinstance(json_api_data, list):
                objects = json_api_data
            else:
                objects = [
                 json_api_data]
            for object in objects:
                obj_type = object.get('type')
                obj_id = object.get('id')
                if obj_type in included_cache and obj_id in included_cache[obj_type]:
                    del included_cache[obj_type][obj_id]
                if not included_cache[obj_type]:
                    del included_cache[obj_type]

        if included_cache:
            render_data['included'] = list()
            for included_type in sorted(included_cache.keys()):
                for included_id in sorted(included_cache[included_type].keys()):
                    render_data['included'].append(included_cache[included_type][included_id])

        if json_api_meta:
            render_data['meta'] = utils.format_field_names(json_api_meta)
        return super(JSONRenderer, self).render(render_data, accepted_media_type, renderer_context)