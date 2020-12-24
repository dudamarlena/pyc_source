# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/json.py
# Compiled at: 2020-04-19 19:55:58
"""
Select a JSON library from any of several known libraries.
"""
try:
    import imp, sys
    f, pathname, desc = imp.find_module('json', sys.path[1:])
    js = imp.load_module('native_json', f, pathname, desc)
    f and f.close()
    encode = js.dumps
    decode = js.loads
except ImportError:
    try:
        import cjson
        encode = cjson.encode
        decode = cjson.decode
    except ImportError:
        try:
            import simplejson
            encode = simplejson.dumps
            decode = simplejson.loads
        except ImportError:
            try:
                import demjson
                encode = demjson.encode
                decode = demjson.decode
            except ImportError:
                raise ImportError('could not load one of: json, cjson, simplejson, demjson')