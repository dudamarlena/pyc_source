# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sao/src/github/django-json-api/django-rest-framework-json-api/rest_framework_json_api/views.py
# Compiled at: 2019-10-10 12:50:33
# Size of source mod 2**32: 15673 bytes
from collections.abc import Iterable
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor, ManyToManyDescriptor, ReverseManyToOneDescriptor, ReverseOneToOneDescriptor
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.urls import NoReverseMatch
import django.utils.module_loading as import_class_from_dotted_path
from rest_framework import generics, viewsets
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.fields import get_attribute
from rest_framework.relations import PKOnlyObject
from rest_framework.response import Response
import rest_framework.reverse as reverse
from rest_framework.serializers import Serializer, SkipField
from rest_framework_json_api.exceptions import Conflict
from rest_framework_json_api.serializers import ResourceIdentifierObjectSerializer
from rest_framework_json_api.utils import Hyperlink, OrderedDict, get_included_resources, get_resource_type_from_instance

class PreloadIncludesMixin(object):
    __doc__ = "\n    This mixin provides a helper attributes to select or prefetch related models\n    based on the include specified in the URL.\n\n    __all__ can be used to specify a prefetch which should be done regardless of the include\n\n\n    .. code:: python\n\n        # When MyViewSet is called with ?include=author it will prefetch author and authorbio\n        class MyViewSet(viewsets.ModelViewSet):\n            queryset = Book.objects.all()\n            prefetch_for_includes = {\n                '__all__': [],\n                'category.section': ['category']\n            }\n            select_for_includes = {\n                '__all__': [],\n                'author': ['author', 'author__authorbio'],\n            }\n    "

    def get_select_related(self, include):
        return getattr(self, 'select_for_includes', {}).get(include, None)

    def get_prefetch_related(self, include):
        return getattr(self, 'prefetch_for_includes', {}).get(include, None)

    def get_queryset(self, *args, **kwargs):
        qs = (super(PreloadIncludesMixin, self).get_queryset)(*args, **kwargs)
        included_resources = get_included_resources(self.request)
        for included in included_resources + ['__all__']:
            select_related = self.get_select_related(included)
            if select_related is not None:
                qs = (qs.select_related)(*select_related)
            prefetch_related = self.get_prefetch_related(included)
            if prefetch_related is not None:
                qs = (qs.prefetch_related)(*prefetch_related)
            return qs


class AutoPrefetchMixin(object):

    def get_queryset(self, *args, **kwargs):
        qs = (super(AutoPrefetchMixin, self).get_queryset)(*args, **kwargs)
        included_resources = get_included_resources(self.request)
        for included in included_resources + ['__all__']:
            included_model = None
            levels = included.split('.')
            level_model = qs.model

        for level in levels:
            if not hasattr(level_model, level):
                break
            field = getattr(level_model, level)
            field_class = field.__class__
            is_forward_relation = issubclass(field_class, (ForwardManyToOneDescriptor, ManyToManyDescriptor))
            is_reverse_relation = issubclass(field_class, (ReverseManyToOneDescriptor, ReverseOneToOneDescriptor))
            if not is_forward_relation:
                if not is_reverse_relation:
                    break
                else:
                    if level == levels[(-1)]:
                        included_model = field
                if issubclass(field_class, ReverseOneToOneDescriptor):
                    model_field = field.related.field
                else:
                    model_field = field.field
                if is_forward_relation:
                    level_model = model_field.related_model
                else:
                    level_model = model_field.model
            if included_model is not None:
                qs = qs.prefetch_related(included.replace('.', '__'))
            return qs


