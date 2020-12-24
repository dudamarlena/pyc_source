# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\avatarenv\myproject\easy_avatar\templatetags\avatar_tags.py
# Compiled at: 2014-02-23 18:31:29
from django import template
from django.contrib.sites.models import Site
from easy_avatar.models import Easy_Avatar
register = template.Library()

def Get_Url(value):
    current_site = Site.objects.get_current()
    value = str(current_site.domain)
    return value


register.filter('site_url', Get_Url)

@register.inclusion_tag('../templates/upload.html', takes_context=True)
def upload_form(context):
    user = ''
    request = context['request']
    if request.user.is_authenticated():
        user = request.user
    if user != '':
        try:
            url = Easy_Avatar.objects.get(user=user)
            url = url.image_url
        except:
            url = ''

    return {'url': url}