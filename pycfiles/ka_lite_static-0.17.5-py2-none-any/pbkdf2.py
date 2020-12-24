# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/pbkdf2/pbkdf2.py
# Compiled at: 2018-07-11 18:15:32
__version__ = '1.3'
__all__ = ['PBKDF2', 'crypt']
from struct import pack
from random import randint
import string, sys
try:
    from Crypto.Hash import HMAC, SHA as SHA1
except ImportError:
    import hmac as HMAC
    try:
        from hashlib import sha1 as SHA1
    except ImportError:
        import sha as SHA1

if sys.version_info[0] == 2:
    _0xffffffffL = long(1) << 32

    def isunicode(s):
        return isinstance(s, unicode)


    def isbytes(s):
        return isinstance(s, str)


    def isinteger(n):
        return isinstance(n, (int, long))


    def b(s):
        return s


    def binxor(a, b):
        return ('').join([ chr(ord(x) ^ ord(y)) for x, y in zip(a, b) ])


    def b64encode(data, chars='+/'):
        tt = string.maketrans('+/', chars)
        return data.encode('base64').replace('\n', '').translate(tt)


    from binascii import b2a_hex
else:
    _0xffffffffL = 4294967295

    def isunicode(s):
        return isinstance(s, str)


    def isbytes(s):
        return isinstance(s, bytes)


    def isinteger(n):
        return isinstance(n, int)


    def callable(obj):
        return hasattr(obj, '__call__')


    def b(s):
        return s.encode('latin-1')


    def binxor(a, b):
        return bytes([ x ^ y for x, y in zip(a, b) ])


    from base64 import b64encode as _b64encode

    def b64encode(data, chars='+/'):
        if isunicode(chars):
            return _b64encode(data, chars.encode('utf-8')).decode('utf-8')
        else:
            return _b64encode(data, chars)


    from binascii import b2a_hex as _b2a_hex

    def b2a_hex(s):
        return _b2a_hex(s).decode('us-ascii')


    xrange = range

class PBKDF2(object):
    """PBKDF2.py : PKCS#5 v2.0 Password-Based Key Derivation

    This implementation takes a passphrase and a salt (and optionally an
    iteration count, a digest module, and a MAC module) and provides a
    file-like object from which an arbitrarily-sized key can be read.

    If the passphrase and/or salt are unicode objects, they are encoded as
    UTF-8 before they are processed.

    The idea behind PBKDF2 is to derive a cryptographic key from a
    passphrase and a salt.

    PBKDF2 may also be used as a strong salted password hash.  The
    'crypt' function is provided for that purpose.

    Remember: Keys generated using PBKDF2 are only as strong as the
    passphrases they are derived from.
    """

    def __init__(self, passphrase, salt, iterations=1000, digestmodule=SHA1, macmodule=HMAC):
        self.__macmodule = macmodule
        self.__digestmodule = digestmodule
        self._setup(passphrase, salt, iterations, self._pseudorandom)

    def _pseudorandom(self, key, msg):
        """Pseudorandom function.  e.g. HMAC-SHA1"""
        return self.__macmodule.new(key=key, msg=msg, digestmod=self.__digestmodule).digest()

    def read(self, bytes):
        """Read the specified number of key bytes."""
        if self.closed:
            raise ValueError('file-like object is closed')
        size = len(self.__buf)
        blocks = [self.__buf]
        i = self.__blockNum
        while size < bytes:
            i += 1
            if i > _0xffffffffL or i < 1:
                raise OverflowError('derived key too long')
            block = self.__f(i)
            blocks.append(block)
            size += len(block)

        buf = b('').join(blocks)
        retval = buf[:bytes]
        self.__buf = buf[bytes:]
        self.__blockNum = i
        return retval

    def __f(self, i):
        assert 1 <= i <= _0xffffffffL
        U = self.__prf(self.__passphrase, self.__salt + pack('!L', i))
        result = U
        for j in xrange(2, 1 + self.__iterations):
            U = self.__prf(self.__passphrase, U)
            result = binxor(result, U)

        return result

    def hexread(self, octets):
        """Read the specified number of octets. Return them as hexadecimal.

        Note that len(obj.hexread(n)) == 2*n.
        """
        return b2a_hex(self.read(octets))

    def _setup(self, passphrase, salt, iterations, prf):
        if isunicode(passphrase):
            passphrase = passphrase.encode('UTF-8')
        elif not isbytes(passphrase):
            raise TypeError('passphrase must be str or unicode')
        if isunicode(salt):
            salt = salt.encode('UTF-8')
        elif not isbytes(salt):
            raise TypeError('salt must be str or unicode')
        if not isinteger(iterations):
            raise TypeError('iterations must be an integer')
        if iterations < 1:
            raise ValueError('iterations must be at least 1')
        if not callable(prf):
            raise TypeError('prf must be callable')
        self.__passphrase = passphrase
        self.__salt = salt
        self.__iterations = iterations
        self.__prf = prf
        self.__blockNum = 0
        self.__buf = b('')
        self.closed = False

    def close(self):
        """Close the stream."""
        if not self.closed:
            del self.__passphrase
            del self.__salt
            del self.__iterations
            del self.__prf
            del self.__blockNum
            del self.__buf
            self.closed = True


def crypt(word, salt=None, iterations=None):
    """PBKDF2-based unix crypt(3) replacement.

    The number of iterations specified in the salt overrides the 'iterations'
    parameter.

    The effective hash length is 192 bits.
    """
    if salt is None:
        salt = _makesalt()
    if isunicode(salt):
        salt = salt.encode('us-ascii').decode('us-ascii')
    elif isbytes(salt):
        salt = salt.decode('us-ascii')
    else:
        raise TypeError('salt must be a string')
    if isunicode(word):
        word = word.encode('UTF-8')
    else:
        if not isbytes(word):
            raise TypeError('word must be a string or unicode')
        if salt.startswith('$p5k2$'):
            iterations, salt, dummy = salt.split('$')[2:5]
            if iterations == '':
                iterations = 400
            else:
                converted = int(iterations, 16)
                if iterations != '%x' % converted:
                    raise ValueError('Invalid salt')
                iterations = converted
                if not iterations >= 1:
                    raise ValueError('Invalid salt')
        allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./'
        for ch in salt:
            if ch not in allowed:
                raise ValueError('Illegal character %r in salt' % (ch,))

    if iterations is None or iterations == 400:
        iterations = 400
        salt = '$p5k2$$' + salt
    else:
        salt = '$p5k2$%x$%s' % (iterations, salt)
    rawhash = PBKDF2(word, salt, iterations).read(24)
    return salt + '$' + b64encode(rawhash, './')


PBKDF2.crypt = staticmethod(crypt)

def _makesalt():
    """Return a 48-bit pseudorandom salt for crypt().

    This function is not suitable for generating cryptographic secrets.
    """
    binarysalt = b('').join([ pack('@H', randint(0, 65535)) for i in range(3) ])
    return b64encode(binarysalt, './')