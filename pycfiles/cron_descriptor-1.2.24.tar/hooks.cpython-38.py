# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/requests/hooks.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 757 bytes
__doc__ = '\nrequests.hooks\n~~~~~~~~~~~~~~\n\nThis module provides the capabilities for the Requests hooks system.\n\nAvailable hooks:\n\n``response``:\n    The response generated from a Request.\n'
HOOKS = [
 'response']

def default_hooks():
    return {[]:event for event in HOOKS}


def dispatch_hook(key, hooks, hook_data, **kwargs):
    """Dispatches a hook dictionary on a given piece of data."""
    hooks = hooks or 
    hooks = hooks.get(key)
    if hooks:
        if hasattr(hooks, '__call__'):
            hooks = [
             hooks]
        for hook in hooks:
            _hook_data = hook(hook_data, **kwargs)
            if _hook_data is not None:
                hook_data = _hook_data

    return hook_data