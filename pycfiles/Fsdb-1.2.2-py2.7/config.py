# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fsdb/config.py
# Compiled at: 2016-03-25 11:09:21
from __future__ import unicode_literals
import json
from .utils import calc_dir_mode
from .compat import string_types
ACCEPTED_HASH_ALG = [
 b'md5', b'sha1', b'sha224', b'sha256', b'sha384', b'sha512']
TAG = b'fsdb_config'
__defaults = dict(fmode=b'660', depth=3, hash_alg=b'sha1')

def get_defaults():
    return __defaults.copy()


def update_backword(conf):
    if b'depth' not in conf and b'deep' in conf:
        conf[b'depth'] = conf.pop(b'deep')


def check_config(conf):
    """Type and boundary check"""
    if b'fmode' in conf and not isinstance(conf[b'fmode'], string_types):
        raise TypeError(TAG + b': `fmode` must be a string')
    if b'dmode' in conf and not isinstance(conf[b'dmode'], string_types):
        raise TypeError(TAG + b': `dmode` must be a string')
    if b'depth' in conf:
        if not isinstance(conf[b'depth'], int):
            raise TypeError(TAG + b': `depth` must be an int')
        if conf[b'depth'] < 0:
            raise ValueError(TAG + b': `depth` must be a positive number')
    if b'hash_alg' in conf:
        if not isinstance(conf[b'hash_alg'], string_types):
            raise TypeError(TAG + b': `hash_alg` must be a string')
        if conf[b'hash_alg'] not in ACCEPTED_HASH_ALG:
            raise ValueError(TAG + b': `hash_alg` must be one of ' + str(ACCEPTED_HASH_ALG))


def from_json_format(conf):
    """Convert fields of parsed json dictionary to python format"""
    if b'fmode' in conf:
        conf[b'fmode'] = int(conf[b'fmode'], 8)
    if b'dmode' in conf:
        conf[b'dmode'] = int(conf[b'dmode'], 8)


def to_json_format(conf):
    """Convert fields of a python dictionary to be dumped in json format"""
    if b'fmode' in conf:
        conf[b'fmode'] = oct(conf[b'fmode'])[-3:]
    if b'dmode' in conf:
        conf[b'dmode'] = oct(conf[b'dmode'])[-3:]


def normalize_conf(conf):
    """Check, convert and adjust user passed config

       Given a user configuration it returns a verified configuration with
       all parameters converted to the types that are needed at runtime.
    """
    conf = conf.copy()
    check_config(conf)
    from_json_format(conf)
    if b'dmode' not in conf:
        conf[b'dmode'] = calc_dir_mode(conf[b'fmode'])
    return conf


def loadConf(configPath):
    with open(configPath, b'r') as (configFile):
        loaded = json.load(configFile)
    return loaded


def writeConf(configPath, conf):
    with open(configPath, b'w') as (outfile):
        json.dump(conf, outfile, indent=4)