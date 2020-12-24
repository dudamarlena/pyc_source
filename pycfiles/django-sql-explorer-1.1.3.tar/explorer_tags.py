# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/templatetags/explorer_tags.py
# Compiled at: 2019-07-02 16:47:10
from django import template
from django.utils.module_loading import import_string
from explorer import app_settings
register = template.Library()

@register.inclusion_tag('explorer/export_buttons.html')
def export_buttons(query=None):
    exporters = []
    for name, classname in app_settings.EXPLORER_DATA_EXPORTERS:
        exporter_class = import_string(classname)
        exporters.append((name, exporter_class.name))

    return {'exporters': exporters, 'query': query}