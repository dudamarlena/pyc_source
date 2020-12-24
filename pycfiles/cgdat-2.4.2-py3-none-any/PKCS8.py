# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud_Crypto/IO/PKCS8.py
# Compiled at: 2016-11-22 15:21:45
__doc__ = '\nModule for handling private keys wrapped according to `PKCS#8`_.\n\nPKCS8 is a standard for storing and transferring private key information.\nThe wrapped key can either be clear or encrypted.\n\nAll encryption algorithms are based on passphrase-based key derivation.\nThe following mechanisms are fully supported:\n\n* *PBKDF2WithHMAC-SHA1AndAES128-CBC*\n* *PBKDF2WithHMAC-SHA1AndAES192-CBC*\n* *PBKDF2WithHMAC-SHA1AndAES256-CBC*\n* *PBKDF2WithHMAC-SHA1AndDES-EDE3-CBC*\n\nThe following mechanisms are only supported for importing keys.\nThey are much weaker than the ones listed above, and they are provided\nfor backward compatibility only:\n\n* *pbeWithMD5AndRC2-CBC*\n* *pbeWithMD5AndDES-CBC*\n* *pbeWithSHA1AndRC2-CBC*\n* *pbeWithSHA1AndDES-CBC*\n\n.. _`PKCS#8`: http://www.ietf.org/rfc/rfc5208.txt\n\n'
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from cgcloud_Crypto.Util.py21compat import *
from cgcloud_Crypto.Util.py3compat import *
from cgcloud_Crypto.Util.asn1 import *
__all__ = [
 'wrap', 'unwrap']

def decode_der(obj_class, binstr):
    """Instantiate a DER object class, decode a DER binary string in it, and
    return the object."""
    der = obj_class()
    der.decode(binstr)
    return der


def wrap(private_key, key_oid, passphrase=None, protection=None, prot_params=None, key_params=None, randfunc=None):
    """Wrap a private key into a PKCS#8 blob (clear or encrypted).

    :Parameters:

      private_key : byte string
        The private key encoded in binary form. The actual encoding is
        algorithm specific. In most cases, it is DER.

      key_oid : string
        The object identifier (OID) of the private key to wrap.
        It is a dotted string, like "``1.2.840.113549.1.1.1``" (for RSA keys).

      passphrase : (binary) string
        The secret passphrase from which the wrapping key is derived.
        Set it only if encryption is required.

      protection : string
        The identifier of the algorithm to use for securely wrapping the key.
        The default value is '``PBKDF2WithHMAC-SHA1AndDES-EDE3-CBC``'.

      prot_params : dictionary
        Parameters for the protection algorithm.

        +------------------+-----------------------------------------------+
        | Key              | Description                                   |
        +==================+===============================================+
        | iteration_count  | The KDF algorithm is repeated several times to|
        |                  | slow down brute force attacks on passwords.   |
        |                  | The default value is 1 000.                   |
        +------------------+-----------------------------------------------+
        | salt_size        | Salt is used to thwart dictionary and rainbow |
        |                  | attacks on passwords. The default value is 8  |
        |                  | bytes.                                        |
        +------------------+-----------------------------------------------+

      key_params : DER object
        The algorithm parameters associated to the private key.
        It is required for algorithms like DSA, but not for others like RSA.

      randfunc : callable
        Random number generation function; it should accept a single integer
        N and return a string of random data, N bytes long.
        If not specified, a new RNG will be instantiated
        from ``Crypto.Random``.

    :Return:
      The PKCS#8-wrapped private key (possibly encrypted),
      as a binary string.
    """
    if key_params is None:
        key_params = DerNull()
    pk_info = newDerSequence(0, newDerSequence(DerObjectId(key_oid), key_params), newDerOctetString(private_key))
    pk_info_der = pk_info.encode()
    if not passphrase:
        return pk_info_der
    else:
        assert False
        return