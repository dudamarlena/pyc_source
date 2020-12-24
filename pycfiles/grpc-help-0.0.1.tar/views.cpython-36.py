# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caowenbin/xuetangx/grpc-help/grpc_help/views.py
# Compiled at: 2019-02-11 21:57:54
# Size of source mod 2**32: 5445 bytes
import re, logging, traceback
from collections import Iterable
import grpc, sys
from google.protobuf.json_format import MessageToDict, ParseDict
from grpc_help.exceptions import RpcException, NotAuthenticatedError
from grpc_help.utils import json_encode, async_to_sync
logger = logging.getLogger(__name__)
SENSITIVE_CREDENTIALS = re.compile('api|token|key|secret|password|signature|pwd', re.I)
CLEANSED_SUBSTITUTE = '********************'

class GenericRpcView:
    auth_user_meta_key = 'auth_user'
    proto_response_class = None
    requires_authentication = False

    def __init__(self, request, content):
        assert self.proto_response_class, 'Missing proto_response_class declaration'
        self.request = request
        self._data = None
        self.content = content

    @property
    def data(self):
        if self._data is not None:
            return self._data
        else:
            if isinstance(self.request, Iterable):
                self._data = tuple(MessageToDict(r, preserving_proto_field_name=True) for r in self.request)
            else:
                self._data = MessageToDict((self.request), preserving_proto_field_name=True)
            return self._data

    def perform_authentication(self):
        if not self.requires_authentication:
            return
        user_data = dict(self.content.invocation_metadata()).get(self.auth_user_meta_key, None)
        if not user_data:
            raise NotAuthenticatedError

    def view_handle(self, *args, **kwargs):
        raise NotImplementedError

    def finalize_response(self, response):
        proto_response_instance = self.proto_response_class()
        return ParseDict(response, proto_response_instance, ignore_unknown_fields=True)

    def __call__(self, *args, **kwargs):
        try:
            self.perform_authentication()
            result = (self.view_handle)(*args, **kwargs)
            return self.finalize_response(result)
        except Exception as e:
            self.exception_handle(e)
            return self.proto_response_class()

    @staticmethod
    def clean_credentials(credentials):
        if isinstance(credentials, (type(None), list, tuple, set)):
            return credentials
        else:
            result = {}
            for key, value in credentials.items():
                key = key.decode() if isinstance(key, bytes) else str(key)
                if SENSITIVE_CREDENTIALS.search(key):
                    result[key] = CLEANSED_SUBSTITUTE
                else:
                    result[key] = value

            return result

    def record_log(self, status_code, exc_info, **kwargs):
        params = self.clean_credentials(self.data)
        exc = exc_info[1]
        if hasattr(exc, 'message'):
            error_info = exc.message
        else:
            if hasattr(exc, 'messages'):
                error_info = exc.messages
            else:
                if hasattr(exc, 'detail'):
                    error_info = exc.detail
                else:
                    error_info = ''
        log_context = {'request_protocol':'grpc', 
         'invocation_metadata':dict(self.content.invocation_metadata()), 
         'request_data':params, 
         'status_code':str(status_code), 
         'reason':error_info}
        if kwargs:
            (log_context.update)(**kwargs)
        log_context = json_encode(log_context)
        logger.error(log_context, exc_info=True)

    def exception_handle(self, exc):
        if issubclass(exc.__class__, RpcException):
            status_code, message = exc.status_code, str(exc)
        else:
            status_code = grpc.StatusCode.UNKNOWN
            exc_info = sys.exc_info()
            try:
                self.record_log(status_code, exc_info)
            except Exception:
                logger.error('Exception in exception handler', exc_info=True)

            status_code = grpc.StatusCode.UNKNOWN
            message = f"{exc}; reason: {traceback.format_exc()}"
        self.content.set_code(status_code)
        self.content.set_details(message)


class StreamRpcView(GenericRpcView):

    def __call__(self, *args, **kwargs):
        try:
            self.perform_authentication()
            results = (self.view_handle)(*args, **kwargs)
            for result in results:
                yield self.finalize_response(result)

        except Exception as e:
            self.exception_handle(e)
            yield self.proto_response_class()


