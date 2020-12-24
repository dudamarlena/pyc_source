# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/factories/dispatcher.py
# Compiled at: 2017-09-11 04:31:05
from .action import action_factory
from ..dispatchers.core import Sequential as DEFAULT
from ..lib import class_loader

def dispatcher_factory(dispatcher, actions):
    _actions = []
    if type(actions) is list:
        for a in actions:
            _actions.append(action_factory(a))

    else:
        _actions.append(action_factory(actions))
    if dispatcher is None:
        return DEFAULT(_actions)
    else:
        if 'kind' not in dispatcher:
            raise KeyError('Malformed dispatcher. "kind" parameter missing.')
        if dispatcher['kind'].startswith('.'):
            dispatcher['kind'] = 'watchm8.dispatchers%s' % (dispatcher['kind'],)
        klass = class_loader(dispatcher['kind'])
        kwargs = dict(dispatcher)
        del kwargs['kind']
        return klass(_actions, **kwargs)