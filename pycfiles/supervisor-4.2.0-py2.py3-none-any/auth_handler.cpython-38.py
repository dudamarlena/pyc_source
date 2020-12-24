# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/auth_handler.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 4990 bytes
RCS_ID = '$Id: auth_handler.py,v 1.6 2002/11/25 19:40:23 akuchling Exp $'
import re, sys, time
from supervisor.compat import as_string, as_bytes
from supervisor.compat import encodestring, decodestring
from supervisor.compat import long
from supervisor.compat import md5
import supervisor.medusa.counter as counter
import supervisor.medusa.default_handler as default_handler
get_header = default_handler.get_header
import supervisor.medusa.producers as producers

class auth_handler:

    def __init__(self, dict, handler, realm='default'):
        self.authorizer = dictionary_authorizer(dict)
        self.handler = handler
        self.realm = realm
        self.pass_count = counter.counter()
        self.fail_count = counter.counter()

    def match(self, request):
        return self.handler.match(request)

    def handle_request--- This code section failed: ---

 L.  48         0  LOAD_GLOBAL              get_header
                2  LOAD_GLOBAL              AUTHORIZATION
                4  LOAD_FAST                'request'
                6  LOAD_ATTR                header
                8  CALL_FUNCTION_2       2  ''
               10  STORE_FAST               'scheme'

 L.  50        12  LOAD_FAST                'scheme'
               14  POP_JUMP_IF_FALSE   202  'to 202'

 L.  51        16  LOAD_FAST                'scheme'
               18  LOAD_METHOD              lower
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'scheme'

 L.  52        24  LOAD_FAST                'scheme'
               26  LOAD_STR                 'basic'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE   174  'to 174'

 L.  53        32  LOAD_GLOBAL              get_header
               34  LOAD_GLOBAL              AUTHORIZATION
               36  LOAD_FAST                'request'
               38  LOAD_ATTR                header
               40  LOAD_CONST               2
               42  CALL_FUNCTION_3       3  ''
               44  STORE_FAST               'cookie'

 L.  54        46  SETUP_FINALLY        68  'to 68'

 L.  55        48  LOAD_GLOBAL              as_string
               50  LOAD_GLOBAL              decodestring
               52  LOAD_GLOBAL              as_bytes
               54  LOAD_FAST                'cookie'
               56  CALL_FUNCTION_1       1  ''
               58  CALL_FUNCTION_1       1  ''
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'decoded'
               64  POP_BLOCK        
               66  JUMP_FORWARD        108  'to 108'
             68_0  COME_FROM_FINALLY    46  '46'

 L.  56        68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  57        74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                stderr
               78  LOAD_METHOD              write
               80  LOAD_STR                 'malformed authorization info <%s>\n'
               82  LOAD_FAST                'cookie'
               84  BINARY_MODULO    
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L.  58        90  LOAD_FAST                'request'
               92  LOAD_METHOD              error
               94  LOAD_CONST               400
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L.  59       100  POP_EXCEPT       
              102  LOAD_CONST               None
              104  RETURN_VALUE     
              106  END_FINALLY      
            108_0  COME_FROM            66  '66'

 L.  60       108  LOAD_FAST                'decoded'
              110  LOAD_METHOD              split
              112  LOAD_STR                 ':'
              114  LOAD_CONST               1
              116  CALL_METHOD_2         2  ''
              118  STORE_FAST               'auth_info'

 L.  61       120  LOAD_FAST                'self'
              122  LOAD_ATTR                authorizer
              124  LOAD_METHOD              authorize
              126  LOAD_FAST                'auth_info'
              128  CALL_METHOD_1         1  ''
              130  POP_JUMP_IF_FALSE   162  'to 162'

 L.  62       132  LOAD_FAST                'self'
              134  LOAD_ATTR                pass_count
              136  LOAD_METHOD              increment
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          

 L.  63       142  LOAD_FAST                'auth_info'
              144  LOAD_FAST                'request'
              146  STORE_ATTR               auth_info

 L.  64       148  LOAD_FAST                'self'
              150  LOAD_ATTR                handler
              152  LOAD_METHOD              handle_request
              154  LOAD_FAST                'request'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
              160  JUMP_ABSOLUTE       200  'to 200'
            162_0  COME_FROM           130  '130'

 L.  66       162  LOAD_FAST                'self'
              164  LOAD_METHOD              handle_unauthorized
              166  LOAD_FAST                'request'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  JUMP_ABSOLUTE       212  'to 212'
            174_0  COME_FROM            30  '30'

 L.  70       174  LOAD_GLOBAL              sys
              176  LOAD_ATTR                stderr
              178  LOAD_METHOD              write
              180  LOAD_STR                 'unknown/unsupported auth method: %s\n'
              182  LOAD_FAST                'scheme'
              184  BINARY_MODULO    
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L.  71       190  LOAD_FAST                'self'
              192  LOAD_METHOD              handle_unauthorized
              194  LOAD_FAST                'request'
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
              200  JUMP_FORWARD        212  'to 212'
            202_0  COME_FROM            14  '14'

 L.  80       202  LOAD_FAST                'self'
              204  LOAD_METHOD              handle_unauthorized
              206  LOAD_FAST                'request'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
            212_0  COME_FROM           200  '200'

Parse error at or near `LOAD_CONST' instruction at offset 102

    def handle_unauthorized(self, request):
        self.fail_count.increment()
        request.channel.set_terminator(None)
        request['Connection'] = 'close'
        request['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        request.error(401)

    def make_nonce(self, request):
        """A digest-authentication <nonce>, constructed as suggested in RFC 2069"""
        ip = request.channel.server.ip
        now = str(long(time.time()))
        if now[-1:] == 'L':
            now = now[:-1]
        private_key = str(id(self))
        nonce = ':'.join([ip, now, private_key])
        return self.apply_hash(nonce)

    def apply_hash(self, s):
        """Apply MD5 to a string <s>, then wrap it in base64 encoding."""
        m = md5()
        m.update(s)
        d = m.digest()
        return encodestring(d)[:-1]

    def status(self):
        r = [
         producers.simple_producer('<li>Authorization Extension : <b>Unauthorized requests:</b> %s<ul>' % self.fail_count)]
        if hasattr(self.handler, 'status'):
            r.append(self.handler.status())
        r.append(producers.simple_producer('</ul>'))
        return producers.composite_producer(r)


class dictionary_authorizer:

    def __init__(self, dict):
        self.dict = dict

    def authorize(self, auth_info):
        username, password = auth_info
        if username in self.dict:
            if self.dict[username] == password:
                return 1
        return 0


AUTHORIZATION = re.compile('Authorization: ([^ ]+) (.*)', re.IGNORECASE)