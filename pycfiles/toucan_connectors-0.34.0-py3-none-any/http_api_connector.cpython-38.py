# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/http_api/http_api_connector.py
# Compiled at: 2020-03-19 08:41:10
# Size of source mod 2**32: 5228 bytes
from enum import Enum
from typing import List, Union
import pandas as pd
from pydantic import BaseModel, Field, FilePath, HttpUrl
from requests import Session
from toucan_connectors.auth import Auth
from toucan_connectors.common import FilterSchema, nosql_apply_parameters_to_query, transform_with_jq
from toucan_connectors.toucan_connector import ToucanConnector, ToucanDataSource

class Method(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'


class Template(BaseModel):
    headers = Field(None,
      description='JSON object of HTTP headers to send with every HTTP request',
      examples=[
     '{ "content-type": "application/xml" }'])
    headers: dict
    params = Field(None,
      description='JSON object of parameters to send in the query string of every HTTP request (e.g. "offset" and "limit" in https://www/api-aseroute/data&offset=100&limit=50)',
      examples=[
     '{ "offset": 100, "limit": 50 }'])
    params: dict
    json_ = Field(None,
      alias='json',
      description='JSON object of parameters to send in the body of every HTTP request',
      examples=[
     '{ "offset": 100, "limit": 50 }'])
    json_: dict
    proxies = Field(None,
      description='JSON object expressing a mapping of protocol or host to corresponding proxy',
      examples=[
     '{"http": "foo.bar:3128", "http://host.name": "foo.bar:4012"}'])
    proxies: dict


class HttpAPIDataSource(ToucanDataSource):
    url = Field(...,
      title='Endpoint URL',
      description='The URL path that will be appended to your baseroute URL. For example "geo/countries"')
    url: str
    method = Field((Method.GET), title='HTTP Method')
    method: Method
    headers = Field(None,
      description='JSON object of HTTP headers to send with every HTTP request',
      examples=[
     '{ "content-type": "application/xml" }'])
    headers: dict
    params = Field(None,
      description='JSON object of parameters to send in the query string of this HTTP request (e.g. "offset" and "limit" in https://www/api-aseroute/data&offset=100&limit=50)',
      examples=[
     '{ "offset": 100, "limit": 50 }'])
    params: dict
    json_ = Field(None,
      alias='json',
      description='JSON object of parameters to send in the body of every HTTP request',
      examples=[
     '{ "offset": 100, "limit": 50 }'])
    json_: dict
    proxies = Field(None,
      description='JSON object expressing a mapping of protocol or host to corresponding proxy',
      examples=[
     '{"http": "foo.bar:3128", "http://host.name": "foo.bar:4012"}'])
    proxies: dict
    data = Field(None,
      description='JSON object to send in the body of the HTTP request')
    data: Union[(str, dict)]
    filter = FilterSchema
    filter: str


class HttpAPIConnector(ToucanConnector):
    data_source_model: HttpAPIDataSource
    baseroute = Field(..., title='Baseroute URL', description='Baseroute URL')
    baseroute: HttpUrl
    cert = Field(None,
      title='Certificate', description='File path of your certificate if any')
    cert: List[FilePath]
    auth = Field(None, title='Authentication type')
    auth: Auth
    template = Field(None,
      description='You can provide a custom template that will be used for every HTTP request')
    template: Template

    def do_request--- This code section failed: ---

 L. 106         0  LOAD_FAST                'query'
                2  LOAD_STR                 'filter'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'jq_filter'

 L. 108         8  LOAD_STR                 'url'
               10  LOAD_STR                 'method'
               12  LOAD_STR                 'params'
               14  LOAD_STR                 'data'
               16  LOAD_STR                 'json'
               18  LOAD_STR                 'headers'
               20  LOAD_STR                 'proxies'
               22  BUILD_LIST_7          7 
               24  STORE_DEREF              'available_params'

 L. 109        26  LOAD_CLOSURE             'available_params'
               28  BUILD_TUPLE_1         1 
               30  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               32  LOAD_STR                 'HttpAPIConnector.do_request.<locals>.<dictcomp>'
               34  MAKE_FUNCTION_8          'closure'
               36  LOAD_FAST                'query'
               38  LOAD_METHOD              items
               40  CALL_METHOD_0         0  ''
               42  GET_ITER         
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'query'

 L. 110        48  LOAD_STR                 '/'
               50  LOAD_METHOD              join
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                baseroute
               56  LOAD_METHOD              rstrip
               58  LOAD_STR                 '/'
               60  CALL_METHOD_1         1  ''
               62  LOAD_FAST                'query'
               64  LOAD_STR                 'url'
               66  BINARY_SUBSCR    
               68  LOAD_METHOD              lstrip
               70  LOAD_STR                 '/'
               72  CALL_METHOD_1         1  ''
               74  BUILD_LIST_2          2 
               76  CALL_METHOD_1         1  ''
               78  LOAD_FAST                'query'
               80  LOAD_STR                 'url'
               82  STORE_SUBSCR     

 L. 111        84  LOAD_FAST                'self'
               86  LOAD_ATTR                cert
               88  POP_JUMP_IF_FALSE   110  'to 110'

 L. 113        90  LOAD_LISTCOMP            '<code_object <listcomp>>'
               92  LOAD_STR                 'HttpAPIConnector.do_request.<locals>.<listcomp>'
               94  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                cert
              100  GET_ITER         
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_FAST                'query'
              106  LOAD_STR                 'cert'
              108  STORE_SUBSCR     
            110_0  COME_FROM            88  '88'

 L. 114       110  LOAD_FAST                'session'
              112  LOAD_ATTR                request
              114  BUILD_TUPLE_0         0 
              116  LOAD_FAST                'query'
              118  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              120  STORE_FAST               'res'

 L. 116       122  SETUP_FINALLY       136  'to 136'

 L. 117       124  LOAD_FAST                'res'
              126  LOAD_METHOD              json
              128  CALL_METHOD_0         0  ''
              130  STORE_FAST               'data'
              132  POP_BLOCK        
              134  JUMP_FORWARD        178  'to 178'
            136_0  COME_FROM_FINALLY   122  '122'

 L. 118       136  DUP_TOP          
              138  LOAD_GLOBAL              ValueError
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   176  'to 176'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 119       150  LOAD_GLOBAL              HttpAPIConnector
              152  LOAD_ATTR                logger
              154  LOAD_METHOD              error
              156  LOAD_STR                 'Could not decode '
              158  LOAD_FAST                'res'
              160  LOAD_ATTR                content
              162  FORMAT_VALUE          2  '!r'
              164  BUILD_STRING_2        2 
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 120       170  RAISE_VARARGS_0       0  'reraise'
              172  POP_EXCEPT       
              174  JUMP_FORWARD        178  'to 178'
            176_0  COME_FROM           142  '142'
              176  END_FINALLY      
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           134  '134'

 L. 122       178  SETUP_FINALLY       192  'to 192'

 L. 123       180  LOAD_GLOBAL              transform_with_jq
              182  LOAD_FAST                'data'
              184  LOAD_FAST                'jq_filter'
              186  CALL_FUNCTION_2       2  ''
              188  POP_BLOCK        
              190  RETURN_VALUE     
            192_0  COME_FROM_FINALLY   178  '178'

 L. 124       192  DUP_TOP          
              194  LOAD_GLOBAL              ValueError
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   236  'to 236'
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L. 125       206  LOAD_GLOBAL              HttpAPIConnector
              208  LOAD_ATTR                logger
              210  LOAD_METHOD              error
              212  LOAD_STR                 'Could not transform '
              214  LOAD_FAST                'data'
              216  FORMAT_VALUE          0  ''
              218  LOAD_STR                 ' using '
              220  LOAD_FAST                'jq_filter'
              222  FORMAT_VALUE          0  ''
              224  BUILD_STRING_4        4 
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 126       230  RAISE_VARARGS_0       0  'reraise'
              232  POP_EXCEPT       
              234  JUMP_FORWARD        238  'to 238'
            236_0  COME_FROM           198  '198'
              236  END_FINALLY      
            238_0  COME_FROM           234  '234'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 30

    def _retrieve_data(self, data_source: HttpAPIDataSource) -> pd.DataFrame:
        if self.auth:
            session = self.auth.get_session
        else:
            session = Session()
        query = nosql_apply_parameters_to_querydata_source.dict(by_alias=True)data_source.parameters
        if self.template:
            template = {v:k for k, v in self.template.dict(by_alias=True).items if v if v}
            for k in query.keys & template.keys:
                if query[k]:
                    template[k].updatequery[k]
                query[k] = template[k]

        return pd.DataFrameself.do_request(query, session)