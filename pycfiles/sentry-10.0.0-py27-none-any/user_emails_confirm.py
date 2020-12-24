# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/user_emails_confirm.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import logging
from rest_framework import serializers, status
from rest_framework.response import Response
from sentry.api.bases.user import UserEndpoint
from sentry.api.decorators import sudo_required
from sentry.api.validators import AllowedEmailField
from sentry.models import UserEmail
logger = logging.getLogger('sentry.accounts')

class InvalidEmailResponse(Response):

    def __init__(self):
        super(InvalidEmailResponse, self).__init__({'detail': 'Invalid email', 'email': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)


class InvalidEmailError(Exception):
    pass


class DuplicateEmailError(Exception):
    pass


class EmailSerializer(serializers.Serializer):
    email = AllowedEmailField(required=True)


class UserEmailsConfirmEndpoint(UserEndpoint):

    @sudo_required
    def post(self, request, user):
        """
        Sends a confirmation email to user
        ``````````````````````````````````

        :auth required:
        """
        from sentry.app import ratelimiter
        if ratelimiter.is_limited(('auth:confirm-email:{}').format(user.id), limit=10, window=60):
            return self.respond({'detail': 'You have made too many email confirmation requests. Please try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        else:
            serializer = EmailSerializer(data=request.data)
            if not serializer.is_valid():
                return InvalidEmailResponse()
            try:
                email_to_send = UserEmail.objects.get(user=user, email=serializer.validated_data['email'].lower().strip())
            except UserEmail.DoesNotExist:
                return InvalidEmailResponse()

            if email_to_send.is_verified:
                return self.respond({'detail': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
            user.send_confirm_email_singular(email_to_send)
            logger.info('user.email.start_confirm', extra={'user_id': user.id, 
               'ip_address': request.META['REMOTE_ADDR'], 
               'email': email_to_send})
            return self.respond(status=status.HTTP_204_NO_CONTENT)