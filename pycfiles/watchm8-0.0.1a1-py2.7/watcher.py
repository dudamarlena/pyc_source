# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/factories/watcher.py
# Compiled at: 2017-09-11 04:31:14
from ..lib import class_loader

def watcher_factory(watcher):
    if 'kind' not in watcher:
        raise KeyError('Malformed watcher. "kind" parameter missing.')
    if watcher['kind'].startswith('.'):
        watcher['kind'] = 'watchm8.watchers%s' % (watcher['kind'],)
    klass = class_loader(watcher['kind'])
    kwargs = dict(watcher)
    del kwargs['kind']
    return klass(**kwargs)