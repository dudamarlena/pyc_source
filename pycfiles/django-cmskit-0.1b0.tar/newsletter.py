# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/newsletter/templatetags/newsletter.py
# Compiled at: 2012-10-03 10:22:24
from django import template
from django.conf import settings
from senpilic.newsletter.forms import SubscriptionForm
register = template.Library()

@register.inclusion_tag('newsletter/_form.html')
def subscription_form(*args, **kwargs):
    return {'form': SubscriptionForm()}