class RelatedMixin(object):
    __doc__ = '\n    This mixin handles all related entities, whose Serializers are declared in "related_serializers"\n    '

    def retrieve_related(self, request, *args, **kwargs):
        serializer_kwargs = {}
        instance = self.get_related_instance()
        if hasattr(instance, 'all'):
            instance = instance.all()
        if callable(instance):
            instance = instance()
        if instance is None:
            return Response(data=None)
        if isinstance(instance, Iterable):
            serializer_kwargs['many'] = True
        serializer = (self.get_serializer)(instance, **serializer_kwargs)
        return Response(serializer.data)

    def get_serializer_class(self):
        parent_serializer_class = super(RelatedMixin, self).get_serializer_class()
        if 'related_field' in self.kwargs:
            field_name = self.kwargs['related_field']
            if hasattr(parent_serializer_class, 'related_serializers'):
                _class = parent_serializer_class.related_serializers.get(field_name, None)
                if _class is None:
                    raise NotFound
            elif hasattr(parent_serializer_class, 'included_serializers'):
                _class = parent_serializer_class.included_serializers.get(field_name, None)
                if _class is None:
                    raise NotFound
            elif not False:
                raise AssertionError('Either "included_serializers" or "related_serializers" should be configured')
            if not isinstance(_class, type):
                return import_class_from_dotted_path(_class)
            return _class
        return parent_serializer_class

    def get_related_field_name(self):
        return self.kwargs['related_field']

    def get_related_instance--- This code section failed: ---

 L. 181         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_object
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'parent_obj'

 L. 182         8  LOAD_FAST                'self'
               10  LOAD_METHOD              serializer_class
               12  LOAD_FAST                'parent_obj'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'parent_serializer'

 L. 183        18  LOAD_FAST                'self'
               20  LOAD_METHOD              get_related_field_name
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'field_name'

 L. 184        26  LOAD_FAST                'parent_serializer'
               28  LOAD_ATTR                fields
               30  LOAD_METHOD              get
               32  LOAD_FAST                'field_name'
               34  LOAD_CONST               None
               36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'field'

 L. 186        40  LOAD_FAST                'field'
               42  LOAD_CONST               None
               44  COMPARE_OP               is-not
               46  POP_JUMP_IF_FALSE   122  'to 122'

 L. 187        48  SETUP_FINALLY        64  'to 64'

 L. 188        50  LOAD_FAST                'field'
               52  LOAD_METHOD              get_attribute
               54  LOAD_FAST                'parent_obj'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'instance'
               60  POP_BLOCK        
               62  JUMP_FORWARD         96  'to 96'
             64_0  COME_FROM_FINALLY    48  '48'

 L. 189        64  DUP_TOP          
               66  LOAD_GLOBAL              SkipField
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE    94  'to 94'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 190        78  LOAD_GLOBAL              get_attribute
               80  LOAD_FAST                'parent_obj'
               82  LOAD_FAST                'field'
               84  LOAD_ATTR                source_attrs
               86  CALL_FUNCTION_2       2  ''
               88  STORE_FAST               'instance'
               90  POP_EXCEPT       
               92  JUMP_FORWARD        118  'to 118'
             94_0  COME_FROM            70  '70'
               94  END_FINALLY      
             96_0  COME_FROM            62  '62'

 L. 192        96  LOAD_GLOBAL              isinstance
               98  LOAD_FAST                'instance'
              100  LOAD_GLOBAL              PKOnlyObject
              102  CALL_FUNCTION_2       2  ''
              104  POP_JUMP_IF_FALSE   118  'to 118'

 L. 194       106  LOAD_GLOBAL              get_attribute
              108  LOAD_FAST                'parent_obj'
              110  LOAD_FAST                'field'
              112  LOAD_ATTR                source_attrs
              114  CALL_FUNCTION_2       2  ''
              116  STORE_FAST               'instance'
            118_0  COME_FROM           104  '104'
            118_1  COME_FROM            92  '92'

 L. 195       118  LOAD_FAST                'instance'
              120  RETURN_VALUE     
            122_0  COME_FROM            46  '46'

 L. 197       122  SETUP_FINALLY       136  'to 136'

 L. 198       124  LOAD_GLOBAL              getattr
              126  LOAD_FAST                'parent_obj'
              128  LOAD_FAST                'field_name'
              130  CALL_FUNCTION_2       2  ''
              132  POP_BLOCK        
              134  RETURN_VALUE     
            136_0  COME_FROM_FINALLY   122  '122'

 L. 199       136  DUP_TOP          
              138  LOAD_GLOBAL              AttributeError
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   158  'to 158'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 200       150  LOAD_GLOBAL              NotFound
              152  RAISE_VARARGS_1       1  'exception instance'
              154  POP_EXCEPT       
              156  JUMP_FORWARD        160  'to 160'
            158_0  COME_FROM           142  '142'
              158  END_FINALLY      
            160_0  COME_FROM           156  '156'

