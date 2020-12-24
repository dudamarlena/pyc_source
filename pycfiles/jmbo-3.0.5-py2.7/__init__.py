# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/__init__.py
# Compiled at: 2017-06-07 04:25:24
from django.conf import settings
USE_GIS = False
if 'atlas' in settings.INSTALLED_APPS and 'django.contrib.gis' in settings.INSTALLED_APPS and settings.DATABASES['default']['ENGINE'].startswith('django.contrib.gis.db.backends.'):
    USE_GIS = True

def modify_classes():
    """
    Auto-discover INSTALLED_APPS class_modifiers.py modules and fail silently
    when not present. This forces an import on them to modify any classes they
    may want.
    """
    import copy
    from django.contrib.admin.sites import site
    from importlib import import_module
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
default_app_config = 'jmbo.apps.JmboAppConfig'