class AsyncGenericRpcView(GenericRpcView):

    async def view_handle(self, *args, **kwargs):
        raise NotImplementedError

    @async_to_sync
    async def __call__(self, *args, **kwargs):
        try:
            self.perform_authentication()
            result = await (self.view_handle)(*args, **kwargs)
            return self.finalize_response(result)
        except Exception as e:
            self.exception_handle(e)
            return self.proto_response_class()


class AsyncStreamRpcView(AsyncGenericRpcView):

    @async_to_sync
    async def __call__--- This code section failed: ---

 L. 153         0  SETUP_EXCEPT        120  'to 120'

 L. 154         2  LOAD_FAST                'self'
                4  LOAD_ATTR                perform_authentication
                6  CALL_FUNCTION_0       0  '0 positional arguments'
                8  POP_TOP          

 L. 155        10  LOAD_FAST                'self'
               12  LOAD_ATTR                view_handle
               14  LOAD_FAST                'args'
               16  LOAD_FAST                'kwargs'
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'results'

 L. 156        22  LOAD_GLOBAL              hasattr
               24  LOAD_FAST                'results'
               26  LOAD_STR                 '__aiter__'
               28  CALL_FUNCTION_2       2  '2 positional arguments'
               30  POP_JUMP_IF_FALSE    98  'to 98'

 L. 157        32  SETUP_LOOP           96  'to 96'
               34  LOAD_FAST                'results'
               36  GET_AITER        
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  SETUP_EXCEPT         56  'to 56'
               44  GET_ANEXT        
               46  LOAD_CONST               None
               48  YIELD_FROM       
               50  STORE_FAST               'result'
               52  POP_BLOCK        
               54  JUMP_FORWARD         78  'to 78'
             56_0  COME_FROM_EXCEPT     42  '42'
               56  DUP_TOP          
               58  LOAD_GLOBAL              StopAsyncIteration
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    76  'to 76'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          
               70  POP_EXCEPT       
               72  POP_BLOCK        
               74  JUMP_ABSOLUTE       116  'to 116'
               76  END_FINALLY      
             78_0  COME_FROM            54  '54'

 L. 158        78  LOAD_FAST                'self'
               80  LOAD_ATTR                finalize_response
               82  LOAD_FAST                'result'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  YIELD_VALUE      
               88  POP_TOP          
               90  JUMP_BACK            42  'to 42'
               92  POP_BLOCK        
               94  JUMP_ABSOLUTE       116  'to 116'
             96_0  COME_FROM_LOOP       32  '32'
               96  JUMP_FORWARD        116  'to 116'
               98  ELSE                     '116'

 L. 160        98  LOAD_FAST                'self'
              100  LOAD_ATTR                finalize_response
              102  LOAD_FAST                'results'
              104  GET_AWAITABLE    
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  YIELD_VALUE      
              114  POP_TOP          
            116_0  COME_FROM            96  '96'
              116  POP_BLOCK        
              118  JUMP_FORWARD        174  'to 174'
            120_0  COME_FROM_EXCEPT      0  '0'

 L. 162       120  DUP_TOP          
              122  LOAD_GLOBAL              Exception
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   172  'to 172'
              128  POP_TOP          
              130  STORE_FAST               'e'
              132  POP_TOP          
              134  SETUP_FINALLY       162  'to 162'

 L. 163       136  LOAD_FAST                'self'
              138  LOAD_ATTR                exception_handle
              140  LOAD_FAST                'e'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  POP_TOP          

 L. 164       146  LOAD_FAST                'self'
              148  LOAD_ATTR                proto_response_class
              150  CALL_FUNCTION_0       0  '0 positional arguments'
              152  YIELD_VALUE      
              154  POP_TOP          
              156  POP_BLOCK        
              158  POP_EXCEPT       
              160  LOAD_CONST               None
            162_0  COME_FROM_FINALLY   134  '134'
              162  LOAD_CONST               None
              164  STORE_FAST               'e'
              166  DELETE_FAST              'e'
              168  END_FINALLY      
              170  JUMP_FORWARD        174  'to 174'
              172  END_FINALLY      
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           118  '118'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 94