# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/security/utils.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import logging
from django.conf import settings
from django.utils import timezone
from .emails import generate_security_email
logger = logging.getLogger('sentry.security')

def capture_security_activity(account, type, actor, ip_address, context=None, send_email=True, current_datetime=None):
    if current_datetime is None:
        current_datetime = timezone.now()
    logger_context = {'ip_address': ip_address, 'user_id': account.id, 'actor_id': actor.id}
    if type == 'mfa-removed' or type == 'mfa-added':
        logger_context['authenticator_id'] = context['authenticator'].id
    logger.info(('user.{}').format(type), extra=logger_context)
    if send_email:
        msg = generate_security_email(account=account, type=type, actor=actor, ip_address=ip_address, context=context, current_datetime=current_datetime)
        msg.send_async([account.email])
    return


def is_valid_email_address(value):
    return not settings.INVALID_EMAIL_ADDRESS_PATTERN.search(value)