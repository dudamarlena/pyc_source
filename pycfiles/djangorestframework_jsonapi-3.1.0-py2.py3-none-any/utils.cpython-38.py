# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sao/src/github/django-json-api/django-rest-framework-json-api/rest_framework_json_api/utils.py
# Compiled at: 2019-12-13 14:54:36
# Size of source mod 2**32: 13171 bytes
import copy, inspect, operator
from collections import OrderedDict
import inflection
from django.conf import settings
from django.db.models import Manager
from django.db.models.fields.related_descriptors import ManyToManyDescriptor, ReverseManyToOneDescriptor
from django.http import Http404
from django.utils import encoding
import django.utils.module_loading as import_class_from_dotted_path
import django.utils.translation as _
from rest_framework import exceptions
from rest_framework.exceptions import APIException
from .settings import json_api_settings
if 'django.contrib.contenttypes' not in settings.INSTALLED_APPS:
    ReverseGenericManyToOneDescriptor = object()
else:
    from django.contrib.contenttypes.fields import ReverseGenericManyToOneDescriptor

def get_resource_name--- This code section failed: ---

 L.  34         0  LOAD_CONST               0
                2  LOAD_CONST               ('PolymorphicModelSerializer',)
                4  IMPORT_NAME_ATTR         rest_framework_json_api.serializers
                6  IMPORT_FROM              PolymorphicModelSerializer
                8  STORE_FAST               'PolymorphicModelSerializer'
               10  POP_TOP          

 L.  35        12  LOAD_FAST                'context'
               14  LOAD_METHOD              get
               16  LOAD_STR                 'view'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'view'

 L.  38        22  LOAD_FAST                'view'
               24  POP_JUMP_IF_TRUE     30  'to 30'

 L.  39        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L.  43        30  SETUP_FINALLY        48  'to 48'

 L.  44        32  LOAD_GLOBAL              str
               34  LOAD_FAST                'view'
               36  LOAD_ATTR                response
               38  LOAD_ATTR                status_code
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'code'
               44  POP_BLOCK        
               46  JUMP_FORWARD         72  'to 72'
             48_0  COME_FROM_FINALLY    30  '30'

 L.  45        48  DUP_TOP          
               50  LOAD_GLOBAL              AttributeError
               52  LOAD_GLOBAL              ValueError
               54  BUILD_TUPLE_2         2 
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    70  'to 70'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  46        66  POP_EXCEPT       
               68  JUMP_FORWARD         96  'to 96'
             70_0  COME_FROM            58  '58'
               70  END_FINALLY      
             72_0  COME_FROM            46  '46'

 L.  48        72  LOAD_FAST                'code'
               74  LOAD_METHOD              startswith
               76  LOAD_STR                 '4'
               78  CALL_METHOD_1         1  ''
               80  POP_JUMP_IF_TRUE     92  'to 92'
               82  LOAD_FAST                'code'
               84  LOAD_METHOD              startswith
               86  LOAD_STR                 '5'
               88  CALL_METHOD_1         1  ''
               90  POP_JUMP_IF_FALSE    96  'to 96'
             92_0  COME_FROM            80  '80'

 L.  49        92  LOAD_STR                 'errors'
               94  RETURN_VALUE     
             96_0  COME_FROM            90  '90'
             96_1  COME_FROM            68  '68'

 L.  51        96  SETUP_FINALLY       112  'to 112'

 L.  52        98  LOAD_GLOBAL              getattr
              100  LOAD_FAST                'view'
              102  LOAD_STR                 'resource_name'
              104  CALL_FUNCTION_2       2  ''
              106  STORE_FAST               'resource_name'
              108  POP_BLOCK        
              110  JUMP_FORWARD        288  'to 288'
            112_0  COME_FROM_FINALLY    96  '96'

 L.  53       112  DUP_TOP          
              114  LOAD_GLOBAL              AttributeError
              116  COMPARE_OP               exception-match
          118_120  POP_JUMP_IF_FALSE   286  'to 286'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L.  54       128  SETUP_FINALLY       184  'to 184'

 L.  55       130  LOAD_FAST                'view'
              132  LOAD_METHOD              get_serializer_class
              134  CALL_METHOD_0         0  ''
              136  STORE_FAST               'serializer'

 L.  56       138  LOAD_FAST                'expand_polymorphic_types'
              140  POP_JUMP_IF_FALSE   166  'to 166'
              142  LOAD_GLOBAL              issubclass
              144  LOAD_FAST                'serializer'
              146  LOAD_FAST                'PolymorphicModelSerializer'
              148  CALL_FUNCTION_2       2  ''
              150  POP_JUMP_IF_FALSE   166  'to 166'

 L.  57       152  LOAD_FAST                'serializer'
              154  LOAD_METHOD              get_polymorphic_types
              156  CALL_METHOD_0         0  ''
              158  POP_BLOCK        
              160  ROT_FOUR         
              162  POP_EXCEPT       
              164  RETURN_VALUE     
            166_0  COME_FROM           150  '150'
            166_1  COME_FROM           140  '140'

 L.  59       166  LOAD_GLOBAL              get_resource_type_from_serializer
              168  LOAD_FAST                'serializer'
              170  CALL_FUNCTION_1       1  ''
              172  POP_BLOCK        
              174  ROT_FOUR         
              176  POP_EXCEPT       
              178  RETURN_VALUE     
              180  POP_BLOCK        
              182  JUMP_FORWARD        282  'to 282'
            184_0  COME_FROM_FINALLY   128  '128'

 L.  60       184  DUP_TOP          
              186  LOAD_GLOBAL              AttributeError
              188  COMPARE_OP               exception-match
          190_192  POP_JUMP_IF_FALSE   280  'to 280'
              194  POP_TOP          
              196  POP_TOP          
              198  POP_TOP          

 L.  61       200  SETUP_FINALLY       216  'to 216'

 L.  62       202  LOAD_GLOBAL              get_resource_type_from_model
              204  LOAD_FAST                'view'
              206  LOAD_ATTR                model
              208  CALL_FUNCTION_1       1  ''
              210  STORE_FAST               'resource_name'
              212  POP_BLOCK        
              214  JUMP_FORWARD        244  'to 244'
            216_0  COME_FROM_FINALLY   200  '200'

 L.  63       216  DUP_TOP          
              218  LOAD_GLOBAL              AttributeError
              220  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   242  'to 242'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L.  64       230  LOAD_FAST                'view'
              232  LOAD_ATTR                __class__
              234  LOAD_ATTR                __name__
              236  STORE_FAST               'resource_name'
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           222  '222'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           214  '214'

 L.  66       244  LOAD_GLOBAL              isinstance
              246  LOAD_FAST                'resource_name'
              248  LOAD_GLOBAL              str
              250  CALL_FUNCTION_2       2  ''
          252_254  POP_JUMP_IF_TRUE    268  'to 268'

 L.  68       256  LOAD_FAST                'resource_name'
              258  ROT_FOUR         
              260  POP_EXCEPT       
              262  ROT_FOUR         
              264  POP_EXCEPT       
              266  RETURN_VALUE     
            268_0  COME_FROM           252  '252'

 L.  71       268  LOAD_GLOBAL              format_resource_type
              270  LOAD_FAST                'resource_name'
              272  CALL_FUNCTION_1       1  ''
              274  STORE_FAST               'resource_name'
              276  POP_EXCEPT       
              278  JUMP_FORWARD        282  'to 282'
            280_0  COME_FROM           190  '190'
              280  END_FINALLY      
            282_0  COME_FROM           278  '278'
            282_1  COME_FROM           182  '182'
              282  POP_EXCEPT       
              284  JUMP_FORWARD        288  'to 288'
            286_0  COME_FROM           118  '118'
              286  END_FINALLY      
            288_0  COME_FROM           284  '284'
            288_1  COME_FROM           110  '110'

 L.  73       288  LOAD_FAST                'resource_name'
              290  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 160


