# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/certs.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals

class Certificate(object):
    """A representation of an HTTPS certificate."""

    def __init__(self, pem_data=b'', valid_from=b'', valid_until=b'', hostname=b'', realm=b'', fingerprint=b'', issuer=b'', failures=[]):
        """Initialize the certificate.

        Args:
            pem_data (unicode):
                The PEM-encoded certificate, if available.

            valid_from (unicode):
                A user-readable representation of the initiation date of the
                certificate.

            valid_until (unicode):
                A user-readable representation of the expiration date of the
                certificate.

            hostname (unicode):
                The hostname that this certificate is tied to.

            realm (unicode):
                An authentication realm (used with SVN).

            fingerprint (unicode):
                The fingerprint of the certificate. This can be in various
                formats depending on the backend which is dealing with the
                certificate, but ideally should be a SHA256-sum of the
                DER-encoded certificate.

            issuer (unicode):
                The common name of the issuer of the certificate.

            failures (list of unicode):
                A list of the verification failures, if available.
        """
        self.pem_data = pem_data
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.hostname = hostname
        self.realm = realm
        self.fingerprint = fingerprint
        self.issuer = issuer
        self.failures = failures