# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/emails/templatetags/email_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 614 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('emails/options.html', takes_context=True)
def emails_options(context, email):
    context.update({'opt_object': email})
    return context


@register.inclusion_tag('emails/nav.html', takes_context=True)
def emails_nav(context, email=None):
    context.update({'nav_object': email})
    return context


@register.inclusion_tag('emails/top_nav_items.html', takes_context=True)
def emails_current_app(context, email=None):
    context.update({'app_object': email})
    return context