# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/resumes/templatetags/resume_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 825 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('resumes/options.html', takes_context=True)
def resume_options(context, user, resume):
    context.update({'opt_object':resume, 
     'user':user})
    return context


@register.inclusion_tag('resumes/nav.html', takes_context=True)
def resume_nav(context, user, resume=None):
    context.update({'nav_object':resume, 
     'user':user})
    return context


@register.inclusion_tag('resumes/search-form.html', takes_context=True)
def resume_search(context):
    return context


@register.inclusion_tag('resumes/top_nav_items.html', takes_context=True)
def resume_current_app(context, user, resume=None):
    context.update({'app_object':resume, 
     'user':user})
    return context