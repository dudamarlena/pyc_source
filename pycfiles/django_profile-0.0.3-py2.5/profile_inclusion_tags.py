# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/profile/templatetags/profile_inclusion_tags.py
# Compiled at: 2010-08-04 04:05:50
from django import template
from django.contrib.auth.models import User
register = template.Library()

@register.inclusion_tag('profile/inclusion_tags/avatar.html')
def avatar(username, width, height):
    try:
        profile = User.objects.get(username=username).profile
    except User.DoesNotExist:
        profile = None

    return {'profile': profile, 
       'width': width, 
       'height': height}