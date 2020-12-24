# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/webencodings/tests.py
# Compiled at: 2019-02-14 00:35:07
"""

    webencodings.tests
    ~~~~~~~~~~~~~~~~~~

    A basic test suite for Encoding.

    :copyright: Copyright 2012 by Simon Sapin
    :license: BSD, see LICENSE for details.

"""
from __future__ import unicode_literals
from . import lookup, LABELS, decode, encode, iter_decode, iter_encode, IncrementalDecoder, IncrementalEncoder, UTF8

def assert_raises(exception, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except exception:
        return

    raise AssertionError(b'Did not raise %s.' % exception)


def test_labels():
    assert lookup(b'utf-8').name == b'utf-8'
    assert lookup(b'Utf-8').name == b'utf-8'
    assert lookup(b'UTF-8').name == b'utf-8'
    assert lookup(b'utf8').name == b'utf-8'
    assert lookup(b'utf8').name == b'utf-8'
    assert lookup(b'utf8 ').name == b'utf-8'
    assert lookup(b' \r\nutf8\t').name == b'utf-8'
    assert lookup(b'u8') is None
    assert lookup(b'utf-8\xa0') is None
    assert lookup(b'US-ASCII').name == b'windows-1252'
    assert lookup(b'iso-8859-1').name == b'windows-1252'
    assert lookup(b'latin1').name == b'windows-1252'
    assert lookup(b'LATIN1').name == b'windows-1252'
    assert lookup(b'latin-1') is None
    assert lookup(b'LATİN1') is None
    return


def test_all_labels():
    for label in LABELS:
        assert decode(b'', label) == (b'', lookup(label))
        assert encode(b'', label) == b''
        for repeat in [0, 1, 12]:
            output, _ = iter_decode([b''] * repeat, label)
            assert list(output) == []
            assert list(iter_encode([b''] * repeat, label)) == []

        decoder = IncrementalDecoder(label)
        assert decoder.decode(b'') == b''
        assert decoder.decode(b'', final=True) == b''
        encoder = IncrementalEncoder(label)
        assert encoder.encode(b'') == b''
        assert encoder.encode(b'', final=True) == b''

    for name in set(LABELS.values()):
        assert lookup(name).name == name


def test_invalid_label():
    assert_raises(LookupError, decode, b'\ufeffé', b'invalid')
    assert_raises(LookupError, encode, b'é', b'invalid')
    assert_raises(LookupError, iter_decode, [], b'invalid')
    assert_raises(LookupError, iter_encode, [], b'invalid')
    assert_raises(LookupError, IncrementalDecoder, b'invalid')
    assert_raises(LookupError, IncrementalEncoder, b'invalid')


def test_decode():
    assert decode(b'\x80', b'latin1') == (b'€', lookup(b'latin1'))
    assert decode(b'\x80', lookup(b'latin1')) == (b'€', lookup(b'latin1'))
    assert decode(b'é', b'utf8') == (b'é', lookup(b'utf8'))
    assert decode(b'é', UTF8) == (b'é', lookup(b'utf8'))
    assert decode(b'é', b'ascii') == (b'Ã©', lookup(b'ascii'))
    assert decode(b'\ufeffé', b'ascii') == (b'é', lookup(b'utf8'))
    assert decode(b'\xfe\xff\x00\xe9', b'ascii') == (b'é', lookup(b'utf-16be'))
    assert decode(b'\xff\xfe\xe9\x00', b'ascii') == (b'é', lookup(b'utf-16le'))
    assert decode(b'\xfe\xff\xe9\x00', b'ascii') == (b'\ue900', lookup(b'utf-16be'))
    assert decode(b'\xff\xfe\x00\xe9', b'ascii') == (b'\ue900', lookup(b'utf-16le'))
    assert decode(b'\x00\xe9', b'UTF-16BE') == (b'é', lookup(b'utf-16be'))
    assert decode(b'\xe9\x00', b'UTF-16LE') == (b'é', lookup(b'utf-16le'))
    assert decode(b'\xe9\x00', b'UTF-16') == (b'é', lookup(b'utf-16le'))
    assert decode(b'\xe9\x00', b'UTF-16BE') == (b'\ue900', lookup(b'utf-16be'))
    assert decode(b'\x00\xe9', b'UTF-16LE') == (b'\ue900', lookup(b'utf-16le'))
    assert decode(b'\x00\xe9', b'UTF-16') == (b'\ue900', lookup(b'utf-16le'))


def test_encode():
    assert encode(b'é', b'latin1') == b'\xe9'
    assert encode(b'é', b'utf8') == b'é'
    assert encode(b'é', b'utf8') == b'é'
    assert encode(b'é', b'utf-16') == b'\xe9\x00'
    assert encode(b'é', b'utf-16le') == b'\xe9\x00'
    assert encode(b'é', b'utf-16be') == b'\x00\xe9'


def test_iter_decode():

    def iter_decode_to_string(input, fallback_encoding):
        output, _encoding = iter_decode(input, fallback_encoding)
        return (b'').join(output)

    assert iter_decode_to_string([], b'latin1') == b''
    assert iter_decode_to_string([b''], b'latin1') == b''
    assert iter_decode_to_string([b'\xe9'], b'latin1') == b'é'
    assert iter_decode_to_string([b'hello'], b'latin1') == b'hello'
    assert iter_decode_to_string([b'he', b'llo'], b'latin1') == b'hello'
    assert iter_decode_to_string([b'hell', b'o'], b'latin1') == b'hello'
    assert iter_decode_to_string([b'é'], b'latin1') == b'Ã©'
    assert iter_decode_to_string([b'\ufeffé'], b'latin1') == b'é'
    assert iter_decode_to_string([
     b'\ufeff', b'\xc3', b'\xa9'], b'latin1') == b'é'
    assert iter_decode_to_string([
     b'\ufeff', b'a', b'\xc3'], b'latin1') == b'a�'
    assert iter_decode_to_string([
     b'', b'\xef', b'', b'', b'\xbb\xbf\xc3', b'\xa9'], b'latin1') == b'é'
    assert iter_decode_to_string([b'\ufeff'], b'latin1') == b''
    assert iter_decode_to_string([b'\xef\xbb'], b'latin1') == b'ï»'
    assert iter_decode_to_string([b'\xfe\xff\x00\xe9'], b'latin1') == b'é'
    assert iter_decode_to_string([b'\xff\xfe\xe9\x00'], b'latin1') == b'é'
    assert iter_decode_to_string([
     b'', b'\xff', b'', b'', b'\xfe\xe9', b'\x00'], b'latin1') == b'é'
    assert iter_decode_to_string([
     b'', b'h\xe9', b'llo'], b'x-user-defined') == b'h\uf7e9llo'


def test_iter_encode():
    assert (b'').join(iter_encode([], b'latin1')) == b''
    assert (b'').join(iter_encode([b''], b'latin1')) == b''
    assert (b'').join(iter_encode([b'é'], b'latin1')) == b'\xe9'
    assert (b'').join(iter_encode([b'', b'é', b'', b''], b'latin1')) == b'\xe9'
    assert (b'').join(iter_encode([b'', b'é', b'', b''], b'utf-16')) == b'\xe9\x00'
    assert (b'').join(iter_encode([b'', b'é', b'', b''], b'utf-16le')) == b'\xe9\x00'
    assert (b'').join(iter_encode([b'', b'é', b'', b''], b'utf-16be')) == b'\x00\xe9'
    assert (b'').join(iter_encode([
     b'', b'h\uf7e9', b'', b'llo'], b'x-user-defined')) == b'h\xe9llo'


def test_x_user_defined():
    encoded = b'2,\x0c\x0b\x1aO\xd9#\xcb\x0f\xc9\xbbt\xcf\xa8\xca'
    decoded = b'2,\x0c\x0b\x1aO\uf7d9#\uf7cb\x0f\uf7c9\uf7bbt\uf7cf\uf7a8\uf7ca'
    encoded = b'aa'
    decoded = b'aa'
    assert decode(encoded, b'x-user-defined') == (decoded, lookup(b'x-user-defined'))
    assert encode(decoded, b'x-user-defined') == encoded