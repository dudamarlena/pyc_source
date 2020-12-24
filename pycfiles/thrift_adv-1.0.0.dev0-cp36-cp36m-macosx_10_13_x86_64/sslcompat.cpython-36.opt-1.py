# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/transport/sslcompat.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 3662 bytes
import logging, sys
from thrift.transport.TTransport import TTransportException
logger = logging.getLogger(__name__)

def legacy_validate_callback(cert, hostname):
    """legacy method to validate the peer's SSL certificate, and to check
    the commonName of the certificate to ensure it matches the hostname we
    used to make this connection.  Does not support subjectAltName records
    in certificates.

    raises TTransportException if the certificate fails validation.
    """
    if 'subject' not in cert:
        raise TTransportException(TTransportException.NOT_OPEN, 'No SSL certificate found from %s' % hostname)
    fields = cert['subject']
    for field in fields:
        if not isinstance(field, tuple):
            pass
        else:
            cert_pair = field[0]
            if len(cert_pair) < 2:
                pass
            else:
                cert_key, cert_value = cert_pair[0:2]
                if cert_key != 'commonName':
                    pass
                else:
                    certhost = cert_value
                    if certhost == hostname:
                        return
                    raise TTransportException(TTransportException.UNKNOWN, 'Hostname we connected to "%s" doesn\'t match certificate provided commonName "%s"' % (
                     hostname, certhost))

    raise TTransportException(TTransportException.UNKNOWN, 'Could not validate SSL certificate from host "%s".  Cert=%s' % (
     hostname, cert))


def _optional_dependencies():
    try:
        import ipaddress
        logger.debug('ipaddress module is available')
        ipaddr = True
    except ImportError:
        logger.warn('ipaddress module is unavailable')
        ipaddr = False

    if sys.hexversion < 50659568:
        try:
            from backports.ssl_match_hostname import match_hostname, __version__ as ver
            ver = list(map(int, ver.split('.')))
            logger.debug('backports.ssl_match_hostname module is available')
            match = match_hostname
            if ver[0] * 10 + ver[1] >= 35:
                return (
                 ipaddr, match)
            logger.warn('backports.ssl_match_hostname module is too old')
            ipaddr = False
        except ImportError:
            logger.warn('backports.ssl_match_hostname is unavailable')
            ipaddr = False

    try:
        from ssl import match_hostname
        logger.debug('ssl.match_hostname is available')
        match = match_hostname
    except ImportError:
        logger.warn('using legacy validation callback')
        match = legacy_validate_callback

    return (
     ipaddr, match)


_match_has_ipaddress, _match_hostname = _optional_dependencies()