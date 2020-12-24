# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/key_binding/registry.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 11495 bytes
"""
Key bindings registry.

A `Registry` object is a container that holds a list of key bindings. It has a
very efficient internal data structure for checking which key bindings apply
for a pressed key.

Typical usage::

    r = Registry()

    @r.add_binding(Keys.ControlX, Keys.ControlC, filter=INSERT)
    def handler(event):
        # Handle ControlX-ControlC key sequence.
        pass

It is also possible to combine multiple registries. We do this in the default
key bindings. There are some registries that contain Emacs bindings, while
others contain the Vi bindings. They are merged together using a
`MergedRegistry`.

We also have a `ConditionalRegistry` object that can enable/disable a group of
key bindings at once.
"""
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from prompt_tool_kit.cache import SimpleCache
from prompt_tool_kit.filters import CLIFilter, to_cli_filter, Never
from prompt_tool_kit.keys import Key, Keys
from six import text_type, with_metaclass
__all__ = ('BaseRegistry', 'Registry', 'ConditionalRegistry', 'MergedRegistry')

class _Binding(object):
    __doc__ = '\n    (Immutable binding class.)\n    '

    def __init__(self, keys, handler, filter=None, eager=None, save_before=None):
        if not isinstance(keys, tuple):
            raise AssertionError
        else:
            if not callable(handler):
                raise AssertionError
            else:
                assert isinstance(filter, CLIFilter)
                assert isinstance(eager, CLIFilter)
            assert callable(save_before)
        self.keys = keys
        self.handler = handler
        self.filter = filter
        self.eager = eager
        self.save_before = save_before

    def call(self, event):
        return self.handler(event)

    def __repr__(self):
        return '%s(keys=%r, handler=%r)' % (
         self.__class__.__name__, self.keys, self.handler)


