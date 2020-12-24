# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/json.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from enum import Enum
from simplejson import JSONEncoder, _default_decoder
import datetime, uuid, six, decimal
from bitfield.types import BitHandler
from django.utils.timezone import is_aware
from django.utils.html import mark_safe

def better_default_encoder(o):
    if isinstance(o, uuid.UUID):
        return o.hex
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    if isinstance(o, datetime.date):
        return o.isoformat()
    if isinstance(o, datetime.time):
        if is_aware(o):
            raise ValueError("JSON can't represent timezone-aware times.")
        r = o.isoformat()
        if o.microsecond:
            r = r[:12]
        return r
    if isinstance(o, (set, frozenset)):
        return list(o)
    if isinstance(o, decimal.Decimal):
        return six.text_type(o)
    if isinstance(o, Enum):
        return o.value
    if isinstance(o, BitHandler):
        return int(o)
    if callable(o):
        return '<function>'
    raise TypeError(repr(o) + ' is not JSON serializable')


class JSONEncoderForHTML(JSONEncoder):

    def encode(self, o):
        chunks = self.iterencode(o, True)
        if self.ensure_ascii:
            return ('').join(chunks)
        else:
            return ('').join(chunks)

    def iterencode(self, o, _one_shot=False):
        chunks = super(JSONEncoderForHTML, self).iterencode(o, _one_shot)
        for chunk in chunks:
            chunk = chunk.replace('&', '\\u0026')
            chunk = chunk.replace('<', '\\u003c')
            chunk = chunk.replace('>', '\\u003e')
            chunk = chunk.replace("'", '\\u0027')
            yield chunk


_default_encoder = JSONEncoder(separators=(',', ':'), ignore_nan=True, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, indent=None, encoding='utf-8', default=better_default_encoder)
_default_escaped_encoder = JSONEncoderForHTML(separators=(',', ':'), ignore_nan=True, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, indent=None, encoding='utf-8', default=better_default_encoder)

def dump(value, fp, **kwargs):
    for chunk in _default_encoder.iterencode(value):
        fp.write(chunk)


def dumps(value, escape=False, **kwargs):
    if escape:
        return _default_escaped_encoder.encode(value)
    return _default_encoder.encode(value)


def loads(value, **kwargs):
    return _default_decoder.decode(value)


def dumps_htmlsafe(value):
    return mark_safe(_default_escaped_encoder.encode(value))