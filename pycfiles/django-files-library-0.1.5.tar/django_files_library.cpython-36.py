# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/templatetags/django_files_library.py
# Compiled at: 2018-02-10 07:51:58
# Size of source mod 2**32: 2139 bytes
from django import template
from django.template import loader
from django_files_library import app_settings
from django_files_library.forms import FileForm
register = template.Library()

@register.simple_tag(takes_context=True)
def render_library(context, library):
    """
    template tag to render library component
    :param context: request context
    :param library: Library object to be rendered
    :return: Html code for library component
    """
    request = context['request']
    csrf_token = context['csrf_token']
    user = request.user
    can_view = library.user_can_read(user)
    can_add_edit = library.user_can_write(user)
    inline_form = app_settings.INLINE_FORM
    template_path = 'django_files_library/full_library.html'
    t = loader.get_template(template_path)
    context = {'library':library, 
     'can_view':can_view, 
     'can_add_edit':can_add_edit, 
     'csrf_token':csrf_token, 
     'inline_form':inline_form, 
     'request':request, 
     'next_page':context['next_page'] if 'next_page' in context else request.path or '/'}
    if inline_form:
        form = FileForm()
        context['form'] = form
    html = t.render(context)
    return html


@register.simple_tag(takes_context=True)
def render_library_list(context, library):
    """
    list view for the library
    :param context: request context
    :param library: Library object to be rendered
    :return: Html code for library files list
    """
    request = context['request']
    user = request.user
    can_view = library.user_can_read(user)
    can_add_edit = library.user_can_write(user)
    template_path = 'django_files_library/library_listing.html'
    t = loader.get_template(template_path)
    context = {'library':library, 
     'request':request, 
     'can_view':can_view, 
     'next_page':context['next_page'] if 'next_page' in context else request.path or '/', 
     'can_add_edit':can_add_edit}
    html = t.render(context)
    return html