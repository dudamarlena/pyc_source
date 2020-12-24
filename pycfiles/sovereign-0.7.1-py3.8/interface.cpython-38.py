# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/views/interface.py
# Compiled at: 2020-04-16 21:27:51
# Size of source mod 2**32: 5970 bytes
from collections import defaultdict
from fastapi import APIRouter, Query, Path, Cookie
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, JSONResponse
from sovereign import html_templates, discovery, XDS_TEMPLATES
from sovereign.discovery import DiscoveryTypes
from sovereign import json_response_class
from sovereign.sources import available_service_clusters, source_metadata
from sovereign.utils.mock import mock_discovery_request
router = APIRouter()
all_types = [t.value for t in DiscoveryTypes]

@router.get('/', summary='Redirect to resource interface')
async def ui_main():
    return RedirectResponse(url=f"/ui/resources/{all_types[0]}")


@router.get('/set-version',
  summary='Filter the UI by a certain Envoy Version (stores a Cookie)')
async def set_envoy_version(request: Request, version: str=Query('__any__', title='The clients envoy version to emulate in this XDS request')):
    url = request.headers.get('Referer', '/ui')
    response = RedirectResponse(url=url)
    response.set_cookie(key='envoy_version', value=version)
    return response


@router.get('/set-service-cluster',
  summary='Filter the UI by a certain service cluster (stores a Cookie)')
async def set_service_cluster(request: Request, service_cluster: str=Query('__any__', title='The clients envoy version to emulate in this XDS request')):
    url = request.headers.get('Referer', '/ui')
    response = RedirectResponse(url=url)
    response.set_cookie(key='service_cluster', value=service_cluster)
    return response


@router.get('/resources/{xds_type}',
  summary='List available resources for a given xDS type')
async def resources(request: Request, xds_type: DiscoveryTypes=Path('clusters', title='xDS type', description='The type of request'), region: str=Query(None, title='The clients region to emulate in this XDS request'), service_cluster: str=Cookie('*', title='The clients service cluster to emulate in this XDS request'), envoy_version: str=Cookie('__any__', title='The clients envoy version to emulate in this XDS request')):
    ret = defaultdict(list)
    try:
        response = await discovery.response(request=mock_discovery_request(service_cluster=service_cluster,
          resource_names=[],
          version=envoy_version,
          region=region),
          xds_type=(xds_type.value))
    except KeyError:
        ret['resources'] = []
    else:
        if isinstance(response, dict):
            ret['resources'] += response.get('resources') or []


@router.get('/resources/{xds_type}/{resource_name}',
  summary='Return JSON representation of a resource')
async def resource--- This code section failed: ---

 L. 104         0  LOAD_GLOBAL              discovery
                2  LOAD_ATTR                response

 L. 105         4  LOAD_GLOBAL              mock_discovery_request

 L. 106         6  LOAD_FAST                'service_cluster'

 L. 107         8  LOAD_FAST                'resource_name'
               10  BUILD_LIST_1          1 

 L. 108        12  LOAD_FAST                'envoy_version'

 L. 109        14  LOAD_FAST                'region'

 L. 105        16  LOAD_CONST               ('service_cluster', 'resource_names', 'version', 'region')
               18  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 111        20  LOAD_FAST                'xds_type'
               22  LOAD_ATTR                value

 L. 104        24  LOAD_CONST               ('request', 'xds_type')
               26  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               28  GET_AWAITABLE    
               30  LOAD_CONST               None
               32  YIELD_FROM       
               34  STORE_FAST               'response'

 L. 113        36  LOAD_GLOBAL              jsonable_encoder
               38  LOAD_FAST                'response'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'safe_response'

 L. 114        44  SETUP_FINALLY        58  'to 58'

 L. 115        46  LOAD_GLOBAL              json_response_class
               48  LOAD_FAST                'safe_response'
               50  LOAD_CONST               ('content',)
               52  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               54  POP_BLOCK        
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY    44  '44'

 L. 116        58  DUP_TOP          
               60  LOAD_GLOBAL              TypeError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    86  'to 86'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 117        72  LOAD_GLOBAL              JSONResponse
               74  LOAD_FAST                'safe_response'
               76  LOAD_CONST               ('content',)
               78  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               80  ROT_FOUR         
               82  POP_EXCEPT       
               84  RETURN_VALUE     
             86_0  COME_FROM            64  '64'
               86  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 68


