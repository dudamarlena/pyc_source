# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/martin/windows/Desarrollo/Python/django-endless-pagination-vue/bin/django-endless-pagination-vue/tests/endless_pagination/loaders.py
# Compiled at: 2015-07-13 19:15:37
# Size of source mod 2**32: 923 bytes
"""Django Endless Pagination object loaders."""
from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

def load_object(path):
    """Return the Python object represented by dotted *path*."""
    i = path.rfind('.')
    module_name, object_name = path[:i], path[i + 1:]
    try:
        module = import_module(module_name)
    except ImportError:
        raise ImproperlyConfigured('Module %r not found' % module_name)
    except ValueError:
        raise ImproperlyConfigured('Invalid module %r' % module_name)

    try:
        return getattr(module, object_name)
    except AttributeError:
        msg = 'Module %r does not define an object named %r'
        raise ImproperlyConfigured(msg % (module_name, object_name))