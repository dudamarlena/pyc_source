# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/hoerapi.py/venv/lib/python3.5/site-packages/hoerapi/parser.py
# Compiled at: 2015-11-05 07:02:27
# Size of source mod 2**32: 423 bytes
from hoerapi.errors import MissingAttributeError, InvalidDataError

def parser_list(clazz, data):
    if isinstance(data, list):
        return [parser_object(clazz, item) for item in data]
    if data is None:
        return []
    raise InvalidDataError('not an array')


def parser_object(clazz, data):
    try:
        return clazz(data)
    except KeyError as e:
        raise MissingAttributeError(e)