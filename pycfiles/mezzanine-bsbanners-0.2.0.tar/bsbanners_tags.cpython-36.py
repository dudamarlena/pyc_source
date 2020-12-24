# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/templatetags/bsbanners_tags.py
# Compiled at: 2018-11-16 08:16:10
# Size of source mod 2**32: 3559 bytes
"""
Mezzanine BS Banners
Making it easier to manage attention grabbing and compelling banners
"""
from __future__ import unicode_literals
from django import template
from django.template import loader
from mezzanine_bsbanners.models import Banners
from mezzanine.conf import settings
register = template.Library()

class BSBannerBlockWrapper(object):
    __doc__ = '\n    Wrapper class to render a BS Banner block\n    '
    slug = None
    template_name = None

    def prepare(self, parser, token):
        """
        The parser checks for following tag invocations:
            {% bsbanner {URL} %}
            {% bsbanner {URL} {template_name} %}
        """
        msg = '%r tag should have between 1 and 2 arguments         for slug of banner to display and optional template'
        tokens = token.split_contents()
        self.slug = None
        self.template_name = None
        if len(tokens) < 2:
            raise template.TemplateSyntaxError(msg % (tokens[0],))
        if len(tokens) > 3:
            raise template.TemplateSyntaxError(msg % (tokens[0],))
        else:
            self.slug = tokens[1]
            if len(tokens) == 3:
                self.template_name = tokens[2]
            if self.slug[0] in ('"', "'"):
                self.slug = self.slug[1:-1]
            else:
                self.slug = template.Variable(self.slug)
            if self.template_name is None:
                self.template_name = 'bsbanners/banner.html'
            else:
                if self.template_name[0] in ('"', "'"):
                    self.template_name = self.template_name[1:-1]
                else:
                    self.template_name = template.Variable(self.template_name)

    def __call__(self, parser, token):
        self.prepare(parser, token)
        return BSBannerBlockNode((self.slug), template_name=(self.template_name))


do_bsbannerblock = BSBannerBlockWrapper()

class BSBannerBlockNode(template.Node):
    __doc__ = '\n    Get a block node\n    '

    def __init__(self, slug, template_name=None):
        self.slug = slug
        self.template_name = template_name

    def render(self, context):
        try:
            if isinstance(self.slug, template.Variable):
                self.slug = self.slug.resolve(context)
            bsbannerblock = Banners.objects.get(slug=(self.slug),
              status=2)
            slides = []
            isfirst = True
            qry_slides = bsbannerblock.slides_set.filter(status=2).order_by('sort_order')
            for slide in qry_slides:
                slide.isfirst = isfirst
                isfirst = False
                slides.append(slide)

            tmpl = loader.get_template(self.template_name)
            new_context = {'bsbannerblock':bsbannerblock, 
             'slides':slides, 
             'MEDIA_URL':settings.MEDIA_URL}
            return tmpl.render(new_context)
        except Banners.DoesNotExist:
            return ''


register.tag('bsbanner', do_bsbannerblock)