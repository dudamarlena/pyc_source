# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/middlewares/authentication/authentication.py
# Compiled at: 2020-05-05 15:56:26
# Size of source mod 2**32: 2016 bytes
import jwt
import django.core.cache as cache
from django.middleware.http import MiddlewareMixin
from django_pds.conf import settings
from django_pds.core.rest.exceptions import access_denied, server_error
from django_pds.core.utils import authorization_token, path
from .settings import conf
TOKEN_MISSING = 'Authorization token not found in the request headers'
INVALID_TOKEN = 'Invalid authentication token'
ACCESS_DENIED = 'Access denied'
TOKEN_AUTH_KEY_NOT_SET = 'Token secret key not set'
audience = settings.JWT_TOKEN_AUDIENCE
algorithm = settings.JWT_TOKEN_ALGORITHM
auth_key = getattr(settings, 'JWT_TOKEN_SECRET_KEY', None)

class AuthenticationMiddleware(MiddlewareMixin):

    def process_request--- This code section failed: ---

 L.  24         0  LOAD_GLOBAL              path
                2  LOAD_FAST                'request'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'url'

 L.  26         8  LOAD_GLOBAL              auth_key
               10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  27        12  LOAD_GLOBAL              server_error
               14  LOAD_FAST                'request'
               16  LOAD_GLOBAL              TOKEN_AUTH_KEY_NOT_SET
               18  LOAD_CONST               ('message',)
               20  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               22  RETURN_VALUE     
             24_0  COME_FROM            10  '10'

 L.  29        24  LOAD_GLOBAL              authorization_token
               26  LOAD_FAST                'request'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'bearer_token'

 L.  31        32  LOAD_CONST               True
               34  STORE_FAST               'flag'

 L.  33        36  LOAD_GLOBAL              conf
               38  LOAD_ATTR                SESSION_MIDDLEWARE_EXEMPT_URLS
               40  GET_ITER         
             42_0  COME_FROM            54  '54'
               42  FOR_ITER             62  'to 62'
               44  STORE_FAST               'exempt_url'

 L.  34        46  LOAD_FAST                'url'
               48  LOAD_METHOD              endswith
               50  LOAD_FAST                'exempt_url'
               52  CALL_METHOD_1         1  ''
               54  POP_JUMP_IF_FALSE    42  'to 42'

 L.  35        56  LOAD_CONST               False
               58  STORE_FAST               'flag'
               60  JUMP_BACK            42  'to 42'

 L.  37        62  LOAD_FAST                'flag'
               64  POP_JUMP_IF_TRUE     70  'to 70'

 L.  38        66  LOAD_CONST               None
               68  RETURN_VALUE     
             70_0  COME_FROM            64  '64'

 L.  40        70  LOAD_FAST                'bearer_token'
               72  LOAD_CONST               None
               74  COMPARE_OP               is
               76  POP_JUMP_IF_FALSE    88  'to 88'

 L.  41        78  LOAD_GLOBAL              access_denied
               80  LOAD_FAST                'request'
               82  LOAD_GLOBAL              TOKEN_MISSING
               84  CALL_FUNCTION_2       2  ''
               86  RETURN_VALUE     
             88_0  COME_FROM            76  '76'

 L.  43        88  SETUP_FINALLY       238  'to 238'

 L.  45        90  LOAD_GLOBAL              str
               92  LOAD_GLOBAL              hash
               94  LOAD_FAST                'bearer_token'
               96  CALL_FUNCTION_1       1  ''
               98  CALL_FUNCTION_1       1  ''
              100  STORE_FAST               'token_hash'

 L.  46       102  LOAD_GLOBAL              cache
              104  LOAD_METHOD              get
              106  LOAD_FAST                'token_hash'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'payload'

 L.  48       112  LOAD_FAST                'payload'
              114  LOAD_CONST               None
              116  COMPARE_OP               is
              118  POP_JUMP_IF_FALSE   174  'to 174'

 L.  49       120  LOAD_FAST                'bearer_token'
              122  LOAD_METHOD              split
              124  CALL_METHOD_0         0  ''
              126  STORE_FAST               'token'

 L.  50       128  LOAD_GLOBAL              jwt
              130  LOAD_ATTR                decode
              132  LOAD_FAST                'token'
              134  LOAD_CONST               1
              136  BINARY_SUBSCR    
              138  LOAD_GLOBAL              auth_key
              140  LOAD_GLOBAL              audience
              142  LOAD_STR                 'utf-8'
              144  LOAD_GLOBAL              algorithm
              146  LOAD_CONST               ('audience', 'unicode', 'algorithms')
              148  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              150  STORE_FAST               'payload'

 L.  51       152  LOAD_FAST                'payload'
              154  LOAD_CONST               None
              156  COMPARE_OP               is
              158  POP_JUMP_IF_FALSE   174  'to 174'

 L.  52       160  LOAD_GLOBAL              access_denied
              162  LOAD_FAST                'request'
              164  LOAD_GLOBAL              INVALID_TOKEN
              166  LOAD_CONST               ('message',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_BLOCK        
              172  RETURN_VALUE     
            174_0  COME_FROM           158  '158'
            174_1  COME_FROM           118  '118'

 L.  54       174  LOAD_FAST                'payload'
              176  LOAD_METHOD              get
              178  LOAD_STR                 'logged_in'
              180  LOAD_CONST               False
              182  CALL_METHOD_2         2  ''
              184  STORE_FAST               'auth'

 L.  56       186  LOAD_GLOBAL              conf
              188  LOAD_ATTR                AUTH_NOT_REQUIRED_URLS
              190  GET_ITER         
            192_0  COME_FROM           204  '204'
              192  FOR_ITER            212  'to 212'
              194  STORE_FAST               'exempt_url'

 L.  57       196  LOAD_FAST                'url'
              198  LOAD_METHOD              endswith
              200  LOAD_FAST                'exempt_url'
              202  CALL_METHOD_1         1  ''
              204  POP_JUMP_IF_FALSE   192  'to 192'

 L.  58       206  LOAD_CONST               True
              208  STORE_FAST               'auth'
              210  JUMP_BACK           192  'to 192'

 L.  60       212  LOAD_FAST                'auth'
              214  POP_JUMP_IF_FALSE   222  'to 222'

 L.  61       216  POP_BLOCK        
              218  LOAD_CONST               None
              220  RETURN_VALUE     
            222_0  COME_FROM           214  '214'

 L.  63       222  LOAD_GLOBAL              access_denied
              224  LOAD_FAST                'request'
              226  LOAD_GLOBAL              ACCESS_DENIED
              228  CALL_FUNCTION_2       2  ''
              230  POP_BLOCK        
              232  RETURN_VALUE     
              234  POP_BLOCK        
              236  JUMP_FORWARD        292  'to 292'
            238_0  COME_FROM_FINALLY    88  '88'

 L.  64       238  DUP_TOP          
              240  LOAD_GLOBAL              BaseException
              242  COMPARE_OP               exception-match
          244_246  POP_JUMP_IF_FALSE   290  'to 290'
              248  POP_TOP          
              250  STORE_FAST               'e'
              252  POP_TOP          
              254  SETUP_FINALLY       278  'to 278'

 L.  65       256  LOAD_GLOBAL              access_denied
              258  LOAD_FAST                'request'
              260  LOAD_GLOBAL              str
              262  LOAD_FAST                'e'
              264  CALL_FUNCTION_1       1  ''
              266  CALL_FUNCTION_2       2  ''
              268  ROT_FOUR         
              270  POP_BLOCK        
              272  POP_EXCEPT       
              274  CALL_FINALLY        278  'to 278'
              276  RETURN_VALUE     
            278_0  COME_FROM           274  '274'
            278_1  COME_FROM_FINALLY   254  '254'
              278  LOAD_CONST               None
              280  STORE_FAST               'e'
              282  DELETE_FAST              'e'
              284  END_FINALLY      
              286  POP_EXCEPT       
              288  JUMP_FORWARD        292  'to 292'
            290_0  COME_FROM           244  '244'
              290  END_FINALLY      
            292_0  COME_FROM           288  '288'
            292_1  COME_FROM           236  '236'

Parse error at or near `LOAD_CONST' instruction at offset 218