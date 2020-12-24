# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/templates.py
# Compiled at: 2015-05-20 08:16:45
# Size of source mod 2**32: 2001 bytes
import functools, jinja2
from django.template.response import TemplateResponse
from django.template.loader import get_template
from ginger.template import library
from ginger.serializer import JSONTemplate
__all__ = [
 'GingerResponse',
 'ginger_tag',
 'filter_tag',
 'function_tag',
 'test_tag']

def ginger_tag(template=None, name=None, takes_context=False, mark_safe=False):

    def closure(orig_func):
        func = orig_func
        name_ = name or getattr(func, '_decorated_function', func).__name__
        if template:

            def wrapper(*args, **kwargs):
                t = get_template(template)
                values = orig_func(*args, **kwargs)
                result = t.render(values)
                result = jinja2.Markup(result)
                return result

            func = functools.update_wrapper(wrapper, func)
        elif mark_safe:

            def wrapper(*args, **kwargs):
                result = orig_func(*args, **kwargs)
                return jinja2.Markup(result)

            func = functools.update_wrapper(wrapper, func)
        if takes_context:
            func = jinja2.contextfunction(func)
        library.global_function(name_, func)
        return orig_func

    return closure


function_tag = library.global_function
filter_tag = library.filter
test_tag = library.test

def field_layout(func):
    from ginger.html import forms
    name = func.__name__
    forms.register_layout(name, func)
    return func


class GingerResponse(TemplateResponse):

    def is_json(self):
        return self['content-type'] == 'application/json'

    def resolve_context(self, context):
        if self.is_json():
            return context
        else:
            context = super(GingerResponse, self).resolve_context(context)
            return context

    def resolve_template(self, template):
        if self.is_json():
            return JSONTemplate
        return super(GingerResponse, self).resolve_template(template)