# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/community/templatetags/sph_tagging.py
# Compiled at: 2012-03-17 12:42:14
from django import template
from sphene.community.models import tag_get_labels
from sphene.community.templatetagutils import SimpleRetrieverNode, simple_retriever_tag
register = template.Library()

@register.filter
def sph_tag_labels(value):
    return tag_get_labels(value)


def get_tag_labels(instance, context):
    return tag_get_labels(instance)


@register.tag(name='sph_tagging_get_labels')
def sphblock_get_blocks(parser, token):
    return simple_retriever_tag(parser, token, 'sph_tagging_get_labels', get_tag_labels)