# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/crypto.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = b'This module contains general utilities for working with external\ncryptographic tools and libraries, including OpenSSL and GnuPG. It also\nincludes utilities for creating callable HMAC functions, generating HMACs for\ndata, and generating and/or storing key material.\n\n.. py:module:: bridgedb.crypto\n   :synopsis: BridgeDB general cryptographic utilities.\n\n::\n\n   bridgedb.crypto\n     |_getGPGContext() - Get a pre-configured GPGME context.\n     |_getHMAC() - Compute an HMAC with some key for some data.\n     |_getHMACFunc() - Get a callable for producing HMACs with the given key.\n     |_getKey() - Load the master HMAC key from a file, or create a new one.\n     |_getRSAKey() - Load an RSA key from a file, or create a new one.\n     |_gpgSignMessage() - Sign a message string according to a GPGME context.\n     |_writeKeyToFile() - Write to a file readable only by the process owner.\n     |\n     \\_SSLVerifyingContextFactory - OpenSSL.SSL.Context factory which verifies\n        |                           certificate chains and matches hostnames.\n        |_getContext() - Retrieve an SSL context configured for certificate\n        |                verification.\n        |_getHostnameFromURL() - Parses the hostname from the request URL.\n        \\_verifyHostname() - Check that the cert CN matches the request\n                             hostname.\n..\n'
from __future__ import absolute_import
from __future__ import unicode_literals
import gnupg, hashlib, hmac, io, logging, os, re, urllib, OpenSSL
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from twisted.internet import ssl
from twisted.python.procutils import which
DIGESTMOD = hashlib.sha1
NEW_BUFFER_INTERFACE = False
try:
    io.BytesIO(buffer(b'test'))
except TypeError:
    logging.warn(b"This Python version is too old! It doesn't support new-style buffer interfaces: https://mail.python.org/pipermail/python-dev/2010-October/104917.html")
else:
    NEW_BUFFER_INTERFACE = True

class PKCS1PaddingError(Exception):
    """Raised when there is a problem adding or removing PKCS#1 padding."""


class RSAKeyGenerationError(Exception):
    """Raised when there was an error creating an RSA keypair."""


def writeKeyToFile(key, filename):
    """Write **key** to **filename**, with ``0400`` permissions.

    If **filename** doesn't exist, it will be created. If it does exist
    already, and is writable by the owner of the current process, then it will
    be truncated to zero-length and overwritten.

    :param bytes key: A key (or some other private data) to write to
        **filename**.
    :param str filename: The path of the file to write to.
    :raises: Any exceptions which may occur.
    """
    logging.info(b'Writing key to file: %r' % filename)
    flags = os.O_WRONLY | os.O_TRUNC | os.O_CREAT | getattr(os, b'O_BIN', 0)
    fd = os.open(filename, flags, 256)
    os.write(fd, key)
    os.fsync(fd)
    os.close(fd)


