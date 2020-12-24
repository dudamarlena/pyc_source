# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aioetcd3/help.py
# Compiled at: 2018-05-26 21:48:07
# Size of source mod 2**32: 2636 bytes
from aioetcd3.utils import increment_last_byte, to_bytes, next_valid_key
from aioetcd3._etcdv3 import auth_pb2 as _auth
from aioetcd3._etcdv3 import rpc_pb2 as _rpc
SORT_ASCEND = 'ascend'
SORT_DESCEND = 'descend'
PER_R = _auth.Permission.READ
PER_W = _auth.Permission.WRITE
PER_RW = _auth.Permission.READWRITE
ALARM_ACTION_GET = _rpc.AlarmRequest.GET
ALARM_ACTION_ACTIVATE = _rpc.AlarmRequest.ACTIVATE
ALARM_ACTION_DEACTIVATE = _rpc.AlarmRequest.DEACTIVATE
ALARM_TYPE_NONE = _rpc.NONE
ALARM_TYPE_NOSPACE = _rpc.NOSPACE

def range_prefix(key):
    if not key:
        return range_all()
    else:
        return (
         to_bytes(key), increment_last_byte(to_bytes(key)))


def range_prefix_excluding(prefix, with_out):
    """
    Return a list of key_range, union of which is a prefix range excluding some keys

    :param prefix: the key to generate the range prefix
    :param with_out: a list of key_range (key or (start,end) tuple)
    :return: a list of key_range, union of which is a prefix range excluding some keys
    """
    return range_excluding(range_prefix(prefix), with_out)


def range_excluding(range_, with_out):
    """
    Return a list of key_range, union of which is a range excluding some keys

    :param range_: the original range
    :param with_out: a list of key_range (key or (start,end) tuple)
    :return: a list of key_range, union of which is a prefix range excluding some keys
    """
    with_out_ranges = [(to_bytes(v), next_valid_key(v)) if isinstance(v, str) or isinstance(v, bytes) else (to_bytes(v[0]), to_bytes(v[1])) for v in with_out]
    with_out_ranges.sort()
    range_start, range_end = range_
    range_start = to_bytes(range_start)
    range_end = to_bytes(range_end)
    re_range = []
    next_start_key = range_start
    for s, e in with_out_ranges:
        if s >= range_end != '\x00':
            break
        start, end = next_start_key, s
        if start < end:
            re_range.append((start, end))
        if e == '\x00':
            next_start_key = None
            break
        else:
            next_start_key = max(next_start_key, e)

    if next_start_key is not None:
        if next_start_key < range_end or range_end == '\x00':
            re_range.append((next_start_key, range_end))
    return re_range


def range_greater(key):
    return (
     next_valid_key(key), '\x00')


def range_greater_equal(key):
    return (
     key, '\x00')


def range_less(key):
    return (
     '\x00', key)


def range_less_equal(key):
    return (
     '\x00', next_valid_key(key))


def range_all():
    return ('\x00', '\x00')