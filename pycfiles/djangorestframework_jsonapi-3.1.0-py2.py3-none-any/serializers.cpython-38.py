# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sao/src/github/django-json-api/django-rest-framework-json-api/rest_framework_json_api/serializers.py
# Compiled at: 2019-12-13 14:45:13
# Size of source mod 2**32: 15311 bytes
import inflection
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
import django.utils.translation as _
from rest_framework.exceptions import ParseError
from rest_framework.serializers import *
from rest_framework_json_api.exceptions import Conflict
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework_json_api.utils import get_included_resources, get_included_serializers, get_resource_type_from_instance, get_resource_type_from_model, get_resource_type_from_serializer

class ResourceIdentifierObjectSerializer(BaseSerializer):
    default_error_messages = {'incorrect_model_type':_('Incorrect model type. Expected {model_type}, received {received_type}.'), 
     'does_not_exist':_('Invalid pk "{pk_value}" - object does not exist.'), 
     'incorrect_type':_('Incorrect type. Expected pk value, received {data_type}.')}
    model_class = None

    def __init__(self, *args, **kwargs):
        self.model_class = kwargs.pop('model_class', self.model_class)
        self.fields = {}
        (super(ResourceIdentifierObjectSerializer, self).__init__)(*args, **kwargs)

    def to_representation(self, instance):
        return {'type':get_resource_type_from_instance(instance), 
         'id':str(instance.pk)}

    def to_internal_value--- This code section failed: ---

 L.  43         0  LOAD_FAST                'data'
                2  LOAD_STR                 'type'
                4  BINARY_SUBSCR    
                6  LOAD_GLOBAL              get_resource_type_from_model
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                model_class
               12  CALL_FUNCTION_1       1  ''
               14  COMPARE_OP               !=
               16  POP_JUMP_IF_FALSE    40  'to 40'

 L.  44        18  LOAD_FAST                'self'
               20  LOAD_ATTR                fail

 L.  45        22  LOAD_STR                 'incorrect_model_type'

 L.  45        24  LOAD_FAST                'self'
               26  LOAD_ATTR                model_class

 L.  45        28  LOAD_FAST                'data'
               30  LOAD_STR                 'type'
               32  BINARY_SUBSCR    

 L.  44        34  LOAD_CONST               ('model_type', 'received_type')
               36  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               38  POP_TOP          
             40_0  COME_FROM            16  '16'

 L.  47        40  LOAD_FAST                'data'
               42  LOAD_STR                 'id'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'pk'

 L.  48        48  SETUP_FINALLY        68  'to 68'

 L.  49        50  LOAD_FAST                'self'
               52  LOAD_ATTR                model_class
               54  LOAD_ATTR                objects
               56  LOAD_ATTR                get
               58  LOAD_FAST                'pk'
               60  LOAD_CONST               ('pk',)
               62  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               64  POP_BLOCK        
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY    48  '48'

 L.  50        68  DUP_TOP          
               70  LOAD_GLOBAL              ObjectDoesNotExist
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   100  'to 100'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L.  51        82  LOAD_FAST                'self'
               84  LOAD_ATTR                fail
               86  LOAD_STR                 'does_not_exist'
               88  LOAD_FAST                'pk'
               90  LOAD_CONST               ('pk_value',)
               92  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               94  POP_TOP          
               96  POP_EXCEPT       
               98  JUMP_FORWARD        148  'to 148'
            100_0  COME_FROM            74  '74'

 L.  52       100  DUP_TOP          
              102  LOAD_GLOBAL              TypeError
              104  LOAD_GLOBAL              ValueError
              106  BUILD_TUPLE_2         2 
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   146  'to 146'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L.  53       118  LOAD_FAST                'self'
              120  LOAD_ATTR                fail
              122  LOAD_STR                 'incorrect_type'
              124  LOAD_GLOBAL              type
              126  LOAD_FAST                'data'
              128  LOAD_STR                 'pk'
              130  BINARY_SUBSCR    
              132  CALL_FUNCTION_1       1  ''
              134  LOAD_ATTR                __name__
              136  LOAD_CONST               ('data_type',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              140  POP_TOP          
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           110  '110'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM            98  '98'

Parse error at or near `POP_TOP' instruction at offset 78


class SparseFieldsetsMixin(object):

    def __init__(self, *args, **kwargs):
        (super(SparseFieldsetsMixin, self).__init__)(*args, **kwargs)
        context = kwargs.get('context')
        request = context.get('request') if context else None
        if request:
            sparse_fieldset_query_param = 'fields[{}]'.format(get_resource_type_from_serializer(self))
            try:
                param_name = next((key for key in request.query_params if sparse_fieldset_query_param in key))
            except StopIteration:
                pass
            else:
                fieldset = request.query_params.get(param_name).split(',')
            for field_name, field in self.fields.fields.copy().items():
                if field_name == api_settings.URL_FIELD_NAME:
                    pass
                elif field_name not in fieldset:
                    self.fields.pop(field_name)


class IncludedResourcesValidationMixin(object):

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context')
        request = context.get('request') if context else None
        view = context.get('view') if context else None

        def validate_path(serializer_class, field_path, path):
            serializers = get_included_serializers(serializer_class)
            if serializers is None:
                raise ParseError('This endpoint does not support the include parameter')
            this_field_name = inflection.underscore(field_path[0])
            this_included_serializer = serializers.get(this_field_name)
            if this_included_serializer is None:
                raise ParseError('This endpoint does not support the include parameter for path {}'.format(path))
            if len(field_path) > 1:
                new_included_field_path = field_path[1:]
                validate_path(this_included_serializer, new_included_field_path, path)

        if request:
            if view:
                included_resources = get_included_resources(request)
                for included_field_name in included_resources:
                    included_field_path = included_field_name.split('.')
                    this_serializer_class = view.get_serializer_class()
                    validate_path(this_serializer_class, included_field_path, included_field_name)

        (super(IncludedResourcesValidationMixin, self).__init__)(*args, **kwargs)


class HyperlinkedModelSerializer(IncludedResourcesValidationMixin, SparseFieldsetsMixin, HyperlinkedModelSerializer):
    __doc__ = "\n    A type of `ModelSerializer` that uses hyperlinked relationships instead\n    of primary key relationships. Specifically:\n\n    * A 'url' field is included instead of the 'id' field.\n    * Relationships to other instances are hyperlinks, instead of primary keys.\n\n    Included Mixins:\n\n    * A mixin class to enable sparse fieldsets is included\n    * A mixin class to enable validation of included resources is included\n    "


class ModelSerializer(IncludedResourcesValidationMixin, SparseFieldsetsMixin, ModelSerializer):
    __doc__ = "\n    A `ModelSerializer` is just a regular `Serializer`, except that:\n\n    * A set of default fields are automatically populated.\n    * A set of default validators are automatically populated.\n    * Default `.create()` and `.update()` implementations are provided.\n\n    The process of automatically determining a set of serializer fields\n    based on the model fields is reasonably complex, but you almost certainly\n    don't need to dig into the implementation.\n\n    If the `ModelSerializer` class *doesn't* generate the set of fields that\n    you need you should either declare the extra/differing fields explicitly on\n    the serializer class, or simply use a `Serializer` class.\n\n\n    Included Mixins:\n\n    * A mixin class to enable sparse fieldsets is included\n    * A mixin class to enable validation of included resources is included\n    "
    serializer_related_field = ResourceRelatedField

    def get_field_names(self, declared_fields, info):
        meta_fields = getattr(self.Meta, 'meta_fields', [])
        declared = OrderedDict()
        for field_name in set(declared_fields.keys()):
            field = declared_fields[field_name]
            if field_name not in meta_fields:
                declared[field_name] = field
            fields = super(ModelSerializer, self).get_field_names(declared, info)
            return list(fields) + list(getattr(self.Meta, 'meta_fields', list()))

    def to_representation--- This code section failed: ---

 L. 178         0  LOAD_GLOBAL              OrderedDict
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'ret'

 L. 179         6  LOAD_LISTCOMP            '<code_object <listcomp>>'
                8  LOAD_STR                 'ModelSerializer.to_representation.<locals>.<listcomp>'
               10  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 180        12  LOAD_FAST                'self'
               14  LOAD_ATTR                fields
               16  LOAD_METHOD              values
               18  CALL_METHOD_0         0  ''

 L. 179        20  GET_ITER         
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'readable_fields'

 L. 184        26  LOAD_FAST                'readable_fields'
               28  GET_ITER         
               30  FOR_ITER             88  'to 88'
               32  STORE_FAST               'field'

 L. 185        34  SETUP_FINALLY        62  'to 62'

 L. 186        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _get_field_representation
               40  LOAD_FAST                'field'
               42  LOAD_FAST                'instance'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'field_representation'

 L. 187        48  LOAD_FAST                'field_representation'
               50  LOAD_FAST                'ret'
               52  LOAD_FAST                'field'
               54  LOAD_ATTR                field_name
               56  STORE_SUBSCR     
               58  POP_BLOCK        
               60  JUMP_BACK            30  'to 30'
             62_0  COME_FROM_FINALLY    34  '34'

 L. 188        62  DUP_TOP          
               64  LOAD_GLOBAL              SkipField
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    84  'to 84'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 189        76  POP_EXCEPT       
               78  JUMP_BACK            30  'to 30'
               80  POP_EXCEPT       
               82  JUMP_BACK            30  'to 30'
             84_0  COME_FROM            68  '68'
               84  END_FINALLY      
               86  JUMP_BACK            30  'to 30'

 L. 191        88  LOAD_FAST                'ret'
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 80

    def _get_field_representation(self, field, instance):
        request = self.context.get('request')
        is_included = field.source in get_included_resources(request)
        if not is_included:
            if isinstance(field, ModelSerializer):
                if hasattr(instance, field.source + '_id'):
                    attribute = getattr(instance, field.source + '_id')
                    if attribute is None:
                        return
                    resource_type = get_resource_type_from_serializer(field)
                    if resource_type:
                        return OrderedDict([('type', resource_type), ('id', attribute)])
        attribute = field.get_attribute(instance)
        check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
        if check_for_none is None:
            return
        return field.to_representation(attribute)


class PolymorphicSerializerMetaclass(SerializerMetaclass):
    __doc__ = '\n    This metaclass ensures that the `polymorphic_serializers` is correctly defined on a\n    `PolymorphicSerializer` class and make a cache of model/serializer/type mappings.\n    '

    def __new__(cls, name, bases, attrs):
        new_class = super(PolymorphicSerializerMetaclass, cls).__new__(cls, name, bases, attrs)
        parents = [b for b in bases if isinstance(b, PolymorphicSerializerMetaclass)]
        if not parents:
            return new_class
        polymorphic_serializers = getattr(new_class, 'polymorphic_serializers', None)
        if not polymorphic_serializers:
            raise NotImplementedError('A PolymorphicModelSerializer must define a `polymorphic_serializers` attribute.')
        serializer_to_model = {serializer.Meta.model:serializer for serializer in polymorphic_serializers}
        model_to_serializer = {serializer:serializer.Meta.model for serializer in polymorphic_serializers}
        type_to_serializer = {serializer:get_resource_type_from_serializer(serializer) for serializer in polymorphic_serializers}
        new_class._poly_serializer_model_map = serializer_to_model
        new_class._poly_model_serializer_map = model_to_serializer
        new_class._poly_type_serializer_map = type_to_serializer
        new_class._poly_force_type_resolution = True
        for serializer in polymorphic_serializers:
            serializer._poly_force_type_resolution = True
        else:
            return new_class


class PolymorphicModelSerializer(ModelSerializer, metaclass=PolymorphicSerializerMetaclass):
    __doc__ = '\n    A serializer for polymorphic models.\n    Useful for "lazy" parent models. Leaves should be represented with a regular serializer.\n    '

    def get_fields(self):
        if self.instance not in (None, []):
            if not isinstance(self.instance, QuerySet):
                serializer_class = self.get_polymorphic_serializer_for_instance(self.instance)
                return serializer_class((self.instance), context=(self.context)).get_fields()
            raise Exception('Cannot get fields from a polymorphic serializer given a queryset')
        return super(PolymorphicModelSerializer, self).get_fields()

    @classmethod
    def get_polymorphic_serializer_for_instance--- This code section failed: ---

 L. 284         0  SETUP_FINALLY        18  'to 18'

 L. 285         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                _poly_model_serializer_map
                6  LOAD_FAST                'instance'
                8  LOAD_ATTR                _meta
               10  LOAD_ATTR                model
               12  BINARY_SUBSCR    
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 286        18  DUP_TOP          
               20  LOAD_GLOBAL              KeyError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    56  'to 56'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 287        32  LOAD_GLOBAL              NotImplementedError

 L. 288        34  LOAD_STR                 'No polymorphic serializer has been found for model {}'
               36  LOAD_METHOD              format

 L. 289        38  LOAD_FAST                'instance'
               40  LOAD_ATTR                _meta
               42  LOAD_ATTR                model
               44  LOAD_ATTR                __name__

 L. 288        46  CALL_METHOD_1         1  ''

 L. 287        48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            24  '24'
               56  END_FINALLY      
             58_0  COME_FROM            54  '54'

Parse error at or near `POP_TOP' instruction at offset 28

    @classmethod
    def get_polymorphic_model_for_serializer--- This code section failed: ---

 L. 298         0  SETUP_FINALLY        14  'to 14'

 L. 299         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                _poly_serializer_model_map
                6  LOAD_FAST                'serializer'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 300        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    48  'to 48'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 301        28  LOAD_GLOBAL              NotImplementedError

 L. 302        30  LOAD_STR                 'No polymorphic model has been found for serializer {}'
               32  LOAD_METHOD              format
               34  LOAD_FAST                'serializer'
               36  LOAD_ATTR                __name__
               38  CALL_METHOD_1         1  ''

 L. 301        40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            20  '20'
               48  END_FINALLY      
             50_0  COME_FROM            46  '46'

Parse error at or near `POP_TOP' instruction at offset 24

    @classmethod
    def get_polymorphic_serializer_for_type--- This code section failed: ---

 L. 311         0  SETUP_FINALLY        14  'to 14'

 L. 312         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                _poly_type_serializer_map
                6  LOAD_FAST                'obj_type'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 313        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    46  'to 46'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 314        28  LOAD_GLOBAL              NotImplementedError

 L. 315        30  LOAD_STR                 'No polymorphic serializer has been found for type {}'
               32  LOAD_METHOD              format
               34  LOAD_FAST                'obj_type'
               36  CALL_METHOD_1         1  ''

 L. 314        38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
               42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
             46_0  COME_FROM            20  '20'
               46  END_FINALLY      
             48_0  COME_FROM            44  '44'

Parse error at or near `POP_TOP' instruction at offset 24

    @classmethod
    def get_polymorphic_model_for_type(cls, obj_type):
        """
        Return the polymorphic model associated with the given type.
        Raise `NotImplementedError` if no model is found for the given type. This usually
        means that a serializer is missing in the class's `polymorphic_serializers` attribute.
        """
        return cls.get_polymorphic_model_for_serializer(cls.get_polymorphic_serializer_for_type(obj_type))

    @classmethod
    def get_polymorphic_types(cls):
        """
        Return the list of accepted types.
        """
        return cls._poly_type_serializer_map.keys()

    def to_representation(self, instance):
        """
        Retrieve the appropriate polymorphic serializer and use this to handle representation.
        """
        serializer_class = self.get_polymorphic_serializer_for_instance(instance)
        return serializer_class(instance, context=(self.context)).to_representation(instance)

    def to_internal_value(self, data):
        """
        Ensure that the given type is one of the expected polymorphic types, then retrieve the
        appropriate polymorphic serializer and use this to handle internal value.
        """
        received_type = data.get('type')
        expected_types = self.get_polymorphic_types()
        if received_type not in expected_types:
            raise Conflict('Incorrect relation type. Expected on of [{expected_types}], received {received_type}.'.format(expected_types=(', '.join(expected_types)),
              received_type=received_type))
        serializer_class = self.get_polymorphic_serializer_for_type(received_type)
        self.__class__ = serializer_class
        return serializer_class(data, context=(self.context), partial=(self.partial)).to_internal_value(data)