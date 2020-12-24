# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/znbstatic/znbstatic/templatetags/znbstatic.py
# Compiled at: 2019-01-07 16:14:59
# Size of source mod 2**32: 972 bytes
from django import template
from django.template.defaultfilters import stringfilter
from znbstatic.utils import add_version_to_url
register = template.Library()

@register.filter
@stringfilter
def znbversion(value, arg):
    """
    Add version query parameter passed as arg to URL passed as value.
    The add_version_to_url function makes the necessary URL parsing and changes.
    Note how static_version is the version passed from the context processor.

    {{ 'http://example.com/file.js?color=red&num=5'|znbversion:static_version }}
    """
    return add_version_to_url(value, arg)


@register.simple_tag(takes_context=True)
def versioned_url(context, url=''):
    """
    A tag to add a version query parameter to a passed URL.
    Note how static_version is retrieved from the context processor.

    {% versioned_url 'http://example.com/file.js?num=1&color=red' %}
    """
    version = context['static_version']
    return add_version_to_url(url, version)