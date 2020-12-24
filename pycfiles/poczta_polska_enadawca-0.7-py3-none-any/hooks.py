# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/thirdparty/requests/hooks.py
# Compiled at: 2018-11-28 03:20:09
__doc__ = '\nrequests.hooks\n~~~~~~~~~~~~~~\n\nThis module provides the capabilities for the Requests hooks system.\n\nAvailable hooks:\n\n``response``:\n    The response generated from a Request.\n\n'
HOOKS = [
 'response']

def default_hooks():
    hooks = {}
    for event in HOOKS:
        hooks[event] = []

    return hooks


def dispatch_hook(key, hooks, hook_data, **kwargs):
    """Dispatches a hook dictionary on a given piece of data."""
    hooks = hooks or dict()
    if key in hooks:
        hooks = hooks.get(key)
        if hasattr(hooks, '__call__'):
            hooks = [
             hooks]
        for hook in hooks:
            _hook_data = hook(hook_data, **kwargs)
            if _hook_data is not None:
                hook_data = _hook_data

    return hook_data