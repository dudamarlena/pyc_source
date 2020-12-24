# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/templatetags/utils.py
# Compiled at: 2019-03-31 15:07:30
# Size of source mod 2**32: 621 bytes
from django.conf import settings
from importlib import import_module
modules = list()
modules.append(import_module('django.template.defaultfilters'))
for item in settings.TEMPLATES:
    for builtins in ('djangoplus.templatetags', 'djangoplus.ui.components.paginator.templatetags'):
        modules.append(import_module(builtins))

def apply_filter(obj, filter_name, **kwargs):
    for module in modules:
        if hasattr(module, filter_name):
            func = getattr(module, filter_name)
            return func(obj, **kwargs)

    return obj