def get_serializer_fields(serializer):
    fields = None
    if hasattrserializer'child':
        fields = getattrserializer.child'fields'
        meta = getattr(serializer.child, 'Meta', None)
    if hasattrserializer'fields':
        fields = getattrserializer'fields'
        meta = getattr(serializer, 'Meta', None)
    if fields is not None:
        meta_fields = getattr(meta, 'meta_fields', {})
        for field in meta_fields:
            try:
                fields.popfield
            except KeyError:
                pass

        else:
            return fields


def format_field_names(obj, format_type=None):
    """
    Takes a dict and returns it with formatted keys as set in `format_type`
    or `JSON_API_FORMAT_FIELD_NAMES`

    :format_type: Either 'dasherize', 'camelize', 'capitalize' or 'underscore'
    """
    if format_type is None:
        format_type = json_api_settings.FORMAT_FIELD_NAMES
    if isinstanceobjdict:
        formatted = OrderedDict()
        for key, value in obj.items:
            key = format_valuekeyformat_type
            formatted[key] = value
        else:
            return formatted

    return obj


def format_value(value, format_type=None):
    if format_type is None:
        format_type = json_api_settings.FORMAT_FIELD_NAMES
    elif format_type == 'dasherize':
        value = inflection.underscorevalue
        value = inflection.dasherizevalue
    else:
        if format_type == 'camelize':
            value = inflection.camelize(value, False)
        else:
            if format_type == 'capitalize':
                value = inflection.camelizevalue
            else:
                if format_type == 'underscore':
                    value = inflection.underscorevalue
    return value


