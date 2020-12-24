# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\david\Projects\cosmicdbsemantic\cosmicdb\templatetags\cosmic_tags.py
# Compiled at: 2018-05-22 10:28:21
# Size of source mod 2**32: 634 bytes
from django.conf import settings
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
import importlib
register = template.Library()

@register.simple_tag
def get_site_title():
    return settings.COSMICDB_SITE_TITLE or 'CosmicDB'


@register.simple_tag(takes_context=True)
def get_formset_label(context, formset_prefix):
    formset_labels = context.get('formset_labels', {})
    formset_label = ''
    if formset_prefix in formset_labels:
        formset_label = '<h3>' + str(formset_labels[formset_prefix]) + '</h3>'
    return mark_safe(formset_label)