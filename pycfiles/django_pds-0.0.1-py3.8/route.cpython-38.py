# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/middlewares/route.py
# Compiled at: 2020-05-02 08:28:14
# Size of source mod 2**32: 420 bytes
from django.middleware.http import MiddlewareMixin
from django.urls import resolve
from django.urls.resolvers import Resolver404
from django_pds.core.rest.exceptions import url_not_found

class UrlPathExistsMiddleware(MiddlewareMixin):

    def process_request--- This code section failed: ---

 L.  11         0  SETUP_FINALLY        18  'to 18'

 L.  12         2  LOAD_GLOBAL              resolve
                4  LOAD_FAST                'request'
                6  LOAD_ATTR                path
                8  CALL_FUNCTION_1       1  ''
               10  POP_TOP          

 L.  13        12  POP_BLOCK        
               14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.  14        18  DUP_TOP          
               20  LOAD_GLOBAL              Resolver404
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    44  'to 44'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  15        32  LOAD_GLOBAL              url_not_found
               34  LOAD_FAST                'request'
               36  CALL_FUNCTION_1       1  ''
               38  ROT_FOUR         
               40  POP_EXCEPT       
               42  RETURN_VALUE     
             44_0  COME_FROM            24  '24'
               44  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 16