def getRSAKey(filename, bits=2048):
    u"""Load the RSA key stored in **filename**, or create and save a new key.

    >>> from bridgedb import crypto
    >>> keyfile = 'doctest_getRSAKey'
    >>> message = "The secret words are Squeamish Ossifrage."
    >>> keypair = crypto.getRSAKey(keyfile, bits=2048)
    >>> (secretkey, publickey) = keypair
    >>> encrypted = publickey.encrypt(message)
    >>> assert encrypted != message
    >>> decrypted = secretkey.decrypt(encrypted)
    >>> assert message == decrypted

    If **filename** already exists, it is assumed to contain a PEM-encoded RSA
    private key, which will be read from the file. (The parameters of a
    private RSA key contain the public exponent and public modulus, which
    together comprise the public key ― ergo having two separate keyfiles is
    assumed unnecessary.)

    If **filename** doesn't exist, a new RSA keypair will be created, and the
    private key will be stored in **filename**, using :func:`writeKeyToFile`.

    Once the private key is either loaded or created, the public key is
    extracted from it. Both keys are then input into PKCS#1 RSAES-OAEP cipher
    schemes (see `RFC 3447 §7.1`__) in order to introduce padding, and then
    returned.

    .. __: https://tools.ietf.org/html/rfc3447#section-7.1

    :param str filename: The filename to which the secret parameters of the
        RSA key are stored in.
    :param int bits: If no key is found within the file, create a new key with
        this bitlength and store it in **filename**.
    :rtype: tuple of ``Crypto.Cipher.PKCS1_OAEP.PKCS1OAEP_Cipher``
    :returns: A 2-tuple of ``(privatekey, publickey)``, which are PKCS#1
        RSAES-OAEP padded and encoded private and public keys, forming an RSA
        keypair.
    """
    filename = os.path.extsep.join([filename, b'sec'])
    keyfile = os.path.join(os.getcwd(), filename)
    try:
        fh = open(keyfile, b'rb')
    except IOError:
        logging.info(b'Generating %d-bit RSA keypair...' % bits)
        secretKey = RSA.generate(bits, e=65537)
        secretKeyPEM = secretKey.exportKey(b'PEM')
        writeKeyToFile(secretKeyPEM, keyfile)
    else:
        logging.info(b'Secret RSA keyfile %r found. Loading...' % filename)
        secretKey = RSA.importKey(fh.read())
        fh.close()

    publicKey = secretKey.publickey()
    sk = PKCS1_OAEP.new(secretKey)
    pk = PKCS1_OAEP.new(publicKey)
    return (
     sk, pk)


def getKey(filename):
    """Load the master key stored in ``filename``, or create a new key.

    If ``filename`` does not exist, create a new 32-byte key and store it in
    ``filename``.

    >>> import os
    >>> from bridgedb import crypto
    >>> name = 'doctest_getKey'
    >>> os.path.exists(name)
    False
    >>> k1 = crypto.getKey(name)
    >>> os.path.exists(name)
    True
    >>> open(name).read() == k1
    True
    >>> k2 = crypto.getKey(name)
    >>> k1 == k2
    True

    :param string filename: The filename to store the secret key in.
    :rtype: bytes
    :returns: A byte string containing the secret key.
    """
    try:
        fh = open(filename, b'rb')
    except IOError:
        logging.debug(b'getKey(): Creating new secret key.')
        key = OpenSSL.rand.bytes(32)
        writeKeyToFile(key, filename)
    else:
        logging.debug(b'getKey(): Secret key file found. Loading...')
        key = fh.read()
        fh.close()

    return key


def getHMAC(key, value):
    """Return the HMAC of **value** using the **key**."""
    h = hmac.new(key, value, digestmod=DIGESTMOD)
    return h.digest()


def getHMACFunc(key, hex=True):
    """Return a function that computes the HMAC of its input using the **key**.

    :param bool hex: If True, the output of the function will be hex-encoded.
    :rtype: callable
    :returns: A function which can be uses to generate HMACs.
    """
    h = hmac.new(key, digestmod=DIGESTMOD)

    def hmac_fn(value):
        h_tmp = h.copy()
        h_tmp.update(value)
        if hex:
            return h_tmp.hexdigest()
        else:
            return h_tmp.digest()

    return hmac_fn


def removePKCS1Padding(message):
    ur"""Remove PKCS#1 padding from a **message**.

    (PKCS#1 v1.0?  See :trac:`13042`.)

    Each block is 128 bytes total in size:

        * 2 bytes for the type info (``'\x00\x01'``)
        * 1 byte for the separator (``'\x00'``)
        * variable length padding (``'\xFF'``)
        * variable length for the **message**

    .. Note that the above strings are double escaped, due to the way that
       Sphinx renders escaped strings in docstrings.

    For more information on the structure of PKCS#1 padding, see :rfc:`2313`,
    particularly `the notes in §8.1`__.

    .. __: https://tools.ietf.org/html/rfc2313#section-8.1

    :param str message: A message which is PKCS#1 padded.
    :raises PKCS1PaddingError: if there is an issue parsing the **message**.
    :rtype: bytes
    :returns: The message without the PKCS#1 padding.
    """
    padding = b'\xff'
    typeinfo = b'\x00\x01'
    separator = b'\x00'
    unpadded = None
    try:
        if message.index(typeinfo) != 0:
            raise PKCS1PaddingError(b"Couldn't find PKCS#1 identifier bytes!")
        start = message.index(separator, 2) + 1
    except ValueError:
        raise PKCS1PaddingError(b"Couldn't find PKCS#1 separator byte!")
    else:
        unpadded = message[start:]

    return unpadded


