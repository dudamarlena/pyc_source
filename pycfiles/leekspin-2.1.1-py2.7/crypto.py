# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/leekspin/crypto.py
# Compiled at: 2015-04-08 22:31:02
"""General cryptographic utilities."""
from __future__ import print_function
from __future__ import absolute_import
import base64, binascii, codecs, hashlib, struct, sys
from Crypto.PublicKey import RSA
from Crypto.Util import asn1
import OpenSSL.crypto
from leekspin import const
from leekspin import rsa
from leekspin import tls
from leekspin.const import TOR_BEGIN_KEY
from leekspin.const import TOR_END_KEY
from leekspin.const import TOR_BEGIN_SIG
from leekspin.const import TOR_END_SIG
from leekspin.const import TOKEN_ONION_KEY
from leekspin.const import TOKEN_ROUTER_SIGNATURE
from leekspin.const import TOKEN_SIGNING_KEY

class InvalidFingerprint(ValueError):
    """Raised when a key fingerprint is invalid."""
    pass


def addPKCS1Padding(message):
    r"""Add PKCS#1 padding to **message**.
    
    .. todo:: What version of PKCS#1? PKCS#1 v1.0? See
        https://bugs.torproject.org/13042.
    
    .. The double-backslashes in the following bytestrings are so that Sphinx
        renders them properly. Each double-backslash is should actually only
        be a single backslash in the code.

    Each block is 128 bytes total in size:

      * 2 bytes for the type info ('\x00\x01')
      * 1 byte for the separator ('\x00')
      * variable length padding ('\xFF')
      * variable length for the **message**

    :param str message: The message will be encoded as bytes before adding
        PKCS#1 padding.
    :rtype: bytes
    :returns: The PKCS#1 padded message.
    """
    padding = ''
    typeinfo = '\x00\x01'
    separator = '\x00'
    for x in range(125 - len(message)):
        padding += b'\xff'

    PKCS1paddedMessage = typeinfo + padding + separator + message
    assert len(PKCS1paddedMessage) == 128
    return PKCS1paddedMessage


def addTorPKHeaderAndFooter(publicKey):
    """Add the ``----BEGIN RSA PUBLIC KEY-----`` and
    ``-----END RSA PUBLIC KEY-----`` headers to a **publicKey**.

    :param bytes publicKey: A headerless, chunked, base64-encoded,
        PKCS#1-padded, ASN.1 DER sequence string representation of a public
        RSA key.
    :rtype: bytes
    :returns: The same signature, with the headers which Tor uses around it.
    """
    return ('\n').join([TOR_BEGIN_KEY, publicKey, TOR_END_KEY])


def addTorSigHeaderAndFooter(signature):
    """Add the ``----BEGIN SIGNATURE-----`` and ``-----END SIGNATURE-----``
    headers to a **signature**.

    :param bytes signature: A headerless, chunked, base64-encoded signature.
    :rtype: bytes
    :returns: The same signature, with the headers which Tor uses around it.
    """
    return ('\n').join([TOR_BEGIN_SIG, signature, TOR_END_SIG])


def bytesToLong(bites):
    r"""Convert a byte string to a long integer.

    This function was stolen from BridgeDB, commit 5ed5c42e_.

    .. The double-backslashes in the following doctest are so that Sphinx
        renders the bytestrings properly. Each double-backslash should only
        be a single backslash if you actually wish to run this doctest.

    >>> from bridgedb.crypto import bytesToLong
    >>> bytesToLong('\x059')
    1337L
    >>> bytesToLong('I\x96\x02\xd2')
    1234567890L
    >>> bytesToLong('\x00\x00\x00\x00I\x96\x02\xd2')
    1234567890L
    >>> bytesToLong('\xabT\xa9\x8c\xeb\x1f\n\xd2')
    12345678901234567890L

    .. _5ed5c42e:
        https://github.com/isislovecruft/bridgedb/commit/5ed5c42ec7ef908991a67cf0cddf714f74e35f7e

    :param bytes bites: The byte string to convert.
    :rtype: long
    """
    length = len(bites)
    if length % 4:
        extra = 4 - length % 4
        bites = '\x00' * extra + bites
        length = length + extra
    acc = 0
    for index in range(0, length, 4):
        acc = (acc << 32) + struct.unpack('>I', bites[index:index + 4])[0]

    return acc


