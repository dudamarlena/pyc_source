# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/msoucy/.virtualenv/fuf/lib/python2.7/site-packages/fuf/action.py
# Compiled at: 2014-09-23 17:45:03
"""
Action Set class and demonstration
Matt Soucy

The main purpose of this file is to demonstrate some of the fun things
that can be done with functions in Python.

Particularly interesting are:
- `ActionSet`: Shows how easy it can be to inherit from `dict`
- `ActionSet().__call__`: uses magic for wrapping a function and hiding metadata

Ideas taken from:
- http://numericalrecipes.wordpress.com/2009/05/25/signature-preserving-function-decorators/
- http://github.com/msoucy/RepBot
"""
from .wrapper import fdup

class ActionSet(dict):
    """Specifies a set of actions
    It's possible to have more than one set at a time
    Derives from dict to allow the user to perform useful actions on it"""

    def __init__(self, prefix=None, *env, **kwenv):
        """Setup
        If a prefix is specified, then it attempts to remove that prefix from
        the names of functions when creating actions"""
        dict.__init__(self)
        self._prefix = prefix
        self._env = env
        self._kwenv = kwenv

    def __call__(self, name=None, helpmsg=None):
        """Create the actual wrapper"""
        if hasattr(name, '__call__') and helpmsg is None:
            return self(None, None)(name)
        else:

            def make_action(func):
                """Set up the wrapper
            Adds attributes to a simple wrapper function
            Could modify the wrapper directly, but if other decorators or functions
            use a similar trick it could cause interference"""
                func = fdup(func)
                func.name = name or func.__name__
                if self._prefix and func.name.startswith(self._prefix):
                    func.name = func.name.replace(self._prefix, '', 1)
                func.helpmsg = helpmsg or func.__doc__.split('\n')[0] if func.__doc__ else ''
                self[func.name] = func
                return func

            return make_action

    def perform(self, msg, *env, **kwenv):
        """Perform an action based on a simplistic CLI-like argument splitting"""
        if not msg.strip():
            return
        args = msg.split()
        command = args.pop(0)
        if command in self:
            import copy
            newkwenv = copy.deepcopy(self._kwenv)
            newkwenv.update(kwenv)
            return self[command](*(self._env + env + tuple(args)), **newkwenv)
        raise KeyError('Invalid action "%s"' % command)