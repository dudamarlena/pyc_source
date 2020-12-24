# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/devel/durian/durian/registry.py
# Compiled at: 2009-09-12 09:43:32
"""durian.registry"""
from celery.exceptions import NotRegistered, AlreadyRegistered
from UserDict import UserDict
from inspect import isclass

class HookRegistry(UserDict):
    """Global hook registry."""
    AlreadyRegistered = AlreadyRegistered
    NotRegistered = NotRegistered

    def __init__(self):
        self.data = {}

    def register(self, hook):
        """Register a hook in the hook registry.

        :param hook: The hook to register.

        :raises AlreadyRegistered: if the task is already registered.

        """
        hook = hook() if isclass(hook) else hook
        name = hook.name
        if name in self.data:
            raise self.AlreadyRegistered('Hook with name %s is already registered.' % name)
        self.data[name] = hook

    def unregister(self, name):
        """Unregister hook by name.

        :param name: name of the hook to unregister, or a
            :class:`durian.event.Hook` class with a valid ``name`` attribute.

        :raises celery.exceptions.NotRegistered: if the hook has not
            been registered.

        """
        if hasattr(name, 'name'):
            name = name.name
        if name not in self.data:
            raise self.NotRegistered('Hook with name %s is not registered.' % name)
        del self.data[name]

    def get_all(self):
        """Get all hooks."""
        return self.data

    def get_hook(self, name):
        """Get hook by name."""
        return self.data[name]

    def as_choices(self):
        """Return the hook registry as a choices tuple for use
        within Django models and forms."""
        dict_types = dict((type.name, type) for type in self.data.values())
        sorted_names = sorted(dict_types.keys())
        return [ (type.name, name.capitalize()) for (name, type) in dict_types.items()
               ]


hooks = HookRegistry()