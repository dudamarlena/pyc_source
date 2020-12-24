# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/email/dkim.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = b'\n.. py:module:: bridgedb.email.dkim\n    :synopsis: Functions for checking DKIM verification results in email\n               headers.\n\nbridgedb.email.dkim\n===================\n\nFunctions for checking DKIM verification results in email headers.\n\n::\n\n bridgedb.email.dkim\n  |_ checkDKIM - Check the DKIM verification results header.\n\n..\n'
from __future__ import unicode_literals
import logging

def checkDKIM(message, rules):
    """Check the DKIM verification results header.

    This check is only run if the incoming email, **message**, originated from
    a domain for which we're configured (in the ``EMAIL_DOMAIN_RULES``
    dictionary in the config file) to check DKIM verification results for.

    Returns ``False`` if:

    1. We're supposed to expect and check the DKIM headers for the
       client's email provider domain.
    2. Those headers were *not* okay.

    Otherwise, returns ``True``.

    :type message: :api:`twisted.mail.smtp.rfc822.Message`
    :param message: The incoming client request email, including headers.
    :param dict rules: The list of configured ``EMAIL_DOMAIN_RULES`` for the
        canonical domain which the client's email request originated from.
    :rtype: bool
    :returns: ``False`` if the checks failed, ``True`` otherwise.
    """
    logging.info(b'Checking DKIM verification results...')
    logging.debug(b'Domain has rules: %s' % (b', ').join(rules))
    if b'dkim' in rules:
        dkimHeaders = message.getheaders(b'X-DKIM-Authentication-Results')
        dkimHeader = b'<no header>'
        if dkimHeaders:
            dkimHeader = dkimHeaders[0]
        if not dkimHeader.startswith(b'pass'):
            logging.info(b'Rejecting bad DKIM header on incoming email: %r ' % dkimHeader)
            return False
    return True