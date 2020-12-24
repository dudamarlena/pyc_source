# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/compat/django/template/context.py
# Compiled at: 2019-06-12 01:17:17
"""Compatibility functions for working with template contexts."""
from __future__ import unicode_literals
from django.template.context import Context

def flatten_context(context):
    """Flatten a template context into a dictionary.

    Django 1.7 introduced :py:meth:`Context.flatten
    <django.template.Context.flatten>`, which converts a template context into
    a dictionary. However, this doesn't exist on Django 1.6. This compatibility
    function ensures equivalent functionality on both.
    """
    assert isinstance(context, Context)
    if hasattr(context, b'flatten'):
        return context.flatten()
    else:
        new_dict = {}
        for d in context.dicts:
            new_dict.update(d)

        return new_dict