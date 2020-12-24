# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/codec.py
# Compiled at: 2019-11-14 08:58:30
# Size of source mod 2**32: 869 bytes
import json
from .itis import is_file

def encode_to_file(obj, filepath, overwrite=True):
    """
    save obj to json file, like json.dump()
    :param filepath:
    :param obj:
    :return:
    """
    if not overwrite:
        if is_file(filepath):
            return
    return json.dump(obj, (open(filepath, 'w')), indent=True)


def decode_from_file(filepath):
    """
    parse json file to obj, like json.load()
    :param filepath:
    :return:
    """
    return json.load(open(filepath))


def json_encode(obj):
    """
    encode obj to json string, like json.dumps()
    :param obj:
    :return:
    """
    return json.dumps(obj, indent=True)


def json_decode(str, encoding='utf-8'):
    """
    decode json string to json object, like json.loads()
    :param str:
    :param encoding:
    :return:
    """
    return json.loads(str, encoding=encoding)