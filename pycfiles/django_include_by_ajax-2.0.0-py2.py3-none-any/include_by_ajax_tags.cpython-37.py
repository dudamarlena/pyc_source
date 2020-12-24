# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/archatas/Projects/django_include_by_ajax/project/django_include_by_ajax/include_by_ajax/templatetags/include_by_ajax_tags.py
# Compiled at: 2018-12-10 21:29:48
# Size of source mod 2**32: 1212 bytes
from __future__ import unicode_literals
import django.apps as apps
from django import template
register = template.Library()

@register.inclusion_tag('include_by_ajax/includes/placeholder.html', takes_context=True)
def include_by_ajax(context, template_name, placeholder_template_name=None):
    app_config = apps.get_app_config('include_by_ajax')
    request = context['request']
    user_agent = request.META.get('HTTP_USER_AGENT') or ''
    is_web_crawler = bool(app_config.web_crawler_pattern.search(user_agent))
    context['include_by_ajax_full_render'] = bool(is_web_crawler or request.is_ajax() and request.GET.get('include_by_ajax_full_render'))
    context['include_by_ajax_no_placeholder_wrapping'] = is_web_crawler
    context['template_name'] = template_name
    context['placeholder_template_name'] = placeholder_template_name
    return context