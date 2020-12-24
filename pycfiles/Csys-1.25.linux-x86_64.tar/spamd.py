# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/spamd.py
# Compiled at: 2009-11-25 02:59:32
"""Module used to communicate with a SpamAssassin spamd process to check
or tag messages.

Usage is as follows:
  >>> conn = spamd.SpamdConnection()
  >>> conn.addheader('User', 'username')
  >>> conn.check(spamd.SYMBOLS, 'From: user@example.com
...')
  >>> print conn.getspamstatus()
  (True, 4.0)
  >>> print conn.response_message
  ...
"""
import socket, mimetools, StringIO

class error(Exception):
    pass


SPAMD_PORT = 783
SKIP = 'SKIP'
PROCESS = 'PROCESS'
CHECK = 'CHECK'
SYMBOLS = 'SYMBOLS'
REPORT = 'REPORT'
REPORT_IFSPAM = 'REPORT_IFSPAM'
EX_OK = 0
EX_USAGE = 64
EX_DATAERR = 65
EX_NOINPUT = 66
EX_NOUSER = 67
EX_NOHOST = 68
EX_UNAVAILABLE = 69
EX_SOFTWARE = 70
EX_OSERR = 71
EX_OSFILE = 72
EX_CANTCREAT = 73
EX_IOERR = 74
EX_TEMPFAIL = 75
EX_PROTOCOL = 76
EX_NOPERM = 77
EX_CONFIG = 78

class SpamdConnection(object):
    """Class to handle talking to SpamAssassin spamd servers."""
    host = 'localhost'
    port = SPAMD_PORT
    PROTOCOL_VERSION = 'SPAMC/1.3'

    def __init__(self, host='', port=0):
        if not port and ':' in host:
            host, port = host.split(':', 1)
            port = int(port)
        if host:
            self.host = host
        if port:
            self.port = port
        self.request_headers = mimetools.Message(StringIO.StringIO(), seekable=False)
        self.request_headers.fp = None
        self.server_version = None
        self.result_code = None
        self.response_message = None
        self.response_headers = mimetools.Message(StringIO.StringIO(), seekable=False)
        return

    def addheader(self, header, value):
        """Adds a header to the request."""
        self.request_headers[header] = value

    def check(self, method='PROCESS', message=''):
        """Sends a request to the spamd process."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
        except socket.error:
            raise error('could not connect to spamd on %s' % self.host)

        del self.request_headers['Content-length']
        self.request_headers['Content-length'] = str(len(message))
        request = '%s %s\r\n%s\r\n' % (
         method, self.PROTOCOL_VERSION,
         str(self.request_headers).replace('\n', '\r\n'))
        try:
            sock.send(request)
            sock.send(message)
            sock.shutdown(1)
        except (socket.error, IOError):
            raise error('could not send request to spamd')

        fp = sock.makefile('rb')
        response = fp.readline()
        words = response.split(None, 2)
        if len(words) != 3:
            raise error('not enough words in response header')
        if words[0][:6] != 'SPAMD/':
            raise error('bad protocol name in response string')
        self.server_version = float(words[0][6:])
        if self.server_version < 1.0 or self.server_version >= 2.0:
            raise error('incompatible server version')
        self.result_code = int(words[1])
        if self.result_code != 0:
            raise error('spamd server returned error %s' % words[2])
        try:
            self.response_headers = mimetools.Message(fp, seekable=False)
            self.response_headers.fp = None
        except IOError:
            raise error('could not read in response headers')

        try:
            self.response_message = fp.read()
        except IOError:
            raise error('could not read in response message')

        fp.close()
        sock.close()
        return

    def getspamstatus(self):
        """Decode the "Spam" response header."""
        if 'Spam' not in self.response_headers:
            raise error('Spam header not found in response')
        isspam, score = self.response_headers['Spam'].split(';', 1)
        isspam = isspam.strip() != 'False'
        score = float(score.split('/', 1)[0])
        return (isspam, score)