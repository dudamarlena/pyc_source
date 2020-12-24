# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johnsanchezc/Projects/django-luhublog/luhublog/templatetags/blog_opengraph_tags.py
# Compiled at: 2015-10-20 10:51:19
from django import template
from django.contrib.contenttypes.models import ContentType
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag
from luhublog.models import OpenGraph
register = template.Library()

class OpenGraphTag(InclusionTag):
    name = 'open_graph_tags'
    template = 'luhublog/__open_graph_tags.html'

    def get_context(self, context):
        object = context.get('object', None)
        if object:
            try:
                content_type = ContentType.objects.get_for_model(object)
            except Exception as e:
                return ''

            try:
                opengraph = OpenGraph.objects.get(content_type=content_type, object_id=object.id)
            except Exception as e:
                return ''

            return {'opengraph': opengraph, 'entry': object}
        return ''


register.tag(OpenGraphTag)