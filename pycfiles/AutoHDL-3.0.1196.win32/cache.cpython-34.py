# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\cache.py
# Compiled at: 2015-05-16 02:47:48
# Size of source mod 2**32: 767 bytes
import os, json
from autohdl import FILE_CACHE

def load(fname, fdate):
    if os.path.exists(FILE_CACHE):
        with open(FILE_CACHE) as (f):
            contents = json.load(f)
            parsed = contents.get(fname)
            if parsed and parsed['fdate'] == fdate:
                print('hit file cache')
                return parsed


def dump(fname, fdate, parsed):
    cache = {}
    parsed['fdate'] = fdate
    d = {fname: parsed}
    if os.path.exists(FILE_CACHE):
        with open(FILE_CACHE) as (f):
            cache = json.load(f)
    else:
        os.makedirs(os.path.dirname(FILE_CACHE))
    cache.update(d)
    with open(FILE_CACHE, 'w') as (f):
        json.dump(cache, f, indent=2)
    print('miss file cache')