def format_resource_type(value, format_type=None, pluralize=None):
    if format_type is None:
        format_type = json_api_settings.FORMAT_TYPES
    if pluralize is None:
        pluralize = json_api_settings.PLURALIZE_TYPES
    if format_type:
        value = format_valuevalueformat_type
    if pluralize:
        return inflection.pluralizevalue
    return value


def get_related_resource_type--- This code section failed: ---

 L. 146         0  SETUP_FINALLY        12  'to 12'

 L. 147         2  LOAD_GLOBAL              get_resource_type_from_serializer
                4  LOAD_FAST                'relation'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 148        12  DUP_TOP          
               14  LOAD_GLOBAL              AttributeError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    30  'to 30'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 149        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            18  '18'
               30  END_FINALLY      
             32_0  COME_FROM            28  '28'

 L. 150        32  LOAD_CONST               None
               34  STORE_FAST               'relation_model'

 L. 151        36  LOAD_GLOBAL              hasattr
               38  LOAD_FAST                'relation'
               40  LOAD_STR                 '_meta'
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_FALSE    58  'to 58'

 L. 152        46  LOAD_FAST                'relation'
               48  LOAD_ATTR                _meta
               50  LOAD_ATTR                model
               52  STORE_FAST               'relation_model'
            54_56  JUMP_FORWARD        468  'to 468'
             58_0  COME_FROM            44  '44'

 L. 153        58  LOAD_GLOBAL              hasattr
               60  LOAD_FAST                'relation'
               62  LOAD_STR                 'model'
               64  CALL_FUNCTION_2       2  ''
               66  POP_JUMP_IF_FALSE    78  'to 78'

 L. 155        68  LOAD_FAST                'relation'
               70  LOAD_ATTR                model
               72  STORE_FAST               'relation_model'
            74_76  JUMP_FORWARD        468  'to 468'
             78_0  COME_FROM            66  '66'

 L. 156        78  LOAD_GLOBAL              hasattr
               80  LOAD_FAST                'relation'
               82  LOAD_STR                 'get_queryset'
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   114  'to 114'
               88  LOAD_FAST                'relation'
               90  LOAD_METHOD              get_queryset
               92  CALL_METHOD_0         0  ''
               94  LOAD_CONST               None
               96  COMPARE_OP               is-not
               98  POP_JUMP_IF_FALSE   114  'to 114'

 L. 157       100  LOAD_FAST                'relation'
              102  LOAD_METHOD              get_queryset
              104  CALL_METHOD_0         0  ''
              106  LOAD_ATTR                model
              108  STORE_FAST               'relation_model'
          110_112  JUMP_FORWARD        468  'to 468'
            114_0  COME_FROM            98  '98'
            114_1  COME_FROM            86  '86'

 L. 159       114  LOAD_GLOBAL              getattr
              116  LOAD_FAST                'relation'
              118  LOAD_STR                 'many'
              120  LOAD_CONST               False
              122  CALL_FUNCTION_3       3  ''

 L. 158       124  POP_JUMP_IF_FALSE   166  'to 166'

 L. 160       126  LOAD_GLOBAL              hasattr
              128  LOAD_FAST                'relation'
              130  LOAD_ATTR                child
              132  LOAD_STR                 'Meta'
              134  CALL_FUNCTION_2       2  ''

 L. 158       136  POP_JUMP_IF_FALSE   166  'to 166'

 L. 161       138  LOAD_GLOBAL              hasattr
              140  LOAD_FAST                'relation'
              142  LOAD_ATTR                child
              144  LOAD_ATTR                Meta
              146  LOAD_STR                 'model'
              148  CALL_FUNCTION_2       2  ''

 L. 158       150  POP_JUMP_IF_FALSE   166  'to 166'

 L. 164       152  LOAD_FAST                'relation'
              154  LOAD_ATTR                child
              156  LOAD_ATTR                Meta
              158  LOAD_ATTR                model
              160  STORE_FAST               'relation_model'
          162_164  JUMP_FORWARD        468  'to 468'
            166_0  COME_FROM           150  '150'
            166_1  COME_FROM           136  '136'
            166_2  COME_FROM           124  '124'

 L. 166       166  LOAD_FAST                'relation'
              168  LOAD_ATTR                parent
              170  STORE_FAST               'parent_serializer'

 L. 167       172  LOAD_CONST               None
              174  STORE_FAST               'parent_model'

 L. 168       176  LOAD_GLOBAL              hasattr
              178  LOAD_FAST                'parent_serializer'
              180  LOAD_STR                 'Meta'
              182  CALL_FUNCTION_2       2  ''
              184  POP_JUMP_IF_FALSE   202  'to 202'

 L. 169       186  LOAD_GLOBAL              getattr
              188  LOAD_FAST                'parent_serializer'
              190  LOAD_ATTR                Meta
              192  LOAD_STR                 'model'
              194  LOAD_CONST               None
              196  CALL_FUNCTION_3       3  ''
              198  STORE_FAST               'parent_model'
              200  JUMP_FORWARD        240  'to 240'
            202_0  COME_FROM           184  '184'

 L. 170       202  LOAD_GLOBAL              hasattr
              204  LOAD_FAST                'parent_serializer'
              206  LOAD_STR                 'parent'
              208  CALL_FUNCTION_2       2  ''
              210  POP_JUMP_IF_FALSE   240  'to 240'
              212  LOAD_GLOBAL              hasattr
              214  LOAD_FAST                'parent_serializer'
              216  LOAD_ATTR                parent
              218  LOAD_STR                 'Meta'
              220  CALL_FUNCTION_2       2  ''
              222  POP_JUMP_IF_FALSE   240  'to 240'

 L. 171       224  LOAD_GLOBAL              getattr
              226  LOAD_FAST                'parent_serializer'
              228  LOAD_ATTR                parent
              230  LOAD_ATTR                Meta
              232  LOAD_STR                 'model'
              234  LOAD_CONST               None
              236  CALL_FUNCTION_3       3  ''
              238  STORE_FAST               'parent_model'
            240_0  COME_FROM           222  '222'
            240_1  COME_FROM           210  '210'
            240_2  COME_FROM           200  '200'

 L. 173       240  LOAD_FAST                'parent_model'
              242  LOAD_CONST               None
              244  COMPARE_OP               is-not
          246_248  POP_JUMP_IF_FALSE   468  'to 468'

 L. 174       250  LOAD_FAST                'relation'
              252  LOAD_ATTR                source
          254_256  POP_JUMP_IF_FALSE   298  'to 298'

 L. 175       258  LOAD_FAST                'relation'
              260  LOAD_ATTR                source
              262  LOAD_STR                 '*'
              264  COMPARE_OP               !=
          266_268  POP_JUMP_IF_FALSE   284  'to 284'

 L. 176       270  LOAD_GLOBAL              getattr
              272  LOAD_FAST                'parent_model'
              274  LOAD_FAST                'relation'
              276  LOAD_ATTR                source
              278  CALL_FUNCTION_2       2  ''
              280  STORE_FAST               'parent_model_relation'
              282  JUMP_FORWARD        296  'to 296'
            284_0  COME_FROM           266  '266'

 L. 178       284  LOAD_GLOBAL              getattr
              286  LOAD_FAST                'parent_model'
              288  LOAD_FAST                'relation'
              290  LOAD_ATTR                field_name
              292  CALL_FUNCTION_2       2  ''
              294  STORE_FAST               'parent_model_relation'
            296_0  COME_FROM           282  '282'
              296  JUMP_FORWARD        310  'to 310'
            298_0  COME_FROM           254  '254'

 L. 180       298  LOAD_GLOBAL              getattr
              300  LOAD_FAST                'parent_model'
              302  LOAD_FAST                'parent_serializer'
              304  LOAD_ATTR                field_name
              306  CALL_FUNCTION_2       2  ''
              308  STORE_FAST               'parent_model_relation'
            310_0  COME_FROM           296  '296'

 L. 182       310  LOAD_GLOBAL              type
              312  LOAD_FAST                'parent_model_relation'
              314  CALL_FUNCTION_1       1  ''
              316  STORE_FAST               'parent_model_relation_type'

 L. 183       318  LOAD_FAST                'parent_model_relation_type'
              320  LOAD_GLOBAL              ReverseManyToOneDescriptor
              322  COMPARE_OP               is
          324_326  POP_JUMP_IF_FALSE   338  'to 338'

 L. 184       328  LOAD_FAST                'parent_model_relation'
              330  LOAD_ATTR                rel
              332  LOAD_ATTR                related_model
              334  STORE_FAST               'relation_model'
              336  JUMP_FORWARD        468  'to 468'
            338_0  COME_FROM           324  '324'

 L. 185       338  LOAD_FAST                'parent_model_relation_type'
              340  LOAD_GLOBAL              ManyToManyDescriptor
              342  COMPARE_OP               is
          344_346  POP_JUMP_IF_FALSE   378  'to 378'

 L. 186       348  LOAD_FAST                'parent_model_relation'
              350  LOAD_ATTR                field
              352  LOAD_ATTR                remote_field
              354  LOAD_ATTR                model
              356  STORE_FAST               'relation_model'

 L. 188       358  LOAD_FAST                'relation_model'
              360  LOAD_FAST                'parent_model'
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   468  'to 468'

 L. 189       368  LOAD_FAST                'parent_model_relation'
              370  LOAD_ATTR                field
              372  LOAD_ATTR                model
              374  STORE_FAST               'relation_model'
              376  JUMP_FORWARD        468  'to 468'
            378_0  COME_FROM           344  '344'

 L. 190       378  LOAD_FAST                'parent_model_relation_type'
              380  LOAD_GLOBAL              ReverseGenericManyToOneDescriptor
              382  COMPARE_OP               is
          384_386  POP_JUMP_IF_FALSE   398  'to 398'

 L. 191       388  LOAD_FAST                'parent_model_relation'
              390  LOAD_ATTR                rel
              392  LOAD_ATTR                model
              394  STORE_FAST               'relation_model'
              396  JUMP_FORWARD        468  'to 468'
            398_0  COME_FROM           384  '384'

 L. 192       398  LOAD_GLOBAL              hasattr
              400  LOAD_FAST                'parent_model_relation'
              402  LOAD_STR                 'field'
              404  CALL_FUNCTION_2       2  ''
          406_408  POP_JUMP_IF_FALSE   460  'to 460'

 L. 193       410  SETUP_FINALLY       426  'to 426'

 L. 194       412  LOAD_FAST                'parent_model_relation'
              414  LOAD_ATTR                field
              416  LOAD_ATTR                remote_field
              418  LOAD_ATTR                model
              420  STORE_FAST               'relation_model'
              422  POP_BLOCK        
              424  JUMP_FORWARD        458  'to 458'
            426_0  COME_FROM_FINALLY   410  '410'

 L. 195       426  DUP_TOP          
              428  LOAD_GLOBAL              AttributeError
              430  COMPARE_OP               exception-match
          432_434  POP_JUMP_IF_FALSE   456  'to 456'
              436  POP_TOP          
              438  POP_TOP          
              440  POP_TOP          

 L. 196       442  LOAD_FAST                'parent_model_relation'
              444  LOAD_ATTR                field
              446  LOAD_ATTR                related
              448  LOAD_ATTR                model
              450  STORE_FAST               'relation_model'
              452  POP_EXCEPT       
              454  JUMP_FORWARD        458  'to 458'
            456_0  COME_FROM           432  '432'
              456  END_FINALLY      
            458_0  COME_FROM           454  '454'
            458_1  COME_FROM           424  '424'
              458  JUMP_FORWARD        468  'to 468'
            460_0  COME_FROM           406  '406'

 L. 198       460  LOAD_GLOBAL              get_related_resource_type
              462  LOAD_FAST                'parent_model_relation'
              464  CALL_FUNCTION_1       1  ''
              466  RETURN_VALUE     
            468_0  COME_FROM           458  '458'
            468_1  COME_FROM           396  '396'
            468_2  COME_FROM           376  '376'
            468_3  COME_FROM           364  '364'
            468_4  COME_FROM           336  '336'
            468_5  COME_FROM           246  '246'
            468_6  COME_FROM           162  '162'
            468_7  COME_FROM           110  '110'
            468_8  COME_FROM            74  '74'
            468_9  COME_FROM            54  '54'

 L. 200       468  LOAD_FAST                'relation_model'
              470  LOAD_CONST               None
              472  COMPARE_OP               is
          474_476  POP_JUMP_IF_FALSE   494  'to 494'

 L. 201       478  LOAD_GLOBAL              APIException
              480  LOAD_GLOBAL              _
              482  LOAD_STR                 'Could not resolve resource type for relation %s'
              484  LOAD_FAST                'relation'
              486  BINARY_MODULO    
              488  CALL_FUNCTION_1       1  ''
              490  CALL_FUNCTION_1       1  ''
              492  RAISE_VARARGS_1       1  'exception instance'
            494_0  COME_FROM           474  '474'

 L. 203       494  LOAD_GLOBAL              get_resource_type_from_model
              496  LOAD_FAST                'relation_model'
              498  CALL_FUNCTION_1       1  ''
              500  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 22


