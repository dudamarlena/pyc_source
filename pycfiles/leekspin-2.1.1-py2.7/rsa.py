# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/leekspin/rsa.py
# Compiled at: 2015-04-08 22:31:02
"""OpenSSL RSA key utilities."""
from __future__ import print_function
from __future__ import absolute_import
import logging, OpenSSL.crypto
from leekspin import tls

class OpenSSLKeyGenError(Exception):
    """Raised when there is a problem generating a new key."""
    pass


def createRSAKey(bits=1024):
    """Create a new RSA keypair.

    The current keysize for OR RSA keys is 1024 bits.

    :param int bits: The bitlength of the keypair to generate.
    :raises OpenSSLKeyGenError: If key creation failed.
    :rtype: :class:`OpenSSL.crypto.PKey`
    :returns: An RSA keypair of bitlength ``bits``.
    """
    key = OpenSSL.crypto.PKey()
    logging.info('Generating new RSA keypair...')
    key.generate_key(OpenSSL.crypto.TYPE_RSA, bits)
    if not key.check():
        raise OpenSSLKeyGenError("Couldn't create new RSA 1024-bit key")
    return key


def createKey(selfsign=True, digest='sha1'):
    """Create a set of public and private RSA keypairs and corresponding certs.

    :param bool selfsign: If ``True``, use the private key to sign the public
       certificate (otherwise, the private key will only sign the private
       certificate to which it is attached).
    :param str digest: The digest to use.
    :raises OpenSSLKeyGenError: If key creation failed.
    :rtype: 4-tuple
    :returns: (private_key, private_cert, public_key, public_cert)
    """
    privateKey = createRSAKey()
    privateCert = tls.attachKey(privateKey, tls.createTLSCert(), selfsign=selfsign)
    publicKey = privateCert.get_pubkey()
    publicCert = tls.attachKey(publicKey, tls.createTLSCert(), selfsign=False)
    logging.debug('Created new secret keypairs and certs: key=%r cert=%r' % (
     privateKey, privateCert))
    logging.debug('Created new public keypairs and certs: key=%r cert=%r' % (
     publicKey, publicCert))
    if selfsign:
        logging.debug('Signing public cert %r with private key %r' % (
         publicCert, privateKey))
        publicCert.sign(privateKey, digest)
    return (privateKey, privateCert, publicKey, publicCert)