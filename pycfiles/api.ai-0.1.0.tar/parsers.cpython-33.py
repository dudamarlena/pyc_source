# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/parsers.py
# Compiled at: 2016-04-14 17:20:33
# Size of source mod 2**32: 1827 bytes
from __future__ import unicode_literals
from api_star.decorators import annotate
from api_star.exceptions import BadRequest
from api_star.utils import parse_header_params
from werkzeug.formparser import MultiPartParser as WerkzeugMultiPartParser
from werkzeug.formparser import default_stream_factory
from werkzeug.urls import url_decode_stream
import json

def json_parser():
    errors = {'malformed': 'Malformed JSON'}

    @annotate(media_type='application/json')
    def parser(stream, **context):
        data = stream.read().decode('utf-8')
        try:
            return json.loads(data)
        except ValueError:
            raise BadRequest(errors['malformed'])

    return parser


def multipart_parser():
    errors = {'missing-boundary-param': 'Multipart message missing boundary in Content-Type header', 
     'malformed': 'Malformed multipart request'}

    @annotate(media_type='multipart/form-data')
    def parser(stream, **context):
        content_type = context['content_type']
        content_length = context['content_length']
        multipart_parser = WerkzeugMultiPartParser(default_stream_factory)
        params = parse_header_params(content_type)
        boundary = params.get('boundary')
        if boundary is None:
            raise BadRequest(errors['missing-boundary-param'])
        boundary = boundary.encode('ascii')
        try:
            data, files = multipart_parser.parse(stream, boundary, content_length)
        except ValueError:
            raise BadRequest(errors['malformed'])

        data.update(files)
        return data

    return parser


def urlencoded_parser():

    @annotate(media_type='application/x-www-form-urlencoded')
    def parser(stream, **context):
        return url_decode_stream(stream)

    return parser