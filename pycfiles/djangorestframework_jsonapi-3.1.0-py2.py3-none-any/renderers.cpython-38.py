# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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
    def extract_attributes--- This code section failed: ---

 L.  54         0  LOAD_GLOBAL              OrderedDict
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'data'

 L.  55         6  LOAD_GLOBAL              iter
                8  LOAD_FAST                'fields'
               10  LOAD_METHOD              items
               12  CALL_METHOD_0         0  ''
               14  CALL_FUNCTION_1       1  ''
               16  GET_ITER         
               18  FOR_ITER            140  'to 140'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'field_name'
               24  STORE_FAST               'field'

 L.  57        26  LOAD_FAST                'field_name'
               28  LOAD_STR                 'id'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    36  'to 36'

 L.  58        34  JUMP_BACK            18  'to 18'
             36_0  COME_FROM            32  '32'

 L.  60        36  LOAD_FAST                'fields'
               38  LOAD_FAST                'field_name'
               40  BINARY_SUBSCR    
               42  LOAD_ATTR                write_only
               44  POP_JUMP_IF_FALSE    48  'to 48'

 L.  61        46  JUMP_BACK            18  'to 18'
             48_0  COME_FROM            44  '44'

 L.  63        48  LOAD_GLOBAL              isinstance

 L.  64        50  LOAD_FAST                'field'

 L.  64        52  LOAD_GLOBAL              relations
               54  LOAD_ATTR                RelatedField
               56  LOAD_GLOBAL              relations
               58  LOAD_ATTR                ManyRelatedField
               60  LOAD_GLOBAL              BaseSerializer
               62  BUILD_TUPLE_3         3 

 L.  63        64  CALL_FUNCTION_2       2  ''
               66  POP_JUMP_IF_FALSE    70  'to 70'

 L.  66        68  JUMP_BACK            18  'to 18'
             70_0  COME_FROM            66  '66'

 L.  71        70  SETUP_FINALLY        84  'to 84'

 L.  72        72  LOAD_FAST                'resource'
               74  LOAD_FAST                'field_name'
               76  BINARY_SUBSCR    
               78  POP_TOP          
               80  POP_BLOCK        
               82  JUMP_FORWARD        118  'to 118'
             84_0  COME_FROM_FINALLY    70  '70'

 L.  73        84  DUP_TOP          
               86  LOAD_GLOBAL              KeyError
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   116  'to 116'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.  74        98  LOAD_FAST                'fields'
              100  LOAD_FAST                'field_name'
              102  BINARY_SUBSCR    
              104  LOAD_ATTR                read_only
              106  POP_JUMP_IF_FALSE   112  'to 112'

 L.  75       108  POP_EXCEPT       
              110  JUMP_BACK            18  'to 18'
            112_0  COME_FROM           106  '106'
              112  POP_EXCEPT       
              114  JUMP_FORWARD        118  'to 118'
            116_0  COME_FROM            90  '90'
              116  END_FINALLY      
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM            82  '82'

 L.  77       118  LOAD_FAST                'data'
              120  LOAD_METHOD              update

 L.  78       122  LOAD_FAST                'field_name'

 L.  78       124  LOAD_FAST                'resource'
              126  LOAD_METHOD              get
              128  LOAD_FAST                'field_name'
              130  CALL_METHOD_1         1  ''

 L.  77       132  BUILD_MAP_1           1 
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
              138  JUMP_BACK            18  'to 18'

 L.  81       140  LOAD_GLOBAL              utils
              142  LOAD_METHOD              format_field_names
              144  LOAD_FAST                'data'
              146  CALL_METHOD_1         1  ''
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 110

    @classmethod
    def extract_relationships(cls, fields, resource, resource_instance):
        """
        Builds the relationships top level object based on related serializers.
        """
        from rest_framework_json_api.relations import ResourceRelatedField
        data = OrderedDict
        if resource_instance is None:
            return
        for field_name, field in iter(fields.items):
            if field_name == api_settings.URL_FIELD_NAME:
                pass
            elif fields[field_name].write_only:
                pass
            elif not isinstancefield(relations.RelatedField, relations.ManyRelatedField, BaseSerializer):
                pass
            else:
                source = field.source
                relation_type = utils.get_related_resource_typefield
                if isinstancefieldrelations.HyperlinkedIdentityField:
                    resolved, relation_instance = utils.get_relation_instance(resource_instance, source, field.parent)
                    if not resolved:
                        pass
                    else:
                        relation_data = list
                        relation_queryset = relation_instance if relation_instance is not None else list
                        for related_object in relation_queryset:
                            relation_data.appendOrderedDict([
                             (
                              'type', relation_type),
                             (
                              'id', encoding.force_strrelated_object.pk)])
                        else:
                            data.update{field_name: {'links':{'related': resource.getfield_name}, 
                                          'data':relation_data, 
                                          'meta':{'count': len(relation_data)}}}

                else:
                    relation_data = {}
                    if isinstancefieldHyperlinkedMixin:
                        field_links = field.get_links(resource_instance, field.related_link_lookup_field)
                        relation_data.update({'links': field_links} if field_links else dict)
                        data.update{field_name: relation_data}
                    if isinstancefield(ResourceRelatedField,):
                        if not isinstancefieldSkipDataMixin:
                            relation_data.update{'data': resource.getfield_name}
                        data.update{field_name: relation_data}
                    elif isinstancefield(relations.PrimaryKeyRelatedField, relations.HyperlinkedRelatedField):
                        resolved, relation = utils.get_relation_instance(resource_instance, '%s_id' % source, field.parent)
                        if not resolved:
                            pass
                        else:
                            relation_id = relation if resource.getfield_name else None
                            relation_data = {'data': OrderedDict([
                                      (
                                       'type', relation_type), ('id', encoding.force_strrelation_id)]) if relation_id is not None else None}
                            if isinstancefieldrelations.HyperlinkedRelatedField:
                                if resource.getfield_name:
                                    relation_data.update{'links': {'related': resource.getfield_name}}
                                data.update{field_name: relation_data}
                            elif isinstancefieldrelations.ManyRelatedField:
                                resolved, relation_instance = utils.get_relation_instance(resource_instance, source, field.parent)
                                if not resolved:
                                    pass
                                else:
                                    relation_data = {}
                                    if isinstanceresource.getfield_nameIterable:
                                        relation_data.update{'meta': {'count': len(resource.getfield_name)}}
                                    if isinstancefield.child_relationResourceRelatedField:
                                        relation_data.update{'data': resource.getfield_name}
                                    if isinstancefield.child_relationHyperlinkedMixin:
                                        field_links = field.child_relation.get_links(resource_instance, field.child_relation.related_link_lookup_field)
                                        relation_data.update({'links': field_links} if field_links else dict)
                                        data.update{field_name: relation_data}
                                    else:
                                        relation_data = list
                                        for nested_resource_instance in relation_instance:
                                            nested_resource_instance_type = relation_type or utils.get_resource_type_from_instancenested_resource_instance
                                            relation_data.appendOrderedDict([
                                             (
                                              'type', nested_resource_instance_type),
                                             (
                                              'id', encoding.force_strnested_resource_instance.pk)])
                                        else:
                                            data.update{field_name: {'data':relation_data, 
                                                          'meta':{'count': len(relation_data)}}}

                    elif isinstancefieldListSerializer:
                        resolved, relation_instance = utils.get_relation_instance(resource_instance, source, field.parent)
                        if not resolved:
                            pass
                        else:
                            relation_data = list
                            serializer_data = resource.getfield_name
                            resource_instance_queryset = list(relation_instance)
                            if isinstanceserializer_datalist:
                                for position in range(len(serializer_data)):
                                    nested_resource_instance = resource_instance_queryset[position]
                                    nested_resource_instance_type = relation_type or utils.get_resource_type_from_instancenested_resource_instance
                                    relation_data.appendOrderedDict([
                                     (
                                      'type', nested_resource_instance_type),
                                     (
                                      'id', encoding.force_strnested_resource_instance.pk)])
                                else:
                                    data.update{field_name: {'data': relation_data}}

                    else:
                        if isinstancefieldSerializer:
                            relation_instance_id = getattr(resource_instance, source + '_id', None)
                            resolved, relation_instance = relation_instance_id or utils.get_relation_instance(resource_instance, source, field.parent)
                            if not resolved:
                                pass
                            else:
                                if relation_instance is not None:
                                    relation_instance_id = relation_instance.pk
                                data.update{field_name: {'data': OrderedDict([
                                                       (
                                                        'type', relation_type),
                                                       (
                                                        'id', encoding.force_strrelation_instance_id)]) if resource.getfield_name else None}}
                                continue
                        return utils.format_field_namesdata

    @classmethod
    def extract_relation_instance--- This code section failed: ---

 L. 306         0  SETUP_FINALLY        42  'to 42'

 L. 307         2  LOAD_FAST                'field'
                4  LOAD_METHOD              get_attribute
                6  LOAD_FAST                'resource_instance'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'res'

 L. 308        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'res'
               16  LOAD_GLOBAL              PKOnlyObject
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    36  'to 36'

 L. 309        22  LOAD_GLOBAL              get_attribute
               24  LOAD_FAST                'resource_instance'
               26  LOAD_FAST                'field'
               28  LOAD_ATTR                source_attrs
               30  CALL_FUNCTION_2       2  ''
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM            20  '20'

 L. 310        36  LOAD_FAST                'res'
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY     0  '0'

 L. 311        42  DUP_TOP          
               44  LOAD_GLOBAL              SkipField
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 312        56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            48  '48'
               62  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 52

    @classmethod
    def extract_included--- This code section failed: ---

 L. 322         0  LOAD_FAST                'resource_instance'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 323         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 325         8  LOAD_FAST                'fields'
               10  LOAD_ATTR                serializer
               12  STORE_FAST               'current_serializer'

 L. 326        14  LOAD_FAST                'current_serializer'
               16  LOAD_ATTR                context
               18  STORE_FAST               'context'

 L. 327        20  LOAD_GLOBAL              utils
               22  LOAD_METHOD              get_included_serializers
               24  LOAD_FAST                'current_serializer'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'included_serializers'

 L. 328        30  LOAD_GLOBAL              copy
               32  LOAD_METHOD              copy
               34  LOAD_FAST                'included_resources'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'included_resources'

 L. 329        40  LOAD_LISTCOMP            '<code_object <listcomp>>'
               42  LOAD_STR                 'JSONRenderer.extract_included.<locals>.<listcomp>'
               44  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               46  LOAD_FAST                'included_resources'
               48  GET_ITER         
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'included_resources'

 L. 331        54  LOAD_GLOBAL              iter
               56  LOAD_FAST                'fields'
               58  LOAD_METHOD              items
               60  CALL_METHOD_0         0  ''
               62  CALL_FUNCTION_1       1  ''
               64  GET_ITER         
             66_0  COME_FROM           620  '620'
             66_1  COME_FROM           596  '596'
             66_2  COME_FROM           268  '268'
            66_68  FOR_ITER            694  'to 694'
               70  UNPACK_SEQUENCE_2     2 
               72  STORE_DEREF              'field_name'
               74  STORE_FAST               'field'

 L. 333        76  LOAD_DEREF               'field_name'
               78  LOAD_GLOBAL              api_settings
               80  LOAD_ATTR                URL_FIELD_NAME
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    88  'to 88'

 L. 334        86  JUMP_BACK            66  'to 66'
             88_0  COME_FROM            84  '84'

 L. 337        88  LOAD_GLOBAL              isinstance

 L. 338        90  LOAD_FAST                'field'

 L. 338        92  LOAD_GLOBAL              relations
               94  LOAD_ATTR                RelatedField
               96  LOAD_GLOBAL              relations
               98  LOAD_ATTR                ManyRelatedField
              100  LOAD_GLOBAL              BaseSerializer
              102  BUILD_TUPLE_3         3 

 L. 337       104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_TRUE    110  'to 110'

 L. 340       108  JUMP_BACK            66  'to 66'
            110_0  COME_FROM           106  '106'

 L. 342       110  SETUP_FINALLY       126  'to 126'

 L. 343       112  LOAD_FAST                'included_resources'
              114  LOAD_METHOD              remove
              116  LOAD_DEREF               'field_name'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
              122  POP_BLOCK        
              124  JUMP_FORWARD        168  'to 168'
            126_0  COME_FROM_FINALLY   110  '110'

 L. 344       126  DUP_TOP          
              128  LOAD_GLOBAL              ValueError
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   166  'to 166'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 347       140  LOAD_DEREF               'field_name'
              142  LOAD_LISTCOMP            '<code_object <listcomp>>'
              144  LOAD_STR                 'JSONRenderer.extract_included.<locals>.<listcomp>'
              146  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              148  LOAD_FAST                'included_resources'
              150  GET_ITER         
              152  CALL_FUNCTION_1       1  ''
              154  COMPARE_OP               not-in
              156  POP_JUMP_IF_FALSE   162  'to 162'

 L. 348       158  POP_EXCEPT       
              160  JUMP_BACK            66  'to 66'
            162_0  COME_FROM           156  '156'
              162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
            166_0  COME_FROM           132  '132'
              166  END_FINALLY      
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           124  '124'

 L. 350       168  LOAD_FAST                'cls'
              170  LOAD_METHOD              extract_relation_instance

 L. 351       172  LOAD_FAST                'field'

 L. 351       174  LOAD_FAST                'resource_instance'

 L. 350       176  CALL_METHOD_2         2  ''
              178  STORE_FAST               'relation_instance'

 L. 353       180  LOAD_GLOBAL              isinstance
              182  LOAD_FAST                'relation_instance'
              184  LOAD_GLOBAL              Manager
              186  CALL_FUNCTION_2       2  ''
              188  POP_JUMP_IF_FALSE   198  'to 198'

 L. 354       190  LOAD_FAST                'relation_instance'
              192  LOAD_METHOD              all
              194  CALL_METHOD_0         0  ''
              196  STORE_FAST               'relation_instance'
            198_0  COME_FROM           188  '188'

 L. 356       198  LOAD_FAST                'resource'
              200  LOAD_METHOD              get
              202  LOAD_DEREF               'field_name'
              204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'serializer_data'

 L. 358       208  LOAD_GLOBAL              isinstance
              210  LOAD_FAST                'field'
              212  LOAD_GLOBAL              relations
              214  LOAD_ATTR                ManyRelatedField
              216  CALL_FUNCTION_2       2  ''
              218  POP_JUMP_IF_FALSE   248  'to 248'

 L. 359       220  LOAD_FAST                'included_serializers'
              222  LOAD_DEREF               'field_name'
              224  BINARY_SUBSCR    
              226  STORE_FAST               'serializer_class'

 L. 360       228  LOAD_FAST                'serializer_class'
              230  LOAD_FAST                'relation_instance'
              232  LOAD_CONST               True
              234  LOAD_FAST                'context'
              236  LOAD_CONST               ('many', 'context')
              238  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              240  STORE_FAST               'field'

 L. 361       242  LOAD_FAST                'field'
              244  LOAD_ATTR                data
              246  STORE_FAST               'serializer_data'
            248_0  COME_FROM           218  '218'

 L. 363       248  LOAD_GLOBAL              isinstance
              250  LOAD_FAST                'field'
              252  LOAD_GLOBAL              relations
              254  LOAD_ATTR                RelatedField
              256  CALL_FUNCTION_2       2  ''
          258_260  POP_JUMP_IF_FALSE   384  'to 384'

 L. 364       262  LOAD_FAST                'relation_instance'
              264  LOAD_CONST               None
              266  COMPARE_OP               is
              268  POP_JUMP_IF_TRUE     66  'to 66'
              270  LOAD_FAST                'serializer_data'
          272_274  POP_JUMP_IF_TRUE    278  'to 278'

 L. 365       276  JUMP_BACK            66  'to 66'
            278_0  COME_FROM           272  '272'

 L. 367       278  LOAD_FAST                'field'
              280  LOAD_ATTR                _kwargs
              282  LOAD_METHOD              get
              284  LOAD_STR                 'child_relation'
              286  LOAD_CONST               None
              288  CALL_METHOD_2         2  ''
              290  LOAD_CONST               None
              292  COMPARE_OP               is-not
              294  STORE_FAST               'many'

 L. 369       296  LOAD_GLOBAL              isinstance
              298  LOAD_FAST                'field'
              300  LOAD_GLOBAL              ResourceRelatedField
              302  CALL_FUNCTION_2       2  ''
          304_306  POP_JUMP_IF_FALSE   356  'to 356'
              308  LOAD_FAST                'many'
          310_312  POP_JUMP_IF_TRUE    356  'to 356'

 L. 370       314  LOAD_FAST                'serializer_data'
              316  LOAD_STR                 'type'
              318  BINARY_SUBSCR    
              320  LOAD_FAST                'included_cache'
              322  COMPARE_OP               in
          324_326  JUMP_IF_FALSE_OR_POP   346  'to 346'

 L. 371       328  LOAD_FAST                'serializer_data'
              330  LOAD_STR                 'id'
              332  BINARY_SUBSCR    
              334  LOAD_FAST                'included_cache'
              336  LOAD_FAST                'serializer_data'
              338  LOAD_STR                 'type'
              340  BINARY_SUBSCR    
              342  BINARY_SUBSCR    
              344  COMPARE_OP               in
            346_0  COME_FROM           324  '324'

 L. 370       346  STORE_FAST               'already_included'

 L. 373       348  LOAD_FAST                'already_included'
          350_352  POP_JUMP_IF_FALSE   356  'to 356'

 L. 374       354  JUMP_BACK            66  'to 66'
            356_0  COME_FROM           350  '350'
            356_1  COME_FROM           310  '310'
            356_2  COME_FROM           304  '304'

 L. 376       356  LOAD_FAST                'included_serializers'
              358  LOAD_DEREF               'field_name'
              360  BINARY_SUBSCR    
              362  STORE_FAST               'serializer_class'

 L. 377       364  LOAD_FAST                'serializer_class'
              366  LOAD_FAST                'relation_instance'
              368  LOAD_FAST                'many'
              370  LOAD_FAST                'context'
              372  LOAD_CONST               ('many', 'context')
              374  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              376  STORE_FAST               'field'

 L. 378       378  LOAD_FAST                'field'
              380  LOAD_ATTR                data
              382  STORE_FAST               'serializer_data'
            384_0  COME_FROM           258  '258'

 L. 380       384  LOAD_CLOSURE             'field_name'
              386  BUILD_TUPLE_1         1 
              388  LOAD_LISTCOMP            '<code_object <listcomp>>'
              390  LOAD_STR                 'JSONRenderer.extract_included.<locals>.<listcomp>'
              392  MAKE_FUNCTION_8          'closure'

 L. 381       394  LOAD_FAST                'included_resources'

 L. 380       396  GET_ITER         
              398  CALL_FUNCTION_1       1  ''
              400  STORE_FAST               'new_included_resources'

 L. 384       402  LOAD_GLOBAL              isinstance
              404  LOAD_FAST                'field'
              406  LOAD_GLOBAL              ListSerializer
              408  CALL_FUNCTION_2       2  ''
          410_412  POP_JUMP_IF_FALSE   588  'to 588'

 L. 385       414  LOAD_FAST                'field'
              416  LOAD_ATTR                child
              418  STORE_FAST               'serializer'

 L. 386       420  LOAD_GLOBAL              utils
              422  LOAD_METHOD              get_resource_type_from_serializer
              424  LOAD_FAST                'serializer'
              426  CALL_METHOD_1         1  ''
              428  STORE_FAST               'relation_type'

 L. 387       430  LOAD_GLOBAL              list
              432  LOAD_FAST                'relation_instance'
              434  CALL_FUNCTION_1       1  ''
              436  STORE_FAST               'relation_queryset'

 L. 389       438  LOAD_FAST                'serializer_data'
          440_442  POP_JUMP_IF_FALSE   588  'to 588'

 L. 390       444  LOAD_GLOBAL              range
              446  LOAD_GLOBAL              len
              448  LOAD_FAST                'serializer_data'
              450  CALL_FUNCTION_1       1  ''
              452  CALL_FUNCTION_1       1  ''
              454  GET_ITER         
              456  FOR_ITER            588  'to 588'
              458  STORE_FAST               'position'

 L. 391       460  LOAD_FAST                'serializer_data'
              462  LOAD_FAST                'position'
              464  BINARY_SUBSCR    
              466  STORE_FAST               'serializer_resource'

 L. 392       468  LOAD_FAST                'relation_queryset'
              470  LOAD_FAST                'position'
              472  BINARY_SUBSCR    
              474  STORE_FAST               'nested_resource_instance'

 L. 394       476  LOAD_FAST                'relation_type'
          478_480  JUMP_IF_TRUE_OR_POP   490  'to 490'

 L. 395       482  LOAD_GLOBAL              utils
              484  LOAD_METHOD              get_resource_type_from_instance
              486  LOAD_FAST                'nested_resource_instance'
              488  CALL_METHOD_1         1  ''
            490_0  COME_FROM           478  '478'

 L. 393       490  STORE_FAST               'resource_type'

 L. 397       492  LOAD_GLOBAL              utils
              494  LOAD_METHOD              get_serializer_fields

 L. 398       496  LOAD_FAST                'serializer'
              498  LOAD_ATTR                __class__

 L. 399       500  LOAD_FAST                'nested_resource_instance'

 L. 399       502  LOAD_FAST                'serializer'
              504  LOAD_ATTR                context

 L. 398       506  LOAD_CONST               ('context',)
              508  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 397       510  CALL_METHOD_1         1  ''
              512  STORE_FAST               'serializer_fields'

 L. 402       514  LOAD_FAST                'cls'
              516  LOAD_METHOD              build_json_resource_obj

 L. 403       518  LOAD_FAST                'serializer_fields'

 L. 404       520  LOAD_FAST                'serializer_resource'

 L. 405       522  LOAD_FAST                'nested_resource_instance'

 L. 406       524  LOAD_FAST                'resource_type'

 L. 407       526  LOAD_GLOBAL              getattr
              528  LOAD_FAST                'serializer'
              530  LOAD_STR                 '_poly_force_type_resolution'
              532  LOAD_CONST               False
              534  CALL_FUNCTION_3       3  ''

 L. 402       536  CALL_METHOD_5         5  ''
              538  STORE_FAST               'new_item'

 L. 410       540  LOAD_GLOBAL              utils
              542  LOAD_METHOD              format_field_names
              544  LOAD_FAST                'new_item'
              546  CALL_METHOD_1         1  ''

 L. 409       548  LOAD_FAST                'included_cache'
              550  LOAD_FAST                'new_item'
              552  LOAD_STR                 'type'
              554  BINARY_SUBSCR    
              556  BINARY_SUBSCR    
              558  LOAD_FAST                'new_item'
              560  LOAD_STR                 'id'
              562  BINARY_SUBSCR    
              564  STORE_SUBSCR     

 L. 411       566  LOAD_FAST                'cls'
              568  LOAD_METHOD              extract_included

 L. 412       570  LOAD_FAST                'serializer_fields'

 L. 413       572  LOAD_FAST                'serializer_resource'

 L. 414       574  LOAD_FAST                'nested_resource_instance'

 L. 415       576  LOAD_FAST                'new_included_resources'

 L. 416       578  LOAD_FAST                'included_cache'

 L. 411       580  CALL_METHOD_5         5  ''
              582  POP_TOP          
          584_586  JUMP_BACK           456  'to 456'
            588_0  COME_FROM           440  '440'
            588_1  COME_FROM           410  '410'

 L. 419       588  LOAD_GLOBAL              isinstance
              590  LOAD_FAST                'field'
              592  LOAD_GLOBAL              Serializer
              594  CALL_FUNCTION_2       2  ''
              596  POP_JUMP_IF_FALSE    66  'to 66'

 L. 420       598  LOAD_GLOBAL              utils
              600  LOAD_METHOD              get_resource_type_from_serializer
              602  LOAD_FAST                'field'
              604  CALL_METHOD_1         1  ''
              606  STORE_FAST               'relation_type'

 L. 423       608  LOAD_GLOBAL              utils
              610  LOAD_METHOD              get_serializer_fields
              612  LOAD_FAST                'field'
              614  CALL_METHOD_1         1  ''
              616  STORE_FAST               'serializer_fields'

 L. 424       618  LOAD_FAST                'serializer_data'
              620  POP_JUMP_IF_FALSE    66  'to 66'

 L. 425       622  LOAD_FAST                'cls'
              624  LOAD_METHOD              build_json_resource_obj

 L. 426       626  LOAD_FAST                'serializer_fields'

 L. 427       628  LOAD_FAST                'serializer_data'

 L. 428       630  LOAD_FAST                'relation_instance'

 L. 429       632  LOAD_FAST                'relation_type'

 L. 430       634  LOAD_GLOBAL              getattr
              636  LOAD_FAST                'field'
              638  LOAD_STR                 '_poly_force_type_resolution'
              640  LOAD_CONST               False
              642  CALL_FUNCTION_3       3  ''

 L. 425       644  CALL_METHOD_5         5  ''
              646  STORE_FAST               'new_item'

 L. 432       648  LOAD_GLOBAL              utils
              650  LOAD_METHOD              format_field_names

 L. 433       652  LOAD_FAST                'new_item'

 L. 432       654  CALL_METHOD_1         1  ''
              656  LOAD_FAST                'included_cache'
              658  LOAD_FAST                'new_item'
              660  LOAD_STR                 'type'
              662  BINARY_SUBSCR    
              664  BINARY_SUBSCR    
              666  LOAD_FAST                'new_item'
              668  LOAD_STR                 'id'
              670  BINARY_SUBSCR    
              672  STORE_SUBSCR     

 L. 435       674  LOAD_FAST                'cls'
              676  LOAD_METHOD              extract_included

 L. 436       678  LOAD_FAST                'serializer_fields'

 L. 437       680  LOAD_FAST                'serializer_data'

 L. 438       682  LOAD_FAST                'relation_instance'

 L. 439       684  LOAD_FAST                'new_included_resources'

 L. 440       686  LOAD_FAST                'included_cache'

 L. 435       688  CALL_METHOD_5         5  ''
              690  POP_TOP          
              692  JUMP_BACK            66  'to 66'

