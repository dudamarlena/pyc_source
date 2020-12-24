# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/mail/utils.py
# Compiled at: 2019-06-12 01:17:17
"""General utility functions for working with e-mail."""
from __future__ import unicode_literals
from email.utils import formataddr, parseaddr
from django.conf import settings

def build_email_address(email, full_name=None):
    """Build an e-mail address for a To/CC/BCC field from a user's information.

    Args:
        email (unicode):
            The e-mail address.

        full_name (unicode, optional):
            The optional full name associated with the e-mail address.

    Returns:
        unicode:
        A formatted e-mail address intended for a To/CC/BCC field.
    """
    return formataddr((full_name, email))


def build_email_address_for_user(user):
    """Build an e-mail address for a To/CC/BCC field from a User.

    Args:
        user (django.contrib.auth.models.User):
            The user.

    Returns:
        unicode:
        A formatted e-mail address intended for a To/CC/BCC field.
    """
    return build_email_address(email=user.email, full_name=user.get_full_name())


def build_email_address_via_service(email, full_name=None, service_name=None, sender_email=None):
    """Build an e-mail address for sending on behalf of a user via a service.

    This will construct a formatted e-mail address that can be safely used
    in a :mailheader:`From` field without risking being quarantined/rejected
    by DMARC rules.

    The address will be in the form of "Full Name via Service Name
    <sender@domain.tld>".

    Args:
        email (unicode):
            The unformatted e-mail address of the user.

        full_name (unicode, optional):
            The full name of the user. If not provided, the username in the
            e-mail address will be used.

        service_name (unicode, optional):
            The name of the service sending the e-mail. If not provided,
            ``settings.EMAIL_DEFAULT_SENDER_SERVICE_NAME`` will be used.

        sender_email (unicode, optional):
            The unformatted e-mail address for the sending service. If not
            provided, the e-mail address in
            :django:setting:`DEFAULT_FROM_EMAIL` will be used.

    Returns:
        unicode:
        A formatted e-mail address safe to use in a :mailheader:`From` field.
    """
    if not service_name:
        service_name = getattr(settings, b'EMAIL_DEFAULT_SENDER_SERVICE_NAME', None) or email.split(b'@')[(-1)]
    if not sender_email:
        sender_email = parseaddr(settings.DEFAULT_FROM_EMAIL)[1]
    if not full_name:
        full_name = email.split(b'@')[0]
    return build_email_address(email=sender_email, full_name=b'%s via %s' % (full_name, service_name))