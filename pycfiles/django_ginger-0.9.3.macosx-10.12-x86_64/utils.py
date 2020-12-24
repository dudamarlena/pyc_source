# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/views/utils.py
# Compiled at: 2016-10-13 21:52:44
from django.utils import six
from importlib import import_module
from ginger.views import GingerView
import inspect
__all__ = [
 'find_views']

def find_views(module, predicate=None):
    if isinstance(module, six.string_types):
        module = import_module(module)
    view_classes = inspect.getmembers(module, lambda a: isinstance(a, type) and issubclass(a, (GingerView,)) and not getattr(a, '__abstract__', False) and inspect.getmodule(a) is module and (predicate is None or predicate(a)))
    return sorted((v[1] for v in view_classes), key=lambda a: a.position)