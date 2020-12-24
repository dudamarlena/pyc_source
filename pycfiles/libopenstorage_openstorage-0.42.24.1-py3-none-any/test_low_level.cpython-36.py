# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/jeepney/jeepney/tests/test_low_level.py
# Compiled at: 2020-01-10 16:25:36
# Size of source mod 2**32: 2554 bytes
import pytest
from jeepney.low_level import *
HELLO_METHOD_CALL = b'l\x01\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00m\x00\x00\x00\x01\x01o\x00\x15\x00\x00\x00/org/freedesktop/DBus\x00\x00\x00\x02\x01s\x00\x14\x00\x00\x00org.freedesktop.DBus\x00\x00\x00\x00\x03\x01s\x00\x05\x00\x00\x00Hello\x00\x00\x00\x06\x01s\x00\x14\x00\x00\x00org.freedesktop.DBus\x00\x00\x00\x00'

def test_parser_simple():
    msg = Parser().feed(HELLO_METHOD_CALL)[0]
    assert msg.header.fields[HeaderFields.member] == 'Hello'


def chunks(src, size):
    pos = 0
    while pos < len(src):
        end = pos + size
        yield src[pos:end]
        pos = end


def test_parser_chunks():
    p = Parser()
    chunked = list(chunks(HELLO_METHOD_CALL, 16))
    for c in chunked[:-1]:
        assert p.feed(c) == []

    msg = p.feed(chunked[(-1)])[0]
    assert msg.header.fields[HeaderFields.member] == 'Hello'


def test_multiple():
    msgs = Parser().feed(HELLO_METHOD_CALL * 6)
    assert len(msgs) == 6
    for msg in msgs:
        assert msg.header.fields[HeaderFields.member] == 'Hello'


def test_roundtrip():
    msg = Parser().feed(HELLO_METHOD_CALL)[0]
    assert msg.serialise() == HELLO_METHOD_CALL


def test_serialise_dict():
    data = {'a':'b', 
     'de':'f'}
    string_type = simple_types['s']
    sig = Array(DictEntry([string_type, string_type]))
    print(sig.serialise(data, 0, Endianness.little))
    assert sig.serialise(data, 0, Endianness.little) == b'\x1e\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00a\x00\x00\x00\x01\x00\x00\x00b\x00\x00\x00\x02\x00\x00\x00de\x00\x00\x01\x00\x00\x00f\x00'


def test_parse_signature():
    sig = parse_signature(list('(a{sv}(oayays)b)'))
    print(sig)
    assert sig == Struct([
     Array(DictEntry([simple_types['s'], Variant()])),
     Struct([
      simple_types['o'],
      Array(simple_types['y']),
      Array(simple_types['y']),
      simple_types['s']]),
     simple_types['b']])


class fake_list(list):

    def __init__(self, n):
        super().__init__()
        self._n = n

    def __len__(self):
        return self._n

    def __iter__(self):
        return iter(range(self._n))


def test_array_limit():
    a = Array(FixedType(8, 'Q'))
    a.serialise(fake_list(100), 0, Endianness.little)
    with pytest.raises(SizeLimitError):
        a.serialise(fake_list(8388609), 0, Endianness.little)