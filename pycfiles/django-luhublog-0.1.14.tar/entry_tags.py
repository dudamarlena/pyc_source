# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johnsanchezc/Projects/django-luhublog/luhublog/templatetags/entry_tags.py
# Compiled at: 2015-10-19 12:03:40
from django import template
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag
register = template.Library()

class EntrySeoTag(InclusionTag):
    name = 'entry_meta_seo'
    template = 'luhublog/__seo_entry_meta.html'

    def get_context(self, context):
        entry = context.get('entry', None)
        if entry:
            try:
                meta = entry.entryseo
            except Exception as e:
                return ''

            return {'meta': meta, 'entry': entry}
        return ''


register.tag(EntrySeoTag)