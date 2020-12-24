# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/djangopypi/templatetags/safemarkup.py
# Compiled at: 2015-10-27 08:49:00
from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
register = template.Library()

def saferst(value):
    try:
        from docutils.core import publish_parts
    except ImportError:
        return force_unicode(value)

    docutils_settings = getattr(settings, 'RESTRUCTUREDTEXT_FILTER_SETTINGS', dict())
    try:
        parts = publish_parts(source=smart_str(value), writer_name='html4css1', settings_overrides=docutils_settings)
    except:
        return force_unicode(value)

    return mark_safe(force_unicode(parts['fragment']))


saferst.is_safe = True
register.filter(saferst)