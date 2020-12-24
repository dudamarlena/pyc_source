# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\utils\tls_backport.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
import re
from ..utils.log import log, log_enabled, NETWORK
try:
    from backports.ssl_match_hostname import match_hostname, CertificateError
except ImportError:

    class CertificateError(ValueError):
        pass


    def _dnsname_match(dn, hostname, max_wildcards=1):
        """Backported from Python 3.4.3 standard library

        Matching according to RFC 6125, section 6.4.3

        http://tools.ietf.org/html/rfc6125#section-6.4.3
        """
        if log_enabled(NETWORK):
            log(NETWORK, 'matching dn %s with hostname %s', dn, hostname)
        pats = []
        if not dn:
            return False
        pieces = dn.split('.')
        leftmost = pieces[0]
        remainder = pieces[1:]
        wildcards = leftmost.count('*')
        if wildcards > max_wildcards:
            raise CertificateError('too many wildcards in certificate DNS name: ' + repr(dn))
        if not wildcards:
            return dn.lower() == hostname.lower()
        if leftmost == '*':
            pats.append('[^.]+')
        elif leftmost.startswith('xn--') or hostname.startswith('xn--'):
            pats.append(re.escape(leftmost))
        else:
            pats.append(re.escape(leftmost).replace('\\*', '[^.]*'))
        for frag in remainder:
            pats.append(re.escape(frag))

        pat = re.compile('\\A' + ('\\.').join(pats) + '\\Z', re.IGNORECASE)
        return pat.match(hostname)


    def match_hostname(cert, hostname):
        """Backported from Python 3.4.3 standard library.

        Verify that *cert* (in decoded format as returned by
        SSLSocket.getpeercert()) matches the *hostname*.  RFC 2818 and RFC 6125
        rules are followed, but IP addresses are not accepted for *hostname*.

        CertificateError is raised on failure. On success, the function
        returns nothing.
        """
        if not cert:
            raise ValueError('empty or no certificate, match_hostname needs a SSL socket or SSL context with either CERT_OPTIONAL or CERT_REQUIRED')
        dnsnames = []
        san = cert.get('subjectAltName', ())
        for (key, value) in san:
            if key == 'DNS':
                if _dnsname_match(value, hostname):
                    return
                dnsnames.append(value)

        if not dnsnames:
            for sub in cert.get('subject', ()):
                for (key, value) in sub:
                    if key == 'commonName':
                        if _dnsname_match(value, hostname):
                            return
                        dnsnames.append(value)

        if len(dnsnames) > 1:
            raise CertificateError("hostname %r doesn't match either of %s" % (
             hostname, (', ').join(map(repr, dnsnames))))
        elif len(dnsnames) == 1:
            raise CertificateError("hostname %r doesn't match %r" % (
             hostname, dnsnames[0]))
        else:
            raise CertificateError('no appropriate commonName or subjectAltName fields were found')