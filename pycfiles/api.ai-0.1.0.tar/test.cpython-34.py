# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/test.py
# Compiled at: 2016-04-18 08:05:11
# Size of source mod 2**32: 2780 bytes
import io
from api_star.compat import urlparse
from requests.adapters import BaseAdapter
from requests.models import Response
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers
import sys

class Content(object):

    def __init__(self, content):
        self._len = len(content)
        self._read = 0
        self._bytes = io.BytesIO(content)

    def __len__(self):
        return self._len

    def read(self, amt=None):
        if amt:
            self._read += amt
        return self._bytes.read(amt)

    def stream(self, amt=None, decode_content=None):
        while self._read < self._len:
            yield self.read(amt)

    def release_conn(self):
        pass


class WSGIAdapter(BaseAdapter):

    def __init__(self, app):
        self.app = app

    def send--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL              urlparse
                3  LOAD_FAST                'request'
                6  LOAD_ATTR                url
                9  CALL_FUNCTION_1       1  '1 positional, 0 named'
               12  STORE_FAST               'urlinfo'

 L.  41        15  LOAD_FAST                'request'
               18  LOAD_ATTR                body
               21  POP_JUMP_IF_FALSE    42  'to 42'
               24  LOAD_FAST                'request'
               27  LOAD_ATTR                body
               30  LOAD_ATTR                encode
               33  LOAD_STR                 'utf-8'
               36  CALL_FUNCTION_1       1  '1 positional, 0 named'
               39  JUMP_FORWARD         45  'to 45'
               42  ELSE                     '45'
               42  LOAD_STR                 ''
             45_0  COME_FROM            39  '39'
               45  STORE_FAST               'data'

 L.  43        48  BUILD_MAP_16         16  ''

 L.  44        51  LOAD_FAST                'request'
               54  LOAD_ATTR                headers
               57  LOAD_ATTR                get
               60  LOAD_STR                 'Content-Type'
               63  CALL_FUNCTION_1       1  '1 positional, 0 named'
               66  LOAD_STR                 'CONTENT_TYPE'
               69  STORE_MAP        

 L.  45        70  LOAD_GLOBAL              len
               73  LOAD_FAST                'data'
               76  CALL_FUNCTION_1       1  '1 positional, 0 named'
               79  LOAD_STR                 'CONTENT_LENGTH'
               82  STORE_MAP        

 L.  46        83  LOAD_FAST                'urlinfo'
               86  LOAD_ATTR                query
               89  LOAD_STR                 'QUERY_STRING'
               92  STORE_MAP        

 L.  47        93  LOAD_FAST                'urlinfo'
               96  LOAD_ATTR                path
               99  LOAD_STR                 'PATH_INFO'
              102  STORE_MAP        

 L.  48       103  LOAD_FAST                'request'
              106  LOAD_ATTR                method
              109  LOAD_STR                 'REQUEST_METHOD'
              112  STORE_MAP        

 L.  49       113  LOAD_FAST                'urlinfo'
              116  LOAD_ATTR                hostname
              119  LOAD_STR                 'SERVER_NAME'
              122  STORE_MAP        

 L.  50       123  LOAD_FAST                'urlinfo'
              126  LOAD_ATTR                port
              129  JUMP_IF_TRUE_OR_POP   156  'to 156'
              132  LOAD_FAST                'urlinfo'
              135  LOAD_ATTR                scheme
              138  LOAD_STR                 'https'
              141  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   153  'to 153'
              147  LOAD_STR                 '443'
            150_0  COME_FROM           129  '129'
              150  JUMP_FORWARD        156  'to 156'
              153  ELSE                     '156'
              153  LOAD_STR                 '80'
            156_0  COME_FROM           150  '150'
              156  LOAD_STR                 'SERVER_PORT'
              159  STORE_MAP        

 L.  51       160  LOAD_STR                 'HTTP/1.1'
              163  LOAD_STR                 'SERVER_PROTOCOL'
              166  STORE_MAP        

 L.  52       167  LOAD_CONST               (1, 0)
              170  LOAD_STR                 'wsgi.version'
              173  STORE_MAP        

 L.  53       174  LOAD_FAST                'urlinfo'
              177  LOAD_ATTR                scheme
              180  LOAD_STR                 'wsgi.url_scheme'
              183  STORE_MAP        

 L.  54       184  LOAD_GLOBAL              Content
              187  LOAD_FAST                'data'
              190  CALL_FUNCTION_1       1  '1 positional, 0 named'
              193  LOAD_STR                 'wsgi.input'
              196  STORE_MAP        

 L.  55       197  LOAD_GLOBAL              sys
              200  LOAD_ATTR                stderr
              203  LOAD_STR                 'wsgi.errors'
              206  STORE_MAP        

 L.  56       207  LOAD_CONST               False
              210  LOAD_STR                 'wsgi.multiprocess'
              213  STORE_MAP        

 L.  57       214  LOAD_CONST               False
              217  LOAD_STR                 'wsgi.multithread'
              220  STORE_MAP        

 L.  58       221  LOAD_CONST               False
              224  LOAD_STR                 'wsgi.run_once'
              227  STORE_MAP        

 L.  59       228  LOAD_FAST                'urlinfo'
              231  LOAD_ATTR                scheme
              234  LOAD_STR                 'wsgi.url_scheme'
              237  STORE_MAP        
              238  STORE_FAST               'environ'

 L.  62       241  LOAD_FAST                'environ'
              244  LOAD_ATTR                update

 L.  63       247  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              250  LOAD_STR                 'WSGIAdapter.send.<locals>.<dictcomp>'
              253  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'

 L.  64       256  LOAD_FAST                'request'
              259  LOAD_ATTR                headers
              262  LOAD_ATTR                items
              265  CALL_FUNCTION_0       0  '0 positional, 0 named'
              268  GET_ITER         
              269  CALL_FUNCTION_1       1  '1 positional, 0 named'
              272  CALL_FUNCTION_1       1  '1 positional, 0 named'
              275  POP_TOP          

 L.  67       276  LOAD_GLOBAL              Response
              279  CALL_FUNCTION_0       0  '0 positional, 0 named'
              282  STORE_DEREF              'response'

 L.  69       285  LOAD_CLOSURE             'response'
              288  BUILD_TUPLE_1         1 
              291  LOAD_CODE                <code_object start_response>
              294  LOAD_STR                 'WSGIAdapter.send.<locals>.start_response'
              297  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'
              300  STORE_FAST               'start_response'

 L.  74       303  LOAD_FAST                'request'
              306  LOAD_DEREF               'response'
              309  STORE_ATTR               request

 L.  75       312  LOAD_FAST                'request'
              315  LOAD_ATTR                url
              318  LOAD_DEREF               'response'
              321  STORE_ATTR               url

 L.  77       324  LOAD_GLOBAL              Content
              327  LOAD_STR                 ''
              330  LOAD_ATTR                join
              333  LOAD_FAST                'self'
              336  LOAD_ATTR                app
              339  LOAD_FAST                'environ'
              342  LOAD_FAST                'start_response'
              345  CALL_FUNCTION_2       2  '2 positional, 0 named'
              348  CALL_FUNCTION_1       1  '1 positional, 0 named'
              351  CALL_FUNCTION_1       1  '1 positional, 0 named'
              354  LOAD_DEREF               'response'
              357  STORE_ATTR               raw

 L.  79       360  LOAD_DEREF               'response'
              363  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ELSE' instruction at offset 153

    def close(self):
        pass


class TestSession(Session):

    def __init__(self, app):
        superTestSessionself.__init__
        self.app = app
        self.mount'http://testserver'WSGIAdapter(app)

    def prepare_request(self, request):
        request.url = 'http://testserver/' + request.url.lstrip('/')
        return superTestSessionself.prepare_request(request)