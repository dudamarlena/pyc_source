# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/user_social_identity_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import logging, six
from rest_framework.response import Response
from social_auth.backends import get_backend
from social_auth.models import UserSocialAuth
from sentry.api.bases.user import UserEndpoint
logger = logging.getLogger('sentry.accounts')

class UserSocialIdentityDetailsEndpoint(UserEndpoint):

    def delete(self, request, user, identity_id):
        """
        Disconnect a Identity from Account
        ```````````````````````````````````````````````````````

        Disconnects a social auth identity from a sentry account

        :pparam string identity_id: identity id
        :auth: required
        """
        try:
            auth = UserSocialAuth.objects.get(id=identity_id)
        except UserSocialAuth.DoesNotExist:
            return Response(status=404)

        backend = get_backend(auth.provider, request, '/')
        if backend is None:
            raise Exception(('Backend was not found for request: {}').format(auth.provider))
        try:
            backend.disconnect(user, identity_id)
        except Exception as exc:
            import sys
            exc_tb = sys.exc_info()[2]
            six.reraise(Exception, exc, exc_tb)
            del exc_tb

        assert not UserSocialAuth.objects.filter(user=user, id=identity_id).exists()
        logger.info('user.identity.disconnect', extra={'user_id': user.id, 
           'ip_address': request.META['REMOTE_ADDR'], 
           'usersocialauth_id': identity_id})
        return Response(status=204)