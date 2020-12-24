# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/factories/action.py
# Compiled at: 2017-09-11 04:31:00
from ..lib import class_loader

def action_factory(action):
    if 'kind' not in action:
        raise KeyError('Malformed action. "kind" parameter missing.')
    if action['kind'].startswith('.'):
        action['kind'] = 'watchm8.actions%s' % (action['kind'],)
    klass = class_loader(action['kind'])
    kwargs = dict(action)
    del kwargs['kind']
    return klass(**kwargs)