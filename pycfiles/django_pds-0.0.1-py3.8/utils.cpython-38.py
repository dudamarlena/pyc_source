# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/utils.py
# Compiled at: 2020-05-02 08:44:02
# Size of source mod 2**32: 1941 bytes
import os, traceback
from django.core.exceptions import ImproperlyConfigured
from mongoengine import base

def is_abstract_document--- This code section failed: ---

 L.   9         0  SETUP_FINALLY        26  'to 26'

 L.  10         2  LOAD_GLOBAL              get_document
                4  LOAD_FAST                'document_name'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               '__doc'

 L.  11        10  LOAD_FAST                '__doc'
               12  LOAD_ATTR                _meta
               14  LOAD_METHOD              get
               16  LOAD_STR                 'abstract'
               18  LOAD_CONST               False
               20  CALL_METHOD_2         2  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY     0  '0'

 L.  12        26  DUP_TOP          
               28  LOAD_GLOBAL              BaseException
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    64  'to 64'
               34  POP_TOP          
               36  STORE_FAST               'e'
               38  POP_TOP          
               40  SETUP_FINALLY        52  'to 52'

 L.  13        42  POP_BLOCK        
               44  POP_EXCEPT       
               46  CALL_FINALLY         52  'to 52'
               48  LOAD_CONST               False
               50  RETURN_VALUE     
             52_0  COME_FROM            46  '46'
             52_1  COME_FROM_FINALLY    40  '40'
               52  LOAD_CONST               None
               54  STORE_FAST               'e'
               56  DELETE_FAST              'e'
               58  END_FINALLY      
               60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            32  '32'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

Parse error at or near `POP_EXCEPT' instruction at offset 44


def get_document--- This code section failed: ---

 L.  17         0  SETUP_FINALLY        14  'to 14'

 L.  18         2  LOAD_GLOBAL              base
                4  LOAD_METHOD              get_document
                6  LOAD_FAST                'document_name'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  19        14  DUP_TOP          
               16  LOAD_GLOBAL              BaseException
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    52  'to 52'
               22  POP_TOP          
               24  STORE_FAST               'e'
               26  POP_TOP          
               28  SETUP_FINALLY        40  'to 40'

 L.  20        30  POP_BLOCK        
               32  POP_EXCEPT       
               34  CALL_FINALLY         40  'to 40'
               36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'
             40_1  COME_FROM_FINALLY    28  '28'
               40  LOAD_CONST               None
               42  STORE_FAST               'e'
               44  DELETE_FAST              'e'
               46  END_FINALLY      
               48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            20  '20'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'

Parse error at or near `POP_EXCEPT' instruction at offset 32


def get_fields(document_name, with_auto_id=False):
    __doc = get_document(document_name)
    _fields = list(__doc._fields.keys())
    if not with_auto_id:
        elem = 'auto_id_0'
        if elem in _fields:
            _fields.removeelem
    return _fields


def origin(request):
    if request.META is not None:
        return request.META.get'HTTP_ORIGIN'


def get_host(request):
    host = origin(request)
    if host is None:
        return (True, None)
    replace = [
     'https://', 'http://', 'www.', '/']
    for item in replace:
        host = host.replaceitem''
    else:
        hosts = host.split':'
        return hosts[0]


def authorization_token(request):
    return request.META.get'HTTP_AUTHORIZATION'None


def get_content_type(request):
    return request.META.get'CONTENT_TYPE'None


def path(request):
    return str(request.META.get'PATH_INFO''')


def get_client_ip(request):
    x_forwarded_for = request.META.get'HTTP_X_FORWARDED_FOR'
    if x_forwarded_for:
        ip = x_forwarded_for.split','[0]
    else:
        ip = request.META.get'REMOTE_ADDR'
    return ip


def print_traceback():
    tb = traceback.format_exc()
    print(tb)


def get_environment--- This code section failed: ---

 L.  79         0  SETUP_FINALLY        14  'to 14'

 L.  80         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                environ
                6  LOAD_FAST                'key'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  81        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    50  'to 50'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  82        28  LOAD_FAST                'raise_exception'
               30  POP_JUMP_IF_FALSE    38  'to 38'

 L.  83        32  LOAD_GLOBAL              ImproperlyConfigured
               34  RAISE_VARARGS_1       1  'exception instance'
               36  JUMP_FORWARD         46  'to 46'
             38_0  COME_FROM            30  '30'

 L.  85        38  LOAD_FAST                'default'
               40  ROT_FOUR         
               42  POP_EXCEPT       
               44  RETURN_VALUE     
             46_0  COME_FROM            36  '36'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            20  '20'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'

Parse error at or near `POP_TOP' instruction at offset 24