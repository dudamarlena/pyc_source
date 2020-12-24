# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/compat/django/template/loader.py
# Compiled at: 2019-06-12 01:17:17
"""Compatibility functions for working with templates.

This module contains compatibility functions for working with templates.
Django 1.8 introduced a new way of working with template backends, and
with this came API changes. The functions in this file help to transition
code over to the new function signatures without breaking older versions of
Django.
"""
from __future__ import unicode_literals
from django.template import Context, RequestContext, Template
from django.template.loader import render_to_string as _render_to_string
try:
    from django.template import engines as template_engines
except ImportError:
    template_engines = None

def render_to_string(template_name, context=None, request=None, using=None):
    """Render a template with a given name to a string.

    This will invoke the original
    :py:func:`~django.template.loader.render_to_string` with the correct
    arguments for the active version of Django. It differs a bit from the
    modern version of the function in that it allows a
    :py:class:`~django.template.Context` argument, which it will convert to
    the correct type.

    Args:
        template_name (unicode):
            The name of the template to render.

        context (object, optional):
            The context data as a dictionary or as a
            :py:class:`~django.template.Context`.

        request (django.http.HttpRequest, optional):
            The HTTP request for the render. If specified, a
            :py:class:`~django.template.RequestContext` will be used.

        using (unicode, optional):
            The optional name of a template engine to use for the render.
            This is only supported on Django 1.8 and higher.

    Returns:
        django.utils.safestring.SafeText:
        The resulting rendered content.
    """
    if template_engines is None:
        if not isinstance(context, Context):
            if request:
                context = RequestContext(request, context)
            else:
                context = Context(context)
        return _render_to_string(template_name, context)
    else:
        if isinstance(context, Context):
            context = context.flatten()
        return _render_to_string(template_name=template_name, context=context, request=request, using=using)
        return


def render_template(template, context={}, request=None):
    """Render a loaded template to a string.

    This will invoke the ``render()`` method on the template object, passing
    in the correct arguments for the active version of Django.

    If the template provided is a :py:class:`django.template.Template`, then
    render calls are consistent across Django versions. However, if it's a
    template returned from a template backend on Django 1.8 or higher, this
    will pass in the raw dictionary instead of a
    :py:class:`~django.template.Context` object to render.

    Args:
        template (object):
            The template to render.

        context (dict, optional):
            The context data as a dictionary.

        request (django.http.HttpRequest, optional):
            The HTTP request for the render. If specified, a
            :py:class:`~django.template.RequestContext` will be used.

    Returns:
        django.utils.safestring.SafeText:
        The resulting rendered content.
    """
    if isinstance(template, Template):
        if request:
            context = RequestContext(request, context)
        else:
            context = Context(context)
        return template.render(context)
    else:
        assert template_engines is not None
        return template.render(context=context, request=request)
        return