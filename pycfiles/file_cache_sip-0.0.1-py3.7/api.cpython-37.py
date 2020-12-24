# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/file_cache/api.py
# Compiled at: 2019-12-09 00:55:31
# Size of source mod 2**32: 1249 bytes
from functools import wraps
from functools import partial
import json, pickle
config = {'pickle':{'dump':pickle.dump, 
  'load':pickle.load, 
  'open_read_file':lambda filename: open(filename, 'rb'), 
  'open_write_file':lambda filename: open(filename, 'wb')}, 
 'json':{'dump':json.dump, 
  'load':json.load, 
  'open_read_file':lambda filename: open(filename, 'r'), 
  'open_write_file':lambda filename: open(filename, 'w')}}

def file_cache(file='cache.dump', type='pickle'):
    conf = config[type]
    dump = conf.get('dump')
    load = conf.get('load')
    open_read_file = conf.get('open_read_file')
    open_write_file = conf.get('open_write_file')

    def wrapperfunc(f):

        @wraps(f)
        def wrapper(*args, **kwds):
            try:
                with open_read_file(file) as (fp):
                    ret = load(fp)
                if ret:
                    return ret
            except:
                pass

            ret = f(*args, **kwds)
            with open_write_file(file) as (fp):
                dump(ret, fp)
            return ret

        return wrapper

    return wrapperfunc