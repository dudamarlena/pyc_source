# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\david\Projects\cosmicdb\cosmicdb\templatetags\cosmic_tags.py
# Compiled at: 2017-10-21 09:38:52
# Size of source mod 2**32: 534 bytes
from django.conf import settings
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def get_site_title():
    return settings.COSMICDB_SITE_TITLE or 'CosmicDB'


@register.simple_tag
def get_signup_link_login():
    if hasattr(settings, 'COSMICDB_ALLOW_SIGNUP'):
        if settings.COSMICDB_ALLOW_SIGNUP or False:
            return mark_safe('<a href="%s">Sign up</a>' % reverse('signup'))
    return ''