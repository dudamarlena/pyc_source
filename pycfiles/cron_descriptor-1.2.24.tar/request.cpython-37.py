# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/urllib3/urllib3/request.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 6018 bytes
from __future__ import absolute_import
from .filepost import encode_multipart_formdata
from packages.six.moves.urllib.parse import urlencode
__all__ = [
 'RequestMethods']

class RequestMethods(object):
    """RequestMethods"""
    _encode_url_methods = {
     'DELETE', 'GET', 'HEAD', 'OPTIONS'}

    def __init__(self, headers=None):
        self.headers = headers or 

    def urlopen(self, method, url, body=None, headers=None, encode_multipart=True, multipart_boundary=None, **kw):
        raise NotImplementedError('Classes extending RequestMethods must implement their own ``urlopen`` method.')

    def request(self, method, url, fields=None, headers=None, **urlopen_kw):
        """
        Make a request using :meth:`urlopen` with the appropriate encoding of
        ``fields`` based on the ``method`` used.

        This is a convenience method that requires the least amount of manual
        effort. It can be used in most situations, while still having the
        option to drop down to more specific methods when necessary, such as
        :meth:`request_encode_url`, :meth:`request_encode_body`,
        or even the lowest level :meth:`urlopen`.
        """
        method = method.upper()
        urlopen_kw['request_url'] = url
        if method in self._encode_url_methods:
            return (self.request_encode_url)(
 method, url, fields=fields, headers=headers, **urlopen_kw)
        return (self.request_encode_body)(
 method, url, fields=fields, headers=headers, **urlopen_kw)

    def request_encode_url(self, method, url, fields=None, headers=None, **urlopen_kw):
        """
        Make a request using :meth:`urlopen` with the ``fields`` encoded in
        the url. This is useful for request methods like GET, HEAD, DELETE, etc.
        """
        if headers is None:
            headers = self.headers
        extra_kw = {'headers': headers}
        extra_kw.update(urlopen_kw)
        if fields:
            url += '?' + urlencode(fields)
        return (self.urlopen)(method, url, **extra_kw)

    def request_encode_body(self, method, url, fields=None, headers=None, encode_multipart=True, multipart_boundary=None, **urlopen_kw):
        """
        Make a request using :meth:`urlopen` with the ``fields`` encoded in
        the body. This is useful for request methods like POST, PUT, PATCH, etc.

        When ``encode_multipart=True`` (default), then
        :meth:`urllib3.filepost.encode_multipart_formdata` is used to encode
        the payload with the appropriate content type. Otherwise
        :meth:`urllib.urlencode` is used with the
        'application/x-www-form-urlencoded' content type.

        Multipart encoding must be used when posting files, and it's reasonably
        safe to use it in other times too. However, it may break request
        signing, such as with OAuth.

        Supports an optional ``fields`` parameter of key/value strings AND
        key/filetuple. A filetuple is a (filename, data, MIME type) tuple where
        the MIME type is optional. For example::

            fields = {
                'foo': 'bar',
                'fakefile': ('foofile.txt', 'contents of foofile'),
                'realfile': ('barfile.txt', open('realfile').read()),
                'typedfile': ('bazfile.bin', open('bazfile').read(),
                              'image/jpeg'),
                'nonamefile': 'contents of nonamefile field',
            }

        When uploading a file, providing a filename (the first parameter of the
        tuple) is optional but recommended to best mimic behavior of browsers.

        Note that if ``headers`` are supplied, the 'Content-Type' header will
        be overwritten because it depends on the dynamic random boundary string
        which is used to compose the body of the request. The random boundary
        string can be explicitly set with the ``multipart_boundary`` parameter.
        """
        if headers is None:
            headers = self.headers
        extra_kw = {'headers': {}}
        if fields:
            if 'body' in urlopen_kw:
                raise TypeError("request got values for both 'fields' and 'body', can only specify one.")
            elif encode_multipart:
                body, content_type = encode_multipart_formdata(fields,
                  boundary=multipart_boundary)
            else:
                body, content_type = urlencode(fields), 'application/x-www-form-urlencoded'
            extra_kw['body'] = body
            extra_kw['headers'] = {'Content-Type': content_type}
        extra_kw['headers'].update(headers)
        extra_kw.update(urlopen_kw)
        return (self.urlopen)(method, url, **extra_kw)