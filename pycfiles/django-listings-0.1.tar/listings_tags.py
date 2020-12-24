# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/skylar/pinax/projects/NASA/apps/listings/templatetags/listings_tags.py
# Compiled at: 2009-08-16 12:25:13
from django import template
from listings.models import WatchRelation
register = template.Library()

@register.inclusion_tag('listings/tags/add_remove.html')
def listing_add_remove(listing, user):
    try:
        try:
            watched = WatchRelation.objects.get(watcher=user, listing=listing)
        except:
            watched = None

    finally:
        return locals()