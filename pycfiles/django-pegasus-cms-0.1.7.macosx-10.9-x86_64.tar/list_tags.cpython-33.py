# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/extensions/content_list/templatetags/list_tags.py
# Compiled at: 2015-02-18 13:07:39
# Size of source mod 2**32: 788 bytes
from __future__ import absolute_import, division
from django.template import Library
from search import order_explicitly
from search.models import CELERITY_SEARCHQUERYSET
register = Library()

@register.assignment_tag(takes_context=True)
def content_list(context, article_types=[], author=None, count=10):
    request = context['request']
    sqs = CELERITY_SEARCHQUERYSET
    if article_types:
        sqs = sqs.filter(article_type__in=map(lambda t: t.slug or 'undefined', article_types))
    if author:
        sqs = sqs.filter(author_id=author.id)
    sqs = order_explicitly(sqs, count)
    return sqs