def longToBytes(number, blocksize=0):
    r"""Convert a long integer to a byte string.

    This function was stolen from BridgeDB, commit 5ed5c42e_.

    .. The double-backslashes in the following doctest are so that Sphinx
        renders the byte strings properly. Each double-backslash should only
        be a single backslash if you actually wish to run this doctest.

    >>> from bridgedb.crypto import longToBytes
    >>> longToBytes(1337L)
    '\x059'
    >>> longToBytes(1234567890L)
    'I\x96\x02\xd2'
    >>> longToBytes(1234567890L, blocksize=8)
    '\x00\x00\x00\x00I\x96\x02\xd2'
    >>> longToBytes(12345678901234567890L)
    '\xabT\xa9\x8c\xeb\x1f\n\xd2'

    .. _5ed5c42e:
        https://github.com/isislovecruft/bridgedb/commit/5ed5c42ec7ef908991a67cf0cddf714f74e35f7e

    :param int number: The long integer to convert.
    :param int blocksize: If **blocksize** is given and greater than zero, pad
        the front of the byte string with binary zeros so that the length is a
        multiple of **blocksize**.
    :rtype: bytes
    """
    bites = ''
    number = long(number)
    while number > 0:
        bites = struct.pack('>I', number & 4294967295) + bites
        number = number >> 32

    for index in range(len(bites)):
        if bites[index] != '\x00':
            break
    else:
        bites = '\x00'
        index = 0

    bites = bites[index:]
    if blocksize > 0 and len(bites) % blocksize:
        bites = (blocksize - len(bites) % blocksize) * '\x00' + bites
    return bytes(bites)


def chunkInto64CharsPerLine(data, separator='\n'):
    """Chunk **data** into lines with 64 characters each.

    :param basestring data: The data to be chunked up.
    :keyword basestring separator: The character to use to join the chunked
        lines.
    :rtype: basestring
    :returns: The **data**, as a string, with 64 characters (plus the
        **separator** character), per line.
    """
    chunked = []
    while len(data) > 0:
        chunked.append(data[:64])
        data = data[64:]

    lines = separator.join(chunked)
    return lines


def convertToSmooshedFingerprint(fingerprint):
    """Convert to a space-delimited 40 character fingerprint

    Given a 49-character string, such as one returned from
    :func:`convertToSpaceyFingerprint`::

        72C2 F0AE 1C14 F40E D37E D5F5 434B 6471 1A65 8E46

    convert it to the following format::

        72C2F0AE1C14F40ED37ED5F5434B64711A658E46

    :param str fingerprint: A 49-character spacey fingerprint.
    :rtype: bytes
    :raises InvalidFingerprint: If the fingerprint isn't 49-bytes in length.
    :returns: A 40-character smooshed fingerprint without spaces.
    """
    if len(fingerprint) != 49:
        raise InvalidFingerprint('Invalid fingerprint (!= 49 bytes): %r' % fingerprint)
    return fingerprint.replace(' ', '')


def convertToSpaceyFingerprint(fingerprint):
    """Convert to a space-delimited 40-character fingerprint

    Given a 40 character string, usually the the SHA-1 hash of the
    DER encoding of an ASN.1 RSA public key, such as::

        72C2F0AE1C14F40ED37ED5F5434B64711A658E46

    convert it to the following format::

        72C2 F0AE 1C14 F40E D37E D5F5 434B 6471 1A65 8E46

    :param str fingerprint: A 40-character hex fingerprint.
    :rtype: bytes
    :raises InvalidFingerprint: If the fingerprint isn't 40 bytes in length.
    :returns: A 4-character space-delimited fingerprint.
    """
    if len(fingerprint) != 40:
        raise InvalidFingerprint('Invalid fingerprint (< 40 bytes): %r' % fingerprint)
    return (' ').join([ fingerprint[i:i + 4] for i in range(0, 40, 4) ])


