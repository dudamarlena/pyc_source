# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gopage/util.py
# Compiled at: 2017-03-22 03:39:04
# Size of source mod 2**32: 2259 bytes
import functools

def cache(ctype=''):
    import json, pickle
    from os.path import exists

    def decorator(func):

        def clean(kw, key, default=None):
            if key in kw:
                return kw.pop(key)
            else:
                return default

        @functools.wraps(func)
        def wrapper(*args, **kw):
            verbose = clean(kw, 'cverbose', True)
            usecache = clean(kw, 'usecache', True)
            if 'cache' in kw and not kw['cache']:
                kw.pop('cache')
                return func(*args, **kw)
            else:
                if usecache:
                    if 'cache' in kw:
                        if exists(kw['cache']):
                            if verbose:
                                print('@{} reading cache'.format(func.__name__))
                            if ctype == 'json':
                                with open(kw['cache']) as (rf):
                                    return json.load(rf)
                            else:
                                if ctype == 'pickle':
                                    with open(kw['cache'], 'rb') as (rf):
                                        return pickle.load(rf)
                                elif ctype == 'text':
                                    with open((kw['cache']), encoding='utf-8') as (rf):
                                        return rf.read()
                dbkey = clean(kw, 'dbkey', None)
                cachepath = clean(kw, 'cache', None)
                ret = func(*args, **kw)
                if cachepath:
                    if verbose:
                        print('@{} creating cache'.format(func.__name__))
                    if ctype == 'json':
                        with open(cachepath, 'w') as (f):
                            json.dump(ret, f, indent=4)
                    else:
                        if ctype == 'pickle':
                            with open(cachepath, 'wb') as (f):
                                pickle.dump(ret, f)
                        elif ctype == 'text':
                            with open(cachepath, 'w', encoding='utf-8') as (f):
                                f.write(ret)
                return ret

        return wrapper

    return decorator


if __name__ == '__main__':
    import util, json

    @util.cache('text')
    def test_text():
        return 'hi'


    @util.cache('json')
    def test_json():
        return {'1': 1}


    test_json(usecache=True, cache='test_json.json')
    test_text(usecache=True, cache='test_text.json')