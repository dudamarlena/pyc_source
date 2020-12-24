# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/transit/sosjson.py
# Compiled at: 2017-12-12 16:52:26
from copy import copy
import json
SKIP = [
 ' ', '\n', '\t']
ESCAPE = '\\'

def read_chunk(stream):
    """Ignore whitespace outside of strings. If we hit a string, read it in
    its entirety.
    """
    chunk = stream.read(1)
    while chunk in SKIP:
        chunk = stream.read(1)

    if chunk == '"':
        chunk += stream.read(1)
        while not chunk.endswith('"'):
            if chunk[(-1)] == ESCAPE:
                chunk += stream.read(2)
            else:
                chunk += stream.read(1)

    return chunk


def items(stream, **kwargs):
    """External facing items. Will return item from stream as available.
    Currently waits in loop waiting for next item. Can pass keywords that
    json.loads accepts (such as object_pairs_hook)
    """
    for s in yield_json(stream):
        yield json.loads(s, **kwargs)


def yield_json(stream):
    """Uses array and object delimiter counts for balancing.
    """
    buff = ''
    arr_count = 0
    obj_count = 0
    while True:
        buff += read_chunk(stream)
        if buff.endswith('{'):
            obj_count += 1
        if buff.endswith('['):
            arr_count += 1
        if buff.endswith(']'):
            arr_count -= 1
            if obj_count == arr_count == 0:
                json_item = copy(buff)
                buff = ''
                yield json_item
        if buff.endswith('}'):
            obj_count -= 1
            if obj_count == arr_count == 0:
                json_item = copy(buff)
                buff = ''
                yield json_item