def digestDescriptorContent(content):
    descriptorDigest = hashlib.sha1(content)
    descriptorDigestBinary = descriptorDigest.digest()
    descriptorDigestHex = descriptorDigest.hexdigest()
    descriptorDigestHexUpper = descriptorDigestHex.upper()
    descriptorDigestHexLower = descriptorDigestHex.lower()
    descriptorDigestBytes = descriptorDigestHexLower.decode('hex_codec')
    descriptorDigestPKCS1 = addPKCS1Padding(descriptorDigestBytes)
    return (
     descriptorDigestBinary, descriptorDigestHexUpper, descriptorDigestPKCS1)


def getASN1Sequence(privateKey):
    """Get an ASN.1 DER sequence string representation of the key's public
    modulus and exponent.

    :type privateKey: ``Crypto.PublicKey.RSA``
    :param privateKey: A private RSA key.
    :rtype: bytes
    :returns: The ASN.1 DER-encoded string representation of the public
        portions of the **privateKey**.
    """
    seq = asn1.DerSequence()
    seq.append(privateKey.n)
    seq.append(privateKey.e)
    asn1seqString = seq.encode()
    return asn1seqString


def getFingerprint(publicKey):
    """Get a digest of the ASN.1 DER-encoded **publicKey**.

    :type publicKey: str
    :param publicKey: A public key (as within the return parameters of
        :func:`generateOnionKey` or :func:`generateSigningKey`.)
    :rtype: str
    :returns: A spacey fingerprint.
    """
    keyDigest = hashlib.sha1(publicKey)
    keyDigestBinary = keyDigest.digest()
    keyDigestHex = keyDigest.hexdigest()
    keyDigestHexUpper = keyDigestHex.upper()
    keyDigestBytes = codecs.latin_1_encode(keyDigestHexUpper, 'replace')[0]
    fingerprint = convertToSpaceyFingerprint(keyDigestBytes)
    return (
     fingerprint, keyDigestBinary)


def _generateRSAKey(bits=1024):
    """Generate an RSA key, suitable for e.g. a router/bridge signing or onion
    key, or an Hidden Service service or permanent key.

    The encodings for the various key and descriptor digests needed are
    described in dir-spec.txt and tor-spec.txt, the latter mostly for the
    padding and encoding used in the creation of an OR's keys.

    :param int bits: The length of the RSA key, in bits.
    :returns: A tuple of strings, ``(key-private, key-public, key-line)``,
       where ``key-line`` should be appropriate for placement directly into a
       descriptor.
    """
    secretKey = RSA.generate(bits)
    publicKey = getASN1Sequence(secretKey)
    publicKeyB64 = base64.b64encode(publicKey)
    publicKeyNoHeaders = chunkInto64CharsPerLine(publicKeyB64)
    return (
     secretKey, publicKey, publicKeyNoHeaders)


