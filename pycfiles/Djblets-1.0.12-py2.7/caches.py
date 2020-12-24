# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/template/caches.py
# Compiled at: 2019-06-12 01:17:17
"""Utility functions for working with template-related caches."""
from __future__ import unicode_literals
try:
    from django.template.base import libraries
except ImportError:
    libraries = None

try:
    from django.template.base import get_templatetags_modules
except ImportError:
    get_templatetags_modules = None

try:
    from django.template import Engine, engines
except ImportError:
    Engine = None
    engines = None

def clear_template_tag_caches():
    """Clear the template tags caches.

    This allows changes to the list of available template tags to be reflected
    in any new templates by emptying all the caches and forcing the available
    list of tags to be rebuilt.
    """
    if libraries is not None:
        libraries.clear()
    try:
        from django.template.base import templatetags_modules
        del templatetags_modules[:]
    except ImportError:
        if get_templatetags_modules is not None:
            get_templatetags_modules.cache_clear()
        if engines:
            engines._engines.clear()
            Engine.get_default.cache_clear()

    return


def clear_template_caches():
    """Clear the templates caches.

    This clears any caches for template parse trees and related state, forcing
    templates to be re-parsed and re-rendered.
    """
    if engines is not None:
        template_loaders = []
        for engine in engines.all():
            template_loaders += engine.engine.template_loaders

    else:
        from django.template.loader import template_source_loaders
        template_loaders = template_source_loaders or []
    for template_loader in template_loaders:
        try:
            template_loader.reset()
        except AttributeError:
            pass

    return