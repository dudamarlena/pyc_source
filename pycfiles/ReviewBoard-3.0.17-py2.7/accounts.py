# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/templatetags/accounts.py
# Compiled at: 2020-02-11 04:03:56
"""Account-related template tags."""
from __future__ import unicode_literals
from django import template
from django.utils.html import escape
register = template.Library()

@register.simple_tag(takes_context=True)
def user_profile_display_name(context, user):
    """Render the user's display name.

    Args:
        context (django.template.context.Context):
            The template rendering context.

        user (django.contrib.auth.models.User):
            The user whose display name is to be rendered.

    Returns:
        unicode:
        The user's display name.
    """
    request = context[b'request']
    if request is not None:
        request_user = request.user
    else:
        request_user = None
    return escape(user.get_profile().get_display_name(request_user))