# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/capabilities/http.py
# Compiled at: 2016-11-12 07:38:04
import base64, socket, logging
from BaseHTTPServer import BaseHTTPRequestHandler
from beeswarm.drones.honeypot.capabilities.handlerbase import HandlerBase
from beeswarm.drones.honeypot.helpers.common import send_whole_file
logger = logging.getLogger(__name__)

class BeeHTTPHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, vfs, server, httpsession, options, users):
        self.vfs = vfs
        self.users = users
        self.current_user = None
        self._options = options
        if 'banner' in self._options:
            self._banner = self._options['banner']
        else:
            self._banner = 'Microsoft-IIS/5.0'
        self._session = httpsession
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self._session.end_session()
        return

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Test"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers.getheader('Authorization') is None:
            self.do_AUTHHEAD()
            self.send_html('please_auth.html')
        else:
            hdr = self.headers.getheader('Authorization')
            _, enc_uname_pwd = hdr.split(' ')
            dec_uname_pwd = base64.b64decode(enc_uname_pwd)
            uname, pwd = dec_uname_pwd.split(':')
            if not self._session.try_auth('plaintext', username=uname, password=pwd):
                self.do_AUTHHEAD()
                self.send_html('please_auth.html')
            else:
                self.do_HEAD()
                self.send_html('index.html')
        self.request.close()
        return

    def send_html(self, filename):
        file_ = self.vfs.open(filename)
        send_whole_file(self.request.fileno(), file_.fileno())
        file_.close()

    def version_string(self):
        return self._banner

    def log_message(self, format_, *args):
        pass


class Http(HandlerBase):
    HandlerClass = BeeHTTPHandler

    def __init__(self, options, workdir):
        super(Http, self).__init__(options, workdir)
        self._options = options

    def handle_session(self, gsocket, address):
        session = self.create_session(address)
        try:
            try:
                self.HandlerClass(gsocket, address, self.vfsystem.opendir('/var/www'), None, httpsession=session, options=self._options, users=self.users)
            except socket.error as err:
                logger.debug(('Unexpected end of http session: {0}, errno: {1}. ({2})').format(err, err.errno, session.id))

        finally:
            self.close_session(session)

        return