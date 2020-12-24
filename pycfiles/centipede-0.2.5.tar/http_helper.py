# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/primitives/http_helper.py
# Compiled at: 2015-10-26 01:57:11
import pycurl, re
from StringIO import StringIO

class ICHTTPConnection:

    def __init__(self, host='127.0.0.1', port=None, timeout=10):
        self.headers = {}
        self.body = None
        self.reason = None
        self.status = 0
        self.host = host
        self.port = port
        self.timeout = timeout
        return

    def header_function(self, header_line):
        if self.reason is None:
            reason = re.match('^HTTP/\\d\\.\\d \\d{3} (\\w+)', header_line)
            if reason is not None:
                self.reason = reason.group(1)
        if ':' not in header_line:
            return
        else:
            name, value = header_line.split(':', 1)
            name = name.strip()
            value = value.strip()
            self.headers[name] = value
            return

    def request(self, path='/', header=None, ssl=False, timeout=None):
        if timeout is None:
            timeout = self.timeout
        buf = StringIO()
        c = pycurl.Curl()
        if header:
            slist = []
            for key, value in header.iteritems():
                slist.append(key + ': ' + value)

            c.setopt(pycurl.HTTPHEADER, slist)
        c.setopt(pycurl.HEADERFUNCTION, self.header_function)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.WRITEDATA, buf)
        c.setopt(pycurl.TIMEOUT, timeout)
        c.setopt(pycurl.ENCODING, 'identity')
        if ssl:
            if self.port is None:
                self.port = 443
            c.setopt(pycurl.URL, 'https://' + self.host + ':' + str(self.port) + path)
            c.setopt(pycurl.SSL_VERIFYPEER, 1)
            c.setopt(pycurl.SSL_VERIFYHOST, 2)
        else:
            if self.port is None:
                self.port = 80
            c.setopt(pycurl.URL, 'http://' + self.host + ':' + str(self.port) + path)
        c.perform()
        self.status = c.getinfo(pycurl.RESPONSE_CODE)
        c.close()
        encoding = None
        if 'content-type' in self.headers:
            content_type = self.headers['content-type'].lower()
            match = re.search('charset=(\\S+)', content_type)
            if match:
                encoding = match.group(1)
        if encoding is None:
            encoding = 'iso-8859-1'
        self.body = buf.getvalue().decode(encoding)
        return

    def getHeaders(self):
        return self.headers

    def getBody(self):
        return self.body

    def getStatus(self):
        return self.status

    def getReason(self):
        return self.reason