def initializeGnuPG(config):
    """Initialize a GnuPG interface and test our configured keys.

    .. note:: This function uses python-gnupg_.

    :type config: :class:`bridgedb.persistent.Conf`
    :param config: The loaded config file.
    :rtype: 2-tuple
    :returns: If ``EMAIL_GPG_SIGNING_ENABLED`` isn't ``True``, or we couldn't
        initialize GnuPG and make a successful test signature with the
        specified key, then a 2-tuple of ``None`` is returned.  Otherwise, the
        first item in the tuple is a :class:`gnupg.GPG` interface_ with the
        GnuPG homedir set to the ``EMAIL_GPG_HOMEDIR`` option and the signing
        key specified by the ``EMAIL_GPG_SIGNING_KEY_FINGERPRINT`` option in
        bridgedb.conf set as the default key. The second item in the tuple is
        a signing function with the passphrase (as specified in either
        ``EMAIL_GPG_PASSPHRASE`` or ``EMAIL_GPG_PASSPHRASE_FILE``) already
        set.

    .. _python-gnupg: https://pypi.python.org/pypi/gnupg/
    .. _interface: https://python-gnupg.readthedocs.org/en/latest/gnupg.html#gnupg-module
    """
    ret = (None, None)
    if not config.EMAIL_GPG_SIGNING_ENABLED:
        return ret
    else:
        homedir = config.EMAIL_GPG_HOMEDIR
        primary = config.EMAIL_GPG_PRIMARY_KEY_FINGERPRINT
        passphrase = config.EMAIL_GPG_PASSPHRASE
        passFile = config.EMAIL_GPG_PASSPHRASE_FILE
        logging.info(b'Using %s as our GnuPG home directory...' % homedir)
        gpg = gnupg.GPG(homedir=homedir)
        logging.info(b'Initialized GnuPG interface using %s binary with version %s.' % (
         gpg.binary, gpg.binary_version))
        primarySK = None
        primaryPK = None
        secrets = gpg.list_keys(secret=True)
        publics = gpg.list_keys()
        if not secrets:
            logging.warn(b'No secret keys found in %s!' % gpg.secring)
            return ret
        primarySK = filter(lambda key: key[b'fingerprint'] == primary, secrets)
        primaryPK = filter(lambda key: key[b'fingerprint'] == primary, publics)
        if primarySK and primaryPK:
            logging.info(b'Found GnuPG primary key with fingerprint: %s' % primary)
            for sub in primaryPK[0][b'subkeys']:
                logging.info(b'  Subkey: %s  Usage: %s' % (sub[0], sub[1].upper()))

        else:
            logging.warn(b'GnuPG key %s could not be found in %s!' % (primary, gpg.secring))
            return ret
        if passphrase:
            logging.info(b'Read GnuPG passphrase from config.')
        else:
            if passFile:
                try:
                    with open(passFile) as (fh):
                        passphrase = fh.read()
                except (IOError, OSError):
                    logging.error(b'Could not open GnuPG passphrase file: %s!' % passFile)
                else:
                    logging.info(b'Read GnuPG passphrase from file: %s' % passFile)

            def gpgSignMessage(message):
                """Sign **message** with the default key specified by
        ``EMAIL_GPG_PRIMARY_KEY_FINGERPRINT``.

        :param str message: A message to sign.
        :rtype: str or ``None``.
        :returns: A string containing the clearsigned message, or ``None`` if
            the signing failed.
        """
                sig = gpg.sign(message, default_key=primary, passphrase=passphrase)
                if sig and sig.data:
                    return sig.data

            logging.debug(b'Testing signature created with GnuPG key...')
            sig = gpgSignMessage(b'Testing 1 2 3')
            if sig:
                logging.info(b'Test signature with GnuPG key %s okay:\n%s' % (primary, sig))
                return (
                 gpg, gpgSignMessage)
        return ret


