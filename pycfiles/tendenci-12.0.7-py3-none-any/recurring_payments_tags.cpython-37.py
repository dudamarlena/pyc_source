# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/recurring_payments/templatetags/recurring_payments_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 491 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('recurring_payments/nav.html', takes_context=True)
def rp_nav(context, user, rp=None):
    context.update({'nav_object':rp, 
     'user':user})
    return context


@register.inclusion_tag('recurring_payments/top_nav_items.html', takes_context=True)
def rp_current_app(context, user, rp=None):
    context.update({'app_object':rp, 
     'user':user})
    return context