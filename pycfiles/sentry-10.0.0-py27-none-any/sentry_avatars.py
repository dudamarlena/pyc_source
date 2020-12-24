# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/templatetags/sentry_avatars.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from six.moves.urllib.parse import urlencode
from sentry.models import User, UserAvatar
from sentry.utils.avatar import get_email_avatar, get_gravatar_url, get_letter_avatar
register = template.Library()

@register.simple_tag(takes_context=True)
def gravatar_url(context, email, size, default='mm'):
    return get_gravatar_url(email, size, default)


@register.simple_tag(takes_context=True)
def letter_avatar_svg(context, display_name, identifier, size=None):
    return get_letter_avatar(display_name, identifier, size=size)


@register.simple_tag(takes_context=True)
def profile_photo_url(context, user_id, size=None):
    try:
        avatar = UserAvatar.objects.get_from_cache(user=user_id)
    except UserAvatar.DoesNotExist:
        return

    url = reverse('sentry-user-avatar-url', args=[avatar.ident])
    if size:
        url += '?' + urlencode({'s': size})
    return settings.SENTRY_URL_PREFIX + url


@register.simple_tag(takes_context=True)
def email_avatar(context, display_name, identifier, size=None, try_gravatar=True):
    return get_email_avatar(display_name, identifier, size, try_gravatar)


@register.inclusion_tag('sentry/partial/avatar.html')
def avatar(user, size=36):
    if isinstance(user, User):
        user_id = user.id
        email = user.email
    else:
        user_id = user.user_id
        email = user.email
        if user_id:
            email = user.user.email
    return {'email': email, 
       'user_id': user_id, 
       'size': size, 
       'avatar_type': user.get_avatar_type(), 
       'display_name': user.get_display_name(), 
       'label': user.get_label()}


@register.inclusion_tag('sentry/partial/avatar.html')
def avatar_for_email(user, size=36):
    if isinstance(user, User):
        user_id = user.id
        email = user.email
    else:
        user_id = user.user_id
        email = user.email
        if user_id:
            email = user.user.email
    return {'for_email': True, 
       'email': email, 
       'user_id': user_id, 
       'size': size, 
       'avatar_type': user.get_avatar_type(), 
       'display_name': user.get_display_name(), 
       'label': user.get_label()}