# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/bestappever/run.py
# Compiled at: 2008-08-25 05:22:59
from repoze.bfg import make_app
from repoze.bfg import get_options

def app(global_config, **kw):
    from bestappever.models import get_root
    import bestappever
    return make_app(get_root, bestappever, options=get_options(kw))


if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(app(None), host='0.0.0.0', port='6543')