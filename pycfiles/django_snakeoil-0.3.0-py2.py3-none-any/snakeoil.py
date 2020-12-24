# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomcarrick/projects/django-snakeoil/snakeoil/templatetags/snakeoil.py
# Compiled at: 2015-03-26 05:49:24
from __future__ import unicode_literals
import logging
from django import template
from ..utils import get_seo_model
from ..models import SeoUrl
logger = logging.getLogger(__name__)
register = template.Library()

class SeoDataNode(template.Node):

    def __init__(self, variable_name):
        self.variable_name = variable_name

    def render(self, context):
        seo_model = get_seo_model()
        flat_context = context.flatten()
        path = flat_context[b'request'].path
        logger.debug(b'Looking for SEO object')
        for obj in flat_context.values():
            if hasattr(obj, b'get_absolute_url') and obj.get_absolute_url() == path:
                logger.debug((b'Found object: `{}`').format(obj))
                seo = {}
                for field in seo_model._meta.fields:
                    if getattr(obj, field.name, b'') != b'':
                        logger.debug((b'Adding field `{}` to SEO dict').format(field.name))
                        seo[field.name] = getattr(obj, field.name)

                if seo:
                    context[self.variable_name] = seo
                    logger.debug(b'Returning with object data')
                    return b''

        logger.debug(b'Looking for SEO URL')
        try:
            seo_url = SeoUrl.objects.get(url=path)
        except SeoUrl.DoesNotExist:
            logger.debug(b'No SEO URL found')
            return b''

        logger.debug(b'SEO URL found')
        seo = {}
        for field in seo_model._meta.fields:
            if getattr(seo_url, field.name, b'') != b'':
                seo[field.name] = getattr(seo_url, field.name)
                logger.debug((b'Adding field `{}` to SEO dict').format(field.name))

        context[self.variable_name] = seo
        logger.debug(b'Returning with URL data')
        return b''


def do_get_seo_data(parser, token):
    bits = token.split_contents()
    if len(bits) > 1 and (len(bits) > 3 or bits[1] != b'as'):
        raise template.TemplateSyntaxError((b'Format is {} [as variable] ').format(bits[0]))
    try:
        variable_name = bits[2]
    except IndexError:
        variable_name = b'seo'

    return SeoDataNode(variable_name)


register.tag(b'get_seo_data', do_get_seo_data)