Parse error at or near `JUMP_BACK' instruction at offset 160

    @classmethod
    def extract_meta(cls, serializer, resource):
        """
        Gathers the data from serializer fields specified in meta_fields and adds it to
        the meta object.
        """
        if hasattrserializer'child':
            meta = getattr(serializer.child, 'Meta', None)
        else:
            meta = getattr(serializer, 'Meta', None)
        meta_fields = getattr(meta, 'meta_fields', [])
        data = OrderedDict
        for field_name in meta_fields:
            data.update{field_name: resource.getfield_name}
        else:
            return data

    @classmethod
    def extract_root_meta(cls, serializer, resource):
        """
        Calls a `get_root_meta` function on a serializer, if it exists.
        """
        many = False
        if hasattrserializer'child':
            many = True
            serializer = serializer.child
        data = {}
        if getattr(serializer, 'get_root_meta', None):
            json_api_meta = serializer.get_root_meta(resource, many)
            assert isinstancejson_api_metadict, 'get_root_meta must return a dict'
            data.updatejson_api_meta
        return data

    @classmethod
    def build_json_resource_obj(cls, fields, resource, resource_instance, resource_name, force_type_resolution=False):
        """
        Builds the resource object (type, id, attributes) and extracts relationships.
        """
        if force_type_resolution:
            resource_name = utils.get_resource_type_from_instanceresource_instance
        else:
            resource_data = [
             (
              'type', resource_name),
             (
              'id', encoding.force_strresource_instance.pk if resource_instance else None),
             (
              'attributes', cls.extract_attributes(fields, resource))]
            relationships = cls.extract_relationships(fields, resource, resource_instance)
            if relationships:
                resource_data.append('relationships', relationships)
            if api_settings.URL_FIELD_NAME in resource and isinstancefields[api_settings.URL_FIELD_NAME]relations.RelatedField:
                resource_data.append('links', {'self': resource[api_settings.URL_FIELD_NAME]})
        return OrderedDict(resource_data)

    def render_relationship_view(self, data, accepted_media_type=None, renderer_context=None):
        view = renderer_context.get('view', None)
        render_data = OrderedDict([
         (
          'data', data)])
        links = view.get_links
        if links:
            (
             render_data.update{'links': links},)
        return superJSONRendererself.render(render_data, accepted_media_type, renderer_context)

    def render_errors(self, data, accepted_media_type=None, renderer_context=None):
        return superJSONRendererself.render(utils.format_errorsdata, accepted_media_type, renderer_context)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        view = renderer_context.get('view', None)
        request = renderer_context.get('request', None)
        resource_name = utils.get_resource_namerenderer_context
        if resource_name == 'errors':
            return self.render_errors(data, accepted_media_type, renderer_context)
        response = renderer_context.get('response', None)
        if response is not None:
            if response.status_code == 204:
                return superJSONRendererself.render(None, accepted_media_type, renderer_context)
        from rest_framework_json_api.views import RelationshipView
        if isinstanceviewRelationshipView:
            return self.render_relationship_view(data, accepted_media_type, renderer_context)
        if resource_name is None or resource_name is False:
            return superJSONRendererself.render(data, accepted_media_type, renderer_context)
        json_api_data = data
        json_api_meta = data.get('meta', {}) if isinstancedatadict else {}
        included_cache = defaultdict(dict)
        if data and 'results' in data:
            serializer_data = data['results']
        else:
            serializer_data = data
        serializer = getattr(serializer_data, 'serializer', None)
        included_resources = utils.get_included_resources(request, serializer)
        if serializer is not None:
            json_api_meta.updateself.extract_root_meta(serializer, serializer_data)
            if getattr(serializer, 'many', False):
                json_api_data = list
                for position in range(len(serializer_data)):
                    resource = serializer_data[position]
                    resource_instance = serializer.instance[position]
                    if isinstanceserializer.childrest_framework_json_api.serializers.PolymorphicModelSerializer:
                        resource_serializer_class = serializer.child.get_polymorphic_serializer_for_instanceresource_instance(context=(serializer.child.context))
                    else:
                        resource_serializer_class = serializer.child
                    fields = utils.get_serializer_fieldsresource_serializer_class
                    force_type_resolution = getattr(resource_serializer_class, '_poly_force_type_resolution', False)
                    json_resource_obj = self.build_json_resource_objfieldsresourceresource_instanceresource_nameforce_type_resolution
                    meta = self.extract_meta(serializer, resource)
                    if meta:
                        json_resource_obj.update{'meta': utils.format_field_namesmeta}
                    json_api_data.appendjson_resource_obj
                    self.extract_includedfieldsresourceresource_instanceincluded_resourcesincluded_cache

            else:
                fields = utils.get_serializer_fieldsserializer
                force_type_resolution = getattr(serializer, '_poly_force_type_resolution', False)
                resource_instance = serializer.instance
                json_api_data = self.build_json_resource_objfieldsserializer_dataresource_instanceresource_nameforce_type_resolution
                meta = self.extract_meta(serializer, serializer_data)
                if meta:
                    json_api_data.update{'meta': utils.format_field_namesmeta}
                self.extract_includedfieldsserializer_dataresource_instanceincluded_resourcesincluded_cache
        else:
            render_data = OrderedDict
            if isinstancedatadict:
                if data.get'links':
                    render_data['links'] = data.get'links'
            if view.__class__:
                if view.__class__.__name__ == 'APIRoot':
                    render_data['data'] = None
                    render_data['links'] = json_api_data
                else:
                    render_data['data'] = json_api_data
                if included_cache:
                    if isinstancejson_api_datalist:
                        objects = json_api_data
            else:
                objects = [
                 json_api_data]
        for object in objects:
            obj_type = object.get'type'
            obj_id = object.get'id'
            if obj_type in included_cache:
                if obj_id in included_cache[obj_type]:
                    del included_cache[obj_type][obj_id]
            if not included_cache[obj_type]:
                del included_cache[obj_type]
            elif included_cache:
                render_data['included'] = list
                for included_type in sorted(included_cache.keys):
                    for included_id in sorted(included_cache[included_type].keys):
                        render_data['included'].appendincluded_cache[included_type][included_id]

            else:
                if json_api_meta:
                    render_data['meta'] = utils.format_field_namesjson_api_meta
                return superJSONRendererself.render(render_data, accepted_media_type, renderer_context)