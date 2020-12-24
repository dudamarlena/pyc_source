# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tmignot/projects/yourlabs/nested-multipart-renderer/drf_nested_multipart/utils/encoders.py
# Compiled at: 2020-02-09 04:42:44
# Size of source mod 2**32: 2516 bytes
"""
Helper classes for parsers.
"""
from django.conf import settings
from django.test.client import encode_file
from django.utils.encoding import force_bytes
from django.utils.itercompat import is_iterable

class NestedMultiPartEncoder:

    def encode(self, boundary, data):
        lines = []

        def to_bytes(s):
            return force_bytes(s, settings.DEFAULT_CHARSET)

        def is_file(thing):
            return hasattr(thing, 'read') and callable(thing.read)

        def to_lines(d, prefix='', dot='.'):
            for key, value in d.items():
                if prefix:
                    key = '%s%s%s' % (prefix, dot, key)
                if value is None:
                    raise TypeError('Cannot encode None as POST data. Did you mean to pass an empty string or omit the value?')
                elif isinstance(value, dict):
                    to_lines(value, key)
                elif is_file(value):
                    lines.extend(encode_file(boundary, key, value))
                elif not isinstance(value, str):
                    if is_iterable(value):
                        for index, item in enumerate(value):
                            if isinstance(item, dict):
                                to_lines(item, '%s[%s]' % (key, index), '')
                            elif is_file(item):
                                lines.extend(encode_file(boundary, '%s[%s]' % (key, index), item))
                            else:
                                lines.extend((to_bytes(val) for val in (
                                 '--%s' % boundary,
                                 'Content-Disposition: form-data; name="%s[%s]"' % (
                                  key, index),
                                 '',
                                 item)))

                else:
                    lines.extend((to_bytes(val) for val in (
                     '--%s' % boundary,
                     'Content-Disposition: form-data; name="%s"' % key,
                     '',
                     value)))

        to_lines(data)
        lines.extend([
         to_bytes('--%s--' % boundary),
         b''])
        return (b'\r\n').join(lines)