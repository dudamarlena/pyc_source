# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/avatars/services/gravatar.py
# Compiled at: 2019-06-12 01:17:17
"""An avatar service for providing Gravatars."""
from __future__ import unicode_literals
from django.utils.html import mark_safe
from djblets.avatars.services.base import AvatarService
from djblets.gravatars import get_gravatar_url_for_email
from djblets.privacy.consent.common import BaseGravatarConsentRequirement

class GravatarService(AvatarService):
    """An avatar service for providing Gravatars."""
    avatar_service_id = b'gravatar'
    name = b'Gravatar'
    consent_requirement_id = BaseGravatarConsentRequirement.requirement_id

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
        return {b'%dx' % resolution:mark_safe(get_gravatar_url_for_email(email=user.email, size=size * resolution)) for resolution in (1,
                                                                                                                                       2,
                                                                                                                                       3)}

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
         self.avatar_service_id, user.email]