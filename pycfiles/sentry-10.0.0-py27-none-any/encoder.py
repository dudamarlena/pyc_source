# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/similarity/encoder.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from collections import Mapping, Set, Sequence
import six

class Encoder(object):
    try:
        number_types = (
         int, long, float)
    except NameError:
        number_types = (
         int, float)

    def __init__(self, types=None):
        self.types = types if types is not None else {}
        return

    def dumps(self, value):
        for cls, function in self.types.items():
            if isinstance(value, cls):
                value = function(value)

        if isinstance(value, six.binary_type):
            return value
        if isinstance(value, six.text_type):
            return value.encode('utf8')
        if isinstance(value, self.number_types):
            return six.text_type(value).encode('utf8')
        if isinstance(value, Set):
            return ('\x00').join(sorted(map(self.dumps, value)))
        if isinstance(value, Sequence):
            return ('\x01').join(map(self.dumps, value))
        if isinstance(value, Mapping):
            return ('\x02').join(sorted(('\x01').join(map(self.dumps, item)) for item in value.items()))
        raise TypeError(('Unsupported type: {}').format(type(value)))