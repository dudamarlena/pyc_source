# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/digest/algorithm.py
# Compiled at: 2019-11-04 17:25:15
# Size of source mod 2**32: 5619 bytes
from opencontainers.struct import StrStruct
from opencontainers.logger import bot
import hashlib, re
from .exceptions import ErrDigestInvalidFormat, ErrDigestUnsupported, ErrDigestInvalidLength

class Algorithm(StrStruct):
    __doc__ = 'Algorithm identifies and implementation of a digester by an identifier.\n       Note the that this defines both the hash algorithm used and the string\n       encoding.\n    '

    def __init__(self, value=None):
        self._algorithm = value
        super().__init__(value)

    def available(self):
        """Available returns true if the digest type is available for use. 
           If this returns false, Digester and Hash will return None.
           we are flexible to allow the user to also provide a full digest
        """
        algorithm = self.value
        match = re.search('^(?P<algorithm>.+?):(?P<digest>.+)', self.value)
        if match:
            algorithm = match.group('algorithm')
        self._algorithm = algorithm
        return algorithm in algorithms

    def digester(self):
        """Digester returns a new digester for the specified algorithm. If the algorithm
           does not have a digester implementation, nil will be returned. This can be
           checked by calling Available before calling Digester. Note that
           the GoLang implementation also had a Hash() function that (seemed to)
           return the same, and instead I'm going to return the same hashlib new.
        """
        if not self.available():
            return
        return hashlib.new(self._algorithm)

    def hash(self):
        """Hash returns a new hash as used by the algorithm.
        """
        return self.digester()

    def validate(self, encoded):
        """Validate validates the encoded portion string. This means
           ensuring that the algorithm is available, checking it's length,
           and the characters provided.
        """
        if not self.available():
            bot.error('%s is not an available algorithm.' % self._algorithm)
            return False
        else:
            hashy = hashlib.new(self._algorithm)
            if hashy.digest_size * 2 != len(encoded):
                raise ErrDigestInvalidLength
            regexp = anchoredEncodedRegexps.get(self._algorithm)
            assert regexp.search(encoded)
        return True

    def size(self):
        """Size returns number of bytes returned by the hash.
        """
        if not self.available():
            return 0
        hashy = hashlib.new(self._algorithm)
        return hashy.digest_size

    def set(self, value):
        """Set implemented to allow use of Algorithm as a command line flag.
           This isn't useful, as we could already call load (but this will
           mirror GoLang.
        """
        self = self.load(value)
        if not self.available():
            raise ErrDigestUnsupported


SHA256 = Algorithm('sha256')
SHA384 = Algorithm('sha384')
SHA512 = Algorithm('sha512')
Canonical = SHA256
algorithms = {'sha256':SHA256, 
 'sha384':SHA384,  'sha512':SHA512}
anchoredEncodedRegexps = {SHA256: re.compile('^[a-f0-9]{64}$'), 
 SHA384: re.compile('^[a-f0-9]{96}$'), 
 SHA512: re.compile('^[a-f0-9]{128}$')}