class SSLVerifyingContextFactory(ssl.CertificateOptions):
    """``OpenSSL.SSL.Context`` factory which does full certificate-chain and
    hostname verfication.
    """
    isClient = True

    def __init__(self, url, **kwargs):
        """Create a client-side verifying SSL Context factory.

        To pass acceptable certificates for a server which does
        client-authentication checks: initialise with a ``caCerts=[]`` keyword
        argument, which should be a list of ``OpenSSL.crypto.X509`` instances
        (one for each peer certificate to add to the store), and set
        ``SSLVerifyingContextFactory.isClient=False``.

        :param str url: The URL being requested by an
            :api:`twisted.web.client.Agent`.
        :param bool isClient: True if we're being used in a client
            implementation; False if we're a server.
        """
        self.hostname = self.getHostnameFromURL(url)
        self.verify = False if self.isClient else True
        super(SSLVerifyingContextFactory, self).__init__(verify=self.verify, fixBrokenPeers=True, **kwargs)

    def getContext(self, hostname=None, port=None):
        """Retrieve a configured ``OpenSSL.SSL.Context``.

        Any certificates in the ``caCerts`` list given during initialisation
        are added to the ``Context``'s certificate store.

        The **hostname** and **port** arguments seem unused, but they are
        required due to some Twisted and pyOpenSSL internals. See
        :api:`twisted.web.client.Agent._wrapContextFactory`.

        :rtype: ``OpenSSL.SSL.Context``
        :returns: An SSL Context which verifies certificates.
        """
        ctx = super(SSLVerifyingContextFactory, self).getContext()
        store = ctx.get_cert_store()
        verifyOptions = OpenSSL.SSL.VERIFY_PEER
        ctx.set_verify(verifyOptions, self.verifyHostname)
        return ctx

    def getHostnameFromURL(self, url):
        """Parse the hostname from the originally requested URL.

        :param str url: The URL being requested by an
            :api:`twisted.web.client.Agent`.
        :rtype: str
        :returns: The full hostname (including any subdomains).
        """
        hostname = urllib.splithost(urllib.splittype(url)[1])[0]
        logging.debug(b'Parsed hostname %r for cert CN matching.' % hostname)
        return hostname

    def verifyHostname(self, connection, x509, errnum, depth, okay):
        """Callback method for additional SSL certificate validation.

        If the certificate is signed by a valid CA, and the chain is valid,
        verify that the level 0 certificate has a subject common name which is
        valid for the hostname of the originally requested URL.

        :param connection: An ``OpenSSL.SSL.Connection``.
        :param x509: An ``OpenSSL.crypto.X509`` object.
        :param errnum: A pyOpenSSL error number. See that project's docs.
        :param depth: The depth which the current certificate is at in the
            certificate chain.
        :param bool okay: True if all the pyOpenSSL default checks on the
            certificate passed. False otherwise.
        """
        commonName = x509.get_subject().commonName
        logging.debug(b"Received cert at level %d: '%s'" % (depth, commonName))
        if okay and depth == 0:
            cn = commonName.replace(b'*', b'.*')
            hostnamesMatch = re.search(cn, self.hostname)
            if not hostnamesMatch:
                logging.warn(b"Invalid certificate subject CN for '%s': '%s'" % (
                 self.hostname, commonName))
                return False
            logging.debug(b"Valid certificate subject CN for '%s': '%s'" % (
             self.hostname, commonName))
        return True