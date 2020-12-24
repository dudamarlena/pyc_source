# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/panya/__init__.py
# Compiled at: 2011-05-26 02:47:52


def modify_classes():
    """
    Auto-discover INSTALLED_APPS class_modifiers.py modules and fail silently when
    not present. This forces an import on them to modify any classes they
    may want.
    """
    import copy
    from django.conf import settings
    from django.contrib.admin.sites import site
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            before_import_registry = copy.copy(site._registry)
            import_module('%s.class_modifiers' % app)
        except:
            site._registry = before_import_registry
            if module_has_submodule(mod, 'class_modifiers'):
                raise


modify_classes()