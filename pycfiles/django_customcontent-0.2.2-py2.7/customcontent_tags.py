# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/customcontent/templatetags/customcontent_tags.py
# Compiled at: 2011-05-29 08:22:06
from django import template
from django.conf import settings
from customcontent.models import CustomContent, CustomItem
from customcontent import wrap_strings
import urlparse
register = template.Library()

def cc_item(content_items, *args):
    """
        Helper method to take the input request and a list of
        attributes (of a CustomContent object) and generates
        the stringified (!?) version of the code.
    """
    content = list()
    if not content_items:
        return None
    else:
        for cc in content_items:
            for arg in args:
                c_content = getattr(cc, arg)
                try:
                    items = c_content.all()
                    for item in items:
                        content.append([item.render()])

                except AttributeError:
                    try:
                        content.append([wrap_strings[arg] % c_content])
                    except KeyError:
                        content.append([c_content])

        return ('\n').join([ item for res in content for item in res ])


def getcontent(request, *args):
    item = CustomContent.find(request)
    return cc_item(item, *args)


@register.simple_tag(takes_context=True)
def customcontent_head(context):
    """
        Render out any extra headers for this path
    """
    return getcontent(context['request'], 'extra_head')


@register.simple_tag(takes_context=True)
def customcontent_js(context):
    """
        Render out any custom JS for this path
    """
    return getcontent(context['request'], 'js')


@register.simple_tag(takes_context=True)
def customcontent_css(context):
    """
        Render out any custom CSS for this path
    """
    return getcontent(context['request'], 'css')


@register.simple_tag(takes_context=True)
def customcontent_allhead(context):
    """
        Saver method to call on all the header attributes
    """
    return getcontent(context['request'], 'extra_head', 'js', 'css')


@register.simple_tag(takes_context=True)
def customcontent_items(context):
    """
        Uses the related manager to return all the items for
        all the matching CustomContent objects for the current path
    """
    return getcontent(context['request'], 'customitem_set')