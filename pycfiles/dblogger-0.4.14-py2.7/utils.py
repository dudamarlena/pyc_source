# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dblogger/utils.py
# Compiled at: 2015-04-26 18:06:04
import random, struct, time
from uuid import UUID

def gen_uuid(timestamp=None, sequence=None):
    if timestamp is None:
        timestamp = time.time()
    if sequence is None:
        sequence = random.getrandbits(32)
    bytes = struct.pack('>qLL', long(timestamp * 1024), sequence, random.getrandbits(32))
    return UUID(bytes=bytes)


def random_slice(items):
    start = random.randint(0, len(items))
    end = random.randint(0, len(items))
    return items[start:end + 1]


def datetime_to_time(datetime):
    return time.mktime(datetime.timetuple())