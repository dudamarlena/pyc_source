# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filip/src/projects/macht/mezzanine_references/templatetags/references_tags.py
# Compiled at: 2015-08-25 14:44:33
from django import template
from mezzanine.conf import settings
from mezzanine_references.models import References
register = template.Library()

@register.inclusion_tag('references/slideshow.html')
def references_slideshow(**kwargs):
    page = References.objects.get(**kwargs)
    return {'references_page': page, 
       'references': page.reference_set.all(), 
       'MEDIA_URL': settings.MEDIA_URL}