def get_resource_type_from_model(model):
    json_api_meta = getattr(model, 'JSONAPIMeta', None)
    return getattr(json_api_meta, 'resource_name', format_resource_type(model.__name__))


def get_resource_type_from_queryset(qs):
    return get_resource_type_from_model(qs.model)


def get_resource_type_from_instance(instance):
    if hasattrinstance'_meta':
        return get_resource_type_from_model(instance._meta.model)


def get_resource_type_from_manager(manager):
    return get_resource_type_from_model(manager.model)


def get_resource_type_from_serializer(serializer):
    json_api_meta = getattr(serializer, 'JSONAPIMeta', None)
    meta = getattr(serializer, 'Meta', None)
    if hasattrjson_api_meta'resource_name':
        return json_api_meta.resource_name
    if hasattrmeta'resource_name':
        return meta.resource_name
    if hasattrmeta'model':
        return get_resource_type_from_model(meta.model)
    raise AttributeError()


def get_included_resources(request, serializer=None):
    """ Build a list of included resources. """
    include_resources_param = request.query_params.get'include' if request else None
    if include_resources_param:
        return include_resources_param.split','
    return get_default_included_resources_from_serializer(serializer)


def get_default_included_resources_from_serializer(serializer):
    meta = getattr(serializer, 'JSONAPIMeta', None)
    if meta is None:
        if getattr(serializer, 'many', False):
            meta = getattr(serializer.child, 'JSONAPIMeta', None)
    return list(getattr(meta, 'included_resources', []))


