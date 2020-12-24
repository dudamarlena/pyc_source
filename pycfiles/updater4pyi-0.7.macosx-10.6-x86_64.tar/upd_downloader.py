# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/updater4pyi/upd_downloader.py
# Compiled at: 2014-12-07 13:03:25
"""
Utilities to download files over secure HTTPS connections, with *server certificate
verification*.

See `Validate SSL certificates with Python <http://stackoverflow.com/q/1087227/1694896>`_
and and `this solution <http://stackoverflow.com/a/14320202/1694896>`_ on Stack Overflow.
"""
import logging, httplib, ssl, socket, shutil, urllib2
from . import upd_version
from . import util
from .upd_log import logger
CERT_FILE = util.resource_path('updater4pyi/cacert.pem')

class ValidHTTPSConnection(httplib.HTTPConnection):
    """
    HTTPS connection based on httplib.HTTPConnection, with complete certificate validation
    based on known root certificates packaged with the program.

    The root certificate file is given in the module-level variable
    :py:data:`CERT_FILE`. Note you may use :py:func:`util.resource_path` to get a file in
    the pyinstaller bundle.
    """
    default_port = httplib.HTTPS_PORT

    def __init__(self, *args, **kwargs):
        httplib.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        """
        Connect to a host on a given (SSL) port.
        """
        logger.debug('Connecting via HTTPS to %s:%d.', self.host, self.port)
        sock = socket.create_connection((self.host, self.port), self.timeout, self.source_address)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        self.sock = ssl.wrap_socket(sock, ca_certs=CERT_FILE, cert_reqs=ssl.CERT_REQUIRED)


class ValidHTTPSHandler(urllib2.HTTPSHandler):
    """
    A HTTPS urllib2 handler using :py:class:`ValidHttpsConnection`, i.e. with correct
    server certificate validation.
    """

    def https_open(self, req):
        return self.do_open(ValidHTTPSConnection, req)


url_opener = urllib2.build_opener(ValidHTTPSHandler)
url_opener.addheaders = [
 (
  'User-agent', 'Updater4Pyi-SoftwareUpdater %s' % upd_version.version_str)]