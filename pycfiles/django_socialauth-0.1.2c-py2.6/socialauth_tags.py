# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialauth/templatetags/socialauth_tags.py
# Compiled at: 2010-07-01 06:59:33
from django import template
register = template.Library()

@register.simple_tag
def get_calculated_username(user):
    if hasattr(user, 'openidprofile_set') and user.openidprofile_set.filter().count():
        if user.openidprofile_set.filter(is_username_valid=True).count():
            return user.openidprofile_set.filter(is_username_valid=True)[0].user.username
        else:
            from django.core.urlresolvers import reverse
            editprof_url = reverse('socialauth_editprofile')
            return 'Anonymous User. <a href="%s">Add name</a>' % editprof_url
    else:
        return user.username