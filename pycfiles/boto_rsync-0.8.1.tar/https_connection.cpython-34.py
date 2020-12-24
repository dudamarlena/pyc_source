# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/https_connection.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 5135 bytes
__doc__ = 'Extensions to allow HTTPS requests with SSL certificate validation.'
import re, socket, ssl, boto
from boto.compat import six, http_client

class InvalidCertificateException(http_client.HTTPException):
    """InvalidCertificateException"""

    def __init__(self, host, cert, reason):
        """Constructor.

        Args:
          host: The hostname the connection was made to.
          cert: The SSL certificate (as a dictionary) the host returned.
        """
        http_client.HTTPException.__init__(self)
        self.host = host
        self.cert = cert
        self.reason = reason

    def __str__(self):
        return 'Host %s returned an invalid certificate (%s): %s' % (
         self.host, self.reason, self.cert)


def GetValidHostsForCert(cert):
    """Returns a list of valid host globs for an SSL certificate.

    Args:
      cert: A dictionary representing an SSL certificate.
    Returns:
      list: A list of valid host globs.
    """
    if 'subjectAltName' in cert:
        return [x[1] for x in cert['subjectAltName'] if x[0].lower() == 'dns']
    else:
        return [x[0][1] for x in cert['subject'] if x[0][0].lower() == 'commonname']


def ValidateCertificateHostname(cert, hostname):
    """Validates that a given hostname is valid for an SSL certificate.

    Args:
      cert: A dictionary representing an SSL certificate.
      hostname: The hostname to test.
    Returns:
      bool: Whether or not the hostname is valid for this certificate.
    """
    hosts = GetValidHostsForCert(cert)
    boto.log.debug('validating server certificate: hostname=%s, certificate hosts=%s', hostname, hosts)
    for host in hosts:
        host_re = host.replace('.', '\\.').replace('*', '[^.]*')
        if re.search('^%s$' % (host_re,), hostname, re.I):
            return True

    return False


class CertValidatingHTTPSConnection(http_client.HTTPConnection):
    """CertValidatingHTTPSConnection"""
    default_port = http_client.HTTPS_PORT

    def __init__(self, host, port=default_port, key_file=None, cert_file=None, ca_certs=None, strict=None, **kwargs):
        """Constructor.

        Args:
          host: The hostname. Can be in 'host:port' form.
          port: The port. Defaults to 443.
          key_file: A file containing the client's private key
          cert_file: A file containing the client's certificates
          ca_certs: A file contianing a set of concatenated certificate authority
              certs for validating the server against.
          strict: When true, causes BadStatusLine to be raised if the status line
              can't be parsed as a valid HTTP/1.0 or 1.1 status line.
        """
        if six.PY2:
            kwargs['strict'] = strict
        http_client.HTTPConnection.__init__(self, host=host, port=port, **kwargs)
        self.key_file = key_file
        self.cert_file = cert_file
        self.ca_certs = ca_certs

    def connect(self):
        """Connect to a host on a given (SSL) port."""
        if hasattr(self, 'timeout'):
            sock = socket.create_connection((self.host, self.port), self.timeout)
        else:
            sock = socket.create_connection((self.host, self.port))
        msg = 'wrapping ssl socket; '
        if self.ca_certs:
            msg += 'CA certificate file=%s' % self.ca_certs
        else:
            msg += 'using system provided SSL certs'
        boto.log.debug(msg)
        self.sock = ssl.wrap_socket(sock, keyfile=self.key_file, certfile=self.cert_file, cert_reqs=ssl.CERT_REQUIRED, ca_certs=self.ca_certs)
        cert = self.sock.getpeercert()
        hostname = self.host.split(':', 0)[0]
        if not ValidateCertificateHostname(cert, hostname):
            raise InvalidCertificateException(hostname, cert, 'remote hostname "%s" does not match certificate' % hostname)