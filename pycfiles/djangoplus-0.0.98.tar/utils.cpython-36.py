# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/templatetags/utils.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 525 bytes
from importlib import import_module
from django.conf import settings
modules = list()
modules.append(import_module('django.template.defaultfilters'))
for item in settings.TEMPLATES:
    for builtins in item['OPTIONS']['builtins']:
        modules.append(import_module(builtins))

def apply_filter(obj, filter_name, **kwargs):
    for module in modules:
        if hasattr(module, filter_name):
            func = getattr(module, filter_name)
            return func(obj, **kwargs)

    return obj