# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/glue/templatetags/glue_tags.py
# Compiled at: 2015-01-01 17:22:32
from django import template
register = template.Library()

@register.inclusion_tag('glue/icon.html')
def icon(name):
    """
    Shortcut to display an icon in templates. Usage:

    .. code-block:: html+django

        {% load glue_tags %}

        {% icon "my-icon" %}
    """
    return {'icon': name}


@register.simple_tag
def query_transform(request, **kwargs):
    """Taken from http://stackoverflow.com/a/24658162/2844093
    return a querystring with updated parameter. Useful, for example
    in pagination to change page number without replacing the whole
    query parameters.

    Usage:

    .. code-block:: html+django

        <a href="/path?{% query_transform request a=5 b=6 %}">
    """
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v

    return updated.urlencode()