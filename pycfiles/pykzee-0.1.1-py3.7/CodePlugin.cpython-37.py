# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykzee/core/CodePlugin.py
# Compiled at: 2019-12-24 08:49:05
# Size of source mod 2**32: 2093 bytes
import builtins, functools, inspect, traceback
from pykzee.core.common import call_soon, Undefined, pathToString
import pykzee.core.Plugin as Plugin
environment = {key:value for key, value in builtins.__dict__.items() if key not in ('__dict__',
                                                                                    '__import__',
                                                                                    '__loader__',
                                                                                    '__name__',
                                                                                    '__package__',
                                                                                    '__spec__',
                                                                                    'eval',
                                                                                    'exec',
                                                                                    'exit',
                                                                                    'open') if key not in ('__dict__',
                                                                                                           '__import__',
                                                                                                           '__loader__',
                                                                                                           '__name__',
                                                                                                           '__package__',
                                                                                                           '__spec__',
                                                                                                           'eval',
                                                                                                           'exec',
                                                                                                           'exit',
                                                                                                           'open')}
environment.update(Undefined=Undefined, call_soon=call_soon)

class CodePlugin(Plugin):

    def init(self, config):
        try:
            code = compile(config['code.py'], f"<{pathToString(self.path + ('code.py', ))}>", 'exec')
            globals = {'__builtins__': dict(environment,
                               path=(self.path),
                               get=(self.get),
                               subscribe=(self.subscribe),
                               command=(self.command),
                               set_state=(self.set),
                               register_command=(self.registerCommand),
                               state_from_subscription=(self.stateFromSubscription))}
            exec(code, globals)
        except Exception as ex:
            try:
                self.set((), {'exception':str(ex),  'traceback':traceback.format_exc()})
            finally:
                ex = None
                del ex

    def stateFromSubscription(self, handler, *paths):
        handler = functools.partial(self.subscriptionCallback, handler)
        if paths:
            self.set((), 'Waiting for subscription...')
            return (self.subscribe)(handler, *paths)
        call_soon(handler)
        return lambda : None

    async def subscriptionCallback(self, handler, *state):
        try:
            ret = handler(*state)
            if inspect.isawaitable(ret):
                ret = await ret
            self.set((), ret)
        except Exception as ex:
            try:
                self.set((), {'exception':str(ex),  'traceback':traceback.format_exc()})
            finally:
                ex = None
                del ex