Parse error at or near `POP_TOP' instruction at offset 146


class ModelViewSet(AutoPrefetchMixin, PreloadIncludesMixin, RelatedMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class ReadOnlyModelViewSet(AutoPrefetchMixin, RelatedMixin, viewsets.ReadOnlyModelViewSet):
    http_method_names = ['get', 'head', 'options']


class RelationshipView(generics.GenericAPIView):
    serializer_class = ResourceIdentifierObjectSerializer
    self_link_view_name = None
    related_link_view_name = None
    field_name_mapping = {}
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if getattr(self, 'action', False) is None:
            return Serializer
        return self.serializer_class

    def __init__(self, **kwargs):
        (super(RelationshipView, self).__init__)(**kwargs)
        self.reverse = reverse

    def get_url(self, name, view_name, kwargs, request):
        """
        Given a name, view name and kwargs, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        if not view_name:
            return
        try:
            url = self.reverse(view_name, kwargs=kwargs, request=request)
        except NoReverseMatch:
            msg = 'Could not resolve URL for hyperlinked relationship using view name "%s". You may have failed to include the related model in your API, or incorrectly configured the `lookup_field` attribute on this field.'
            raise ImproperlyConfigured(msg % view_name)
        else:
            if url is None:
                return
            return Hyperlink(url, name)

    def get_links(self):
        return_data = OrderedDict()
        self_link = self.get_url('self', self.self_link_view_name, self.kwargs, self.request)
        related_kwargs = {self.lookup_field: self.kwargs.get(self.lookup_field)}
        related_link = self.get_url('related', self.related_link_view_name, related_kwargs, self.request)
        if self_link:
            return_data.update({'self': self_link})
        if related_link:
            return_data.update({'related': related_link})
        return return_data

    def get(self, request, *args, **kwargs):
        related_instance = self.get_related_instance()
        serializer_instance = self._instantiate_serializer(related_instance)
        return Response(serializer_instance.data)

    def remove_relationships(self, instance_manager, field):
        field_object = getattr(instance_manager, field)
        if field_object.null:
            for obj in instance_manager.all():
                setattr(obj, field_object.name, None)
                obj.save()

        else:
            instance_manager.all().delete()
        return instance_manager

    def patch(self, request, *args, **kwargs):
        parent_obj = self.get_object()
        related_instance_or_manager = self.get_related_instance()
        if isinstance(related_instance_or_manager, Manager):
            related_model_class = related_instance_or_manager.model
            serializer = self.get_serializer(data=(request.data),
              model_class=related_model_class,
              many=True)
            serializer.is_valid(raise_exception=True)
            if hasattr(related_instance_or_manager, 'field'):
                related_instance_or_manager = self.remove_relationships(instance_manager=related_instance_or_manager,
                  field='field')
            else:
                related_instance_or_manager = self.remove_relationships(instance_manager=related_instance_or_manager,
                  field='target_field')
            class_name = related_instance_or_manager.__class__.__name__
            if class_name != 'ManyRelatedManager':
                (related_instance_or_manager.add)(*serializer.validated_data, **{'bulk': False})
            else:
                (related_instance_or_manager.add)(*serializer.validated_data)
        else:
            related_model_class = related_instance_or_manager.__class__
            serializer = self.get_serializer(data=(request.data), model_class=related_model_class)
            serializer.is_valid(raise_exception=True)
            setattr(parent_obj, self.get_related_field_name(), serializer.validated_data)
            parent_obj.save()
            related_instance_or_manager = self.get_related_instance()
        result_serializer = self._instantiate_serializer(related_instance_or_manager)
        return Response(result_serializer.data)

    def post(self, request, *args, **kwargs):
        related_instance_or_manager = self.get_related_instance()
        if isinstance(related_instance_or_manager, Manager):
            related_model_class = related_instance_or_manager.model
            serializer = self.get_serializer(data=(request.data),
              model_class=related_model_class,
              many=True)
            serializer.is_valid(raise_exception=True)
            if frozenset(serializer.validated_data) <= frozenset(related_instance_or_manager.all()):
                return Response(status=204)
            (related_instance_or_manager.add)(*serializer.validated_data)
        else:
            raise MethodNotAllowed('POST')
        result_serializer = self._instantiate_serializer(related_instance_or_manager)
        return Response(result_serializer.data)

    def delete(self, request, *args, **kwargs):
        related_instance_or_manager = self.get_related_instance()
        if isinstance(related_instance_or_manager, Manager):
            related_model_class = related_instance_or_manager.model
            serializer = self.get_serializer(data=(request.data),
              model_class=related_model_class,
              many=True)
            serializer.is_valid(raise_exception=True)
            objects = related_instance_or_manager.all()
            if frozenset(serializer.validated_data).isdisjoint(frozenset(objects)):
                return Response(status=204)
            try:
                (related_instance_or_manager.remove)(*serializer.validated_data)
            except AttributeError:
                raise Conflict('This object cannot be removed from this relationship without being added to another')

        else:
            raise MethodNotAllowed('DELETE')
        result_serializer = self._instantiate_serializer(related_instance_or_manager)
        return Response(result_serializer.data)

    def get_related_instance--- This code section failed: ---

 L. 372         0  SETUP_FINALLY        22  'to 22'

 L. 373         2  LOAD_GLOBAL              getattr
                4  LOAD_FAST                'self'
                6  LOAD_METHOD              get_object
                8  CALL_METHOD_0         0  ''
               10  LOAD_FAST                'self'
               12  LOAD_METHOD              get_related_field_name
               14  CALL_METHOD_0         0  ''
               16  CALL_FUNCTION_2       2  ''
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L. 374        22  DUP_TOP          
               24  LOAD_GLOBAL              AttributeError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    44  'to 44'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 375        36  LOAD_GLOBAL              NotFound
               38  RAISE_VARARGS_1       1  'exception instance'
               40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            28  '28'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

Parse error at or near `POP_TOP' instruction at offset 32

    def get_related_field_name(self):
        field_name = self.kwargs['related_field']
        if field_name in self.field_name_mapping:
            return self.field_name_mapping[field_name]
        return field_name

    def _instantiate_serializer(self, instance):
        if isinstance(instance, Model) or instance is None:
            return self.get_serializer(instance=instance)
        if isinstance(instance, (QuerySet, Manager)):
            instance = instance.all()
        return self.get_serializer(instance=instance, many=True)

    def get_resource_name(self):
        if not hasattr(self, '_resource_name'):
            instance = getattr(self.get_object(), self.get_related_field_name())
            self._resource_name = get_resource_type_from_instance(instance)
        return self._resource_name

    def set_resource_name(self, value):
        self._resource_name = value

    resource_name = property(get_resource_name, set_resource_name)