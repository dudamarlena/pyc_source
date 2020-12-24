# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/discounts/templatetags/discount_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1575 bytes
from datetime import datetime
from django.template import Library
from django.utils.safestring import mark_safe
register = Library()

@register.inclusion_tag('discounts/options.html', takes_context=True)
def discount_options(context, user, discount):
    context.update({'opt_object':discount, 
     'user':user})
    return context


@register.inclusion_tag('discounts/nav.html', takes_context=True)
def discount_nav(context, user, discount=None):
    context.update({'nav_object':discount, 
     'user':user})
    return context


@register.inclusion_tag('discounts/search-form.html', takes_context=True)
def discount_search(context):
    return context


@register.inclusion_tag('discounts/top_nav_items.html', takes_context=True)
def discount_current_app(context, user, discount=None):
    context.update({'app_object':discount, 
     'user':user})
    return context


@register.simple_tag
def discount_expiration(obj):
    t = '<span class="status-%s">%s</span>'
    if not obj.never_expires:
        if obj.end_dt < datetime.now():
            value = t % ('inactive', 'Expired on %s' % obj.end_dt.strftime('%m/%d/%Y at %I:%M %p'))
        elif obj.start_dt > datetime.now():
            value = t % ('inactive', 'Starts on %s' % obj.start_dt.strftime('%m/%d/%Y at %I:%M %p'))
        else:
            value = t % ('active', 'Expires on %s' % obj.end_dt.strftime('%m/%d/%Y at %I:%M %p'))
    else:
        value = t % ('active', 'Never Expires')
    return mark_safe(value)