# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/hooks.py
# Compiled at: 2018-11-17 20:47:49
# Size of source mod 2**32: 868 bytes
_resolve_mongodb_hook = lambda env: env
_log_exception_hook = lambda *args, **kwargs: None
_get_auth_hook = lambda *args, **kwargs: None

def get_mongodb_uri(host):
    """
    Return the MongoDB URI for the passed in host-alias / environment.

    Allows an indirection point for mapping aliases to particular
    MongoDB instances.
    """
    global _resolve_mongodb_hook
    return _resolve_mongodb_hook(host)


def register_resolve_mongodb_hook(hook):
    global _resolve_mongodb_hook
    _resolve_mongodb_hook = hook


def log_exception(fn_name, exception, retry_count, **kwargs):
    """
    External exception logging hook.
    """
    global _log_exception_hook
    _log_exception_hook(fn_name, exception, retry_count, **kwargs)


def register_log_exception_hook(hook):
    global _log_exception_hook
    _log_exception_hook = hook


def register_get_auth_hook(hook):
    global _get_auth_hook
    _get_auth_hook = hook