# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /www/elorus/local/lib/python2.7/site-packages/yawdadmin/templatetags/yawdadmin_filters.py
# Compiled at: 2013-10-20 16:22:18
from django import template
from ..admin import PopupInline
from ..forms import PopupInlineFormSet
register = template.Library()

@register.filter
def divide(value, num):
    return int(value / num)


@register.filter
def app_title(value):
    return value.replace('_', ' ')


@register.filter
def utfupper(value):
    orig = ['Ά', 'Έ', 'Ή', 'Ί', 'ΐ', 'Ό', 'Ύ', 'Ώ']
    rep = ['Α', 'Ε', 'Η', 'Ι', 'Ϊ', 'Ο', 'Υ', 'Ω']
    return ('').join([ rep[orig.index(x)] if x in orig else x for x in value.upper()
                     ])


@register.filter
def istranslationinline(value):
    """
    This filter is used if yawd-translations is installed.
    """
    try:
        from translations.admin import TranslationInline
    except:
        return False

    if hasattr(value, 'opts') and isinstance(value.opts, TranslationInline):
        return True
    return False


@register.filter
def ispopupinline(value):
    """
    This filter is used if yawd-translations is installed.
    """
    if hasattr(value, 'opts') and isinstance(value.opts, PopupInline):
        return True
    return False


@register.filter
def popup_change_url(formset, obj_id):
    """
    Used in PopupInline
    """
    if isinstance(formset, PopupInlineFormSet):
        return formset.get_change_url(obj_id)


@register.filter
def popup_delete_url(formset, obj_id):
    if isinstance(formset, PopupInlineFormSet):
        return formset.get_delete_url(obj_id)


@register.filter
def fix_collapse(classes):
    return classes.replace('collapse', '')