def get_included_serializers(serializer):
    included_serializers = copy.copygetattr(serializer, 'included_serializers', dict())
    for name, value in iter(included_serializers.items):
        if not isinstancevaluetype:
            if value == 'self':
                included_serializers[name] = serializer if isinstanceserializertype else serializer.__class__
            else:
                included_serializers[name] = import_class_from_dotted_path(value)
        return included_serializers


def get_relation_instance--- This code section failed: ---

 L. 271         0  SETUP_FINALLY        20  'to 20'

 L. 272         2  LOAD_GLOBAL              operator
                4  LOAD_METHOD              attrgetter
                6  LOAD_FAST                'source'
                8  CALL_METHOD_1         1  ''
               10  LOAD_FAST                'resource_instance'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'relation_instance'
               16  POP_BLOCK        
               18  JUMP_FORWARD         82  'to 82'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 273        20  DUP_TOP          
               22  LOAD_GLOBAL              AttributeError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    80  'to 80'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 276        34  LOAD_GLOBAL              getattr
               36  LOAD_FAST                'serializer'
               38  LOAD_FAST                'source'
               40  LOAD_CONST               None
               42  CALL_FUNCTION_3       3  ''
               44  STORE_FAST               'serializer_method'

 L. 277        46  LOAD_FAST                'serializer_method'
               48  POP_JUMP_IF_FALSE    70  'to 70'
               50  LOAD_GLOBAL              hasattr
               52  LOAD_FAST                'serializer_method'
               54  LOAD_STR                 '__call__'
               56  CALL_FUNCTION_2       2  ''
               58  POP_JUMP_IF_FALSE    70  'to 70'

 L. 278        60  LOAD_FAST                'serializer_method'
               62  LOAD_FAST                'resource_instance'
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'relation_instance'
               68  JUMP_FORWARD         76  'to 76'
             70_0  COME_FROM            58  '58'
             70_1  COME_FROM            48  '48'

 L. 280        70  POP_EXCEPT       
               72  LOAD_CONST               (False, None)
               74  RETURN_VALUE     
             76_0  COME_FROM            68  '68'
               76  POP_EXCEPT       
               78  JUMP_FORWARD         82  'to 82'
             80_0  COME_FROM            26  '26'
               80  END_FINALLY      
             82_0  COME_FROM            78  '78'
             82_1  COME_FROM            18  '18'

 L. 282        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'relation_instance'
               86  LOAD_GLOBAL              Manager
               88  CALL_FUNCTION_2       2  ''
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 283        92  LOAD_FAST                'relation_instance'
               94  LOAD_METHOD              all
               96  CALL_METHOD_0         0  ''
               98  STORE_FAST               'relation_instance'
            100_0  COME_FROM            90  '90'

 L. 285       100  LOAD_CONST               True
              102  LOAD_FAST                'relation_instance'
              104  BUILD_TUPLE_2         2 
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 72


