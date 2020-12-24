# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/key_binding/manager.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 3727 bytes
__doc__ = "\nDEPRECATED:\nUse `prompt_tool_kit.key_binding.defaults.load_key_bindings` instead.\n\n:class:`KeyBindingManager` is a utility (or shortcut) for loading all the key\nbindings in a key binding registry, with a logic set of filters to quickly to\nquickly change from Vi to Emacs key bindings at runtime.\n\nYou don't have to use this, but it's practical.\n\nUsage::\n\n    manager = KeyBindingManager()\n    app = Application(key_bindings_registry=manager.registry)\n"
from __future__ import unicode_literals
from .defaults import load_key_bindings
from prompt_tool_kit.filters import to_cli_filter
from prompt_tool_kit.key_binding.registry import Registry, ConditionalRegistry, MergedRegistry
__all__ = ('KeyBindingManager', )

class KeyBindingManager(object):
    """KeyBindingManager"""

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