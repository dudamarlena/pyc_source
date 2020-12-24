# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/utils.py
# Compiled at: 2019-08-07 08:55:31
# Size of source mod 2**32: 1397 bytes
from web3 import Web3
import json, time, hashlib
from collections import OrderedDict

def get_timestamp():
    return int(round(time.time()))


def get_timestamp_ms():
    return int(round(time.time() * 1000))


def dump_dict_pretty(input_dict):
    return json.dumps(input_dict, separators=(',', ':'), indent=4, ensure_ascii=False)


def dump_dict(input_dict):
    return json.dumps(input_dict, separators=(',', ':'), ensure_ascii=False)


def load_dict(str_dict):
    return json.loads(str_dict, object_pairs_hook=OrderedDict)


def keccak256(item):
    if type(item) != str:
        raise ValueError
    return Web3.sha3(text=item).hex()[2:]


def b2bsha3_512(text):
    if type(text) != str:
        raise ValueError
    return _blake2b_512(_sha3_512(text) + text)


def b2bsha3_256(text):
    if type(text) != str:
        raise ValueError
    return _blake2b_256(_sha3_512(text) + text)


def _blake2b_512(text):
    if type(text) != str:
        raise ValueError
    return hashlib.blake2b((text.encode('utf-8')), digest_size=64).hexdigest()


def _blake2b_256(text):
    if type(text) != str:
        raise ValueError
    return hashlib.blake2b((text.encode('utf-8')), digest_size=32).hexdigest()


def _sha3_512(text):
    if type(text) != str:
        raise ValueError
    return hashlib.sha3_512(text.encode('utf-8')).hexdigest()