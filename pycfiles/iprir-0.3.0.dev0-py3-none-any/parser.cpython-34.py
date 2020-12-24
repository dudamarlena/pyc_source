# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib/iprir/parser.py
# Compiled at: 2017-01-25 00:55:53
# Size of source mod 2**32: 1033 bytes
from io import StringIO
from iprir.record import RIRRecord
__all__ = ('parse_string', 'parse_file', 'parse_iter')

def st_version(line: str):
    return (st_sumary, None)


def st_sumary(line: str):
    if line.endswith('summary'):
        return (st_sumary, None)
    else:
        return st_record(line)


def st_record(line: str):
    registry, cc, type_, start, value, date, status, *ext = line.split('|')
    record = RIRRecord(cc, type_, start, value, status)
    return (st_record, record)


def parse_iter(lines):
    status = st_version
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            status, result = status(line)
            if result is not None:
                yield result
            else:
                continue


def parse(lines):
    return list(parse_iter(lines))


def parse_file(filename):
    with open(filename, 'rt') as (fp):
        return parse(fp)


def parse_string(string):
    lines = StringIO(string)
    return parse(lines)