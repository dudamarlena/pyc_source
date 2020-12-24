# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/wsgi.py
# Compiled at: 2020-05-04 07:52:33
# Size of source mod 2**32: 5491 bytes
"""
web2ldap.wsgi -- WSGI app wrapper eventually starting a stand-alone HTTP server

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import sys, os, socketserver, time, codecs, wsgiref.util, wsgiref.simple_server, web2ldap.app.core
from web2ldap.log import logger
import web2ldapcnf

class W2lWSGIRequestHandler(wsgiref.simple_server.WSGIRequestHandler):
    __doc__ = '\n    custom WSGIServer class\n    '


class W2lWSGIServer(wsgiref.simple_server.WSGIServer, socketserver.ThreadingMixIn):
    __doc__ = '\n    custom WSGIServer class\n    '


class WSGIBytesWrapper:

    def __init__(self, outf):
        self._outf = outf

    def set_headers(self, headers):
        self._outf.set_headers(headers)

    def write(self, buf):
        self._outf.write_bytes(buf)


class AppResponse:
    __doc__ = '\n    Application response class as file-like object\n    '

    def __init__(self):
        self.bytelen = 0
        self.lines = []
        self.headers = []
        self.reset()

    def reset(self):
        """
        reset the output completely (e.g. in case of error message)
        """
        self.bytelen = 0
        del self.lines
        self.lines = []
        del self.headers
        self.headers = []
        self._charset = None
        self.charset = 'utf-8'

    @property
    def charset(self):
        return self._charset

    @charset.setter
    def charset(self, charset):
        self._charset = charset
        codec = codecs.lookup(self._charset)
        self._uc_encode, self._uc_decode = codec[0], codec[1]

    def set_headers(self, headers):
        """
        set all HTTP headers at once
        """
        self.headers = headers

    def write(self, buf):
        """
        file-like method
        """
        assert isinstance(buf, str), TypeError('expected str for buf, but got %r', buf)
        self.write_bytes(self._uc_encode(buf, 'replace')[0])

    def write_bytes(self, buf):
        assert isinstance(buf, bytes), TypeError('expected bytes for buf, but got %r', buf)
        self.lines.append(buf)
        self.bytelen += len(buf)

    def close(self):
        """
        file-like method
        """
        del self.lines


import web2ldap.app.handler

def application--- This code section failed: ---

 L. 118         0  LOAD_FAST                'environ'
                2  LOAD_STR                 'REQUEST_METHOD'
                4  BINARY_SUBSCR    
                6  LOAD_CONST               {'POST', 'GET'}
                8  COMPARE_OP               not-in
               10  POP_JUMP_IF_FALSE    44  'to 44'

 L. 119        12  LOAD_GLOBAL              logger
               14  LOAD_METHOD              error
               16  LOAD_STR                 'Invalid HTTP request method %r'
               18  LOAD_FAST                'environ'
               20  LOAD_STR                 'REQUEST_METHOD'
               22  BINARY_SUBSCR    
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          

 L. 120        28  LOAD_FAST                'start_response'
               30  LOAD_STR                 '400 invalid request'
               32  LOAD_CONST               ('Content-type', 'text/plain')
               34  CALL_FUNCTION_2       2  ''
               36  POP_TOP          

 L. 121        38  LOAD_STR                 '400 - Invalid request.'
               40  BUILD_LIST_1          1 
               42  RETURN_VALUE     
             44_0  COME_FROM            10  '10'

 L. 123        44  LOAD_FAST                'environ'
               46  LOAD_STR                 'PATH_INFO'
               48  BINARY_SUBSCR    
               50  LOAD_METHOD              startswith
               52  LOAD_STR                 '/css/web2ldap'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE   242  'to 242'

 L. 124        58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_METHOD              join

 L. 125        64  LOAD_GLOBAL              web2ldapcnf
               66  LOAD_ATTR                etc_dir

 L. 126        68  LOAD_STR                 'css'

 L. 127        70  LOAD_GLOBAL              os
               72  LOAD_ATTR                path
               74  LOAD_METHOD              basename
               76  LOAD_FAST                'environ'
               78  LOAD_STR                 'PATH_INFO'
               80  BINARY_SUBSCR    
               82  CALL_METHOD_1         1  ''

 L. 124        84  CALL_METHOD_3         3  ''
               86  STORE_FAST               'css_filename'

 L. 129        88  SETUP_FINALLY       158  'to 158'

 L. 130        90  LOAD_GLOBAL              os
               92  LOAD_METHOD              stat
               94  LOAD_FAST                'css_filename'
               96  CALL_METHOD_1         1  ''
               98  LOAD_ATTR                st_size
              100  STORE_FAST               'css_size'

 L. 131       102  LOAD_GLOBAL              open
              104  LOAD_FAST                'css_filename'
              106  LOAD_STR                 'rb'
              108  CALL_FUNCTION_2       2  ''
              110  STORE_FAST               'css_file'

 L. 133       112  LOAD_CONST               ('Content-type', 'text/css')

 L. 134       114  LOAD_STR                 'Content-Length'
              116  LOAD_GLOBAL              str
              118  LOAD_FAST                'css_size'
              120  CALL_FUNCTION_1       1  ''
              122  BUILD_TUPLE_2         2 

 L. 132       124  BUILD_LIST_2          2 
              126  STORE_FAST               'css_http_headers'

 L. 136       128  LOAD_FAST                'css_http_headers'
              130  LOAD_METHOD              extend
              132  LOAD_GLOBAL              web2ldapcnf
              134  LOAD_ATTR                http_headers
              136  LOAD_METHOD              items
              138  CALL_METHOD_0         0  ''
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          

 L. 137       144  LOAD_FAST                'start_response'
              146  LOAD_STR                 '200 OK'
              148  LOAD_FAST                'css_http_headers'
              150  CALL_FUNCTION_2       2  ''
              152  POP_TOP          
              154  POP_BLOCK        
              156  JUMP_FORWARD        230  'to 230'
            158_0  COME_FROM_FINALLY    88  '88'

 L. 138       158  DUP_TOP          
              160  LOAD_GLOBAL              IOError
              162  LOAD_GLOBAL              OSError
              164  BUILD_TUPLE_2         2 
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   228  'to 228'
              170  POP_TOP          
              172  STORE_FAST               'err'
              174  POP_TOP          
              176  SETUP_FINALLY       216  'to 216'

 L. 139       178  LOAD_GLOBAL              logger
              180  LOAD_METHOD              error
              182  LOAD_STR                 'Error reading CSS file %r: %s'
              184  LOAD_FAST                'css_filename'
              186  LOAD_FAST                'err'
              188  CALL_METHOD_3         3  ''
              190  POP_TOP          

 L. 140       192  LOAD_FAST                'start_response'
              194  LOAD_STR                 '404 not found'
              196  LOAD_CONST               ('Content-type', 'text/plain')
              198  CALL_FUNCTION_2       2  ''
              200  POP_TOP          

 L. 141       202  LOAD_STR                 '404 - CSS file not found.'
              204  BUILD_LIST_1          1 
              206  ROT_FOUR         
              208  POP_BLOCK        
              210  POP_EXCEPT       
              212  CALL_FINALLY        216  'to 216'
              214  RETURN_VALUE     
            216_0  COME_FROM           212  '212'
            216_1  COME_FROM_FINALLY   176  '176'
              216  LOAD_CONST               None
              218  STORE_FAST               'err'
              220  DELETE_FAST              'err'
              222  END_FINALLY      
              224  POP_EXCEPT       
              226  JUMP_FORWARD        242  'to 242'
            228_0  COME_FROM           168  '168'
              228  END_FINALLY      
            230_0  COME_FROM           156  '156'

 L. 143       230  LOAD_GLOBAL              wsgiref
              232  LOAD_ATTR                util
              234  LOAD_METHOD              FileWrapper
              236  LOAD_FAST                'css_file'
              238  CALL_METHOD_1         1  ''
              240  RETURN_VALUE     
            242_0  COME_FROM           226  '226'
            242_1  COME_FROM            56  '56'

 L. 144       242  LOAD_FAST                'environ'
              244  LOAD_STR                 'SCRIPT_NAME'
              246  BINARY_SUBSCR    
          248_250  POP_JUMP_IF_TRUE    264  'to 264'

 L. 145       252  LOAD_GLOBAL              wsgiref
              254  LOAD_ATTR                util
              256  LOAD_METHOD              shift_path_info
              258  LOAD_FAST                'environ'
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
            264_0  COME_FROM           248  '248'

 L. 146       264  LOAD_GLOBAL              AppResponse
              266  CALL_FUNCTION_0       0  ''
              268  STORE_FAST               'outf'

 L. 147       270  LOAD_GLOBAL              web2ldap
              272  LOAD_ATTR                app
              274  LOAD_ATTR                handler
              276  LOAD_METHOD              AppHandler
              278  LOAD_FAST                'environ'
              280  LOAD_FAST                'outf'
              282  CALL_METHOD_2         2  ''
              284  STORE_FAST               'app'

 L. 148       286  LOAD_FAST                'app'
              288  LOAD_METHOD              run
              290  CALL_METHOD_0         0  ''
              292  POP_TOP          

 L. 149       294  LOAD_GLOBAL              logger
              296  LOAD_METHOD              debug

 L. 150       298  LOAD_STR                 'Executing %s.run() took %0.3f secs'

 L. 151       300  LOAD_FAST                'app'
              302  LOAD_ATTR                __class__
              304  LOAD_ATTR                __name__

 L. 152       306  LOAD_GLOBAL              time
              308  LOAD_METHOD              time
              310  CALL_METHOD_0         0  ''
              312  LOAD_FAST                'app'
              314  LOAD_ATTR                current_access_time
              316  BINARY_SUBTRACT  

 L. 149       318  CALL_METHOD_3         3  ''
              320  POP_TOP          

 L. 154       322  LOAD_FAST                'outf'
              324  LOAD_ATTR                headers
              326  LOAD_METHOD              append
              328  LOAD_STR                 'Content-Length'
              330  LOAD_GLOBAL              str
              332  LOAD_FAST                'outf'
              334  LOAD_ATTR                bytelen
              336  CALL_FUNCTION_1       1  ''
              338  BUILD_TUPLE_2         2 
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          

 L. 155       344  LOAD_FAST                'start_response'
              346  LOAD_STR                 '200 OK'
              348  LOAD_FAST                'outf'
              350  LOAD_ATTR                headers
              352  CALL_FUNCTION_2       2  ''
              354  POP_TOP          

 L. 156       356  LOAD_FAST                'outf'
              358  LOAD_ATTR                lines
              360  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 208


def run_standalone():
    """
    start a simple stand-alone web server
    """
    logger.debug('Start stand-alone WSGI server')
    if len(sys.argv) == 1:
        host_arg = '127.0.0.1'
        port_arg = 1760
    else:
        if len(sys.argv) == 2:
            host_arg = '127.0.0.1'
            port_arg = int(sys.argv[1])
        else:
            if len(sys.argv) == 3:
                port_arg = int(sys.argv[2])
                host_arg = sys.argv[1]
            else:
                raise ValueError('Command-line arguments must be: [host] port')
    with wsgiref.simple_server.make_server(host_arg,
      port_arg,
      application,
      server_class=W2lWSGIServer,
      handler_class=W2lWSGIRequestHandler) as (httpd):
        host, port = httpd.socket.getsockname()
        logger.info'Serving http://%s:%s/web2ldap'hostport
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

    logger.info'Stopped service http://%s:%s/web2ldap'hostport
    web2ldap.app.session.cleanUpThread.enabled = 0


if __name__ == '__main__':
    run_standalone()