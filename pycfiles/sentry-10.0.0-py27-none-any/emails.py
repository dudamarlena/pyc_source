# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/security/emails.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.utils import timezone
from sentry.utils.email import MessageBuilder

def generate_security_email(account, type, actor, ip_address, context=None, current_datetime=None):
    if current_datetime is None:
        current_datetime = timezone.now()
    subject = 'Security settings changed'
    if type == 'mfa-removed':
        assert 'authenticator' in context
        template = 'sentry/emails/mfa-removed.txt'
        html_template = 'sentry/emails/mfa-removed.html'
    elif type == 'mfa-added':
        assert 'authenticator' in context
        template = 'sentry/emails/mfa-added.txt'
        html_template = 'sentry/emails/mfa-added.html'
    elif type == 'password-changed':
        template = 'sentry/emails/password-changed.txt'
        html_template = 'sentry/emails/password-changed.html'
    elif type == 'recovery-codes-regenerated':
        template = 'sentry/emails/recovery-codes-regenerated.txt'
        html_template = 'sentry/emails/recovery-codes-regenerated.html'
    elif type == 'api-token-generated':
        template = 'sentry/emails/api-token-generated.txt'
        html_template = 'sentry/emails/api-token-generated.html'
    else:
        raise ValueError(('unknown type: {}').format(type))
    new_context = {'account': account, 
       'actor': actor, 
       'ip_address': ip_address, 
       'datetime': current_datetime}
    if context:
        new_context.update(context)
    return MessageBuilder(subject=subject, context=new_context, template=template, html_template=html_template, type=type)