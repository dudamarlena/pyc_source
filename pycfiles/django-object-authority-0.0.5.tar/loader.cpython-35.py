# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomeu/workspace/wdna/django-object-authority/django_object_authority/loader.py
# Compiled at: 2017-05-31 09:11:55
# Size of source mod 2**32: 1051 bytes
import copy
from importlib import import_module

def autodiscover_authorizations(*args, **kwargs):
    """
    Auto-discover authorization modules and fail silently when not present.
    This forces an import on them to register any authorization classes.

    You may provide a register_to keyword parameter as a way to access a
    registry. This register_to object must have a _registry instance variable
    to access it.
    """
    from django.apps import apps
    register_to = kwargs.get('register_to')
    for app_config in apps.get_app_configs():
        for module_to_search in args:
            if register_to:
                before_import_registry = copy.copy(register_to._registry)
            try:
                import_module('{}.{}'.format(app_config.name, module_to_search))
            except Exception:
                if register_to:
                    register_to._registry = before_import_registry