@router.get('/resources/routes/{route_configuration}/{virtual_host}',
  summary='Return JSON representation of Virtual Hosts')
async def virtual_hosts--- This code section failed: ---

 L. 131         0  LOAD_GLOBAL              discovery
                2  LOAD_ATTR                response

 L. 132         4  LOAD_GLOBAL              mock_discovery_request

 L. 133         6  LOAD_FAST                'service_cluster'

 L. 134         8  LOAD_DEREF               'route_configuration'
               10  BUILD_LIST_1          1 

 L. 135        12  LOAD_FAST                'envoy_version'

 L. 136        14  LOAD_FAST                'region'

 L. 132        16  LOAD_CONST               ('service_cluster', 'resource_names', 'version', 'region')
               18  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 138        20  LOAD_STR                 'routes'

 L. 131        22  LOAD_CONST               ('request', 'xds_type')
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  STORE_FAST               'response'

 L. 140        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'response'
               38  LOAD_GLOBAL              dict
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE   178  'to 178'

 L. 141        44  LOAD_CLOSURE             'route_configuration'
               46  BUILD_TUPLE_1         1 
               48  LOAD_LISTCOMP            '<code_object <listcomp>>'
               50  LOAD_STR                 'virtual_hosts.<locals>.<listcomp>'
               52  MAKE_FUNCTION_8          'closure'

 L. 143        54  LOAD_FAST                'response'
               56  LOAD_METHOD              get
               58  LOAD_STR                 'resources'
               60  BUILD_LIST_0          0 
               62  CALL_METHOD_2         2  ''

 L. 141        64  GET_ITER         
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'route_configs'

 L. 146        70  LOAD_FAST                'route_configs'
               72  GET_ITER         
               74  FOR_ITER            178  'to 178'
               76  STORE_FAST               'route_config'

 L. 147        78  LOAD_FAST                'route_config'
               80  LOAD_STR                 'virtual_hosts'
               82  BINARY_SUBSCR    
               84  GET_ITER         
             86_0  COME_FROM           100  '100'
               86  FOR_ITER            172  'to 172'
               88  STORE_FAST               'vhost'

 L. 148        90  LOAD_FAST                'vhost'
               92  LOAD_STR                 'name'
               94  BINARY_SUBSCR    
               96  LOAD_FAST                'virtual_host'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE    86  'to 86'

 L. 149       102  LOAD_GLOBAL              jsonable_encoder
              104  LOAD_FAST                'vhost'
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'safe_response'

 L. 150       110  SETUP_FINALLY       132  'to 132'

 L. 151       112  LOAD_GLOBAL              json_response_class
              114  LOAD_FAST                'safe_response'
              116  LOAD_CONST               ('content',)
              118  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              120  POP_BLOCK        
              122  ROT_TWO          
              124  POP_TOP          
              126  ROT_TWO          
              128  POP_TOP          
              130  RETURN_VALUE     
            132_0  COME_FROM_FINALLY   110  '110'

 L. 152       132  DUP_TOP          
              134  LOAD_GLOBAL              TypeError
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   168  'to 168'
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 153       146  LOAD_GLOBAL              JSONResponse
              148  LOAD_FAST                'safe_response'
              150  LOAD_CONST               ('content',)
              152  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              154  ROT_FOUR         
              156  POP_EXCEPT       
              158  ROT_TWO          
              160  POP_TOP          
              162  ROT_TWO          
              164  POP_TOP          
              166  RETURN_VALUE     
            168_0  COME_FROM           138  '138'
              168  END_FINALLY      
              170  JUMP_BACK            86  'to 86'

 L. 154       172  POP_TOP          
              174  BREAK_LOOP          178  'to 178'
              176  JUMP_BACK            74  'to 74'
            178_0  COME_FROM            42  '42'

Parse error at or near `ROT_TWO' instruction at offset 122