class Hyperlink(str):
    __doc__ = '\n    A string like object that additionally has an associated name.\n    We use this for hyperlinked URLs that may render as a named link\n    in some contexts, or render as a plain URL in others.\n\n    Comes from Django REST framework 3.2\n    https://github.com/tomchristie/django-rest-framework\n    '

    def __new__(self, url, name):
        ret = str.__new__(self, url)
        ret.name = name
        return ret

    is_hyperlink = True


def format_drf_errors(response, context, exc):
    errors = []
    if isinstanceresponse.datalist:
        for message in response.data:
            errors.appendformat_error_object(message, '/data', response)

    else:
        for field, error in response.data.items:
            field = format_value(field)
            pointer = '/data/attributes/{}'.formatfield
            if isinstanceerrordict:
                errors.appenderror
            elif isinstanceexcHttp404 and isinstanceerrorstr:
                errors.appendformat_error_object(error, None, response)
            elif isinstanceerrorstr:
                classes = inspect.getmembers(exceptions, inspect.isclass)
                if isinstanceexctuple((x[1] for x in classes)):
                    pointer = '/data'
                errors.appendformat_error_object(error, pointer, response)
            elif isinstanceerrorlist:
                for message in error:
                    errors.appendformat_error_object(message, pointer, response)
                else:
                    errors.appendformat_error_object(error, pointer, response)

            else:
                context['view'].resource_name = 'errors'
                response.data = errors
                return response


def format_error_object(message, pointer, response):
    error_obj = {'detail':message,  'status':encoding.force_strresponse.status_code}
    if pointer is not None:
        error_obj['source'] = {'pointer': pointer}
    code = getattr(message, 'code', None)
    if code is not None:
        error_obj['code'] = code
    return error_obj


def format_errors(data):
    if len(data) > 1:
        if isinstancedatalist:
            data.sort(key=(lambda x: x.get('source', {}).get('pointer', '')))
    return {'errors': data}