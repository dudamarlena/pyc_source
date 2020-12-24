# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/templatetags/beanbag_licensing.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django import template
from djblets.util.decorators import basictag
register = template.Library()

@register.tag
@basictag(takes_context=True)
def licensing_trial_url(context, extension):
    return extension.get_trial_url(context[b'request'])


@register.tag
@basictag(takes_context=True)
def licensing_purchase_url(context, extension):
    return extension.get_purchase_url(context[b'request'])