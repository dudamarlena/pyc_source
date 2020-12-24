# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jack/Projects/MaterialDjango/materialdjango/templatetags/polymerdep.py
# Compiled at: 2017-03-08 16:51:50
from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(is_safe=True)
def dep(value='polymer/polymer.html'):
    static_url = static('materialdjango/components/bower_components/%s' % value)
    return ('<link rel="import" href="{0}">').format(static_url)


@register.simple_tag
def polymer_shim():
    static_url = static('materialdjango/components/bower_components/webcomponentsjs/webcomponents.js')
    return mark_safe(("<script src='{0}'></script>").format(static_url))