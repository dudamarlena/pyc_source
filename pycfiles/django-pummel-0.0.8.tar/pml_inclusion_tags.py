# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tonym/work/django-pummel/pml/templatetags/pml_inclusion_tags.py
# Compiled at: 2013-12-11 01:48:45
from django import template
from django.template import Template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe, SafeData
from pml import utils

class PMLTagException(Exception):
    pass


register = template.Library()

def base_builder(context):
    context['color'] = utils.resolve_color(context['color'])
    return context


@register.inclusion_tag('pml/inclusion_tags/banner.xml', takes_context=True)
def banner(context, image_url):
    t = Template(image_url)
    return {'image_url': t.render(context)}


@register.inclusion_tag('pml/inclusion_tags/divider.xml')
def divider():
    return {}


@register.inclusion_tag('pml/inclusion_tags/header.xml', takes_context=True)
def header(context, text, color=None):
    text = Template(text).render(context)
    context = {}
    context.update(locals())
    return base_builder(context)


@register.inclusion_tag('pml/inclusion_tags/list.xml')
def link_list(objects, url_property, text_property, color=None, role=None):
    context = {}
    context.update(locals())
    context = base_builder(context)
    object_list = []
    for obj in objects:
        if isinstance(obj, dict) and url_property in obj:
            url = obj[url_property]
        else:
            url = getattr(obj, url_property, '')
        if isinstance(obj, dict) and text_property in obj:
            text = obj[text_property]
        else:
            text = getattr(obj, text_property, '')
        object_list.append({'url': url, 
           'text': text})

    context['object_list'] = object_list
    return context


@register.inclusion_tag('pml/inclusion_tags/list.xml')
def horizontal_links(objects, url_property, text_property, color=None):
    context = link_list(objects, url_property, text_property, color)
    context['role'] = 'MOD19'
    return context


@register.inclusion_tag('pml/inclusion_tags/thumbnail_html.xml', takes_context=True)
def thumbnail_html(context, image_url, html, color=None, align='left'):
    image_url = Template(image_url).render(context)
    context.update(locals())
    return base_builder(context)


@register.inclusion_tag('pml/inclusion_tags/thumbnail_html.xml', takes_context=True)
def thumbnail_include(context, image_url, template, color=None, align='left'):
    image_url = Template(image_url).render(context)
    context.update(locals())
    html = render_to_string(template, context)
    context['html'] = mark_safe(utils.html_to_text(html))
    return base_builder(context)


@register.inclusion_tag('pml/inclusion_tags/page_banner.xml', takes_context=True)
def page_banner_include(context, image_url, template, color=None, role=None):
    context.update(locals())
    html = render_to_string(template, context)
    context['html'] = mark_safe(utils.html_to_text(html))
    return base_builder(context)


@register.inclusion_tag('pml/inclusion_tags/clickable_banner.xml', takes_context=True)
def clickable_banner_include(context, image_url, link_url, template, color=None, role=None):
    context.update(locals())
    html = render_to_string(template, context)
    if not isinstance(html, SafeData):
        html = utils.html_to_text(html)
    context['html'] = html
    return base_builder(context)


@register.inclusion_tag('pml/inclusion_tags/link_tag.xml')
def link_tag(url, text, color=None):
    context = {}
    context.update(locals())
    return base_builder(context)


@register.inclusion_tag('pml/inclusion_tags/text_module.xml', takes_context=True)
def text_module(context, html=None, template=None, color=None, role=None):
    if template:
        html = Template(template).render(context)
        html = mark_safe(utils.html_to_text(html))
    context = {}
    context.update(locals())
    return base_builder(context)


@register.inclusion_tag('pml/inclusion_tags/text_module.xml', takes_context=True)
def text_include(context, template, color=None, role=None):
    context.update(locals())
    html = render_to_string(template, context)
    context['html'] = mark_safe(utils.html_to_text(html))
    return base_builder(context)


@register.inclusion_tag('pml/inclusion_tags/text_tag.xml', takes_context=True)
def text_tag(context, html):
    if not isinstance(html, SafeData):
        html = utils.html_to_text(html)
    return locals()


@register.inclusion_tag('pml/inclusion_tags/title_tag.xml', takes_context=True)
def title_tag(context, html):
    html = utils.html_to_text(html)
    return locals()


@register.inclusion_tag('pml/inclusion_tags/redirect.xml', takes_context=True)
def redirect(context, seconds, url=None):
    tenths_of_seconds = seconds * 10
    if not url:
        url = context['request'].META['HTTP_REFERER']
    return locals()