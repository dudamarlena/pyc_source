# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/requests-toolbelt/requests_toolbelt/multipart/decoder.py
# Compiled at: 2020-01-10 16:25:32
# Size of source mod 2**32: 4861 bytes
"""

requests_toolbelt.multipart.decoder
===================================

This holds all the implementation details of the MultipartDecoder

"""
import sys, email.parser
from .encoder import encode_with
from requests.structures import CaseInsensitiveDict

def _split_on_find(content, bound):
    point = content.find(bound)
    return (content[:point], content[point + len(bound):])


class ImproperBodyPartContentException(Exception):
    pass


class NonMultipartContentTypeException(Exception):
    pass


def _header_parser(string, encoding):
    major = sys.version_info[0]
    if major == 3:
        string = string.decode(encoding)
    headers = email.parser.HeaderParser().parsestr(string).items()
    return ((encode_with(k, encoding), encode_with(v, encoding)) for k, v in headers)


class BodyPart(object):
    __doc__ = '\n\n    The ``BodyPart`` object is a ``Response``-like interface to an individual\n    subpart of a multipart response. It is expected that these will\n    generally be created by objects of the ``MultipartDecoder`` class.\n\n    Like ``Response``, there is a ``CaseInsensitiveDict`` object named headers,\n    ``content`` to access bytes, ``text`` to access unicode, and ``encoding``\n    to access the unicode codec.\n\n    '

    def __init__(self, content, encoding):
        self.encoding = encoding
        headers = {}
        if b'\r\n\r\n' in content:
            first, self.content = _split_on_find(content, b'\r\n\r\n')
            if first != b'':
                headers = _header_parser(first.lstrip(), encoding)
        else:
            raise ImproperBodyPartContentException('content does not contain CR-LF-CR-LF')
        self.headers = CaseInsensitiveDict(headers)

    @property
    def text(self):
        """Content of the ``BodyPart`` in unicode."""
        return self.content.decode(self.encoding)


class MultipartDecoder(object):
    __doc__ = "\n\n    The ``MultipartDecoder`` object parses the multipart payload of\n    a bytestring into a tuple of ``Response``-like ``BodyPart`` objects.\n\n    The basic usage is::\n\n        import requests\n        from requests_toolbelt import MultipartDecoder\n\n        response = request.get(url)\n        decoder = MultipartDecoder.from_response(response)\n        for part in decoder.parts:\n            print(part.headers['content-type'])\n\n    If the multipart content is not from a response, basic usage is::\n\n        from requests_toolbelt import MultipartDecoder\n\n        decoder = MultipartDecoder(content, content_type)\n        for part in decoder.parts:\n            print(part.headers['content-type'])\n\n    For both these usages, there is an optional ``encoding`` parameter. This is\n    a string, which is the name of the unicode codec to use (default is\n    ``'utf-8'``).\n\n    "

    def __init__(self, content, content_type, encoding='utf-8'):
        self.content_type = content_type
        self.encoding = encoding
        self.parts = tuple()
        self._find_boundary()
        self._parse_body(content)

    def _find_boundary(self):
        ct_info = tuple(x.strip() for x in self.content_type.split(';'))
        mimetype = ct_info[0]
        if mimetype.split('/')[0].lower() != 'multipart':
            raise NonMultipartContentTypeException("Unexpected mimetype in content-type: '{0}'".format(mimetype))
        for item in ct_info[1:]:
            attr, value = _split_on_find(item, '=')
            if attr.lower() == 'boundary':
                self.boundary = encode_with(value.strip('"'), self.encoding)

    @staticmethod
    def _fix_first_part(part, boundary_marker):
        bm_len = len(boundary_marker)
        if boundary_marker == part[:bm_len]:
            return part[bm_len:]
        else:
            return part

    def _parse_body(self, content):
        boundary = (b'').join((b'--', self.boundary))

        def body_part(part):
            fixed = MultipartDecoder._fix_first_part(part, boundary)
            return BodyPart(fixed, self.encoding)

        def test_part(part):
            return part != b'' and part != b'\r\n' and part[:4] != b'--\r\n' and part != b'--'

        parts = content.split((b'').join((b'\r\n', boundary)))
        self.parts = tuple(body_part(x) for x in parts if test_part(x))

    @classmethod
    def from_response(cls, response, encoding='utf-8'):
        content = response.content
        content_type = response.headers.get('content-type', None)
        return cls(content, content_type, encoding)