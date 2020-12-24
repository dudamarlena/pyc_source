# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/avatars/services/fallback.py
# Compiled at: 2019-06-12 01:17:17
"""An avatar service used as a fallback to show something basic for a user."""
from __future__ import unicode_literals
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from djblets.avatars.services.base import AvatarService

class FallbackService(AvatarService):
    """An avatar service used as a fallback.

    This will display a simple avatar showing the first two characters of the
    user's username, displayed on top of a background with a color based on the
    username.

    This will automatically be used as a fallback if no other avatar backends
    are usable for the user.
    """
    avatar_service_id = b'fallback'
    name = _(b'Fallback')
    template_name = b'avatars/fallback.html'
    hidden = True

    def render(self, request, user, size, template_name=None):
        """Render a user's avatar to HTML.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

            user (django.contrib.auth.models.User):
                The user for whom the avatar is to be rendered.

            size (int):
                The requested avatar size (height and width) in pixels.

            template_name (unicode, optional):
                The name of the template to use for rendering.

        Returns:
            django.utils.safestring.SafeText:
            The rendered avatar HTML.
        """
        return render_to_string(template_name or self.template_name, {b'bg': self.get_bg_color(user), 
           b'font_size': b'%spx' % (size / 3), 
           b'size': size, 
           b'text': user.username[:2].upper(), 
           b'user': user})

    def get_bg_color(self, user):
        """Return a background color for the avatar.

        This will compute a basic HSL color for the avatar, based on the
        username.

        Args:
            user (django.contrib.auth.models.User):
                The user to generate the color for.

        Returns:
            unicode:
            The resulting HSL color definition.
        """
        i = 0
        for c in user.username:
            i = ord(c) + ((i << 5) - i)

        i = i % 360
        return b'hsl(%s, 60%%, 80%%)' % i

    def get_avatar_urls_uncached(self, user, size):
        """Return the Gravatar URLs for the requested user.

        Args:
            user (django.contrib.auth.models.User):
                The user whose avatar URLs are to be fetched.

            size (int):
                The size (in pixels) the avatar is to be rendered at.

        Returns
            dict:
            A dictionary containing the URLs of the user's avatars at normal-
            and high-DPI.
        """
        return {b'1x': b'', 
           b'2x': b'', 
           b'3x': b''}

    def get_etag_data(self, user):
        """Return the ETag data for the user's avatar.

        Args:
            user (django.contrib.auth.models.User):
                The user.

        Returns:
            list of unicode:
            The uniquely identifying information for the user's avatar.
        """
        return [
         self.avatar_service_id, user.username]