class BaseRegistry(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    Interface for a Registry.\n    '
    _version = 0

    @abstractmethod
    def get_bindings_for_keys(self, keys):
        pass

    @abstractmethod
    def get_bindings_starting_with_keys(self, keys):
        pass


class Registry(BaseRegistry):
    __doc__ = '\n    Key binding registry.\n    '

    def __init__(self):
        self.key_bindings = []
        self._get_bindings_for_keys_cache = SimpleCache(maxsize=10000)
        self._get_bindings_starting_with_keys_cache = SimpleCache(maxsize=1000)
        self._version = 0

    def _clear_cache(self):
        self._version += 1
        self._get_bindings_for_keys_cache.clear()
        self._get_bindings_starting_with_keys_cache.clear()

    def add_binding(self, *keys, **kwargs):
        """
        Decorator for annotating key bindings.

        :param filter: :class:`~prompt_tool_kit.filters.CLIFilter` to determine
            when this key binding is active.
        :param eager: :class:`~prompt_tool_kit.filters.CLIFilter` or `bool`.
            When True, ignore potential longer matches when this key binding is
            hit. E.g. when there is an active eager key binding for Ctrl-X,
            execute the handler immediately and ignore the key binding for
            Ctrl-X Ctrl-E of which it is a prefix.
        :param save_before: Callable that takes an `Event` and returns True if
            we should save the current buffer, before handling the event.
            (That's the default.)
        """
        filter = to_cli_filter(kwargs.pop('filter', True))
        eager = to_cli_filter(kwargs.pop('eager', False))
        save_before = kwargs.pop('save_before', lambda e: True)
        to_cli_filter(kwargs.pop('invalidate_ui', True))
        if not not kwargs:
            raise AssertionError
        else:
            if not keys:
                raise AssertionError
            else:
                assert all(isinstance(k, (Key, text_type)) for k in keys), 'Key bindings should consist of Key and string (unicode) instances.'
                assert callable(save_before)
            if isinstance(filter, Never):

                def decorator(func):
                    return func

            else:

                def decorator(func):
                    self.key_bindings.append(_Binding(keys, func, filter=filter, eager=eager, save_before=save_before))
                    self._clear_cache()
                    return func

        return decorator

    def remove_binding(self, function):
        """
        Remove a key binding.

        This expects a function that was given to `add_binding` method as
        parameter. Raises `ValueError` when the given function was not
        registered before.
        """
        assert callable(function)
        for b in self.key_bindings:
            if b.handler == function:
                self.key_bindings.remove(b)
                self._clear_cache()
                return

        raise ValueError('Binding not found: %r' % (function,))

    def get_bindings_for_keys(self, keys):
        """
        Return a list of key bindings that can handle this key.
        (This return also inactive bindings, so the `filter` still has to be
        called, for checking it.)

        :param keys: tuple of keys.
        """

        def get():
            result = []
            for b in self.key_bindings:
                if len(keys) == len(b.keys):
                    match = True
                    any_count = 0
                    for i, j in zip(b.keys, keys):
                        if i != j:
                            if i != Keys.Any:
                                match = False
                                break
                            if i == Keys.Any:
                                any_count += 1

                    if match:
                        result.append((any_count, b))

            result = sorted(result, key=(lambda item: -item[0]))
            return [item[1] for item in result]

        return self._get_bindings_for_keys_cache.get(keys, get)

    def get_bindings_starting_with_keys(self, keys):
        """
        Return a list of key bindings that handle a key sequence starting with
        `keys`. (It does only return bindings for which the sequences are
        longer than `keys`. And like `get_bindings_for_keys`, it also includes
        inactive bindings.)

        :param keys: tuple of keys.
        """

        def get():
            result = []
            for b in self.key_bindings:
                if len(keys) < len(b.keys):
                    match = True
                    for i, j in zip(b.keys, keys):
                        if i != j:
                            if i != Keys.Any:
                                match = False
                                break

                    if match:
                        result.append(b)

            return result

        return self._get_bindings_starting_with_keys_cache.get(keys, get)


class _AddRemoveMixin(BaseRegistry):
    __doc__ = '\n    Common part for ConditionalRegistry and MergedRegistry.\n    '

    def __init__(self):
        self._registry2 = Registry()
        self._last_version = None
        self._extra_registry = Registry()

    def _update_cache(self):
        raise NotImplementedError

    def add_binding(self, *k, **kw):
        return (self._extra_registry.add_binding)(*k, **kw)

    def remove_binding(self, *k, **kw):
        return (self._extra_registry.remove_binding)(*k, **kw)

    @property
    def key_bindings(self):
        self._update_cache()
        return self._registry2.key_bindings

    @property
    def _version(self):
        self._update_cache()
        return self._last_version

    def get_bindings_for_keys(self, *a, **kw):
        self._update_cache()
        return (self._registry2.get_bindings_for_keys)(*a, **kw)

    def get_bindings_starting_with_keys(self, *a, **kw):
        self._update_cache()
        return (self._registry2.get_bindings_starting_with_keys)(*a, **kw)


class ConditionalRegistry(_AddRemoveMixin):
    __doc__ = '\n    Wraps around a `Registry`. Disable/enable all the key bindings according to\n    the given (additional) filter.::\n\n        @Condition\n        def setting_is_true(cli):\n            return True  # or False\n\n        registy = ConditionalRegistry(registry, setting_is_true)\n\n    When new key bindings are added to this object. They are also\n    enable/disabled according to the given `filter`.\n\n    :param registries: List of `Registry` objects.\n    :param filter: `CLIFilter` object.\n    '

    def __init__(self, registry=None, filter=True):
        registry = registry or Registry()
        assert isinstance(registry, BaseRegistry)
        _AddRemoveMixin.__init__(self)
        self.registry = registry
        self.filter = to_cli_filter(filter)

    def _update_cache(self):
        """ If the original registry was changed. Update our copy version. """
        expected_version = (
         self.registry._version, self._extra_registry._version)
        if self._last_version != expected_version:
            registry2 = Registry()
            for reg in (self.registry, self._extra_registry):
                for b in reg.key_bindings:
                    registry2.key_bindings.append(_Binding(keys=(b.keys),
                      handler=(b.handler),
                      filter=(self.filter & b.filter),
                      eager=(b.eager),
                      save_before=(b.save_before)))

            self._registry2 = registry2
            self._last_version = expected_version


class MergedRegistry(_AddRemoveMixin):
    __doc__ = '\n    Merge multiple registries of key bindings into one.\n\n    This class acts as a proxy to multiple `Registry` objects, but behaves as\n    if this is just one bigger `Registry`.\n\n    :param registries: List of `Registry` objects.\n    '

    def __init__(self, registries):
        assert all(isinstance(r, BaseRegistry) for r in registries)
        _AddRemoveMixin.__init__(self)
        self.registries = registries

    def _update_cache(self):
        """
        If one of the original registries was changed. Update our merged
        version.
        """
        expected_version = tuple(r._version for r in self.registries) + (
         self._extra_registry._version,)
        if self._last_version != expected_version:
            registry2 = Registry()
            for reg in self.registries:
                registry2.key_bindings.extend(reg.key_bindings)

            registry2.key_bindings.extend(self._extra_registry.key_bindings)
            self._registry2 = registry2
            self._last_version = expected_version