def generateOnionKey(bits=1024):
    u"""Generate a router's onion key, which is used to encrypt CERT cells.

    The encodings for the various key and descriptor digests needed are
    described in dir-spec.txt and tor-spec.txt, the latter mostly for the
    padding and encoding used in the creation of an OR's keys.

    For the ``router`` line in a networkstatus document, the following
    encodings are specified:

    .. epigraph::
        […] "Identity" is a hash of its identity key, encoded in base64, with
        trailing equals sign(s) removed.  "Digest" is a hash of its most
        recent descriptor as signed (that is, not including the signature),
        encoded in base64.

        -- dir-spec.txt_ L1504-1512_

    Before the hash digest of an OR's identity key is base64-encoded for
    inclusion in a networkstatus document, the hash digest is created in the
    following manner:

    .. epigraph::
        When we refer to "the hash of a public key", we mean the SHA-1 hash of the
        DER encoding of an ASN.1 RSA public key (as specified in PKCS.1).
        […]
        The "legacy identity" and "identity fingerprint" fields are the SHA1
        hash of the PKCS#1 ASN1 encoding of the next onion router's identity
        (signing) key.

        -- tor-spec.txt_ L109-110_ and L784-786_

    .. _dir-spec.txt: https://gitweb.torproject.org/torspec.git/tree/dir-spec.txt
    .. _L1504-1512: https://gitweb.torproject.org/torspec.git/tree/dir-spec.txt?id=36761c7d5#n1504
    .. _tor-spec.txt: https://gitweb.torproject.org/torspec.git/tree/tor-spec.txt
    .. _L109-110: https://gitweb.torproject.org/torspec.git/tree/tor-spec.txt?id=36761c7d5#n109
    .. _L784-786: https://gitweb.torproject.org/torspec.git/tree/tor-spec.txt?id=36761c7d5#n784

    :param int bits: The length of the RSA key, in bits.
    :returns: A tuple of strings,
       ``(onion-key-private, onion-key-public, onion-key-line)``, where
       ``onion-key-line`` should directly go into a server-descriptor.
    """
    secretOnionKey, publicOnionKey, publicOnionKeyNoHeaders = _generateRSAKey(bits)
    onionKeyWithHeaders = addTorPKHeaderAndFooter(publicOnionKeyNoHeaders)
    onionKeyLine = TOKEN_ONION_KEY + onionKeyWithHeaders
    return (
     secretOnionKey, publicOnionKey, onionKeyLine)


def generateSigningKey(bits=1024):
    """Generate a router's signing-key, which is used to sign e.g. descriptor
    contents.

    :param int bits: The length of the RSA key, in bits.
    :returns: A tuple of strings, ``(signing-key-private, signing-key-public,
       signing-key-line)``, where ``signign-key-line`` should directly go into
       a descriptor.
    """
    secretSigningKey, publicSigningKey, publicSigningKeyNoHeaders = _generateRSAKey(bits)
    signingKeyWithHeaders = addTorPKHeaderAndFooter(publicSigningKeyNoHeaders)
    signingKeyLine = TOKEN_SIGNING_KEY + signingKeyWithHeaders
    return (
     secretSigningKey, publicSigningKey, signingKeyLine)


def signDescriptorContent(content, privateKey, digest=None, token=TOKEN_ROUTER_SIGNATURE):
    """Sign the **content** or the **digest** of the content, and postpend it
    to the **content**.

    :param str content: The contents of a descriptor.
    :type privateKey: ``Crypto.PublicKey.RSA``
    :param privateKey: A private RSA key.
    :type digest: str or ``None``
    :param digest: If given, this should be the PKCS#1-padded binary digest of
        the descriptor contents (i.e. the third return value from
        :func:`digestDescriptorContent`).  If the **digest** is given, then
        this **digest** will be signed.  Otherwise, if ``None``, then
        **contents** will be signed.
    :param str token: The token to search for when appending the signature to
        the end of the descriptor **content**
    """
    if digest is None:
        _, _, digest = digestDescriptorContent(content)
    signatureLong, = privateKey.sign(digest, None)
    signatureBytes = longToBytes(signatureLong, 128)
    signatureBase64 = base64.b64encode(signatureBytes)
    signature = chunkInto64CharsPerLine(signatureBase64)
    signatureWithHeaders = addTorSigHeaderAndFooter(signature)
    routerSignatureLine = token + signatureWithHeaders
    rsStart = content.find(token)
    content = content[:rsStart] + routerSignatureLine + '\n'
    return content