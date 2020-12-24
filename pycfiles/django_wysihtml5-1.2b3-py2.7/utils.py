# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/wysihtml5/utils.py
# Compiled at: 2014-01-19 03:33:05
from __future__ import unicode_literals
import re
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import allow_lazy
from django.utils.importlib import import_module

def get_function(function_path):
    """
    import and return function from ``path.to.module.function`` argument
    """
    try:
        mod_name, func_name = function_path.rsplit(b'.', 1)
        mod = import_module(mod_name)
    except ImportError as e:
        raise ImproperlyConfigured(b'Error importing module %s: "%s"' % (
         mod_name, e))

    return getattr(mod, func_name)


def keeptags(value, tags):
    tags = [ re.escape(tag) for tag in tags.split() ]

    def _replacer(match):
        if match.group(1) in tags:
            return match.group(0)
        else:
            return b''

    return re.sub(b'</?([^> ]+).*?>', _replacer, value)


keeptags = allow_lazy(keeptags)