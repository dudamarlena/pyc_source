# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.mpro-virenv/bizdir/lib/python3.4/site-packages/menuware/utils.py
# Compiled at: 2016-08-18 14:52:30
# Size of source mod 2**32: 1081 bytes
from importlib import import_module

def get_callable(func_or_path):
    """
    Receives a dotted path or a callable, Returns a callable or None
    """
    if callable(func_or_path):
        return func_or_path
    module_name = '.'.join(func_or_path.split('.')[:-1])
    function_name = func_or_path.split('.')[(-1)]
    _module = import_module(module_name)
    func = getattr(_module, function_name)
    return func


def is_superuser(request):
    """
    Returns True if request.user is superuser else returns False
    """
    return is_authenticated(request) and request.user.is_superuser


def is_staff(request):
    """
    Returns True if request.user is staff else returns False
    """
    return is_authenticated(request) and request.user.is_staff


def is_authenticated(request):
    """
    Returns True if request.user authenticated else returns False
    """
    return request.user.is_authenticated


def is_anonymous(request):
    """
    Returns True if request.user is not authenticated else returns False
    """
    return not request.user.is_authenticated