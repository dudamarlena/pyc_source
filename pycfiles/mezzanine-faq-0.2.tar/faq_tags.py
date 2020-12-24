# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filip/src/projects/arpamynt/mezzanine_faq/templatetags/faq_tags.py
# Compiled at: 2016-01-14 17:34:20
from django import template
from mezzanine.conf import settings
from mezzanine_faq.models import FaqPage
register = template.Library()

@register.inclusion_tag('includes/faqlist.html')
def faq_list(**kwargs):
    page = FaqPage.objects.get(**kwargs)
    return {'page': page, 
       'faq_questions': page.faqquestion_set.all(), 
       'MEDIA_URL': settings.MEDIA_URL}


@register.inclusion_tag('includes/faqlist.html')
def faq_last(**kwargs):
    page = FaqPage.objects.get(**kwargs)
    return {'page': page, 
       'faq_questions': page.faqquestion_set.all().order_by('-id')[:1], 
       'MEDIA_URL': settings.MEDIA_URL}