# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/mgxrace/django-warmama/warmama/fields.py
# Compiled at: 2015-05-15 22:07:08
# Size of source mod 2**32: 3614 bytes
import binascii, json, logging, zlib
from base64 import urlsafe_b64decode
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
logger = logging.getLogger(__name__)

class IPAddressField(forms.GenericIPAddressField):
    __doc__ = 'IPAddressField which strips port\n\n    Splits the port from the value before interpreting it as an ip address.\n    For ipv6 this takes the non-standard form `ip:port`, if port is specified\n    empty groups must be explicitly written. (e.g.\n    `2001:db8:85a3::::370:7334:port` not `2001:db8:85a3::370:7334:port`)\n    '

    def to_python(self, value):
        try:
            value = value.strip()
        except AttributeError:
            raise ValidationError('Value must be a string', code='invalid')

        addr, port = value, None
        if '.' in value and ':' in value:
            port_start = value.rfind(':', value.rfind('.'))
            if port_start != -1:
                addr, port = value[:port_start], value[port_start + 1:]
        else:
            if value.count(':') == 8:
                addr, port = value.rsplit(':', 1)
            addr = super(IPAddressField, self).to_python(addr)
            if port:
                try:
                    port = int(port)
                except ValueError:
                    raise ValidationError('Port must be an integer')

            port = None
        return (addr, port)

    def validate(self, value):
        addr, port = value
        super(IPAddressField, self).validate(addr)

    def run_validators(self, value):
        addr, port = value
        super(IPAddressField, self).run_validators(addr)


class GzipJsonField(forms.Field):
    __doc__ = 'Field which expects urlsafe-base64 encoded gzipped data'

    def to_python(self, value):
        try:
            value = value.encode('utf-8')
        except ValueError:
            raise ValidationError('Couldnt UTF-8 encode value', code='invalid')

        try:
            value = urlsafe_b64decode(value)
        except (TypeError, binascii.Error):
            raise ValidationError('Couldnt base64 decode value', code='invalid')

        try:
            value = zlib.decompress(value)
        except zlib.error:
            raise ValidationError('Couldnt zlib decompress value', code='invalid')

        try:
            value = value.decode('utf-8')
        except ValueError:
            raise ValidationError('Couldnt UTF-8 decode the decompressed value', code='invalid')

        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            raise ValidationError('Couldnt parse value as JSON', code='invalid')

        return super(GzipJsonField, self).to_python(value)


class TimestampField(serializers.Field):
    __doc__ = 'Convert POSIX timestamps to/from TZ-aware datetime objects'
    default_error_messages = {'invalid': 'Must be a TZ-aware datetime object'}

    def to_representation(self, obj):
        """Convert a TZ-aware datetime to its POSIX timestamp"""
        if timezone.is_naive(obj):
            self.fail('invalid')
        return (obj - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()

    def to_internal_value(self, data):
        """Convert a POSIX timestamp to a TZ-aware datetime"""
        return datetime.utcfromtimestamp(data).replace(tzinfo=timezone.utc)