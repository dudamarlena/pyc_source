# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/templatetags/bsbanners_tags.py
# Compiled at: 2018-11-16 08:16:10
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
    """
    Wrapper class to render a BS Banner block
    """
    slug = None
    template_name = None

    def prepare(self, parser, token):
        """
        The parser checks for following tag invocations:
            {% bsbanner {URL} %}
            {% bsbanner {URL} {template_name} %}
        """
        msg = b'%r tag should have between 1 and 2 arguments         for slug of banner to display and optional template'
        tokens = token.split_contents()
        self.slug = None
        self.template_name = None
        if len(tokens) < 2:
            raise template.TemplateSyntaxError(msg % (tokens[0],))
        if len(tokens) > 3:
            raise template.TemplateSyntaxError(msg % (tokens[0],))
        self.slug = tokens[1]
        if len(tokens) == 3:
            self.template_name = tokens[2]
        if self.slug[0] in ('"', "'"):
            self.slug = self.slug[1:-1]
        else:
            self.slug = template.Variable(self.slug)
        if self.template_name is None:
            self.template_name = b'bsbanners/banner.html'
        elif self.template_name[0] in ('"', "'"):
            self.template_name = self.template_name[1:-1]
        else:
            self.template_name = template.Variable(self.template_name)
        return

    def __call__(self, parser, token):
        self.prepare(parser, token)
        return BSBannerBlockNode(self.slug, template_name=self.template_name)


do_bsbannerblock = BSBannerBlockWrapper()

class BSBannerBlockNode(template.Node):
    """
    Get a block node
    """

    def __init__(self, slug, template_name=None):
        self.slug = slug
        self.template_name = template_name

    def render(self, context):
        try:
            if isinstance(self.slug, template.Variable):
                self.slug = self.slug.resolve(context)
            bsbannerblock = Banners.objects.get(slug=self.slug, status=2)
            slides = []
            isfirst = True
            qry_slides = bsbannerblock.slides_set.filter(status=2).order_by(b'sort_order')
            for slide in qry_slides:
                slide.isfirst = isfirst
                isfirst = False
                slides.append(slide)

            tmpl = loader.get_template(self.template_name)
            new_context = {b'bsbannerblock': bsbannerblock, 
               b'slides': slides, 
               b'MEDIA_URL': settings.MEDIA_URL}
            return tmpl.render(new_context)
        except Banners.DoesNotExist:
            return b''


register.tag(b'bsbanner', do_bsbannerblock)