# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/key_binding/manager.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 3727 bytes
"""
DEPRECATED:
Use `prompt_tool_kit.key_binding.defaults.load_key_bindings` instead.

:class:`KeyBindingManager` is a utility (or shortcut) for loading all the key
bindings in a key binding registry, with a logic set of filters to quickly to
quickly change from Vi to Emacs key bindings at runtime.

You don't have to use this, but it's practical.

Usage::

    manager = KeyBindingManager()
    app = Application(key_bindings_registry=manager.registry)
"""
from __future__ import unicode_literals
from .defaults import load_key_bindings
from prompt_tool_kit.filters import to_cli_filter
from prompt_tool_kit.key_binding.registry import Registry, ConditionalRegistry, MergedRegistry
__all__ = ('KeyBindingManager', )

class KeyBindingManager(object):
    __doc__ = '\n    Utility for loading all key bindings into memory.\n\n    :param registry: Optional `Registry` instance.\n    :param enable_abort_and_exit_bindings: Filter to enable Ctrl-C and Ctrl-D.\n    :param enable_system_bindings: Filter to enable the system bindings\n            (meta-! prompt and Control-Z suspension.)\n    :param enable_search: Filter to enable the search bindings.\n    :param enable_open_in_editor: Filter to enable open-in-editor.\n    :param enable_open_in_editor: Filter to enable open-in-editor.\n    :param enable_extra_page_navigation: Filter for enabling extra page navigation.\n        (Bindings for up/down scrolling through long pages, like in Emacs or Vi.)\n    :param enable_auto_suggest_bindings: Filter to enable fish-style suggestions.\n\n    :param enable_vi_mode: Deprecated!\n    '

    def __init__(self, registry=None, enable_vi_mode=None, enable_all=True, get_search_state=None, enable_abort_and_exit_bindings=False, enable_system_bindings=False, enable_search=False, enable_open_in_editor=False, enable_extra_page_navigation=False, enable_auto_suggest_bindings=False):
        if not registry is None:
            if not isinstance(registry, Registry):
                raise AssertionError
        if not get_search_state is None:
            if not callable(get_search_state):
                raise AssertionError
        enable_all = to_cli_filter(enable_all)
        defaults = load_key_bindings(get_search_state=get_search_state,
          enable_abort_and_exit_bindings=enable_abort_and_exit_bindings,
          enable_system_bindings=enable_system_bindings,
          enable_search=enable_search,
          enable_open_in_editor=enable_open_in_editor,
          enable_extra_page_navigation=enable_extra_page_navigation,
          enable_auto_suggest_bindings=enable_auto_suggest_bindings)
        self.registry = MergedRegistry([
         ConditionalRegistry(defaults, enable_all)])

    @classmethod
    def for_prompt(cls, **kw):
        """
        Create a ``KeyBindingManager`` with the defaults for an input prompt.
        This activates the key bindings for abort/exit (Ctrl-C/Ctrl-D),
        incremental search and auto suggestions.

        (Not for full screen applications.)
        """
        kw.setdefault('enable_abort_and_exit_bindings', True)
        kw.setdefault('enable_search', True)
        kw.setdefault('enable_auto_suggest_bindings', True)
        return cls(**kw)

    def reset(self, cli):
        pass

    def get_vi_state(self, cli):
        return cli.vi_state