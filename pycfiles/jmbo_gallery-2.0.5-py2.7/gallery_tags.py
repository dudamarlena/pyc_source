# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gallery/templatetags/gallery_tags.py
# Compiled at: 2016-03-10 07:26:59
import re
from django import template
from photologue.models import PhotoSizeCache
register = template.Library()

@register.tag
def videoembed(parser, token):
    try:
        tag_name, obj, photosize = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('videoembed tag requires arguments obj and photosize')

    return VideoEmbedNode(obj, photosize)


class VideoEmbedNode(template.Node):

    def __init__(self, obj, photosize):
        self.obj = template.Variable(obj)
        self.photosize = template.Variable(photosize)

    def render(self, context):
        obj = self.obj.resolve(context)
        photosize = self.photosize.resolve(context)
        size = PhotoSizeCache().sizes.get(photosize)
        result = obj.embed
        result = re.sub('width="([\\d]*)"', 'width="%s"' % size.width, result)
        result = re.sub('height="([\\d]*)"', 'height="%s"' % size.height, result)
        return result