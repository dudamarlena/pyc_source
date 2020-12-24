# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/email/dkim.py
# Compiled at: 2015-11-05 10:40:17
"""
.. py:module:: bridgedb.email.dkim
    :synopsis: Functions for checking DKIM verification results in email
               headers.

bridgedb.email.dkim
===================

Functions for checking DKIM verification results in email headers.

::

 bridgedb.email.dkim
  |_ checkDKIM - Check the DKIM verification results header.

..
"""
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