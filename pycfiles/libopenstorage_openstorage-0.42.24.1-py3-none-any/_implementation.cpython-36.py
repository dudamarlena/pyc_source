# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/urllib3/urllib3/packages/ssl_match_hostname/_implementation.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 5679 bytes
"""The match_hostname() function from Python 3.3.3, essential when using SSL."""
import re, sys
try:
    import ipaddress
except ImportError:
    ipaddress = None

__version__ = '3.5.0.1'

class CertificateError(ValueError):
    pass


def _dnsname_match(dn, hostname, max_wildcards=1):
    """Matching according to RFC 6125, section 6.4.3

    http://tools.ietf.org/html/rfc6125#section-6.4.3
    """
    pats = []
    if not dn:
        return False
    else:
        parts = dn.split('.')
        leftmost = parts[0]
        remainder = parts[1:]
        wildcards = leftmost.count('*')
        if wildcards > max_wildcards:
            raise CertificateError('too many wildcards in certificate DNS name: ' + repr(dn))
        if not wildcards:
            return dn.lower() == hostname.lower()
        if leftmost == '*':
            pats.append('[^.]+')
        else:
            if leftmost.startswith('xn--') or hostname.startswith('xn--'):
                pats.append(re.escape(leftmost))
            else:
                pats.append(re.escape(leftmost).replace('\\*', '[^.]*'))
        for frag in remainder:
            pats.append(re.escape(frag))

        pat = re.compile('\\A' + '\\.'.join(pats) + '\\Z', re.IGNORECASE)
        return pat.match(hostname)


def _to_unicode(obj):
    if isinstance(obj, str):
        if sys.version_info < (3, ):
            obj = unicode(obj, encoding='ascii', errors='strict')
    return obj


def _ipaddress_match(ipname, host_ip):
    """Exact matching of IP addresses.

    RFC 6125 explicitly doesn't define an algorithm for this
    (section 1.7.2 - "Out of Scope").
    """
    ip = ipaddress.ip_address(_to_unicode(ipname).rstrip())
    return ip == host_ip


def match_hostname(cert, hostname):
    """Verify that *cert* (in decoded format as returned by
    SSLSocket.getpeercert()) matches the *hostname*.  RFC 2818 and RFC 6125
    rules are followed, but IP addresses are not accepted for *hostname*.

    CertificateError is raised on failure. On success, the function
    returns nothing.
    """
    if not cert:
        raise ValueError('empty or no certificate, match_hostname needs a SSL socket or SSL context with either CERT_OPTIONAL or CERT_REQUIRED')
    else:
        try:
            host_ip = ipaddress.ip_address(_to_unicode(hostname))
        except ValueError:
            host_ip = None
        except UnicodeError:
            host_ip = None
        except AttributeError:
            if ipaddress is None:
                host_ip = None
            else:
                raise

        dnsnames = []
        san = cert.get('subjectAltName', ())
        for key, value in san:
            if key == 'DNS':
                if host_ip is None:
                    if _dnsname_match(value, hostname):
                        return
                dnsnames.append(value)
            else:
                if key == 'IP Address':
                    if host_ip is not None:
                        if _ipaddress_match(value, host_ip):
                            return
                    dnsnames.append(value)

        if not dnsnames:
            for sub in cert.get('subject', ()):
                for key, value in sub:
                    if key == 'commonName':
                        if _dnsname_match(value, hostname):
                            return
                        dnsnames.append(value)

        if len(dnsnames) > 1:
            raise CertificateError("hostname %r doesn't match either of %s" % (
             hostname, ', '.join(map(repr, dnsnames))))
        else:
            if len(dnsnames) == 1:
                raise CertificateError("hostname %r doesn't match %r" % (hostname, dnsnames[0]))
            else:
                raise CertificateError('no appropriate commonName or subjectAltName fields were found')