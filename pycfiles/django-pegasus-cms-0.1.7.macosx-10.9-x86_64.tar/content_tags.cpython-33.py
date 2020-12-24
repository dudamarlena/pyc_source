# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/apps/content/templatetags/content_tags.py
# Compiled at: 2015-02-18 13:07:39
# Size of source mod 2**32: 2165 bytes
from __future__ import absolute_import, division
from content.models import Promo, PromoPlacement
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.template import Library
register = Library()

@register.filter
def summarize(article, num_words=15):
    """ Gets a text summary of the article. This is often used as the
        default 'promo text' for an article."""
    try:
        return article.summary(num_words)
    except:
        return article


@register.inclusion_tag('partials/promos.html')
def get_page_promos(page, position=None):
    page = page.get_public_object()
    promos = Promo.objects.fitler(page=page)
    if position is not None:
        promos = promos.filter(position=position)
    return {'promos': promos}


@register.inclusion_tag('partials/in-the-news.html')
def get_home_right_promos():
    return {'promos': Promo.objects.filter(page=1)}


@register.inclusion_tag('partials/upcoming_event.html')
def get_home_middle_promos():
    return {'promos': Promo.objects.filter(page=1)[:2]}


@register.assignment_tag(takes_context=True)
def get_promos(context, position=None):
    request = context.get('request', {})
    page = getattr(request, 'current_page', None)
    ContentModel = context.get('content_model', None)
    if ContentModel:
        content_type = ContentType.objects.get_for_model(ContentModel)
        if content_type.model == 'author':
            object_id = context['author'].pk
        else:
            object_id = context['article'].pk
    elif page:
        page = page.get_public_object()
        content_type = ContentType.objects.get_for_model(page.__class__)
        object_id = page.pk
    promos = PromoPlacement.objects.filter(content_type=content_type, object_id=object_id)
    if position:
        promos = promos.filter(position=position)
    return promos