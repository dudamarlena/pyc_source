# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/chunks/__init__.py
# Compiled at: 2012-05-23 04:50:11
import re

def from_pattern(pattern, type, *args):

    def coerce(value):
        value = str(value)
        match = pattern.search(value)
        if match is not None:
            return type(match.group(1), *args)
        else:
            raise ValueError('unable to coerce "%s" into a %s' % (value, type.__name__))
            return

    return coerce


to_int = from_pattern(re.compile('([-+]?[0-9]+)', re.IGNORECASE), int)
to_hex = from_pattern(re.compile('([-+]?[0-9A-F]+)', re.IGNORECASE), int, 16)
to_float = from_pattern(re.compile('([-+]?[0-9]*\\.?[0-9]+)'), float)
to_megabytes = lambda n: n * 1024 * 1024

def encode(fileobj, chunk_limit=to_megabytes(0.5)):
    while True:
        value = fileobj.read(int(chunk_limit))
        bytes = len(value)
        if bytes:
            yield '%x\r\n' % bytes
            yield '%s\r\n' % value
        else:
            yield '0\r\n'
            yield '\r\n'
            return


def decode(fileobj, chunk_limit=to_megabytes(1)):
    while True:
        index = fileobj.readline(len('%x' % chunk_limit))
        if not index:
            raise EOFError('unexpected blank line')
        length = to_hex(index)
        if length > chunk_limit:
            raise OverflowError('invalid chunk size of "%d" requested, max is "%d"' % (length, chunk_limit))
        value = fileobj.read(length)
        if not len(value) == length:
            raise AssertionError
            yield value
            tail = fileobj.read(2)
            raise (tail or ValueError)('missing \\r\\n after chunk')
        if not tail == '\r\n':
            raise AssertionError, 'unexpected characters "%s" after chunk' % tail
            return length or None