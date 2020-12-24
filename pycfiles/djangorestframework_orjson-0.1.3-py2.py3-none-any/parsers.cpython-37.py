# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mauricio.abreua/Code/django-rest-framework-orjson/rest_framework_orjson/parsers.py
# Compiled at: 2019-07-19 07:57:42
# Size of source mod 2**32: 623 bytes
import codecs, orjson
from django.conf import settings
from rest_framework_orjson.renderers import ORJSONRenderer
from rest_framework.parsers import BaseParser

class ORJSONParser(BaseParser):
    __doc__ = '\n    Parses JSON-serialized data.\n    '
    media_type = 'application/json'
    renderer_class = ORJSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        decoded_stream = codecs.getreader(encoding)(stream)
        return orjson.loads(decoded_stream.read())