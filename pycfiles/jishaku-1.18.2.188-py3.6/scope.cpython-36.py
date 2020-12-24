# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/repl/scope.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 4253 bytes
"""
jishaku.repl.scope
~~~~~~~~~~~~~~~~~~

The Scope class and functions relating to it.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import inspect, typing

class Scope:
    __doc__ = "\n    Class that represents a global and local scope for both scope inspection and creation.\n\n    Many REPL functions expect or return this class.\n\n    .. code:: python3\n\n        scope = Scope()  # an empty Scope\n\n        scope = Scope(globals(), locals())  # a Scope imitating the current, real scope.\n\n        scope = Scope({'a': 3})  # a Scope with a pre-existing global scope key, and an empty local scope.\n    "
    __slots__ = ('globals', 'locals')

    def __init__(self, globals_: dict=None, locals_: dict=None):
        self.globals = globals_ or {}
        self.locals = locals_ or {}

    def clear_intersection(self, other_dict):
        """
        Clears out locals and globals from this scope where the key-value pair matches
        with other_dict.

        This allows cleanup of temporary variables that may have washed up into this
        Scope.

        Parameters
        -----------
        other_dict: :class:`dict`
            The dictionary to be used to determine scope clearance.

            If a key from this dict matches an entry in the globals or locals of this scope,
            and the value is identical, it is removed from the scope.

        Returns
        -------
        Scope
            The updated scope (self).
        """
        for key, value in other_dict.items():
            if key in self.globals:
                if self.globals[key] is value:
                    del self.globals[key]
                if key in self.locals and self.locals[key] is value:
                    del self.locals[key]

        return self

    def update(self, other):
        """
        Updates this scope with the content of another scope.

        Parameters
        ---------
        other: :class:`Scope`
            The scope to overlay onto this one.

        Returns
        -------
        Scope
            The updated scope (self).
        """
        self.globals.update(other.globals)
        self.locals.update(other.locals)
        return self

    def update_globals(self, other: dict):
        """
        Updates this scope's globals with a dict.

        Parameters
        -----------
        other: :class:`dict`
            The dictionary to be merged into this scope.

        Returns
        -------
        Scope
            The updated scope (self).
        """
        self.globals.update(other)
        return self

    def update_locals(self, other: dict):
        """
        Updates this scope's locals with a dict.

        Parameters
        -----------
        other: :class:`dict`
            The dictionary to be merged into this scope.

        Returns
        -------
        Scope
            The updated scope (self).
        """
        self.locals.update(other)
        return self


def get_parent_scope_from_var(name, global_ok=False, skip_frames=0) -> typing.Optional[Scope]:
    """
    Iterates up the frame stack looking for a frame-scope containing the given variable name.

    Returns
    --------
    Optional[Scope]
        The relevant :class:`Scope` or None
    """
    stack = inspect.stack()
    try:
        for frame_info in stack[skip_frames + 1:]:
            frame = None
            try:
                frame = frame_info.frame
                if name in frame.f_locals or global_ok and name in frame.f_globals:
                    return Scope(globals_=(frame.f_globals), locals_=(frame.f_locals))
            finally:
                del frame

    finally:
        del stack


def get_parent_var(name, global_ok=False, default=None, skip_frames=0):
    """
    Directly gets a variable from a parent frame-scope.

    Returns
    --------
    Any
        The content of the variable found by the given name, or None.
    """
    scope = get_parent_scope_from_var(name, global_ok=global_ok, skip_frames=(skip_frames + 1))
    if not scope:
        return default
    else:
        if name in scope.locals:
            return scope.locals.get(name, default)
        return scope.globals.get(name, default)