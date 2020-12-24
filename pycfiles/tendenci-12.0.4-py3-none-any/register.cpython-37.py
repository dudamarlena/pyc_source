# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/registry/register.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 1487 bytes
import copy
from django.conf import settings
from importlib import import_module
from django.utils.module_loading import module_has_submodule
from tendenci.apps.registry.sites import site

def autodiscover():
    """
    Auto-discover INSTALLED_APPS app_registry.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            before_import_registry = copy.copy(site._registry)
            import_module('%s.app_registry' % app)
        except:
            site._registry = before_import_registry
            try:
                if module_has_submodule(mod, 'app_registry'):
                    raise
            except (ImportError, AttributeError):
                pass