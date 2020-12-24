# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\medusa\auth_handler.py
# Compiled at: 2015-07-18 10:13:56
RCS_ID = '$Id: auth_handler.py,v 1.6 2002/11/25 19:40:23 akuchling Exp $'
import re, sys, time
from supervisor.compat import encodestring, decodestring
from supervisor.compat import md5
from supervisor.compat import as_string, as_bytes
import supervisor.medusa.counter as counter, supervisor.medusa.default_handler as default_handler
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

    def handle_request(self, request):
        scheme = get_header(AUTHORIZATION, request.header)
        if scheme:
            scheme = scheme.lower()
            if scheme == 'basic':
                cookie = get_header(AUTHORIZATION, request.header, 2)
                try:
                    decoded = as_string(decodestring(as_bytes(cookie)))
                except:
                    sys.stderr.write('malformed authorization info <%s>\n' % cookie)
                    request.error(400)
                    return

                auth_info = decoded.split(':', 1)
                if self.authorizer.authorize(auth_info):
                    self.pass_count.increment()
                    request.auth_info = auth_info
                    self.handler.handle_request(request)
                else:
                    self.handle_unauthorized(request)
            else:
                sys.stderr.write('unknown/unsupported auth method: %s\n' % scheme)
                self.handle_unauthorized(request)
        else:
            self.handle_unauthorized(request)

    def handle_unauthorized(self, request):
        self.fail_count.increment()
        request.channel.set_terminator(None)
        request['Connection'] = 'close'
        request['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        request.error(401)
        return

    def make_nonce(self, request):
        """A digest-authentication <nonce>, constructed as suggested in RFC 2069"""
        ip = request.channel.server.ip
        now = str(long(time.time()))
        if now[-1:] == 'L':
            now = now[:-1]
        private_key = str(id(self))
        nonce = (':').join([ip, now, private_key])
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
        if username in self.dict and self.dict[username] == password:
            return 1
        else:
            return 0


AUTHORIZATION = re.compile('Authorization: ([^ ]+) (.*)', re.IGNORECASE)