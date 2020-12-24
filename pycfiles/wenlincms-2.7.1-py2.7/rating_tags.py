# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/generic/templatetags/rating_tags.py
# Compiled at: 2016-05-20 23:42:06
from __future__ import unicode_literals
from wenlincms import template
from wenlincms.generic.forms import RatingForm
register = template.Library()

@register.inclusion_tag(b'generic/includes/rating.html', takes_context=True)
def rating_for(context, obj):
    """
    Provides a generic context variable name for the object that
    ratings are being rendered for, and the rating form.
    """
    context[b'rating_object'] = context[b'rating_obj'] = obj
    context[b'rating_form'] = RatingForm(context[b'request'], obj)
    ratings = context[b'request'].COOKIES.get(b'wenlincms-rating', b'')
    rating_string = b'%s.%s' % (obj._meta, obj.pk)
    context[b'rated'] = rating_string in ratings
    rating_name = obj.get_ratingfield_name()
    for f in ('average', 'count', 'sum'):
        context[b'rating_' + f] = getattr(obj, b'%s_%s' % (rating_name, f))

    return context