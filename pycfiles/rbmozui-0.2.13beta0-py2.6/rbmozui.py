# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbmozui/templatetags/rbmozui.py
# Compiled at: 2015-01-17 18:30:02
from django import template
register = template.Library()

@register.filter()
def isSquashed(aReviewRequest):
    return str(aReviewRequest.extra_data.get('p2rb.is_squashed', 'False')).lower() == 'true'


@register.filter()
def isPush(aReviewRequest):
    return str(aReviewRequest.extra_data.get('p2rb', 'False')).lower() == 'true'