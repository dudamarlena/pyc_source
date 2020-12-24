# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johnsanchezc/Projects/django-luhublog/luhublog/templatetags/blog_seo_tags.py
# Compiled at: 2015-10-20 08:08:57
from django import template
from django.contrib.contenttypes.models import ContentType
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag
from luhublog.models import SeoMeta
register = template.Library()

class SeoTag(InclusionTag):
    name = 'seo_tags'
    template = 'luhublog/__seo_tags.html'

    def get_context(self, context):
        object = context.get('object', None)
        if object:
            try:
                content_type = ContentType.objects.get_for_model(object)
            except Exception as e:
                return ''

            try:
                seo = SeoMeta.objects.get(content_type=content_type, object_id=object.id)
            except Exception as e:
                return ''

            return {'seo': seo}
        return ''


register.tag(SeoTag)