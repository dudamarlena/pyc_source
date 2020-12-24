# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/events/templatetags/event_filters.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 454 bytes
from django.template import Library
register = Library()

@register.filter
def assign_mapped_fields(obj):
    """assign mapped field from custom registration form to registrant"""
    if hasattr(obj, 'custom_reg_form_entry'):
        if obj.custom_reg_form_entry:
            obj.assign_mapped_fields()
    return obj


@register.filter
def discount_used(events):
    for event in events:
        if event.discount_count > 0:
            return True

    return False