# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/primitives/http_helper.py
# Compiled at: 2016-02-15 11:05:27
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
        c.setopt(pycurl.NOSIGNAL, 1)
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