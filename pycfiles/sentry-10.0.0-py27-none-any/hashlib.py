# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/hashlib.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import six
from hashlib import md5 as _md5
from hashlib import sha1 as _sha1
from django.utils.encoding import force_bytes

def md5_text(*args):
    m = _md5()
    for x in args:
        m.update(force_bytes(x, errors='replace'))

    return m


def sha1_text(*args):
    m = _sha1()
    for x in args:
        m.update(force_bytes(x, errors='replace'))

    return m


def hash_value(h, value):
    if value is None:
        h.update('\x00')
    elif value is True:
        h.update('\x01')
    elif value is False:
        h.update('\x02')
    elif isinstance(value, six.integer_types):
        h.update('\x03' + six.text_type(value).encode('ascii') + '\x00')
    elif isinstance(value, (tuple, list)):
        h.update('\x04' + six.text_type(len(value)).encode('utf-8'))
        for item in value:
            hash_value(h, item)

    elif isinstance(value, dict):
        h.update('\x05' + six.text_type(len(value)).encode('utf-8'))
        for k, v in six.iteritems(value):
            hash_value(h, k)
            hash_value(h, v)

    elif isinstance(value, bytes):
        h.update('\x06' + value + '\x00')
    elif isinstance(value, six.text_type):
        h.update('\x07' + value.encode('utf-8') + '\x00')
    else:
        raise TypeError('Invalid hash value')
    return


def hash_values(values, seed=None, algorithm=_md5):
    h = _md5()
    if seed is not None:
        h.update(('%sÿ' % seed).encode('utf-8'))
    for value in values:
        hash_value(h, value)

    return h.hexdigest()