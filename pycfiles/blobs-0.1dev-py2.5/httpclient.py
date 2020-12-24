# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blobs/client/httpclient.py
# Compiled at: 2008-02-19 12:19:12
import httplib, urlparse, uuid, os, mimetypes, email.utils

def mimeencode(boundary, key, value):
    key = email.utils.quote(key)
    value = str(value)
    size = len(value)
    return '--%(boundary)s\nContent-Disposition: form-data; name="%(key)s"\nContent-Length: %(size)i\n\n%(value)s\n' % vars()


class FileProxy(object):

    def __init__(self, filename=None, file_obj=None, size=None, contentType=None):
        if filename is None:
            if file_obj is None:
                raise ValueError('At least one of filename and file_obj must be set')
            if contentType:
                self.contentType = contentType
            elif filename:
                self.contentType = mimetypes.guess_type(filename)[0]
            else:
                self.contentType = 'application/octet-stream'
            if filename:
                self.filename = filename
                self.data = None
                if not file_obj:
                    self.file_obj = file(filename)
                else:
                    self.file_obj = file_obj
                self.size = size or os.path.getsize(filename)
            else:
                self.size = size
        elif file_obj:
            if not filename:
                self.filename = 'fileobj'
            else:
                self.filename = filename
            self.file_obj = file_obj
            if not size:
                self.data = file_obj.read()
                self.size = len(self.data)
            else:
                self.size = size
        return

    def getMimeHeader(self, name, boundary):
        name = email.utils.quote(name)
        filename = email.utils.quote(self.filename)
        contentType = self.contentType
        size = self.size
        return ('--%(boundary)s\nContent-Disposition: form-data; name="%(name)s"; filename="%(filename)s"\nContent-Type: %(contentType)s\nContent-Length: %(size)i\n\n' % vars()).replace('\n', '\r\n')

    def getLen(self, name, boundary):
        return len(self.getMimeHeader(name, boundary)) + self.size


class HTTPClient(object):
    """
    Wrapper around httplib to simplify some operations
    """

    def __init__(self, url):
        if not url.startswith('http'):
            url = 'http://' + url
        (self.proto, hostport, self.baseurl) = urlparse.urlsplit(url)[:3]
        if self.proto not in ('http', 'https'):
            raise ValueError('Invalid protocol')
        if ':' in hostport:
            (self.host, self.port) = hostport.split(':', 1)
            self.port = int(self.port)
        else:
            self.host = hostport
            if self.proto == 'http':
                self.port = httplib.HTTP_PORT
            elif self.proto == 'https':
                self.port = httplib.HTTPS_PORT

    def _getConnection(self):
        if self.proto == 'http':
            return httplib.HTTPConnection(self.host, self.port, True)
        else:
            return httplib.HTTPSConnection(self.host, self.port, strict=True)

    def get(self, url, body=None, headers={}):
        """
        Requests self.baseurl / url from the server

        Returns an httplib.HTTPResponse object which supports
        a .read() method to get the response data.
        """
        url = urlparse.urljoin(self.baseurl, url)
        conn = self._getConnection()
        conn.request('GET', url, body, headers)
        return conn.getresponse()

    def post(self, url, params={}, headers={}, multipart=True):
        """
        Sends a POST request to the given URL
        Params is a dictionary of key / value pairs

        If value can be an instance of FileProxy to handle file uploads
        """
        if not multipart:
            raise NotImplementedError('Non-multipart POSTs are not yet supported')
        boundary = uuid.uuid4().hex
        headers['Content-Type'] = 'multipart/form-data; boundary=%s' % boundary
        url = urlparse.urljoin(self.baseurl, url)
        normalParts = []
        fileParts = []
        for (key, value) in params.items():
            if isinstance(value, FileProxy):
                fileParts.append((key, value))
            else:
                normalParts.append(mimeencode(boundary, key, value))

        normalParts = ('\n').join(normalParts).replace('\n', '\r\n')
        totalSize = len(normalParts)
        footer = '\r\n--%(boundary)s--\r\n' % vars()
        totalSize += len(footer)
        for (name, f) in fileParts:
            totalSize += f.getLen(name, boundary)

        headers['Content-Length'] = totalSize
        conn = self._getConnection()
        conn.putrequest('POST', url)
        for (k, v) in headers.items():
            conn.putheader(k, v)

        conn.endheaders()
        conn.send(normalParts)
        for (name, f) in fileParts:
            data = f.getMimeHeader(name, boundary)
            conn.send(data)
            if f.data:
                conn.send(f.data)
            else:
                while True:
                    data = f.file_obj.read(4096)
                    if not data:
                        break
                    conn.send(data)

        conn.send(footer)
        return conn.getresponse()

    def postFileObj(self, url, filename, fileparam, type=None, filesize=None, fileobj=None, params={}, headers={}):
        """
        POSTs a file to the given url

        params is a dictionary of other parameters to include in the POST
        body
        """
        boundary = uuid.uuid4().hex
        headers['Content-Type'] = 'multipart/form-data; boundary=%s' % boundary
        url = urlparse.urljoin(self.baseurl, url)
        if fileobj is None:
            fileobj = open(filename)
        if filesize is None:
            filesize = os.path.getsize(filename)
        if type is None:
            type = 'application/octet-stream'
        mimePieces = []
        for (k, v) in params.items():
            name = email.utils.quote(k)
            value = str(v)
            size = len(value)
            mimePieces.append('--%(boundary)s\nContent-Disposition: form-data; name="%(name)s"\nContent-Length: %(size)i\n\n%(value)s\n' % vars())

        name = email.utils.quote(fileparam)
        basename = os.path.basename(filename)
        contentType = type or 'application/octet-stream'
        mimePieces.append('--%(boundary)s\nContent-Disposition: form-data; name="%(name)s"; filename=%(basename)s\nContent-Type: %(contentType)s\nContent-Length: %(filesize)i\n\n' % vars())
        mimeHeaders = ('\n').join(mimePieces).replace('\n', '\r\n')
        totalSize = len(mimeHeaders) + filesize + len(boundary) + 4
        headers['Content-Length'] = totalSize
        conn = self._getConnection()
        conn.putrequest('POST', url)
        for (k, v) in headers.items():
            conn.putheader(k, v)

        conn.endheaders()
        conn.send(mimeHeaders)
        while True:
            data = fileobj.read(4096)
            if not data:
                break
            conn.send(data)

        conn.send('\r\n--%(boundary)s' % vars())
        return conn.getresponse()